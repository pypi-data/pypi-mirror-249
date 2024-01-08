import pathlib
import warnings

from json import dump
from os import environ, remove
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple

from dotenv import load_dotenv
from urllib3 import disable_warnings

from .excel_definition import ExcelDefinition
from .excel_operation import output_to_excel_file, read_excel_file
from .jira_client import JiraClient, JiraIssueType
from .sprint_schedule import SprintScheduleStore
from .story import (
    Story,
    sort_stories_by_inline_weights,
    sort_stories_by_property_and_order,
    sort_stories_by_raise_ranking,
)

__all__ = ["run_steps_and_sort_excel_file", "generate_jira_field_mapping_file"]

# Currently, the openpyxl package will report an obsolete warning.
warnings.simplefilter(action="ignore", category=UserWarning)
# Disable the HTTPS certificate verification warning.
disable_warnings()

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
DEFAULT_JSON_IDENT = 4
DEFAULT_SPRINT_SCHEDULE_FILE = ASSETS / "sprint_schedule.json"
DEFAULT_EXCEL_DEFINITION_FILE = ASSETS / "excel_definition.json"


def _clear_env_variables():
    if "JIRA_URL" in environ:
        del environ["JIRA_URL"]
    if "JIRA_ACCESS_TOKEN" in environ:
        del environ["JIRA_ACCESS_TOKEN"]


def _get_jira_client(env_file: Optional[Path] = None) -> Optional[JiraClient]:
    if env_file is None:
        if not load_dotenv(ASSETS / ".env"):
            print(
                "The default env file is missing. Please use the update-jira-info command to run any command for creating the file."
            )
            return None
    else:
        _clear_env_variables()
        if not load_dotenv(env_file):
            print("The env file is invalid. Please double check the env file.")
            return None

    jira_url: Optional[str] = environ.get("JIRA_URL", default=None)
    if jira_url is None or jira_url.isspace() or len(jira_url) == 0:
        print(
            "The jira url is invalid. Please use the update-jira-info command to add/update url."
        )
        return None

    jira_acccess_token: Optional[str] = environ.get("JIRA_ACCESS_TOKEN", default=None)
    if (
        jira_acccess_token is None
        or jira_acccess_token.isspace()
        or len(jira_acccess_token) == 0
    ):
        print(
            "The jira access token is invalid. Please use the update-jira-info command to add/update token."
        )
        return None

    jira_client = JiraClient(jira_url, jira_acccess_token)

    if not jira_client.health_check():
        print(
            "The jira access token is revoked. Please use the update-jira-info command to add/update token."
        )
        return None

    print(f"Jira info: {jira_url}")

    return jira_client


def _query_jira_information(
    stories: List[Story],
    excel_definition: ExcelDefinition,
    env_file: Optional[Path] = None,
) -> bool:
    jira_client = _get_jira_client(env_file)

    if jira_client is None:
        return False

    jira_fields = []

    for definition_column in excel_definition.get_columns():
        if not definition_column["query_jira_info"] or (
            definition_column["name"] is None
            or definition_column["jira_field_mapping"] is None
        ):
            continue
        jira_fields.append(
            {
                "name": definition_column["name"],
                "jira_name": definition_column["jira_field_mapping"]["name"],
                "jira_path": definition_column["jira_field_mapping"]["path"],
            }
        )

    jira_query_result = jira_client.get_stories_detail(
        [story["storyId"].strip() for story in stories], jira_fields
    )

    for story in stories:
        story_id: str = story["storyId"].lower().strip()
        if story_id in jira_query_result:
            for jira_field in jira_fields:
                story[jira_field["name"]] = jira_query_result[story_id].get(
                    jira_field["jira_name"], None
                )
        else:
            # Story ID has been changed because of convertion.
            temp_result = jira_client.get_stories_detail([story_id], jira_fields)
            if len(temp_result) > 0:
                story["storyId"] = list(temp_result.keys())[0].upper()
                for jira_field in jira_fields:
                    story[jira_field["name"]] = (
                        list(temp_result.values())[0]
                        .get(jira_field["jira_name"], "")
                        .upper()
                    )
                print(
                    f"Story id has been changed. Previous: {story_id.upper()}, Current: {story['storyId'].upper()}"
                )
            else:
                print(f"Cannot find related information for story: {story_id}")
                story.need_sort = False
                continue

    return True


