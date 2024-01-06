from datetime import datetime

from peewee import AutoField, DateTimeField, DecimalField, ForeignKeyField

from .base_model import DbBaseModel
from .function.function import FunctionModel
from .user.script_way import UserScriptWayModel


class LogModel(DbBaseModel):
    """
    Используется для логирования на втором бэкенде, который обрабатывает
    пользовательские триггеры
    """

    id = AutoField(column_name="id")
    id_function = ForeignKeyField(FunctionModel, backref="id_function")
    id_script_way = ForeignKeyField(UserScriptWayModel, backref="id_script_way")

    datetime = DateTimeField(default=datetime.now(), column_name="datetime")
    cost = DecimalField(column_name="cost")  # затраченные мощности на момент лога
