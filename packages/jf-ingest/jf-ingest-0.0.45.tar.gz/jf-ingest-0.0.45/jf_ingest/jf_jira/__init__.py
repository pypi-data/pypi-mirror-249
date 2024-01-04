import logging
from enum import Enum

from jira import Issue

from jf_ingest import diagnostics, logging_helper
from jf_ingest.config import IngestionConfig, IngestionType, JiraAuthMethod, JiraConfig
from jf_ingest.file_operations import IngestIOHelper, SubDirectory
from jf_ingest.jf_jira.auth import get_jira_connection
from jf_ingest.jf_jira.downloaders import (
    IssueMetadata,
    download_boards_and_sprints,
    download_fields,
    download_issuelinktypes,
    download_issues,
    download_issuetypes,
    download_priorities,
    download_projects_and_versions_and_components,
    download_resolutions,
    download_statuses,
    download_users,
    download_worklogs,
)
from jf_ingest.utils import ThreadPoolWithTqdm, batch_iterable

logger = logging.getLogger(__name__)


class JiraObject(Enum):
    JiraFields = "jira_fields"
    JiraProjectsAndVersions = "jira_projects_and_versions"
    JiraUsers = "jira_users"
    JiraResolutions = "jira_resolutions"
    JiraIssueTypes = "jira_issuetypes"
    JiraLinkTypes = "jira_linktypes"
    JiraPriorities = "jira_priorities"
    JiraBoards = "jira_boards"
    JiraSprints = "jira_sprints"
    JiraBoardSprintLinks = "jira_board_sprint_links"
    JiraIssues = "jira_issues"
    JiraIssuesIdsDownloaded = "jira_issue_ids_downloaded"
    JiraIssuesIdsDeleted = "jira_issue_ids_deleted"
    JiraWorklogs = "jira_worklogs"
    JiraStatuses = "jira_statuses"


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def load_and_push_jira_to_s3(ingest_config: IngestionConfig):
    """Loads data from JIRA, Dumps it to disc, and then uploads that data to S3

    All configuration for this object is done via the JIRAIngestionConfig object

    Args:
        config (IngestionConfig): A dataclass that holds several different configuration args for this task

    Returns:
        bool: Returns True on Success
    """
    jira_config = ingest_config.jira_config
    if jira_config.skip_issues and jira_config.only_issues:
        logger.warning(f"only_issues and skip_issues are both True, so all tasks will be skipped. ")
        return False

    #######################################################################
    # SET UP JIRA CONNECTIONS (Basic and Potentially Atlassian Connect)
    #######################################################################
    jira_basic_connection = get_jira_connection(
        config=jira_config, auth_method=JiraAuthMethod.BasicAuth
    )
    jira_atlas_connect_connection = (
        get_jira_connection(config=jira_config, auth_method=JiraAuthMethod.AtlassianConnect)
        if JiraAuthMethod.AtlassianConnect in jira_config.available_auth_methods
        else None
    )
    # There is an ongoing effort to cut all things over to Atlassian Connect only,
    # but it is a piece wise migration for now.
    # OJ-29745
    jira_connect_or_fallback_connection = jira_basic_connection
    if jira_config.feature_flags.get("lusca-auth-always-use-connect-for-atlassian-apis-Q423"):
        jira_connect_or_fallback_connection = jira_atlas_connect_connection

    #######################################################################
    # Init IO Helper
    #######################################################################
    ingest_io_helper = IngestIOHelper(ingest_config=ingest_config)

    #######################################################################
    # Jira Projects
    #######################################################################
    projects_and_versions = download_projects_and_versions_and_components(
        jira_connection=jira_basic_connection,  # Always use BasicAuth because we want to respect permission restrictions on projects
        is_agent_run=ingest_config.ingest_type == IngestionType.AGENT,
        jellyfish_project_ids_to_keys=jira_config.jellyfish_project_ids_to_keys,
        jellyfish_issue_metadata=jira_config.jellyfish_issue_metadata,
        include_projects=jira_config.include_projects,
        exclude_projects=jira_config.exclude_projects,
        include_categories=jira_config.include_project_categories,
        exclude_categories=jira_config.exclude_project_categories,
    )

    project_ids = {proj["id"] for proj in projects_and_versions}
    ingest_io_helper.write_json_data_to_local(
        object_name=JiraObject.JiraProjectsAndVersions.value,
        json_data=projects_and_versions,
        subdirectory=SubDirectory.JIRA,
    )

    if not jira_config.only_issues:
        #######################################################################
        # Jira Fields
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraFields.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_fields(
                jira_connect_or_fallback_connection,
                jira_config.include_fields,
                jira_config.exclude_fields,
            ),
        )

        ######################################################################
        # Jira Users
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraUsers.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_users(
                jira_basic_connection=jira_basic_connection,  # Use BasicAuth because /users/search is not supported by Connect apps.
                jira_atlas_connect_connection=jira_atlas_connect_connection,  # Use AtlasConnect for 'augment with email' subtask
                gdpr_active=jira_config.gdpr_active,
                search_users_by_letter_email_domain=jira_config.search_users_by_letter_email_domain,
                required_email_domains=jira_config.required_email_domains,
                is_email_required=jira_config.is_email_required,
            ),
        )

        #######################################################################
        # Jira Resolutions
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraResolutions.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_resolutions(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Issue Types
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssueTypes.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_issuetypes(
                jira_connect_or_fallback_connection, project_ids=project_ids
            ),
        )

        #######################################################################
        # Jira Link Types
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraLinkTypes.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_issuelinktypes(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Priorities
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraPriorities.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_priorities(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Statuses
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraStatuses.value,
            subdirectory=SubDirectory.JIRA,
            json_data=download_statuses(jira_basic_connection),
        )

        #######################################################################
        # Jira Boards, Sprints, and Links
        #######################################################################
        boards, sprints, links = download_boards_and_sprints(
            jira_basic_connection,  # Always use BasicAuth because we want to respect permission restrictions on projects
            jira_config.download_sprints,
        )
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraBoards.value,
            subdirectory=SubDirectory.JIRA,
            json_data=boards,
        )

        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraSprints.value,
            subdirectory=SubDirectory.JIRA,
            json_data=sprints,
        )

        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraBoardSprintLinks.value,
            subdirectory=SubDirectory.JIRA,
            json_data=links,
        )

    if not jira_config.skip_issues:
        jira_issues, deleted_issue_ids = download_issues(
            jira_connection=jira_connect_or_fallback_connection,
            jira_projects=[
                proj["key"]
                for proj in projects_and_versions
                if proj["key"] not in jira_config.exclude_projects
            ],
            full_redownload=jira_config.full_redownload,
            earliest_issue_dt=jira_config.earliest_issue_dt,
            issue_download_concurrent_threads=jira_config.issue_download_concurrent_threads,
            jellyfish_issue_metadata=jira_config.jellyfish_issue_metadata,
            include_fields=jira_config.include_fields,
            exclude_fields=jira_config.exclude_fields,
        )

        jira_issues_per_file = 2000
        # Force lazy load to load
        batched_issues: list[list[Issue]] = [
            batch for batch in batch_iterable(jira_issues, batch_size=jira_issues_per_file)
        ]
        logger.debug(f"Attempting to save {len(batched_issues)} issue batches to local disc...")
        with ThreadPoolWithTqdm(
            desc=f"Saving {len(batched_issues)} batches of jira issues to local disc ({jira_issues_per_file} issues per file)",
            total=len(batched_issues),
            max_workers=5,
            thread_name_prefix="JiraIssuesFileWriter",
        ) as pool:
            for batch_number, issue_batch in enumerate(batched_issues):
                pool.submit(
                    ingest_io_helper.write_json_data_to_local,
                    object_name=JiraObject.JiraIssues.value,
                    json_data=issue_batch,
                    subdirectory=SubDirectory.JIRA,
                    batch_number=batch_number,
                )
        logger.debug(f"Done saving {len(batched_issues)} issue batches to local disc!")

        all_downloaded_issue_ids: list[str] = [issue["id"] for issue in jira_issues]

        # Write Issues
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssuesIdsDownloaded.value,
            json_data=[int(issue_id) for issue_id in all_downloaded_issue_ids],
            subdirectory=SubDirectory.JIRA,
        )

        # Write issues that got deleted
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssuesIdsDeleted.value,
            subdirectory=SubDirectory.JIRA,
            json_data=list(deleted_issue_ids),
        )

        #######################################################################
        # Jira Work Logs
        #######################################################################
        if jira_config.download_worklogs:
            ingest_io_helper.write_json_data_to_local(
                object_name=JiraObject.JiraWorklogs.value,
                subdirectory=SubDirectory.JIRA,
                json_data=download_worklogs(
                    jira_basic_connection,
                    all_downloaded_issue_ids,
                    jira_config.work_logs_pull_from,
                ),
            )
    else:
        logger.info(
            f"Skipping issues and worklogs bc config.skip_issues is {jira_config.skip_issues}"
        )
    logger.info(f"Data has been saved locally to: {ingest_io_helper.local_file_path}")
    #######################################################################
    # Upload files to S3
    #######################################################################
    if ingest_config.upload_to_s3:
        ingest_io_helper.upload_all_directory_output_to_s3(SubDirectory.JIRA)
    else:
        logger.info(
            f"Not uploading to S3 because upload_to_s3 in the Ingestion config is set to {ingest_config.upload_to_s3}"
        )

    return True
