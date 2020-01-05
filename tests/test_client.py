import os
import time
import unittest
import mbtaw

API_KEY = os.environ['MBTA_TEST_KEY']


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.client = mbtaw.Client(API_KEY)


class ClientTest(BaseTest):

    def test_create_client_no_key(self):
        with self.assertRaises(TypeError):
            mbtaw.Client()

    def test_client_headers(self):
        self.assertEqual(self.client._session.headers['X-API-Key'], API_KEY)


class RateLimitTest(BaseTest):

    def test_get_rate_limit(self):
        self.assertEqual(self.client.get_rate_limit(), 20)

    def test_get_rate_limit_remaining(self):
        self.assertEqual(self.client.get_rate_limit_remaining(), 20)

    def test_get_rate_limit_reset(self):
        self.assertEqual(self.client.get_rate_limit_reset(), 0)

    def test_request_with_no_remaining(self):
        self.client.rate_limit['x-ratelimit-remaining'] = 0
        with self.assertRaises(mbtaw.errors.RateLimitError):
            self.client.get_lines()


class LinesTest(BaseTest):

    def test_get_lines_no_parameters(self):
        resp = self.client.get_lines()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.url, 'https://api-v3.mbta.com/lines/')

    def test_get_lines_invalid_sort(self):
        with self.assertRaises(mbtaw.errors.InvalidQueryParameterError):
            self.client.get_lines(sort='foo')

    def test_get_lines_invalid_include(self):
        with self.assertRaises(mbtaw.errors.InvalidQueryParameterError):
            self.client.get_lines(include='foo')

    def test_get_lines_full_parameters(self):
        resp = self.client.get_lines(page_offset=1, page_limit=10, sort='color', fields_line='color,short_name', include='routes', filter_id='line-Red')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(int(self.client.get_rate_limit_reset() - time.time()) < 60)


class LinesIdTest(BaseTest):

    def test_get_lines_id_empty_id(self):
        with self.assertRaises(mbtaw.errors.InvalidQueryParameterError):
            self.client.get_lines_id('')

    def test_get_lines_id_no_parameters(self):
        resp = self.client.get_lines_id('line-Red')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.url, 'https://api-v3.mbta.com/lines/line-Red')

    def test_get_lines_id_invalid_include(self):
        with self.assertRaises(mbtaw.errors.InvalidQueryParameterError):
            self.client.get_lines_id('line-Red', include='foo')

    def test_get_lines_id_full_parameters(self):
        resp = self.client.get_lines_id('line-Red', fields_line='color', include='routes')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(int(self.client.get_rate_limit_reset() - time.time()) < 60)
