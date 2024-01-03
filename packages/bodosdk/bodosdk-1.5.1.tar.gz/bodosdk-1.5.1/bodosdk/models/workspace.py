from typing import Optional, List, Any, Dict, Union
from uuid import UUID

from pydantic import Field

from bodosdk.models.base import CamelCaseBase, BodoRole, WorkspaceStatus


class CreateUpdateNotebookConfig(CamelCaseBase):
    instance_type: Optional[str] = Field(..., alias="instanceType")
    image_version: Optional[str] = Field(..., alias="imageVersion")


class AWSNetworkData(CamelCaseBase):
    vpc_id: Optional[str] = Field(..., alias="vpcId")
    public_subnets_ids: Optional[List[str]] = Field(..., alias="publicSubnetsIds")
    private_subnets_ids: Optional[List[str]] = Field(..., alias="privateSubnetsIds")


class WorkspaceDefinition(CamelCaseBase):
    name: str
    cloud_config_uuid: Union[UUID, str] = Field(..., alias="cloudConfigUUID")
    region: str = Field(..., alias="region")
    # TODO: [Important] In new endpoint workspaces/v1 is renamed to networkData
    aws_network_data: Optional[AWSNetworkData] = Field(None, alias="awsNetworkData")
    # TODO: [Deprecated] should be deleted in version +2.x.x
    default_notebook_config: Optional[CreateUpdateNotebookConfig] = Field(
        None, alias="defaultNotebookConfig"
    )
    # TODO: [Deprecated] should be deleted in version +2.x.x
    notebook_auto_deploy_enabled: Optional[bool] = Field(
        False, alias="notebookAutoDeployEnabled"
    )
    storage_endpoint: Optional[bool] = Field(True, alias="storageEndpoint")


class WorkspaceInfo(CamelCaseBase):
    id: str = Field(..., hidden=True)
    # TODO: This should be UUID in version +2.x.x
    uuid: str
    name: str
    # TODO: This should be WorkspaceStatus in version +2.x.x
    status: str
    # TODO: This should be UUID in version +2.x.x
    organization_uuid: str
    # TODO: [Deprecated] In new endpoints /workspaces/ maybe should be deleted when switch to new endpoint
    region: str
    cloud_config: Optional[Any] = Field(None, alias="cloudConfig")
    # TODO: [Deprecated] In new endpoints /workspaces/ maybe should be deleted when switch to new endpoint
    data: Any
    created_by: Optional[str] = Field(None, alias="createdBy")
    #  TODO: [Deprecated] should be deleted in version +2.x.x
    default_notebook_config: Any
    # TODO: [Deprecated] should be deleted in version +2.x.x
    notebook_autodeploy_enabled: Optional[bool] = Field(
        False, alias="notebookAutoDeployEnabled"
    )
    # TODO: [Deprecated] Not existing in backend anymore should be deleted in version +2.x.x
    type: str


class WorkspaceCreatedResponse(WorkspaceInfo):
    # TODO: [Deprecated] should be deleted in version +2.x.x
    notebook_auto_deploy_enabled: Optional[bool] = Field(
        False, alias="notebookAutoDeployEnabled"
    )
    # TODO: [Deprecated] maybe should be deleted in version +2.x.x there is no record that have value for that field
    assigned_at: Any = Field(..., alias="assignedAt")
    # TODO: [Deprecated] Not existing in backend anymore should be deleted in version +2.x.x
    cluster_credits_used_this_month: int = Field(
        None, alias="clusterCreditsUsedThisMonth"
    )
    # TODO: [Deprecated] should be deleted in version +2.x.x
    clusters: Any
    # TODO: [Deprecated] should be deleted in version +2.x.x
    notebooks: Any
    # TODO: [Deprecated] should be deleted in version +2.x.x
    jobs: Any


class WorkspaceListItem(CamelCaseBase):
    name: str
    # TODO: This should be UUID in version +2.x.x
    uuid: str
    status: WorkspaceStatus
    provider: str
    # TODO: [Deprecated] In new endpoints /workspaces/ maybe should be deleted when switch to new endpoint
    region: str
    # TODO: This should be UUID in version +2.x.x
    organization_uuid: str
    # TODO: [Deprecated] In new endpoints /workspaces/ maybe should be deleted when switch to new endpoint
    data: Optional[Any]
    server_time: Optional[str] = Field(..., alias="serverTime")
    # TODO: We don't need to return that field
    cloud_config: Optional[Any] = Field(..., alias="cloudConfig")
    created_by: Optional[str] = Field(..., alias="createdBy")
    # TODO: [Deprecated] Not existing in backend anymore should be deleted in version +2.x.x
    type: str


class WorkspaceResponse(CamelCaseBase):
    name: str
    # TODO: This should be UUID in version +2.x.x
    uuid: str
    status: WorkspaceStatus
    region: str
    organization_uuid: UUID = Field(..., alias="organizationUUID")
    data: Optional[Any]
    cloud_config: Optional[Dict] = Field(..., alias="cloudConfig")
    created_by: Optional[str] = Field(..., alias="createdBy")
    # TODO: [Deprecated] should be deleted in version +2.x.x
    notebook_auto_deploy_enabled: Optional[bool] = Field(
        False, alias="notebookAutoDeployEnabled"
    )
    # TODO: [Deprecated] should be deleted in version +2.x.x
    default_notebook_config: Optional[Dict] = Field(None, alias="defaultNotebookConfig")
    # TODO: [Deprecated] Not existing in backend anymore should be deleted in version +2.x.x
    type: str


class UserAssignment(CamelCaseBase):
    class Config:
        use_enum_values = True

    email: str
    skip_email: bool = Field(..., alias="skipEmail")
    bodo_role: BodoRole = Field(..., alias="bodoRole")
