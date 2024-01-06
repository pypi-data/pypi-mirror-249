import re
from typing import Optional, Union
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

optional_field = Field(default=None, json_schema_extra=lambda x: x.pop("default"))


def optional_field_alt(description: str):
    return Field(
        default=None,
        json_schema_extra=lambda x: x.pop("default"),
        description=description,
    )


class EmptyModel(BaseModel):
    pass


class ResourceModel(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    deleted_by: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def _describe(cls, return_description: bool = False):
        description = f"{cls.__name__}:\n"
        for field_name, field_info in cls.model_fields.items():
            if field_name in ResourceModel.model_fields:
                continue

            field_type = field_info.annotation
            if str(field_type).startswith("typing."):
                type_name = str(field_type)[7:]
            else:
                type_name = field_type.__name__
            type_name = re.sub(r"(\w+\.)+", "", type_name)

            field_title = f"{field_name} [{type_name}]"
            buffer_length = 38 - len(field_title)
            description += (
                f"{field_title}: {' ' * buffer_length}{field_info.description or ''}\n"
            )
        description = description[:-1]
        if return_description:
            return description
        else:
            print(description)

    _repr_fields = ("id", "name")

    def __repr__(self):
        model_name = self.__class__.__name__
        value = f"<{model_name} "
        for field_name in self._repr_fields:
            if field_name in self.model_fields:
                value += f"{field_name}={getattr(self, field_name)}, "
        value = value[:-2] + ">"
        return value

    @classmethod
    def set_app(cls, app):
        cls.app = app

    @classmethod
    def fetch(cls, *args):
        if len(args) == 0:
            raise ValueError("No ID or name provided.")

        id = None
        friendly_id = None
        parent_id = None
        try:
            if type(args[0]) == UUID:
                id = args[0]
            elif type(args[0]) == int:
                id = int(args[0])
            else:
                id = UUID(args[0])
        except ValueError:
            friendly_id = args[0]
        if len(args) > 1:
            try:
                parent_id = UUID(args[1])
            except ValueError:
                raise ValueError(
                    "Second argument must be the UUID of the parent resource."
                )

        if id is not None:
            fetch_method = getattr(cls.app.fetch, cls.__name__.lower())
            if parent_id is not None:
                return fetch_method(id, parent_id).data
            else:
                return fetch_method(id).data
        elif friendly_id is not None:
            fields = cls._repr_fields.default
            if len(fields) < 2:
                raise Exception(f"Cannot fetch {cls.__name__} without it's ID.")

            list_method = getattr(cls.app.list, cls.__name__.lower())

            list_args = {
                fields[1]: friendly_id,
                "order": "created_at",
                "sort": "desc",
                "limit": 1,
            }
            if parent_id is not None:
                list_res = list_method(parent_id, **list_args)
            else:
                list_res = list_method(**list_args)
            if list_res.count == 0:
                raise ValueError(f"No {cls.__name__} found.")
            elif list_res.count > 1:
                cls.warn(f"Multiple {cls.__name__}s ({list_res.count}) found.")
            return list_res.data[0]
        else:
            raise ValueError("No ID provided.")

    @classmethod
    def list(cls, *args, **kwargs):
        list_method = getattr(cls.app.list, cls.__name__.lower())
        return list_method(*args, **kwargs).data

    @classmethod
    def create(cls, *args, **kwargs):
        create_method = getattr(cls.app.create, cls.__name__.lower())
        return create_method(*args, **kwargs).data

    @classmethod
    def update(cls, *args, **kwargs):
        update_method = getattr(cls.app.update, cls.__name__.lower())
        return update_method(*args, **kwargs).data

    @classmethod
    def delete(cls, *args, **kwargs):
        delete_method = getattr(cls.app.delete, cls.__name__.lower())
        return delete_method(*args, **kwargs).data


class CommonModel(ResourceModel):
    id: UUID = Field(..., description="The ID of the resource.")


class TimeSeriesModel(ResourceModel):
    timestamp: int = Field(..., description="The timestamp of the resource.")


class PaginationModel(BaseModel):
    offset: int
    limit: int
    order: str
    sort: str
    count: int


class PatchOperation(BaseModel):
    op: str
    path: str
    value: Optional[Union[str, int, float, bool, dict, list, None]]


class JSONFilter(BaseModel):
    var: str
    op: str
    val: Union[str, int, float, bool, list, None]
