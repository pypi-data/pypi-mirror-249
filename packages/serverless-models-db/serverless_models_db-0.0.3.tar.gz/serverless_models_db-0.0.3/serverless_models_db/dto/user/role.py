from ..base import DtoBase  # type: ignore


# API
class UserRoleDtoBase(DtoBase):
    name: str


# DB
class UserRoleInDbDtoBase(UserRoleDtoBase):
    id: int


class UserRoleInDtoDb(UserRoleInDbDtoBase):
    pass


# GET
class UserRoleDto(UserRoleInDbDtoBase):
    pass


# POST
class UserRoleAddDto(UserRoleDtoBase):
    pass


class UserRoleUpdateDto(UserRoleAddDto):
    pass
