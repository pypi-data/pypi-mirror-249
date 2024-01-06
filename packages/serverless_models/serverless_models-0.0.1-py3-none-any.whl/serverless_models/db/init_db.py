# type: ignore

from peewee import PostgresqlDatabase

from .model import *  # pylint: disable=W0401,W0614

db_models = DbBaseModel.__subclasses__()


def init_database(db: PostgresqlDatabase) -> None:
    # pylint: disable=no-member
    related_models = {
        FunctionModel: [FunctionModel.tags.through_model],
        UserModel: [UserModel.role.through_model],
    }
    for model in db_models:
        db.create_tables([model])
        if model in related_models:
            db.create_tables(related_models[model])
