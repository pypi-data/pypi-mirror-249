from unittest import TestCase
from .. import CommuneApi, CommunesResponse
# from ..commune.schemas import Geometry, GpsCoordinate, AddressFeature
import time
import requests

WAIT_TIME = 0.2


class TestCommune(TestCase):

    def setUp(self) -> None:
        self.api = CommuneApi()
        return super().setUp()

    def test_communes(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.communes(codePostal="44000", limit=5)
        self.assertTrue(r.status_code == 200)

        return r

    def test_communes_by_code(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_code(code=44109)
        self.assertTrue(r.status_code == 200)

    def test_communes_by_departement(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_departement(code="57")
        self.assertTrue(r.status_code == 200)

    def test_communes_by_epcis(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_epcis(code="244400404")
        self.assertTrue(r.status_code == 200)

    def test_communes_response(self) -> None:
        try:
            results = [CommunesResponse(**r) for r in self.test_communes().json()]
            self.assertTrue(results is not None)
        except Exception as e:
            print(e)
            self.assertTrue(False)
