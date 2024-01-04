import os
import requests
from .schemas import SearchParams, SearchCSVParams, ReverseParams


# """This table provides the base elements for all tables in database

#     Attributes:
#         date_created:
#         last_modified: This field should automatically update when the line is updated
#     """


class Api:
    """This is the api to interact with the adress endpoint

    Documentation : https://adresse.data.gouv.fr/api-doc/adresse

    """

    def __init__(self, **kwargs):
        self.url = kwargs.get("url", "https://api-adresse.data.gouv.fr")
        self.timeout = kwargs.get("timeout", 10)

    def search(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (SearchParams):
        """
        params = SearchParams(**kwargs)
        return requests.get(
            self.url + "/search", params=params.model_dump(), timeout=self.timeout
        )

    def reverse(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (ReverseParams):
        """
        params = ReverseParams(**kwargs)
        return requests.get(
            self.url + "/reverse", params=params.model_dump(), timeout=self.timeout
        )

    def search_csv(self, csv: str, **kwargs) -> requests.Response:
        """
        Args:
            csv (str): file path to the csv file
            **kwargs (SearchCSVParams):
        Raises:
            FileNotFoundError: if the `csv` file is not found

        """
        # read the csv file
        if not os.path.isfile(csv):
            raise FileNotFoundError(csv)

        # check max size
        file_stats = os.stat(csv)
        file_size = file_stats.st_size / (1024 * 1024)
        print(file_size)
        if file_size > 50:
            print(f"csv file size is too big (>50Mo), current size : {file_size}")
            raise ValueError(
                f"csv file size is too big (>50Mo), current size : {file_size}"
            )

        params = SearchCSVParams(**kwargs)

        with open(csv, "r") as f:
            r = requests.post(
                self.url + "/search/csv/",
                data=params.model_dump(),
                files={"data": f},
                timeout=self.timeout,
            )

        return r

    def reverse_csv(self, csv: str) -> requests.Response:
        """
        Args:
            csv (str): file path to the csv file

        Raises:
            FileNotFoundError: if the `csv` file is not found

        """
        # read the csv file
        if not os.path.isfile(csv):
            raise FileNotFoundError(csv)

        # check max size
        file_stats = os.stat(csv)
        file_size = file_stats.st_size / (1024 * 1024)
        if file_size > 6:
            print(f"csv file size is too big (>6Mo), current size : {file_size}")
            raise ValueError(
                f"csv file size is too big (>6Mo), current size : {file_size}"
            )

        with open(csv, "r") as f:
            r = requests.post(
                self.url + "/search/csv/", files={"data": f}, timeout=self.timeout
            )

        return r
