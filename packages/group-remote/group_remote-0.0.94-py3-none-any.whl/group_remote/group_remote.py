# TODO: This is an example file which you should delete after implementing
import os
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local.url_circlez import OurUrl
from url_local.component_name_enum import ComponentName
from url_local.entity_name_enum import EntityName
from url_local.action_name_enum import ActionName
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
        self.logger = Logger.create_logger(object=GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT)
        self.brand_name = os.getenv("BRAND_NAME")
        self.environment_name = os.getenv("ENVIRONMENT_NAME")

    def get_all_groups(self):  # GET
        self.logger.start("Start get_all_groups group-remote")

        query_params = dict(langCode=self.logger.user_context.get_effective_profile_preferred_lang_code())

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

            self.logger.info("Endpoint group remote - getAllGroups action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(f"End get_all_groups group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
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

            self.logger.info("Endpoint group remote - getGroupByName action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(f"End get_group_by_name group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
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

            self.logger.info("Endpoint group remote - getGroupById action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.get(url, headers=header)
            self.logger.end(f"End get_group_by_id group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
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

            self.logger.info("Endpoint group remote - createGroup action: " + url)

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
            self.logger.end(f"End create group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
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

            self.logger.info("Endpoint group remote - updateGroup action: " + url)

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
            self.logger.end(f"End update group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
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

            self.logger.info("Endpoint group remote - deleteGroup action: " + url)
            user_jwt = user.get_user_jwt()
            header = utilities.create_http_headers(user_jwt)
            response = requests.delete(url, headers=header)
            self.logger.end(f"End delete group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception(log_message="ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise
        except requests.Timeout as exception:
            self.logger.exception(log_message="Timeout Exception- Request timed out", object={'exception': exception})
            raise
        except requests.RequestException as exception:
            self.logger.exception(log_message=(f"RequestException Exception- General error: {str(exception)}", exception))
            raise
        except Exception as exception:
            self.logger.exception(log_message=(f"An unexpected error occurred: {str(exception)}", exception))
            raise
        finally:
            self.logger.end("End delete group-remote")

        # TODO Develop merge_groups( main_group_id_a, identical_group_id) # We should link everything from identical_group
        # to main_group, main_group should have new alias names, we should be logically delete identical_group, we
        # should be able to unmerge_groups
        # TODO Develop unmerge_groups( main_group_id_a, identical_group_id ) # Low priority
        # TODO Develop link_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents
        # TODO Develop unlink_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents
