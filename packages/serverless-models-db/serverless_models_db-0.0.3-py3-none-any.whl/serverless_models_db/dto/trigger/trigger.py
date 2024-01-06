from ..base import DtoBase  # type: ignore


# API
class TriggerDtoBase(DtoBase):
    condition: str
    id_type: int


# DB
class TriggerInDbDtoBase(TriggerDtoBase):
    id: int


class TriggerInDbDto(TriggerInDbDtoBase):
    pass


# GET
class TriggerDto(TriggerInDbDtoBase):
    pass


# POST
class TriggerCreateDto(TriggerDtoBase):
    pass
