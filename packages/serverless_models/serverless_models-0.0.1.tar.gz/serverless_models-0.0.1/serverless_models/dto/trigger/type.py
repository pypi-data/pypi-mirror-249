from ..base import DtoBase


# API
class TriggerTypeDtoBase(DtoBase):
    name: str
    can_be_first: bool


# DB
class TriggerTypeInDbDtoBase(TriggerTypeDtoBase):
    id: int


class TriggerTypeInDbDto(TriggerTypeInDbDtoBase):
    pass


# GET
class TriggerTypeDto(TriggerTypeInDbDtoBase):
    pass


# POST
class TriggerTypeCreateDto(TriggerTypeDtoBase):
    pass
