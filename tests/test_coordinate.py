from tests.base import BaseTestCase
from flask import url_for


class IndexTestCase(BaseTestCase):
    def test_point_select(self):
        resp = self.client.get(url_for('coordinate.point_select'))
        data = resp.get_data(as_text=True)
        self.assertIn('200', resp.status)
        self.assertIn('三坐标测点数据分析图', data)

    def test_upload_data(self):
        resp = self.client.get(url_for('coordinate.upload_data'))
        data = resp.get_data(as_text=True)
        self.assertIn('200', resp.status)

    def test_chart_fig(self):
        resp = self.client.get(url_for('coordinate.chart_fig'))
        data = resp.get_data(as_text=True)
        self.assertIn('500', resp.status)

    def test_show_data(self):
        resp = self.client.get(url_for('coordinate.show_data'))
        data = resp.get_data(as_text=True)
        self.assertIn('200', resp.status)


    def test_ex1(self):
        self.assertEqual('abc', 'abc')

    def test_ex2(self):
        self.assertEqual(2, 5, '2 is not greater than 5')


