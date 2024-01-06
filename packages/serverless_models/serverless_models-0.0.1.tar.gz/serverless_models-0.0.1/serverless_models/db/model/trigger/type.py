from peewee import AutoField, BooleanField, CharField

from ..base_model import DbBaseModel


class TriggerTypeModel(DbBaseModel):
    id = AutoField(column_name="id")
    name = CharField(column_name="name")
    can_be_first = BooleanField(column_name="can_be_first")
