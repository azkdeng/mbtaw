import unittest
import mbta


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client = mbta.Client('test key')

    def test_create_client_no_key(self):
        with self.assertRaises(TypeError):
            mbta.Client()

    def test_client_headers(self):
        self.assertEqual('test key', self.client.session.headers['X-API-Key'])
