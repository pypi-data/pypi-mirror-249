from pydantic import create_model

from .base_model import DbBaseModel


def create_new_model(base_model, exclude_fields):
    fields = {
        field: (field_type, ...)
        for field, field_type in base_model.__annotations__.items()
        if field not in exclude_fields
    }

    return create_model(f"new{base_model.__name__}", __base__=DbBaseModel, **fields)  # type: ignore
