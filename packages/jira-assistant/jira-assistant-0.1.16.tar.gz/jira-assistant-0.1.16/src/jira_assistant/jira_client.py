# -*- coding: utf-8 -*-
"""
This module is used to store excel column definition information.
"""
import pathlib
import warnings

from json import loads
from sys import version_info

from typing import Any, Dict, List, Optional, TypedDict, Tuple

from jira import JIRA, JIRAError, Issue
from urllib3 import disable_warnings

if version_info < (3, 11):
    from typing_extensions import NotRequired, Self
else:
    from typing import NotRequired, Self


# Currently, the openpyxl package will report an obsolete warning.
warnings.simplefilter(action="ignore", category=UserWarning)
# Disable the HTTPS certificate verification warning.
disable_warnings()

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
DEFAULT_JIRA_FIELD_TYPE_FILE = ASSETS / "jira_field_type.json"


class JiraFieldTypeDefinition(TypedDict):
    type: NotRequired[str]
    name: NotRequired[str]
    properties: NotRequired[List[Self]]
    isBasic: NotRequired[bool]
    arrayItemType: NotRequired[str]


_jira_field_types = []
_current_jira_field_types_file_path: pathlib.Path = DEFAULT_JIRA_FIELD_TYPE_FILE
# TODO: If file path changed, then reload.


def _init_jira_field_types(jira_field_type_file: Optional[pathlib.Path]):
    if not _jira_field_types or (
        jira_field_type_file is not None
        and not _current_jira_field_types_file_path.samefile(jira_field_type_file)
    ):
        if jira_field_type_file is None:
            jira_field_type_file = DEFAULT_JIRA_FIELD_TYPE_FILE
        for i in loads(jira_field_type_file.read_text(encoding="utf-8")):
            _jira_field_types.append(i)


def get_jira_field(
    field_type: Optional[str], jira_field_type_file: Optional[pathlib.Path] = None
) -> Optional[JiraFieldTypeDefinition]:
    if field_type is None or len(field_type.strip()) == 0:
        return None
    _init_jira_field_types(jira_field_type_file)
    for jira_field_type in _jira_field_types:
        if jira_field_type.get("type", "").lower() == field_type.lower():
            return jira_field_type
    return None


class JiraFieldPropertyPathDefinition(TypedDict):
    path: str
    isArray: bool


def get_field_paths_of_jira_field(
    field_type: str,
    field_property_name: str,
    jira_field_type_file: Optional[pathlib.Path] = None,
) -> Optional[List[JiraFieldPropertyPathDefinition]]:
    jira_field = get_jira_field(field_type, jira_field_type_file)
    if jira_field is None:
        return None
    if jira_field.get("isBasic", False) is True:
        return [{"path": field_property_name, "isArray": False}]
    result = []
    is_array_item = "arrayItemType" in jira_field
    # Following code will use the same jira field type file, so no need to pass.
    _internal_get_field_paths_of_jira_field(
        jira_field,
        is_array_item,
        [
            {
                "path": field_property_name,
                "isArray": is_array_item,
            }
        ],
        result,
    )
    return result


