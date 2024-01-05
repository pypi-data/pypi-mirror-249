from decimal import Decimal
from time import struct_time

from .base import DtoBase
from .function import FunctionInDbDto
from .user import UserScriptWayInDtoDb


# API
class LogDtoBase(DtoBase):
    name: str
    datetime: struct_time
    cost: Decimal


# DB
class LogInDbDtoBase(LogDtoBase):
    id: int
    id_function: int
    id_script_way: int


class LogInDbDto(LogInDbDtoBase):
    function: FunctionInDbDto
    user_scrpit_way: UserScriptWayInDtoDb


# GET
class LogDto(LogInDbDtoBase):
    pass


# POST
class LogCreateDto(LogDtoBase):
    pass
