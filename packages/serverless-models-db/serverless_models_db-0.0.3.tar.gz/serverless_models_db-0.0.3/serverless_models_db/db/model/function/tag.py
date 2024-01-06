from peewee import AutoField, CharField

from ..base_model import DbBaseModel


class FunctionTagModel(DbBaseModel):
    id = AutoField(column_name="id")
    name = CharField(column_name="name")
