from tests.base import BaseTestCase
from flask import url_for


class ProcessTestCase(BaseTestCase):
    def test_stations(self):
        resp = self.client.get(url_for('process.stations'))
        data = resp.get_data(as_text=True)
        self.assertIn('200', resp.status)
        self.assertIn('工位清单表', data)

    def test_station(self):
        resp = self.client.get(url_for('process.station', station='station_test'))
        data = resp.get_data(as_text=True)
        self.assertIn('200', resp.status)
        self.assertIn('station_test', data)





