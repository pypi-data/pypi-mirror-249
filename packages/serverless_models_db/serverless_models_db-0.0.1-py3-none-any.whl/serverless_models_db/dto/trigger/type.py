from ..base import DtoBase  # type: ignore


# API
class TriggerTypeDtoBase(DtoBase):
    name: str


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
