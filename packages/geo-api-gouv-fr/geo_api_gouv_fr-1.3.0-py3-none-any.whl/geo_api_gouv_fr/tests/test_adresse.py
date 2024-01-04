from unittest import TestCase
from .. import AdressApi, SearchResponse, ReverseResponse
from ..adress.schemas import Geometry, GpsCoordinate, AddressFeature
import time
import requests
import os
from base64 import b64encode
WAIT_TIME = 0.2


def generate_file(size_in_mb, file_name):
    mega_byte = int(1024 * 1024 * 0.75)  # need to make it a bit smaller because bytes takes less space that str
    with open(file_name, 'w') as file:
        file.write(b64encode(os.urandom(size_in_mb * mega_byte)).decode('utf-8'))


class TestAdress(TestCase):

    def setUp(self) -> None:
        self.api = AdressApi()
        return super().setUp()

    def test_search(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.search(q="8+bd+du+port", limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", postcode=44380, limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", type="street", limit=15)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_csv(self) -> None:

        # non existant csv
        with self.assertRaises(FileNotFoundError):
            r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/nowhere.csv")

        # bloated csv
        tmpFile = "./geo_api_gouv_fr/tests/data/bloated-50mo.csv"
        generate_file(51, tmpFile)
        with self.assertRaises(ValueError):
            r = self.api.search_csv(csv=tmpFile)

        time.sleep(WAIT_TIME)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv", columns=["adresse", "postcode"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-simple.json", "wb") as f:
            f.write(r.content)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv",
                                postcode="postcode", columns=["adresse", "postcode"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-columns.json", "wb") as f:
            f.write(r.content)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv",
                                postcode="postcode", result_columns=["latitude", "longitude"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-postcode.json", "wb") as f:
            f.write(r.content)

    def test_reverse_csv(self) -> None:

        # non existant csv
        with self.assertRaises(FileNotFoundError):
            r = self.api.reverse_csv(csv="./geo_api_gouv_fr/tests/data/nowhere.csv")

        # bloated csv
        tmpFile = "./geo_api_gouv_fr/tests/data/bloated-7mo.csv"
        generate_file(7, tmpFile)
        with self.assertRaises(ValueError):
            r = self.api.reverse_csv(csv=tmpFile)

        time.sleep(WAIT_TIME)
        r = self.api.reverse_csv(csv="./geo_api_gouv_fr/tests/data/reverse.csv")
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/reversecsv-simple.json", "wb") as f:
            f.write(r.content)

    def test_search_error(self) -> None:

        with self.assertRaises(ValueError):
            self.api.search(q="8+bd+du+port", type="noclue", limit=15)

    def test_reverse(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.reverse(lon=2.37, lat=48.357)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_response(self) -> None:
        r = self.test_search()
        parsed = SearchResponse(**r.json())
        self.assertTrue(True)

    def test_reversed_response(self) -> None:
        r = self.test_reverse()
        parsed = ReverseResponse(**r.json())
        self.assertTrue(True)

    def test_geometry(self) -> None:
        with self.assertRaises(ValueError):
            Geometry(type="any", coordinates=[])

        with self.assertRaises(ValueError):
            Geometry(type="any", coordinates=[190, 0])

        with self.assertRaises(ValueError):
            Geometry(type="any", coordinates=[0, -190])

        with self.assertRaises(ValueError):
            Geometry(type="any", coordinates=[1, 2, 3])

    def test_adress_feature(self) -> None:

        geo = Geometry(type="any", coordinates=[1.6, 9.2])
        addr = AddressFeature(geometry=geo)

        self.assertTrue(addr.get_coords() == GpsCoordinate(latitude=1.6, longitude=9.2))

    def test_issue_with_07500_postcode(self):
        time.sleep(WAIT_TIME)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/lbb-search.csv", columns=[
                                "streetnumber", "street", "postcode"], citycode="citycode", result_columns=["latitude", "longitude", "result_city"])
        self.assertTrue(r.status_code == 200)

        with open("./testResults/issue_with_07500_postcode.txt", "w") as f:
            f.write(r.text)
