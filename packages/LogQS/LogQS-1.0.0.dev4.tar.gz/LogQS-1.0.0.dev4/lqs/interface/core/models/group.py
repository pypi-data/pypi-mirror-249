from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    LockModel,
    LockCreateRequest,
    LockUpdateRequest,
    PaginationModel,
    optional_field,
)


class Group(CommonModel, LockModel):
    name: str
    note: Optional[str]
    context: Optional[dict]
    default_workflow_id: Optional[UUID]


class GroupDataResponse(BaseModel):
    data: Group


class GroupListResponse(PaginationModel):
    data: List[Group]


class GroupCreateRequest(LockCreateRequest):
    name: str
    note: Optional[str] = None
    context: Optional[dict] = None
    default_workflow_id: Optional[UUID] = None


class GroupUpdateRequest(LockUpdateRequest):
    name: str = optional_field
    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    default_workflow_id: Optional[UUID] = optional_field