def _internal_get_field_paths_of_jira_field(
    jira_field: Optional[JiraFieldTypeDefinition],
    is_array_item: bool,
    temp: List[JiraFieldPropertyPathDefinition],
    final: List[JiraFieldPropertyPathDefinition],
):
    if jira_field is None:
        return None
    if jira_field.get("isBasic", False) is True:
        for item in temp:
            final.append(
                {
                    "path": connect_jira_field_path(
                        item["path"], jira_field.get("name", "")
                    ),
                    "isArray": is_array_item,
                }
            )
    if "arrayItemType" in jira_field:
        _internal_get_field_paths_of_jira_field(
            get_jira_field(jira_field["arrayItemType"]), True, temp, final
        )
    if "properties" in jira_field:
        field_properties = jira_field.get("properties", [])
        for field_property in field_properties:
            if field_property.get("arrayItemType", None) is not None:
                for item in temp:
                    item["path"] = connect_jira_field_path(
                        item["path"], field_property.get("name", "")
                    )
                _internal_get_field_paths_of_jira_field(
                    get_jira_field(field_property.get("arrayItemType")),
                    True,
                    temp,
                    final,
                )
            if field_property.get("type", None) is None:
                continue
            child_field = get_jira_field(field_property.get("type"))
            if child_field is None:
                continue
            child_field_is_basic = child_field.get("isBasic", False)
            if child_field_is_basic:
                for item in temp:
                    final.append(
                        {
                            "path": connect_jira_field_path(
                                item["path"], field_property.get("name", "")
                            ),
                            "isArray": is_array_item,
                        }
                    )
                continue
            for item in temp:
                item["path"] = connect_jira_field_path(
                    item["path"], field_property.get("name", "")
                )
            _internal_get_field_paths_of_jira_field(
                child_field, is_array_item, temp, final
            )
    return None


def connect_jira_field_path(path_a: str, path_b: str) -> str:
    return path_a + "." + path_b


class JiraProject(TypedDict):
    id: int
    name: str


class JiraIssueType(TypedDict):
    id: int
    name: str
    projectId: int


class JiraField(TypedDict):
    required: bool
    isArray: bool
    name: str
    id: str
    # TODO: Some allowed values are not str.
    allowedValues: NotRequired[List[Any]]