def _create_jira_stories(
    stories: List[Story],
    excel_definition: ExcelDefinition,
    env_file: Optional[Path] = None,
) -> bool:
    jira_client = _get_jira_client(env_file)

    if jira_client is None:
        return False

    for story in stories:
        input_project_type: Optional[str] = story["projectType"]
        input_story_type: Optional[str] = story["storyType"]
        if input_project_type is None or input_story_type is None:
            print("Please fulfill ProjectType/StoryType field.")
            continue
        project_type = jira_client.get_project_by_project_name(input_project_type)
        if project_type is None:
            print(f"ProjectType: {input_project_type} is not supported.")
            continue
        issue_type: Optional[JiraIssueType] = None
        for item in jira_client.get_issue_types(project_type["name"]):
            if item["name"].lower() == input_story_type.lower():
                issue_type = item
                break
        if issue_type is None:
            print(f"StoryType: {input_story_type} is not supported.")
            continue
        required_fields = jira_client.get_fields_by_project_id_and_issue_id(
            project_type["id"], issue_type["id"]
        )
        all_fields_exist: bool = True
        new_story_fields: Dict[str, Any] = {}
        for required_field in required_fields:
            required_field_name: str = required_field["id"].replace(" ", "").lower()
            excel_column = excel_definition.get_column_by_jira_field_mapping_name(
                required_field_name
            )
            if excel_column is None or excel_column["jira_field_mapping"] is None:
                all_fields_exist = False
                break
            if not hasattr(story, excel_column["name"]):
                all_fields_exist = False
                break
            # TODO: Check allowed values.
            new_story_fields[excel_column["jira_field_mapping"]["path"]] = story[
                excel_column["name"]
            ]
        # Some special fields
        new_story_fields["project.id"] = project_type["id"]
        if not all_fields_exist:
            print(f"StoryType: {input_story_type} missing required fields.")
            continue

        new_story = jira_client.create_story(new_story_fields)
        if new_story is not None:
            story["storyId"] = new_story.key
            print(
                f"New story created. {jira_client.get_jira_browser_link(new_story.key)}"
            )
        return False
    return True


def _run_pre_steps(
    stories: List[Story],
    excel_definition: ExcelDefinition,
    env_file: Optional[Path] = None,
):
    # Execute pre-process steps
    pre_process_steps = excel_definition.get_pre_process_steps()

    for pre_process_step in pre_process_steps:
        pre_process_step_name: str = pre_process_step["name"]
        print(f"Executing step: {pre_process_step_name}...")
        if pre_process_step_name.lower() in "RetrieveJiraInformation".lower():
            need_call_jira_api: bool = False
            for excel_definition_column in excel_definition.get_columns():
                if excel_definition_column["jira_field_mapping"] is not None:
                    need_call_jira_api = True
                    break

            if need_call_jira_api:
                stories_need_call_jira: List[Story] = []
                for story in stories:
                    if story.need_sort and story["storyId"] is not None:
                        stories_need_call_jira.append(story)
                if not _query_jira_information(
                    stories_need_call_jira, excel_definition, env_file
                ):
                    print("Retrieve jira information failed.")
                    return
        elif pre_process_step_name.lower() in "FilterOutStoryWithoutId".lower():
            for story in stories:
                if story["storyId"] is None:
                    story.need_sort = False
        elif pre_process_step_name.lower() in "FilterOutStoryBasedOnJiraStatus".lower():
            for story in stories:
                if story["status"] is not None and story[
                    "status"
                ].upper() in pre_process_step["config"].get("JiraStatuses", []):
                    story.need_sort = False
        elif pre_process_step_name.lower() in "CreateJiraStory".lower():
            stories_need_to_create: List[Story] = []
            for story in stories:
                if story["storyId"] is None or story["storyId"].strip() == "":
                    stories_need_to_create.append(story)

            if stories_need_to_create:
                if not _create_jira_stories(
                    stories_need_to_create, excel_definition, env_file
                ):
                    print("Error occurred when creating Jira stories.")
                    return
        print("Executing finish.")


