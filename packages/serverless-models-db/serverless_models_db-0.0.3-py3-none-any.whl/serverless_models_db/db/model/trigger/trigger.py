from peewee import AutoField, ForeignKeyField, TextField

from ..base_model import DbBaseModel
from .type import TriggerTypeModel


class TriggerModel(DbBaseModel):
    id = AutoField(column_name="id")

    condition = TextField(column_name="condition")
    id_type = ForeignKeyField(TriggerTypeModel, backref="triggers")