# Jira are case-sensitive APIs.
class JiraClient:
    def __init__(self, url: str, access_token: str) -> None:
        self.jira = JIRA(
            server=url,
            token_auth=access_token,
            timeout=20,
            options={"verify": False},
        )
        self._field_cache: Dict[
            str, Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]]
        ] = {}
        self._project_map: Dict[str, JiraProject] = {}
        # The dict key is project_name
        self._project_issue_map_using_name: Dict[str, List[JiraIssueType]] = {}
        # The dict key is project_id
        self._project_issue_map_using_id: Dict[int, List[JiraIssueType]] = {}
        # The dict key is: (project_id, issue_id).
        self._project_issue_field_map: Dict[Tuple[int, int], List[JiraField]] = {}

    def health_check(self) -> bool:
        try:
            if self.jira.myself() is not None:
                return True
            return False
        except JIRAError:
            return False

    # TODO: Based on jira field mapping path to build the dict.
    def create_story(self, fields: Dict[str, Any]) -> "Optional[Issue]":
        try:
            create_issue_body = convert_fields_to_create_issue_body(fields)
            return self.jira.create_issue(
                fields=create_issue_body,
                prefetch=False,
            )
        except JIRAError as e:
            print(
                f"Calling JIRA API failed. HttpStatusCode: {e.status_code}. Response: {e.response.json()}"
            )
        return None

    def get_jira_browser_link(self, key: str) -> "str":
        return f"{self.jira.server_url}/browse/{key}"

    def get_project_by_project_name(self, project_name: str) -> "Optional[JiraProject]":
        project_name = project_name.strip().lower()
        result = self._project_map.get(project_name, None)
        if result is None:
            self.get_projects()
        return self._project_map.get(project_name, None)

    def get_projects(
        self, include_archived: bool = False, force_refresh: bool = False
    ) -> "List[JiraProject]":
        # Otherwise, if there is no project, still will call API to retrieve project list.
        if self._project_map and force_refresh is not True:
            return list(self._project_map.values())
        self._project_map.clear()
        project_response = self.jira.projects()
        for proj in project_response:
            if include_archived or proj.archived is False:
                proj_name: str = proj.key
                proj_id: int = proj.id
                if proj_name:
                    self._project_map[proj_name.strip().lower()] = {
                        "id": proj.id,
                        "name": proj.key,
                    }
                    # loading project related issue types
                    try:
                        response = self.jira.createmeta_issuetypes(proj_id)
                        total = response.get("total", 0)
                        max_results = response.get("maxResults", 0)
                        if total > max_results:
                            raise NotImplementedError(
                                "Please check https://github.com/pycontribs/jira/pull/1729 for more info."
                            )
                        issue_types: List[JiraIssueType] = [
                            {
                                "id": issue_type["id"],
                                "name": issue_type.get("name", ""),
                                "projectId": proj.id,
                            }
                            for issue_type in response.get("values", [])
                        ]
                        self._project_issue_map_using_name[
                            proj_name.strip().lower()
                        ] = issue_types
                        self._project_issue_map_using_id[proj_id] = issue_types
                    except JIRAError:
                        print(f"Get issue types for project: {proj_name} failed.")
                        continue
        return list(self._project_map.values())

    def get_issue_type_by_project_id_and_issue_name(
        self, project_id: int, issue_name: str
    ) -> "Optional[JiraIssueType]":
        match_result = [
            i
            for i in self._project_issue_map_using_id[project_id]
            if i["name"].strip().lower() == issue_name.strip().lower()
        ]
        if match_result:
            return match_result[0]
        return None

    def get_issue_type_by_project_name_and_issue_name(
        self, project_name: str, issue_name: str
    ) -> "Optional[JiraIssueType]":
        project_name = project_name.strip().lower()
        if project_name not in self._project_issue_map_using_name:
            return None
        match_result = [
            i
            for i in self._project_issue_map_using_name[project_name]
            if i["name"].strip().lower() == issue_name.strip().lower()
        ]
        if match_result:
            return match_result[0]
        return None

    def get_issue_types(self, project_name: str) -> "List[JiraIssueType]":
        project_name = project_name.strip().lower()
        result = self._project_issue_map_using_name.get(project_name, [])
        if not result:
            self.get_project_by_project_name(project_name)
        return self._project_issue_map_using_name.get(project_name, [])

    def get_fields_by_project_id_and_issue_id(
        self, project_id: int, issue_id: int, required: bool = True
    ) -> "List[JiraField]":
        result = self._project_issue_field_map.get(
            (project_id, issue_id),
            [],
        )
        if not result:
            issue_response = self.jira.createmeta_issuetypes(project_id)
            total = issue_response.get("total", 0)
            max_results = issue_response.get("maxResults", 0)
            if total > max_results:
                raise NotImplementedError(
                    "Please check https://github.com/pycontribs/jira/pull/1729 for more info."
                )
            issue_types = issue_response.get("values", [])
            # Loading all issue types and related fields.
            for issue_type in issue_types:
                # Should be same as issue_name
                issue_type_id: int = issue_type.get("id", None)
                if (
                    project_id,
                    issue_type_id,
                ) not in self._project_issue_field_map:
                    field_response = self.jira.createmeta_fieldtypes(
                        project_id, issue_type_id
                    )
                    total = field_response.get("total", 0)
                    max_results = field_response.get("maxResults", 0)
                    if total > max_results:
                        raise NotImplementedError(
                            "Please check https://github.com/pycontribs/jira/pull/1729 for more info."
                        )
                    field_types = field_response.get("values", [])
                    if field_types:
                        self._project_issue_field_map[(project_id, issue_type_id)] = [
                            self._convert_field_type_to_jira_field(field_type)
                            for field_type in field_types
                        ]
        # Try to search again.
        result = self._project_issue_field_map.get(
            (project_id, issue_id),
            [],
        )
        return [i for i in result if i["required"] is required]

    def _convert_field_type_to_jira_field(self, field_type: Any) -> "JiraField":
        result: JiraField
        schema: Dict = field_type.get("schema")
        is_array: bool = "items" in schema
        if is_array:
            allowed_value_type: str = schema.get("items", "")
        else:
            allowed_value_type: str = schema.get("type", "")
        result = {
            "name": field_type.get("name", ""),
            "id": field_type.get("fieldId", ""),
            "isArray": field_type["schema"]["type"] == "array",
            "required": field_type["required"],
        }
        if "allowedValues" in field_type:
            allowed_value_path: str = "value"
            if allowed_value_type == "issuetype":
                allowed_value_path = "name"
            result["allowedValues"] = [
                allowed_value.get(allowed_value_path, "")
                for allowed_value in field_type.get("allowedValues", [])
            ]
        return result

    def get_all_fields(
        self,
    ) -> "Dict[str, Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]]]":
        if not self._field_cache:
            for field in self.jira.fields():
                if "schema" not in field.keys():
                    continue

                temp: Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]] = {
                    "id": field["id"],
                }

                class FieldSchema(TypedDict):
                    type: str
                    items: NotRequired[str]
                    custom: NotRequired[str]
                    customId: NotRequired[int]
                    system: NotRequired[str]

                schema: FieldSchema = field["schema"]
                property_name = field["id"]
                is_array = "items" in schema
                if is_array:
                    field_type = schema.get("items", None)
                else:
                    field_type = schema.get("type", None)

                if field_type is not None:
                    temp["properties"] = get_field_paths_of_jira_field(
                        field_type, property_name
                    )

                    self._field_cache[field["name"]] = temp
        return self._field_cache

    def get_stories_detail(
        self, story_ids: List[str], jira_fields: List[Dict[str, str]]
    ) -> "Dict[str, Dict[str, str]]":
        final_result = {}
        batch_size = 200

        try:
            if len(story_ids) > batch_size:
                start_index = 0
                end_index = batch_size
                while end_index <= len(story_ids) and start_index < len(story_ids):
                    # print(f"Start: {start_index}, End: {end_index}")
                    final_result.update(
                        self._internal_get_stories_detail(
                            story_ids[start_index:end_index], jira_fields
                        )
                    )
                    start_index = end_index
                    if start_index + batch_size < len(story_ids):
                        end_index = start_index + batch_size
                    else:
                        end_index = start_index + (len(story_ids) - end_index)
                return final_result

            return self._internal_get_stories_detail(story_ids, jira_fields)
        except JIRAError as e:
            print(
                f"Calling JIRA API failed. HttpStatusCode: {e.status_code}. Response: {e.response.json()}"
            )

            return {}

    def _internal_get_stories_detail(
        self, story_ids: List[str], jira_fields: List[Dict[str, str]]
    ) -> "Dict[str, Dict[str, str]]":
        id_query = ",".join([f"'{str(story_id).strip()}'" for story_id in story_ids])

        try:
            search_result: Dict[str, Any] = self.jira.search_issues(
                jql_str=f"id in ({id_query})",
                maxResults=len(story_ids),
                fields=[field["jira_name"] for field in jira_fields],
                json_result=True,
            )  # type: ignore

            final_result = {}
            for issue in search_result["issues"]:
                fields_result = {}
                for field in jira_fields:
                    # First element in the tuple is jira field name like "customfield_13210 or status..."
                    field_name = field["jira_name"]
                    # Remain elements represent the property path.
                    # Maybe no fields.
                    if "fields" in issue:
                        field_value: Any = issue["fields"]
                        for field_path in field["jira_path"].split("."):
                            if field_value is None:
                                field_value = ""
                                break
                            field_value = field_value.get(field_path, None)
                        fields_result[field_name] = field_value
                final_result[issue["key"].lower()] = fields_result

            return final_result
        except JIRAError as e:
            print(
                f"Calling JIRA API failed. HttpStatusCode: {e.status_code}. Response: {e.response.json()}"
            )

            return {}


def convert_fields_to_create_issue_body(fields: Dict[str, Any]) -> "Dict[str, Any]":
    issue_fields: Dict[str, Any] = {}
    for key, value in fields.items():
        field_paths = key.split(".")
        tmp = issue_fields
        for count, field_path in enumerate(field_paths):
            if count == len(field_paths) - 1:
                tmp[field_path] = value
            else:
                if tmp.get(field_path, None) is not None:
                    # merge exist dict keys.
                    tmp[field_path] = {**{}, **tmp[field_path]}
                else:
                    tmp[field_path] = {}
            tmp = tmp[field_path]
    return issue_fields
