import pathlib
from os import environ
import pytest

from requests_mock import Mocker

from jira_assistant.assistant import (
    generate_jira_field_mapping_file,
    run_steps_and_sort_excel_file,
)
from jira_assistant.excel_definition import ExcelDefinition
from jira_assistant.excel_operation import read_excel_file
from jira_assistant.jira_client import JiraClient
from jira_assistant.sprint_schedule import SprintScheduleStore
from jira_assistant.story import compare_story_based_on_inline_weights
from tests.mock_server import (
    mock_jira_requests,
    mock_jira_requests_with_failed_status_code,
)
from tests.utils import read_stories_from_excel

from . import ASSETS_ENV_FILES, ASSETS_FILES, SRC_ASSETS


def test_run_steps_and_sort_excel_file(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )

        excel_definition = ExcelDefinition()
        excel_definition.load_file(SRC_ASSETS / "excel_definition.json")
        sprint_schedule = SprintScheduleStore()
        sprint_schedule.load_file(SRC_ASSETS / "sprint_schedule.json")

        _, stories = read_excel_file(
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition,
            sprint_schedule,
        )

        assert len(stories) == 8

        jira_client = JiraClient(environ["JIRA_URL"], environ["JIRA_ACCESS_TOKEN"])

        noneed_sort_statuses = [
            "SPRINT COMPLETE",
            "PENDING RELEASE",
            "PRODUCTION TESTING",
            "CLOSED",
        ]

        jira_fields = [
            {
                "name": "domain",
                "jira_name": "customfield_15601",
                "jira_path": "customfield_15601.value",
            },
            {"name": "status", "jira_name": "status", "jira_path": "status.name"},
        ]

        for i in range(len(stories) - 1):
            story_id_0 = stories[i]["storyId"].lower().strip()
            story_id_1 = stories[i + 1]["storyId"].lower().strip()
            query_result = jira_client.get_stories_detail(
                [story_id_0, story_id_1], jira_fields
            )
            if (
                query_result[story_id_0]["status"].upper() not in noneed_sort_statuses
                and query_result[story_id_1]["status"].upper()
                not in noneed_sort_statuses
            ):
                assert (
                    compare_story_based_on_inline_weights(stories[i], stories[i + 1])
                    >= 0
                )


def test_run_steps_and_sort_excel_file_use_default_files(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            env_file=ASSETS_ENV_FILES / "default.env",
        )

        excel_definition = ExcelDefinition()
        excel_definition.load_file(SRC_ASSETS / "excel_definition.json")
        sprint_schedule = SprintScheduleStore()
        sprint_schedule.load_file(SRC_ASSETS / "sprint_schedule.json")

        _, stories = read_excel_file(
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition,
            sprint_schedule,
        )

        assert len(stories) == 8


def test_run_steps_and_sort_excel_file_use_wrong_excel_definition_file(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=ASSETS_FILES
            / "excel_definition_duplicate_index.json",
            env_file=ASSETS_ENV_FILES / "default.env",
        )
        output = capsys.readouterr()
        assert "Validating excel definition failed." in output.out


def test_run_steps_and_sort_excel_file_with_empty_excel_file(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "empty_excel.xlsx",
            tmpdir / "empty_excel_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
        )


def test_run_steps_and_sort_excel_file_with_raise_ranking_file(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=str(
                ASSETS_FILES / "excel_definition_with_raise_ranking.json"
            ),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )

        stories = read_stories_from_excel(
            tmpdir / "happy_path_sorted.xlsx",
            SRC_ASSETS / "excel_definition.json",
            SRC_ASSETS / "sprint_schedule.json",
        )

        false_value_begin = False
        for story in stories:
            if story["isThisAHardDate"] is True:
                continue
            if story["isThisAHardDate"] is False and false_value_begin is False:
                false_value_begin = True
                continue
            if story["isThisAHardDate"] is True and false_value_begin is True:
                raise AssertionError


def test_run_steps_and_sort_excel_file_missing_jira_url(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "missing_jira_url.env",
        )
        output = capsys.readouterr()
        assert "The jira url is invalid." in output.out


def test_run_steps_and_sort_excel_file_missing_access_token(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "missing_jira_access_token.env",
        )
        output = capsys.readouterr()
        assert "The jira access token is invalid." in output.out


def test_run_steps_and_sort_excel_file_jira_health_check_failed(capsys, tmpdir):
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests_with_failed_status_code(),
    ):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path.xlsx",
            tmpdir / "happy_path_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )
        output = capsys.readouterr()
        assert "The jira access token is revoked." in output.out


