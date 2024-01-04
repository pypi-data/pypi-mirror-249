import dataclasses
import gzip
import json
import logging
import os
import threading
import traceback
from pathlib import Path
from typing import Optional

import requests

from jf_ingest import logging_helper
from jf_ingest.config import IngestionConfig, IngestionType, JiraConfig
from jf_ingest.utils import ReauthSession, retry_session

logger = logging.getLogger(__name__)


class SubDirectory:
    JIRA = "jira"
    GIT = "git"


def _is_auth_error(exception_string: str) -> bool:
    """
    Checks if the exception string is an authentication error.
    :param exception_string: str
    :return: bool
    """
    for auth_str in [
        "authentication",
        "permission",
        "secreterror",
        "connecttimeouterror",
        "authorize",
    ]:
        if auth_str in exception_string:
            return True
    return False


class StrDefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


class IngestIOHelper:
    def __init__(self, ingest_config: IngestionConfig):
        self.ingest_config = ingest_config
        # EVERYTHING in this file path will (potentially) be uploaded to S3!
        # DO NOT put any creds file in this path!!!!
        self.local_file_path = ingest_config.local_file_path

        if not os.path.exists(self.local_file_path):
            os.makedirs(self.local_file_path)

    def _get_file_name(self, object_name: str, batch_number: Optional[int] = 0):
        return f'{object_name}{batch_number if batch_number else ""}.json'

    def _write_file(self, json_data: dict | list[dict], full_file_path: str):
        """
        Writes json file data to local file system at filepath. Called by write_json_data_to_local.
        :param json_data:
        :param full_file_path:
        :return: nothing
        """
        with open(full_file_path, "wb") as f:
            f.write(json.dumps(json_data, indent=2, cls=StrDefaultEncoder).encode("utf-8"))
            logger.debug(f"File: {full_file_path}, Size: {round(f.tell() / 1000000, 1)}MB")

    def write_json_data_to_local(
        self,
        object_name: str,
        json_data: dict | list[dict],
        subdirectory: SubDirectory,
        batch_number: Optional[int] = 0,
    ) -> None:
        """
        Writes json data to local file system in proper subdirectory (depending on jira or git)
        :param object_name: from JiraObject or GitObject enum, eg "jira_boards", "git_prs", etc
        :param json_data: data returned from ingestion
        :param subdirectory: directory under `<output_dir>/<timestamp>/` to write to, eg "jira" or "git"
        :param batch_number: if this is a batched file, the batch number
        :return: None
        """
        try:
            file_name = self._get_file_name(object_name=object_name, batch_number=batch_number)
            full_file_path = f"{self.local_file_path}/{subdirectory}/{file_name}"
            logger.info(f"Attempting to save {object_name} data to {full_file_path}")
            try:
                self._write_file(json_data, full_file_path)
            except FileNotFoundError as e:
                Path(full_file_path).parent.mkdir(exist_ok=True, parents=True)
                self._write_file(json_data, full_file_path)
        except Exception as e:
            logger.error(
                f"Exception encountered when attempting to write data to local file! Error: {e}"
            )

    def get_signed_urls(
        self, filenames: list[str], timestamp: str, ingestion_type: IngestionType
    ) -> dict[str, dict]:
        """
        Gets signed urls from Jellyfish API for uploading to S3
        :param filenames: list of filenames that will need urls
        :param timestamp: timestamp created at beginning of ingestion (used for output directory)
        :return: the signed urls dict of shape {
            '<filename>': {
                's3_path': '<s3_path>',
                'url': {
                    'url': '<signed_url>',
                    'fields': {
                        '<field>': '<value>' for field in (key, AWSAccessKeyId, x-amz-security-token, policy, signature)
                    }
                }
            }
        }
        """
        base_url = self.ingest_config.jellyfish_api_base
        headers = {"Jellyfish-API-Token": self.ingest_config.jellyfish_api_token}
        payload = {
            "files": [f"{name}.gz" for name in filenames],
            "ingestType": ingestion_type,
        }  # the files will be gzipped before uploading

        r = requests.post(
            f"{base_url}/endpoints/ingest/signed-url?timestamp={timestamp}",
            headers=headers,
            json=payload,
        )
        r.raise_for_status()

        return r.json()["signed_urls"]

    def upload_file_to_s3(
        self, file_obj: bytes, s3_obj_path: str, signed_url: dict, dry_run=False
    ) -> None:
        """
        Uploads a given file object to the s3 path using the signed url
        :param file_obj: python file object opened in bytes mode
        :param s3_obj_path: s3 path; <company_slug>/<timestamp>/<filepath>
        :param signed_url: dict with signed url value and AWS fields
        :param dry_run: bool, set to True to prevent actual upload
        :return: None (will call raise_for_status on the upload response)
        """
        if dry_run:
            return
        session = retry_session()
        upload_resp = session.post(
            signed_url["url"],
            data=signed_url["fields"],
            files={"file": (s3_obj_path, file_obj)},
        )
        upload_resp.raise_for_status()
        return

    def wrapped_upload_file_to_s3(self, filepath: str, s3_obj_path: str, signed_url: dict) -> bool:
        """
        Wraps upload_file_to_s3 with error handling
        :param filepath: full filepath to local file
        :param s3_obj_path: s3 path; <company_slug>/<timestamp>/<filepath>
        :param signed_url: dict with signed url value and AWS fields
        :return: bool, True/False on Success/Failure
        """
        try:
            with open(filepath, "rb") as file_obj:
                logger.info(f"Compressing {filepath}...")
                gzip_object = gzip.compress(file_obj.read())
                self.upload_file_to_s3(gzip_object, s3_obj_path, signed_url)
                logger.info(f"Successfully uploaded {filepath} to S3")

                return True
        except Exception as e:
            if _is_auth_error(str(e).lower()):
                logger.error(
                    f"Authentication error encountered when uploading {filepath} to S3! Error: \n{e} "
                    f"\nIs there a proxy or firewall blocking the connection?"
                )
            else:
                logger.error(f"Exception encountered when uploading {filepath} to S3! Error: {e}")
            logger.debug(traceback.format_exc())

            return False

    def upload_local_files_to_s3_threaded(self, filenames: list[str], prefix: str = "") -> bool:
        """
        Uploads a list of local files to S3 using a thread pool.
        :param filenames: list[str]
        :param prefix: str
        :return: bool, True/False on Success/Failure
        """
        filenames_for_s3 = [f"{prefix}{Path(filename).name}" for filename in filenames]
        signed_urls = self.get_signed_urls(
            filenames_for_s3,
            self.ingest_config.timestamp,
            ingestion_type=self.ingest_config.ingest_type,
        )
        threads = [
            threading.Thread(
                target=self.wrapped_upload_file_to_s3,
                args=[
                    f"{self.local_file_path}/{filename.replace('.gz', '')}",
                    url_dict["s3_path"],
                    url_dict["url"],
                ],
            )
            for (filename, url_dict) in signed_urls.items()
        ]

        logger.info(f"Uploading {len(filenames)} files to S3 using {len(threads)} threads...")

        thread_exceptions = []

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        success = True

        if any(thread_exceptions):
            # Run through exceptions and inject them into the agent log
            for exception in thread_exceptions:
                logger.error(
                    f"A thread exception was encountered when uploading files to S3: {exception}"
                )
            logger.error(
                "There was an error uploading files to S3. Please check the agent log for more details. When "
                "connectivity has been restored you may run the agent in `send-only` mode to retry sending the files."
            )
            success = False
            logger.info("✗")
        if success:
            logger.info("✓")

        return success

    def upload_all_directory_output_to_s3(self, directory: str) -> bool:
        """
        Uploads all files in a given directory to S3
        :param directory: string directory name
        :return: bool, True/False on Success/Failure
        """
        logger.info(f"Uploading all {directory} output to S3...")
        success = False
        try:
            _, directories, filenames = next(os.walk(f"{self.local_file_path}/{directory}/"))
            filenames = [f"{self.local_file_path}/{directory}/{filename}" for filename in filenames]
            success = self.upload_local_files_to_s3_threaded(filenames, prefix=f"{directory}/")
        except StopIteration:
            logger.warning(f"No {directory} output to upload, skipping.")
        if success:
            logger.info(f"Successfully compressed and uploaded {directory} output to S3")

        return success

    def upload_all_locals_to_s3(self) -> None:
        """
        Uploads all local files to S3
        :return: None
        """
        success_jira = self.upload_all_directory_output_to_s3(SubDirectory.JIRA)
        success_git = self.upload_all_directory_output_to_s3(SubDirectory.GIT)

        logger.info("Uploading all remaining files to S3...")
        success_remaining = self.upload_all_directory_output_to_s3("./")

        logger.info("Uploading agent log to S3...")
        success_log = self.upload_local_files_to_s3_threaded([logging_helper.LOG_FILE_NAME])
        if success_log:
            logger.info("✓")
        else:
            logger.info("✗")

        if success_jira and success_git and success_remaining:
            done_file_dict = self.get_signed_urls(
                [".done"],
                timestamp=self.ingest_config.timestamp,
                ingestion_type=self.ingest_config.ingest_type,
            )[".done"]
            self.upload_file_to_s3(b".done", done_file_dict["s3_path"], done_file_dict["url"])
