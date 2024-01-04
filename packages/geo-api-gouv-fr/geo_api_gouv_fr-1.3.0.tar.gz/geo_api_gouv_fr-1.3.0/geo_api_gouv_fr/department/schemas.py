from typing import Optional, List, Annotated
from pydantic import field_validator, BaseModel, BeforeValidator


LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class DepartmentsParams(BaseModel):
    """
    Attributes:
        nom:
        codeRegion:
        code:
        limit:
        fields:

    """

    nom: Optional[str] = None
    codeRegion: Optional[LaxStr] = None
    code: Optional[LaxStr] = None
    limit: Optional[int] = None
    fields: Optional[List[str]] = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v

    @field_validator("codeRegion")
    @classmethod
    def code_region_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
    """

    code: Optional[LaxStr] = None
    fields: Optional[list] = None
    limit: Optional[int] = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class RegionDepartmentCodeParams(BaseModel):
    """
    Attributes:
        regioncode:
        limit:
    """

    code: Optional[LaxStr] = None
    limit: Optional[int] = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codeRegion: int
        fields:
        _score:
    """

    nom: str
    code: int
    codeRegion: int
    fields: Optional[list] = None
    _score: Optional[float] = None
