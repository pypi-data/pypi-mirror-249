from typing import Optional, Annotated
from pydantic import field_validator, BaseModel, BeforeValidator

LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class RegionsParams(BaseModel):
    """
    Attributes:
        nom:
        code:
        limit:
    """

    nom: Optional[str] = None
    code: Optional[LaxStr] = None
    limit: Optional[int] = None


class RegionCodeParams(BaseModel):
    """
    Attributes:
        code:
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


class RegionsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        _score:
    """

    nom: str
    code: int
    _score: Optional[float] = None
