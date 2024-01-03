import logging
from typing import List, Union
from uuid import UUID

from bodosdk.api.workspace import WorkspaceApi
from bodosdk.models import (
    WorkspaceDefinition,
    WorkspaceCreatedResponse,
    WorkspaceListItem,
    TaskInfo,
)
from bodosdk.models.workspace import UserAssignment, WorkspaceResponse


class WorkspaceClient:
    def __init__(self, api: WorkspaceApi):
        self._api = api

    def create(
        self, workspace_definition: WorkspaceDefinition
    ) -> WorkspaceCreatedResponse:
        """
        Creates workspace
        :param workspace_definition:
        :type workspace_definition: WorkspaceDefinition
        :return: workspace object
        :rtype: WorkspaceCreatedResponse
        """
        logging.warning(
            "Fields [notebook_auto_deploy_enabled, default_notebook_config, type] in WorkspaceCreatedResponse "
            "are deprecated. Will be removed in version +2.x.x"
        )
        return self._api.create_workspace(workspace_definition)

    # TODO: need to unify sometimes parameter is uuid sometimes is called workspace_uuid
    def remove(self, uuid: Union[str, UUID], mark_as_terminated: bool = False):
        """
        Removes workspace
        :param uuid: uuid of workspace to remove
        :type uuid: str
        :param mark_as_terminated: if True workspace resources won't be removed, workspace will be marked as terminated
        :type mark_as_terminated: bool
        """
        return self._api.remove_workspace(uuid, mark_as_terminated)

    def list(self) -> List[WorkspaceListItem]:
        """
        Gets list of workspaces
        :return:
        """
        logging.warning(
            "Fields [type] in WorkspaceListItem "
            "are deprecated. Will be removed in version +2.x.x"
        )
        return self._api.list_all_workspaces()

    # TODO: need to unify sometimes parameter is uuid sometimes is called workspace_uuid
    def get(self, workspace_uuid: Union[str, UUID]) -> WorkspaceResponse:
        """
        Get workspace for specific uuid
        :param workspace_uuid:
        :return:
        """
        logging.warning(
            "Fields [notebook_auto_deploy_enabled, default_notebook_config, type] in WorkspaceResponse "
            "are deprecated. Will be removed in version +2.x.x"
        )
        return self._api.get_workspace(str(workspace_uuid))

    # TODO: need to unify sometimes parameter is uuid sometimes is called workspace_uuid
    def assign_users(
        self, workspace_uuid: Union[str, UUID], users: List[UserAssignment]
    ):
        """
        Assign users to specifed workspace
        :param workspace_uuid:
        :param users:
        :type users: List[UserAssignment]
        :return:
        """
        self._api.assign_users(workspace_uuid, users)

    # TODO: need to unify sometimes parameter is uuid sometimes is called workspace_uuid
    def get_tasks(self, workspace_uuid: Union[str, UUID]) -> List[TaskInfo]:
        """
        Get workspace tasks for specific uuid
        :param workspace_uuid: Union[str, UUID]
        :return: List[TaskInfo]
        """
        return self._api.get_tasks(workspace_uuid)