def test_generate_jira_field_mapping_file(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        output_file: pathlib.Path = tmpdir / "jira_field_mapping.json"

        assert (
            generate_jira_field_mapping_file(
                output_file, env_file=ASSETS_ENV_FILES / "default.env"
            )
            is True
        )
        assert output_file.exists() is True


def test_generate_jira_field_mapping_file_over_write_is_true(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        output_file: pathlib.Path = pathlib.Path(tmpdir) / "jira_field_mapping.json"
        output_file.touch(exist_ok=True)

        assert (
            generate_jira_field_mapping_file(
                output_file, over_write=True, env_file=ASSETS_ENV_FILES / "default.env"
            )
            is True
        )
        assert output_file.exists() is True


def test_generate_jira_field_mapping_file_over_write_is_false(tmpdir):
    with pytest.raises(FileExistsError) as e:
        with Mocker(
            real_http=False, case_sensitive=False, adapter=mock_jira_requests()
        ):
            output_file: pathlib.Path = pathlib.Path(tmpdir) / "jira_field_mapping.json"
            output_file.touch(exist_ok=True)

            generate_jira_field_mapping_file(
                output_file,
                over_write=False,
                env_file=ASSETS_ENV_FILES / "default.env",
            )
    assert "already exist" in str(e.value.args[0])


def test_run_steps_and_sort_excel_file_with_no_need_sort_stories(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path_with_no_need_sort_stories.xlsx",
            tmpdir / "happy_path_with_no_need_sort_stories_sorted.xlsx",
            excel_definition_file=str(ASSETS_FILES / "excel_definition.json"),
            sprint_schedule_file=str(ASSETS_FILES / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )

        excel_definition = ExcelDefinition()
        excel_definition.load_file(SRC_ASSETS / "excel_definition.json")
        sprint_schedule = SprintScheduleStore()
        sprint_schedule.load_file(SRC_ASSETS / "sprint_schedule.json")

        _, stories = read_excel_file(
            tmpdir / "happy_path_with_no_need_sort_stories_sorted.xlsx",
            excel_definition,
            sprint_schedule,
        )

        assert len(stories) == 8

        jira_client = JiraClient(environ["JIRA_URL"], environ["JIRA_ACCESS_TOKEN"])

        noneed_sort_statuses = [
            "SPRINT COMPLETE",
            "PENDING RELEASE",
            "PRODUCTION TESTING",
            "CLOSED",
        ]

        jira_fields = [
            {
                "name": "domain",
                "jira_name": "customfield_15601",
                "jira_path": "customfield_15601.value",
            },
            {"name": "status", "jira_name": "status", "jira_path": "status.name"},
        ]

        for i in range(len(stories) - 1):
            if stories[i]["storyId"] is None or stories[i + 1]["storyId"] is None:
                continue
            story_id_0 = stories[i]["storyId"].lower().strip()
            story_id_1 = stories[i + 1]["storyId"].lower().strip()
            query_result = jira_client.get_stories_detail(
                [story_id_0, story_id_1], jira_fields
            )
            if (
                query_result[story_id_0]["status"].upper() not in noneed_sort_statuses
                and query_result[story_id_1]["status"].upper()
                not in noneed_sort_statuses
            ):
                assert (
                    compare_story_based_on_inline_weights(stories[i], stories[i + 1])
                    >= 0
                )


def test_create_jira_stories_and_sort_excel_file(tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path_create_story.xlsx",
            tmpdir / "happy_path_create_story_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )

        excel_definition = ExcelDefinition()
        excel_definition.load_file(SRC_ASSETS / "excel_definition.json")
        sprint_schedule = SprintScheduleStore()
        sprint_schedule.load_file(SRC_ASSETS / "sprint_schedule.json")

        _, stories = read_excel_file(
            tmpdir / "happy_path_create_story_sorted.xlsx",
            excel_definition,
            sprint_schedule,
        )

        assert len(stories) == 1


def test_create_jira_stories_invalid_project_type(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path_create_story_invalid_project_type.xlsx",
            tmpdir / "happy_path_create_story_invalid_project_type_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )
        output = capsys.readouterr()
        assert "ProjectType: ABC is not supported." in output.out


def test_create_jira_stories_invalid_issue_type(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path_create_story_invalid_issue_type.xlsx",
            tmpdir / "happy_path_create_story_invalid_issue_type_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )
        output = capsys.readouterr()
        assert "StoryType: WHH is not supported." in output.out


# def test_create_jira_stories_missing_required_field(capsys, tmpdir):
#    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
#        run_steps_and_sort_excel_file(
#            ASSETS_FILES / "happy_path_create_story_missing_required_field.xlsx",
#            tmpdir / "happy_path_create_story_missing_required_field_sorted.xlsx",
#            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
#            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
#            env_file=ASSETS_ENV_FILES / "default.env",
#        )
#        output = capsys.readouterr()
#        assert "StoryType: sd missing required fields." in output.out


def test_create_jira_stories_no_project_type(capsys, tmpdir):
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        run_steps_and_sort_excel_file(
            ASSETS_FILES / "happy_path_create_story_no_project_type.xlsx",
            tmpdir / "happy_path_create_story_no_project_type_sorted.xlsx",
            excel_definition_file=str(SRC_ASSETS / "excel_definition.json"),
            sprint_schedule_file=str(SRC_ASSETS / "sprint_schedule.json"),
            env_file=ASSETS_ENV_FILES / "default.env",
        )
        output = capsys.readouterr()
        assert "Please fulfill ProjectType/StoryType field." in output.out
