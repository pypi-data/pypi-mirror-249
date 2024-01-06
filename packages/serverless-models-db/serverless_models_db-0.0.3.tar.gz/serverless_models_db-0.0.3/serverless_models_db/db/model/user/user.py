from peewee import AutoField, CharField, ManyToManyField

from ..base_model import DbBaseModel
from .role import UserRoleModel


class UserModel(DbBaseModel):
    """
    Используется как основная модель пользователя
    """

    id = AutoField(column_name="id")
    role = ManyToManyField(UserRoleModel, backref="users")

    password_hash = CharField(column_name="password_hash")

    email = CharField(column_name="email", default="")
    first_name = CharField(column_name="first_name", default="")
    last_name = CharField(column_name="last_name", default="")
    name = CharField(column_name="name", unique=True)
