import json

import requests_mock

from jf_ingest.config import IngestionConfig, IngestionType
from jf_ingest.file_operations import IngestIOHelper, SubDirectory


class TestIngestIOHelper:
    company_slug = "test_company"
    timestamp = "20231205_123456"
    local_file_path = "/tmp"
    api_token = "test_token"
    ingest_io_helper = None

    def _get_ingest_io_helper(self) -> IngestIOHelper:
        return IngestIOHelper(ingest_config=self._get_ingest_config())

    def _get_ingest_config(self):
        return IngestionConfig(
            company_slug=self.company_slug,
            timestamp=self.timestamp,
            local_file_path=self.local_file_path,
            jellyfish_api_token=self.api_token,
        )

    def setup(self):
        self.ingest_io_helper = self._get_ingest_io_helper()

    def test_write_and_read_file(self):
        self.ingest_io_helper.write_json_data_to_local(
            "jira_test_data", {"test": "data"}, SubDirectory.JIRA
        )
        with open("/tmp/jira/jira_test_data.json", "r") as f:
            data = json.load(f)
            assert data == {"test": "data"}

    def test_upload_to_s3_with_mocked_s3_direct_connect(self):
        filepath = "jira_test_data.json"
        s3_obj_path = f"{self.company_slug}/{self.timestamp}/jira/jira_test_data.json"
        s3_url = "https://jellyfish-agent-upload.s3.amazonaws.com/"
        json_resp = {
            "signed_urls": [
                {
                    "url": f"{s3_url}",
                    "fields": {
                        "key": f"{self.company_slug}/{self.timestamp}/jira/{filepath}.gz",
                        "AWSAccessKeyId": "PLACEHOLDER",
                        "x-amz-security-token": "PLACEHOLDER",
                    },
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m: requests_mock.Mocker = m
            m.register_uri(
                method="POST",
                url="https://app.jellyfish.co/endpoints/ingest/signed-url?timestamp=20231205_123456",
                json=json_resp,
            )
            m.register_uri(method="POST", url=s3_url, status_code=200)

            signed_url = self.ingest_io_helper.get_signed_urls(
                [filepath], self.timestamp, ingestion_type=IngestionType.DIRECT_CONNECT
            )[0]

            assert m.last_request.json()["ingestType"] == "DIRECT_CONNECT"
            self.ingest_io_helper.write_json_data_to_local(
                filepath, {"test": "data"}, SubDirectory.JIRA
            )
            success = self.ingest_io_helper.wrapped_upload_file_to_s3(
                f"{self.local_file_path}/{SubDirectory.JIRA}/{filepath}",
                s3_obj_path,
                signed_url,
            )
            assert success

    def test_upload_to_s3_with_mocked_s3_agent(self):
        filepath = "jira_test_data.json"
        s3_obj_path = f"{self.company_slug}/{self.timestamp}/jira/jira_test_data.json"
        s3_url = "https://jellyfish-agent-upload.s3.amazonaws.com/"
        json_resp = {
            "signed_urls": [
                {
                    "url": f"{s3_url}",
                    "fields": {
                        "key": f"{self.company_slug}/{self.timestamp}/jira/{filepath}.gz",
                        "AWSAccessKeyId": "PLACEHOLDER",
                        "x-amz-security-token": "PLACEHOLDER",
                    },
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m: requests_mock.Mocker = m
            m.register_uri(
                method="POST",
                url="https://app.jellyfish.co/endpoints/ingest/signed-url?timestamp=20231205_123456",
                json=json_resp,
            )
            m.register_uri(method="POST", url=s3_url, status_code=200)

            signed_url = self.ingest_io_helper.get_signed_urls(
                [filepath], self.timestamp, ingestion_type=IngestionType.AGENT
            )[0]

            assert m.last_request.json()["ingestType"] == "AGENT"

            self.ingest_io_helper.write_json_data_to_local(
                filepath, {"test": "data"}, SubDirectory.JIRA
            )
            success = self.ingest_io_helper.wrapped_upload_file_to_s3(
                f"{self.local_file_path}/{SubDirectory.JIRA}/{filepath}",
                s3_obj_path,
                signed_url,
            )
            assert success
