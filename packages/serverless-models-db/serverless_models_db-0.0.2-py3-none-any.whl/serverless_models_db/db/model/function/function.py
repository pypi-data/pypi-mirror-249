from datetime import datetime

from peewee import (
    AutoField,
    BlobField,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    ManyToManyField,
    TextField,
)

from ..base_model import DbBaseModel
from ..user import UserModel
from .tag import FunctionTagModel


class FunctionModel(DbBaseModel):

    """
    Используется для сохранения пользовательских скриптов
    """

    id = AutoField(column_name="id")
    id_owner = ForeignKeyField(UserModel, backref="id_owner")

    is_public = BooleanField(default=False, column_name="is_public")

    name = CharField(column_name="name")
    description = TextField(column_name="description")
    file = BlobField(column_name="file")
    datetime_creation = DateTimeField(
        default=datetime.now(), column_name="datetime_creation"
    )
    tags = ManyToManyField(FunctionTagModel, backref="functions")
