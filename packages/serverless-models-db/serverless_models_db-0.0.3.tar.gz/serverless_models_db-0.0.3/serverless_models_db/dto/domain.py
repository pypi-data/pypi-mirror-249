from .base import DtoBase
from .trigger import TriggerInDbDto


# API
class DomainDtoBase(DtoBase):
    name: str


# DB
class DomainInDbDtoBase(DomainDtoBase):
    id: int
    id_trigger: int


class DomainInDbDto(DomainInDbDtoBase):
    trigger: TriggerInDbDto


# POST
class DomainCreateDto(DomainDtoBase):
    pass


class DomainUpdateDto(DomainDtoBase):
    pass


# GET
class DomainDto(DomainInDbDtoBase):
    pass
