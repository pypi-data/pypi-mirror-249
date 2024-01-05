from ..base import DtoBase  # type: ignore


# API
class FunctionTagDtoBase(DtoBase):
    name: str


# DB
class FunctionTagInDbDtoBase(FunctionTagDtoBase):
    id: int


class FunctionTagInDbDto(FunctionTagInDbDtoBase):
    pass


# GET
class FunctionTagDto(FunctionTagInDbDtoBase):
    pass


# POST
class FunctionTagCreateDto(FunctionTagDtoBase):
    pass
