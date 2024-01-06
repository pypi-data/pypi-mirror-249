from pydantic import validator

from ..base import DtoBase  # type: ignore
from .role import UserRoleInDtoDb


# API
class UserDtoBase(DtoBase):
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    name: str


# DB
class UserInDbDtoBase(UserDtoBase):
    id: int
    id_role: int = None  # type: ignore


class UserInDbDto(UserInDbDtoBase):
    hashed_password: str
    role: UserRoleInDtoDb


# POST
class UserAddDto(UserDtoBase):
    password: str

    @validator("password", pre=True)
    def validate_password_length(  # pylint: disable=no-self-argument
        cls, value: str
    ) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class UserAddResponseDto(DtoBase):
    access_token: str


class UserUpdateDto(DtoBase):
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    name: str = ""
    password: str = ""


# GET
class UserDto(UserInDbDtoBase):
    pass
