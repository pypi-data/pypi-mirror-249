from unittest import TestCase
from .. import DepartmentApi, DepartmentsResponse
import requests
import time

WAIT_TIME = 0.2


class TestDepartment(TestCase):
    def setUp(self) -> None:
        self.api = DepartmentApi()
        return super().setUp()

    def test_departements(self) -> requests.Response:
        r = self.api.departements(codeRegion=1, code=1)
        self.assertTrue(r.status_code == 200)
        time.sleep(WAIT_TIME)
        r = self.api.departements(nom="Mar", limit=5)
        self.assertTrue(r.status_code == 200)
        return r

    def test_departements_by_code(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.departements_by_code(code=92)
        self.assertTrue(r.status_code == 200)
        time.sleep(WAIT_TIME)
        r = self.api.departements_by_code(code=1)
        self.assertTrue(r.status_code == 200)

    def test_departements_by_region(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.departements_by_region(code=28)
        self.assertTrue(r.status_code == 200)

    def test_departements_response(self) -> None:
        results = [DepartmentsResponse(**r) for r in self.test_departements().json()]
        assert len(results) > 0
