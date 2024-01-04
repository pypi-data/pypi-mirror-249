import requests

from .schemas import RegionsParams, RegionCodeParams


class Api:
    """This is the api to interact with the regions

    Documentation : https://geo.api.gouv.fr/decoupage-administratif/regions

    """

    def __init__(self, **kwargs):
        self.url = kwargs.pop("url", "https://geo.api.gouv.fr")
        self.timeout = kwargs.get("timeout", 10)

    def regions(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (RegionsParams):
        """
        params = RegionsParams(**kwargs)
        return requests.get(
            self.url + "/regions", params=params.model_dump(), timeout=self.timeout
        )

    def regions_by_code(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (RegionCodeParams):
        """
        params = RegionCodeParams(**kwargs)

        return requests.get(
            self.url + "/regions/" + params.code,
            params=params.model_dump(),
            timeout=self.timeout,
        )
