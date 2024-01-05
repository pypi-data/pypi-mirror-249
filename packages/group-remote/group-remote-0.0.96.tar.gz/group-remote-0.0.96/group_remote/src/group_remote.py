# TODO: This is an example file which you should delete after implementing
import os
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local.url_circlez import OurUrl
from url_local.component_name_enum import ComponentName
from url_local.entity_name_enum import EntityName
from url_local.action_name_enum import ActionName
from circles_local_database_python.generic_mapping import GenericMapping
import requests
import sdk.src.utilities as utilities
from user_context_remote.user_context import UserContext
from dotenv import load_dotenv
load_dotenv()

# user variable is created by UserContext._instance() call in login_using_user_identification_and_password()
user_context = UserContext()
user = user_context.login_using_user_identification_and_password()


GROUP_REMOTE_COMPONENT_ID = 213
GROUP_PROFILE_COMPONENT_NAME = "Group Remote Python"
DEVELOPER_EMAIL = "yarden.d@circ.zone"

GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT = {
    'component_id': GROUP_REMOTE_COMPONENT_ID,
    'component_name': GROUP_PROFILE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'component_type': LoggerComponentEnum.ComponentType.Remote.value,
    "developer_email": DEVELOPER_EMAIL
}

GROUP_REMOTE_API_VERSION = 1


