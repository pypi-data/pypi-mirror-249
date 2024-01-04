import requests

from .schemas import DepartmentsParams, DepartmentCodeParams, RegionDepartmentCodeParams


class Api:
    """This is the api to interact with the department

    Documentation : https://geo.api.gouv.fr/decoupage-administratif/departements

    """

    def __init__(self, **kwargs):
        self.url = kwargs.pop("url", "https://geo.api.gouv.fr")
        self.timeout = kwargs.get("timeout", 10)

    def departements(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (DepartmentsParams):
        """
        params = DepartmentsParams(**kwargs)
        return requests.get(
            self.url + "/departements", params=params.model_dump(), timeout=self.timeout
        )

    def departements_by_code(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (DepartmentCodeParams):
        """
        params = DepartmentCodeParams(**kwargs)
        return requests.get(
            self.url + "/departements/" + params.code,
            params=params.model_dump(),
            timeout=self.timeout,
        )

    def departements_by_region(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (RegionDepartmentCodeParams):
        """
        params = RegionDepartmentCodeParams(**kwargs)
        return requests.get(
            self.url + f"/regions/{params.code}/departements",
            params=params.model_dump(),
            timeout=self.timeout,
        )
