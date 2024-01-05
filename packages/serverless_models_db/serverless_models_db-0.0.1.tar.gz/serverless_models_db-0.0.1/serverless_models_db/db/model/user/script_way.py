from peewee import AutoField, CharField, ForeignKeyField

from ..base_model import DbBaseModel
from ..function import FunctionModel
from ..trigger import TriggerModel
from .user import UserModel


class UserScriptWayModel(DbBaseModel):
    """
    Используется для сохранения пользовательских скриптов
    """

    id = AutoField(column_name="id")
    id_trigger = ForeignKeyField(TriggerModel, backref="id_trigger")
    id_function = ForeignKeyField(FunctionModel, backref="id_function")
    id_owner = ForeignKeyField(UserModel, backref="id_user")

    name_unique = CharField(
        column_name="name_unique", unique=True
    )  # Для ссылки на узел графа workspace'а
    name_workspace = CharField(column_name="name_workspace")
