from typing import List, Optional, Annotated
from pydantic import field_validator, BaseModel, BeforeValidator

LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class SearchParams(BaseModel):
    """
    Attributes:
        q:
        limit:
        autocomplete:
        type:
        postcode:
        lat:
        lon:

    """

    q: Optional[str] = None
    limit: Optional[int] = None
    autocomplete: Optional[int] = None
    type: Optional[str] = None
    postcode: Optional[LaxStr] = None
    citycode: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

    @field_validator("q")
    @classmethod
    def add_smaller_than_200(cls, v):
        """Validator for query to be smaller than 200 characters"""
        return v[:200]

    @field_validator("type")
    @classmethod
    def type_must_be_in(cls, v):
        """Validator for type

        Rules:
            Must be part of:
                - housenumber
                - street
                - locality
                - municipality

        Raises:
            ValueError:
        """
        values = ["housenumber", "street", "locality", "municipality"]
        if v not in values:
            raise ValueError(f"Type value must be in {values}")
        return v


class SearchCSVParams(BaseModel):
    """
    Attributes:
        columns:
        result_columns:
        postcode:
        citycode:
    """

    columns: Optional[List[str]] = None
    result_columns: Optional[List[str]] = None
    postcode: Optional[LaxStr] = ""
    citycode: Optional[str] = ""


class ReverseParams(BaseModel):
    """
    Attributes:
        lat:
        lon:
        type:
        limit:
    """

    lat: float
    lon: float
    type: Optional[str] = None
    limit: Optional[int] = None


# results ( everything optional in order to avoid mistakes)


class GpsCoordinate(BaseModel):
    """
    Attributes:
        latitude:
        longitude:
    """

    latitude: float
    longitude: float


class Geometry(BaseModel):
    """
    Attributes:
        type:
        coordinates:
    """

    type: Optional[str] = None
    coordinates: Optional[List] = None

    @field_validator("coordinates")
    @classmethod
    def coord_must_have_lat_lon(cls, v):
        """Validator for coordinates

        Rules:
            - Coordinates muse have latitude & longitude
            - Latitude value must be in [-180, 180]
            - Longitude value must be in [-90, 90]

        Raises:
            ValueError:
        """
        if len(v) != 2:
            raise ValueError("Coordinates muse have latitude & longitude")

        if v[0] > 180 or v[0] < -180:
            raise ValueError("Latitude value must be in [-180, 180]")

        if v[1] > 90 or v[1] < -90:
            raise ValueError("Longitude value must be in [-90, 90]")

        return v


class Properties(BaseModel):
    """Properties of search result

    Attributes:
        label:
        score:
        housenumber:
        id:
        type:
        name:
        postcode:
        citycode:
        x:
        y:
        city:
        context:
        importance:
        street:
        population:

    """

    label: Optional[str] = None
    score: Optional[float] = None
    housenumber: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    postcode: Optional[LaxStr] = None
    citycode: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    city: Optional[str] = None
    context: Optional[str] = None
    importance: Optional[float] = None
    street: Optional[str] = None
    population: Optional[int] = None


class AddressFeature(BaseModel):
    """Properties of search result

    Attributes:
        geometry:
        properties:

    """

    geometry: Optional[Geometry] = None
    properties: Optional[Properties] = None

    def get_coords(self):
        """Get GpsCoordinate from geometry

        Returns:
            (GpsCoordinate):
        """
        return GpsCoordinate(
            latitude=self.geometry.coordinates[0],
            longitude=self.geometry.coordinates[1],
        )


class ReverseResponse(BaseModel):
    """Properties of /reverse/ result

    Attributes:
        type:
        version:
        features:
    """

    type: str
    version: str
    features: List[AddressFeature]


class SearchResponse(ReverseResponse):
    """Properties of /search/ result

    Attributes:
        type:
        version:
        features:
    """
