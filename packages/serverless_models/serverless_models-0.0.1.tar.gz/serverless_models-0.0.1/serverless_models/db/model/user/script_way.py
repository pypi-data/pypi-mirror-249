from peewee import AutoField, CharField, ForeignKeyField

from ..base_model import DbBaseModel
from ..trigger import TriggerModel
from .function import FunctionModel
from .user import UserModel


class WorkspaceModel(DbBaseModel):
    """
    Используется для сохранения рабочих областей пользователя
    """

    id = AutoField(column_name="id")
    id_owner = ForeignKeyField(UserModel, backref="id_user")
    name_workspace = CharField(column_name="name_workspace")

    class Meta:
        indexes = ((("id_owner", "name_workspace"), True),)


class UserScriptWayModel(DbBaseModel):
    """
    Используется для сохранения пользовательских скриптов
    """

    id = AutoField(column_name="id")
    id_trigger = ForeignKeyField(TriggerModel, backref="id_trigger")
    id_function = ForeignKeyField(FunctionModel, backref="id_function")

    name_unique = CharField(
        column_name="name_unique", unique=True
    )  # Для ссылки на узел графа workspace'а
    workspace_name = ForeignKeyField(WorkspaceModel, backref="id_workspace")
