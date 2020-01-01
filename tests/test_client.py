import os
import time
import unittest
import mbta

API_KEY = os.environ['MBTA_TEST_KEY']


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client = mbta.Client(API_KEY)

    def test_create_client_no_key(self):
        with self.assertRaises(TypeError):
            mbta.Client()

    def test_client_headers(self):
        self.assertEqual(self.client._session.headers['X-API-Key'], API_KEY)


class RateLimitTest(unittest.TestCase):

    def setUp(self):
        self.client = mbta.Client(API_KEY)

    def test_get_rate_limit(self):
        self.assertEqual(self.client.get_rate_limit(), 20)

    def test_get_rate_limit_remaining(self):
        self.assertEqual(self.client.get_rate_limit_remaining(), 20)

    def test_get_rate_limit_reset(self):
        self.assertEqual(self.client.get_rate_limit_reset(), 0)

    def test_request_with_no_remaining(self):
        self.client.rate_limit['x-ratelimit-remaining'] = 0
        with self.assertRaises(mbta.errors.RateLimitError):
            self.client.get_lines()


class LinesTest(unittest.TestCase):

    def setUp(self):
        self.client = mbta.Client(API_KEY)

    def test_get_lines_no_parameters(self):
        resp = self.client.get_lines()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.url, 'https://api-v3.mbta.com/lines/')

    def test_get_lines_invalid_sort(self):
        with self.assertRaises(mbta.errors.InvalidQueryParameterError):
            self.client.get_lines(sort='foo')

    def test_get_lines_invalid_include(self):
        with self.assertRaises(mbta.errors.InvalidQueryParameterError):
            self.client.get_lines(include='foo')

    def test_get_lines_full_parameters(self):
        resp = self.client.get_lines(page_offset=1, page_limit=10, sort='color', include='routes')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(int(self.client.get_rate_limit_reset() - time.time()) < 60)
