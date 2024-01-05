from enum import Enum

from peewee import AutoField, CharField

from ..base_model import DbBaseModel


class UserRoleEnum(str, Enum):
    ADMIN = "Admin"
    USER = "User"


class UserRoleModel(DbBaseModel):
    """
    Роли пользователя
    """

    id = AutoField(column_name="id")
    name = CharField(column_name="name", unique=True)
