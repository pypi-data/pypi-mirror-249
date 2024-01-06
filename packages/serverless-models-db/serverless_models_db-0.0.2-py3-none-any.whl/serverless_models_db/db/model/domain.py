from peewee import AutoField, CharField, ForeignKeyField

from .base_model import DbBaseModel
from .trigger.trigger import TriggerModel


class DomainModel(DbBaseModel):
    """
    Домен - то, на что мы можем подписаться, для...

    Пример:
    Github - это домен, а тот факт,
    что мы можем подписаться на событие обновления репозитория - это его функция
    """

    id = AutoField(column_name="id")
    id_trigger = ForeignKeyField(TriggerModel, backref="trigger")

    name = CharField(column_name="name")
