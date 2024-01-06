from typing import List

from ..base import DtoBase
from .script_way import UserScriptWayCreateDto


# API
class WorkspaceDtoBase(DtoBase):
    id_owner: int
    name_workspace: str


# DB
class WorkspaceInDbDtoBase(WorkspaceDtoBase):
    id: int


# GET
class WorkspaceDto(WorkspaceInDbDtoBase):
    pass


# POST
class WorkspaceCreateDto(WorkspaceDtoBase):
    bindings: List[UserScriptWayCreateDto] = []
