from typing import Optional, List, Annotated
from enum import Enum
from pydantic import field_validator, BaseModel, BeforeValidator


LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class GeoFormat(Enum):
    """
    Attributes:
        type:
        fields:
        format:
    """

    json = "json"
    geojson = "geojson"


class CommunesParams(BaseModel):
    """
    Attributes:
        codePostal:
        lon:
        lat:
        nom:
        boost:
        code:
        siren:
        codeEpci:
        codeDepartement:
        codeRegion:
        zone:
        type:
        fields:
        format:
        geometry:
        limit:

    """

    codePostal: Optional[LaxStr] = None
    lon: Optional[float] = None
    lat: Optional[float] = None
    nom: Optional[str] = None
    boost: Optional[str] = None
    code: Optional[LaxStr] = None
    siren: Optional[str] = None
    codeEpci: Optional[LaxStr] = None
    codeDepartement: Optional[LaxStr] = None
    codeRegion: Optional[LaxStr] = None
    zone: Optional[str] = None
    type: Optional[str] = None
    fields: Optional[List[str]] = None
    format: Optional[GeoFormat] = GeoFormat.json
    geometry: Optional[str] = None
    limit: Optional[int] = None

    @field_validator("codeDepartement")
    @classmethod
    def code_departement_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v

    @field_validator("codeRegion")
    @classmethod
    def code_region_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class CommuneCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
        format:
        geometry:
    """

    code: Optional[LaxStr] = None
    fields: Optional[list] = None
    geometry: Optional[str] = None
    format: Optional[GeoFormat] = GeoFormat.json
    limit: Optional[int] = None


class EpcisCodeParams(CommuneCodeParams):
    pass


class DepartmentCommuneCodeParams(CommuneCodeParams):
    pass


class CommunesResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codePostaux:
        codeEpci:
        codeDepartement:
        codeRegion:
        population:
        _score:
    """

    nom: str
    code: LaxStr
    codePostaux: Optional[List[LaxStr]] = None
    codeEpci: Optional[str] = None
    codeDepartement: Optional[LaxStr] = None
    codeRegion: Optional[LaxStr] = None
    population: Optional[int] = None
    _score: Optional[float] = None
