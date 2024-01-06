from datetime import datetime

from ..base import DtoBase
from ..user import UserInDbDto
from .tag import FunctionTagInDbDto


# API
class FunctionDtoBase(DtoBase):
    datetime_creation: datetime
    description: str
    file: str
    name: str
    is_public: bool
    owner_name: str


# DB
class FunctionInDbDtoBase(FunctionDtoBase):
    id: int
    id_owner: int
    id_tags: list[int]


class FunctionInDbDto(FunctionInDbDtoBase):
    owner: UserInDbDto
    tags: list[FunctionTagInDbDto]


# GET
class FunctionDto(FunctionInDbDtoBase):
    pass


# POST
class FunctionCreateDto(FunctionDtoBase):
    pass
