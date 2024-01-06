from ..base import DtoBase  # type: ignore


# API
class UserScriptWayDtoBase(DtoBase):
    id_trigger: int
    id_function: int
    name_unique: str
    workspace_name: int


# DB
class UserScriptWayInDbDtoBase(UserScriptWayDtoBase):
    id: int


class UserScriptWayInDtoDb(UserScriptWayInDbDtoBase):
    pass


# POST
class UserScriptWayCreateDto(UserScriptWayDtoBase):
    pass


class UserScriptWayUpdateDto(UserScriptWayDtoBase):
    pass


# GET
class UserScriptWayDto(UserScriptWayInDbDtoBase):
    pass
