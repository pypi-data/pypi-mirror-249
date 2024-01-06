from typing import Any

from peewee import Model

from ..session import get_db


class DbBaseModel(Model):  # type: ignore
    id: Any
    __name__: str

    class Meta:
        legacy_table_names = False
        database = get_db()
