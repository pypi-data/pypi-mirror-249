from ..base import DtoBase  # type: ignore


# API
class UserScriptWayDtoBase(DtoBase):
    id_trigger: int
    id_function: int
    id_owner: int
    name_unique: str
    name_workspace: str


# DB
class UserScriptWayInDbDtoBase(UserScriptWayDtoBase):
    id: int


class UserScriptWayInDtoDb(UserScriptWayInDbDtoBase):
    pass


# POST
class UserScriptWayCreateDto(UserScriptWayDtoBase):
    pass


class UserScriptWayUpdateDto(UserScriptWayDtoBase):
    pass


# GET
class UserScriptWayDto(UserScriptWayInDbDtoBase):
    pass