class GroupsRemote:

    def __init__(self) -> None:
        self.our_url = OurUrl()
        self.logger = Logger.create_logger(
            object=GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT)
        self.brand_name = os.getenv("BRAND_NAME")
        self.environment_name = os.getenv("ENVIRONMENT_NAME")

    def get_all_groups(self):  # GET
        self.logger.start("Start get_all_groups group-remote")

        query_params = dict(
            langCode=self.logger.user_context.get_effective_profile_preferred_lang_code())

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_ALL_GROUPS.value,  # "getAllGroups",
                query_parameters=query_params
            )

            self.logger.info(
                "Endpoint group remote - getAllGroups action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(
                f"End get_all_groups group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End get_all_groups group-remote")

    # TODO I wish we can change groupName: GroupName (so group name will no be from type str but from GroupName type/class)
    def get_group_by_group_name(self, groupName: str, titleLangCode=None):  # GET
        self.logger.start("Start get_group_by_name group-remote")
        titleLangCode = titleLangCode or self.logger.user_context.get_effective_profile_preferred_lang_code()
        query_params = dict(langCode=titleLangCode,
                            name=groupName)

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_GROUP_BY_NAME.value,  # "getGroupByName",
                query_parameters=query_params
            )

            self.logger.info(
                "Endpoint group remote - getGroupByName action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(
                f"End get_group_by_name group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End get_group_by_name group-remote")

    def get_group_by_group_id(self, groupId: str, titleLangCode=None):  # GET
        self.logger.start("Start get_group_by_id group-remote")
        titleLangCode = titleLangCode or self.logger.user_context.get_effective_profile_preferred_lang_code()
        query_params = dict(langCode=titleLangCode)

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_GROUP_BY_ID.value,  # "getGroupById",
                path_parameters={'groupId': groupId},
                query_parameters=query_params,
            )

            self.logger.info(
                "Endpoint group remote - getGroupById action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(
                f"End get_group_by_id group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End get_group_by_id group-remote")

    def create_group(self, title: str, titleLangCode: str = None, parentGroupId: str = None, isInterest: bool = None,
                     image: str = None):  # POST
        self.logger.start("Start create group-remote")

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.CREATE_GROUP.value,  # "createGroup",
            )

            self.logger.info(
                "Endpoint group remote - createGroup action: " + url)

            payload = {
                "title": title
            }

            if titleLangCode:
                payload["titleLangCode"] = titleLangCode
            if parentGroupId:
                payload["parentGroupId"] = parentGroupId
            if isInterest:
                payload["isInterest"] = isInterest
            if image:
                payload["image"] = image

            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.post(url, json=payload, headers=header)
            self.logger.end(
                f"End create group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End create group-remote")

    def update_group(self, groupId: int, title: str = None, titleLangCode: str = None, parentGroupId: str = None,
                     isInterest: bool = None, image: str = None):  # PATCH
        self.logger.start("Start update group-remote")

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.UPDATE_GROUP.value,  # "updateGroup",
                path_parameters={'groupId': groupId},

            )

            self.logger.info(
                "Endpoint group remote - updateGroup action: " + url)

            payload = {
                "title": title,
            }

            if titleLangCode is not None:
                payload["titleLangCode"] = titleLangCode
            if parentGroupId is not None:
                payload["parentGroupId"] = parentGroupId
            if isInterest is not None:
                payload["isInterest"] = isInterest
            if image is not None:
                payload["image"] = image

            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.patch(url, json=payload, headers=header)
            self.logger.end(
                f"End update group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End update group-remote")

    def delete_group(self, groupId: int):  # DELETE
        self.logger.start("Start delete group-remote")

        try:
            url = self.our_url.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.DELETE_GROUP.value,  # "deleteGroup",
                path_parameters={'groupId': groupId},
            )

            self.logger.info(
                "Endpoint group remote - deleteGroup action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.delete(url, headers=header)
            self.logger.end(
                f"End delete group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(
                log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(
                f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End delete group-remote")

        # TODO Develop merge_groups( main_group_id_a, identical_group_id) # We should link everything from identical_group
        # to main_group, main_group should have new alias names, we should be logically delete identical_group, we
        # should be able to unmerge_groups
        # TODO Develop unmerge_groups( main_group_id_a, identical_group_id ) # Low priority
        # TODO Develop link_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents
        # TODO Develop unlink_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents

    # TODO: temporary location: Move to group-local after changing group=local to current python local tamplate
    def add_update_group_and_link_to_contact(self, entity_name: str, contact_id: str, mapping_info: dict, title: str = None,
                                             title_lang_code: str = None, parent_group_id: str = None,
                                             is_interest: bool = None, image: str = None):

        self.logger.start(
            "Start add_update_group_and_link_to_contact group-remote")
        try:
            # Creating an instance of GenericMapping
            generic_mapping = GenericMapping(default_schema_name=mapping_info['default_schema_name'],
                                             default_id_column_name=mapping_info['default_id_column_name'],
                                             default_table_name=mapping_info['default_table_name'],
                                             default_view_table_name=mapping_info['default_view_table_name'],
                                             default_entity_name1=mapping_info['default_entity_name1'],
                                             default_entity_name2=mapping_info['default_entity_name2'])

            # Retrieving all group names
            groups = self.get_all_groups()
            group_names = []
            for group in groups['data']:
                group_names.append(group['name'])

            # Initializing lists to store groups to link and groups that are successfully linked
            groups_to_link = []
            groups_linked = []

            # Iterating through group names to find matching groups based on entity_name
            for group in group_names:
                if group is None:
                    continue
                if entity_name in group:
                    groups_to_link.append(group)

            # If no matching groups found based on entity_name
            if len(groups_to_link) == 0:
                # Creating a new group with the entity_name
                title = entity_name
                group_id = self.create_group(title=title, titleLangCode=title_lang_code,
                                             isInterest=is_interest)
                # Inserting mapping between contact and the newly created group
                generic_mapping.insert_mapping(
                    'contact', 'group', contact_id, group_id)
                groups_linked.append((group_id, title))
            else:
                # Linking contact with existing groups found based on entity_name
                for group in groups_to_link:
                    group_id = self.get_group_by_group_name(
                        groupName=group).json()['data'][0]['id']

                    # Check if contact is already linked to group
                    if self.is_mapping_exist(generic_mapping, 'contact', 'group', contact_id, group_id):
                        self.logger.info(
                            f"Contact is already linked to group: {group}")
                        self.update_group(groupId=group_id, title=title, titleLangCode=title_lang_code,
                                          parentGroupId=parent_group_id, isInterest=is_interest, image=image)
                    else:
                        generic_mapping.insert_mapping(
                            'contact', 'group', contact_id, group_id)
                        groups_linked.append((group_id, group))

            self.logger.end("Group linked to contact", object={
                            'groups_linked': groups_linked})
            return groups_linked

        except Exception as e:
            self.logger.exception("Failed to link group to contact", object={
                                  'groups_linked': groups_linked})
            self.logger.end("Failed to link group to contact")
            raise e

    #TODO: temporary location: Move to generic-mapping after resolving issue with generic-crud tests
    def is_mapping_exist(self, generic_mapping: GenericMapping, entity_name1: str, entity_name2: str, entity_id1: int, entity_id2: int) -> bool:
        """Checks if a link between two entities exists.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :return: True if the link exists, False otherwise.
        """
        self.logger.start(object={"entity_name1": entity_name1, "entity_name2": entity_name2, "entity_id1": entity_id1,
                                  "entity_id2": entity_id2})
        combined_table_name = f"{entity_name1}_{entity_name2}_table"
        where = f"{entity_name1}_id=%s AND {entity_name2}_id=%s"
        params = (entity_id1, entity_id2)
        select_query = f"SELECT * " \
                       f"FROM {generic_mapping.schema_name}.{combined_table_name} " \
                       f"WHERE {where}"
        try:
            generic_mapping.cursor.execute(select_query, params)
            result = generic_mapping.cursor.fetchall()
            self.logger.end("Data selected successfully.",
                            object={"result": result})
            return True if result else False
        except Exception as e:
            self.logger.exception("Failed to select data.",
                                  object={"select_query": select_query, "params": params})
            self.logger.end("Failed to select data.")
            raise e