def _run_sort_logics(
    stories: List[Story], excel_definition: ExcelDefinition
) -> Tuple[List[Story], List[Story]]:
    stories_no_need_sort = []
    stories_need_sort = []

    for story in stories:
        if story.need_sort:
            stories_need_sort.append(story)
        else:
            stories_no_need_sort.append(story)

    # Execute sorting logic.
    sort_strategies = excel_definition.get_sort_strategies()

    for sort_strategy in sort_strategies:
        print(f"Executing {sort_strategy['name']} sorting...")
        if sort_strategy["name"] is None:
            continue
        if sort_strategy["name"].lower() in "InlineWeights".lower():
            stories_need_sort = sort_stories_by_inline_weights(stories_need_sort)
        elif sort_strategy["name"].lower() in "SortOrder".lower():
            sort_stories_by_property_and_order(
                stories_need_sort, excel_definition, sort_strategy["config"]
            )
        elif sort_strategy["name"].lower() in "RaiseRanking".lower():
            stories_need_sort = sort_stories_by_raise_ranking(
                stories_need_sort, excel_definition, sort_strategy["config"]
            )
        print("Executing finish.")

    return (stories_need_sort, stories_no_need_sort)


def run_steps_and_sort_excel_file(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    excel_definition_file: Optional[Union[str, Path]] = None,
    sprint_schedule_file: Optional[Union[str, Path]] = None,
    over_write: bool = True,
    env_file: Optional[Path] = None,
):
    """
    Sort the excel file and output the result

    :parm input_file:
        The excel file need to be sorted. (Absolute path only)

    :parm output_file:
        The sorted excel file location. (Absolute path only)

    :parm sprint_schedule_file:
        The JSON file which contains the priority list to calculate the :py:class:`Milestone`

    :parm excel_definition_file:
        The JSON file which contains the input excel file's structure.

    :parm over_write:
        Whether or not the exist output file will be over-write.
    """
    sprint_schedule = SprintScheduleStore()
    if sprint_schedule_file is None:
        print("Using default sprint schedule...")
        sprint_schedule.load(DEFAULT_SPRINT_SCHEDULE_FILE.read_text(encoding="utf-8"))
    else:
        print("Using custom sprint schedule...")
        sprint_schedule.load_file(sprint_schedule_file)

    excel_definition = ExcelDefinition()
    if excel_definition_file is None:
        print("Using default excel definition...")
        excel_definition.load(DEFAULT_EXCEL_DEFINITION_FILE.read_text(encoding="utf-8"))
    else:
        print("Using custom excel definition...")
        excel_definition.load_file(excel_definition_file)

    validation_result = excel_definition.validate()
    if len(validation_result) != 0:
        print(
            "Validating excel definition failed. Please check below information to fix first."
        )
        for item in validation_result:
            print(item)
        return
    print("Validating excel definition success.")

    excel_columns, stories = read_excel_file(
        input_file, excel_definition, sprint_schedule
    )

    if stories is None or len(stories) == 0:
        print("There are no stories inside the excel file.")
        return

    _run_pre_steps(stories, excel_definition, env_file)

    stories_need_sort, stories_no_need_sort = _run_sort_logics(
        stories, excel_definition
    )

    output_to_excel_file(
        output_file,
        stories_need_sort + stories_no_need_sort,  # First output the sorted stories.
        excel_definition,
        excel_columns,
        over_write,
    )

    print(f"{output_file} has been saved.")


def generate_jira_field_mapping_file(
    file: Union[str, Path], over_write: bool = True, env_file: Optional[Path] = None
) -> bool:
    jira_client = _get_jira_client(env_file)

    if jira_client is None:
        return False

    output_file_path: Path = Path(file).absolute()

    if output_file_path.exists():
        if over_write:
            try:
                remove(file)
            except PermissionError as e:
                raise FileExistsError(
                    f"The exist jira field mapping file: {file} cannot be removed. {e.args[0]}"
                ) from e
        else:
            raise FileExistsError(
                f"The jira field mapping file: {file} is already exist."
            )

    with open(output_file_path, mode="x", encoding="utf-8") as output_file:
        dump(jira_client.get_all_fields(), output_file, indent=DEFAULT_JSON_IDENT)
        output_file.flush()
        output_file.close()

    return True
