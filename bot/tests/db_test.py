import unittest
from unittest.mock import patch, MagicMock
from db import DB

class TestDB(unittest.TestCase):
    @patch('psycopg2.pool.SimpleConnectionPool')
    @patch.dict('os.environ', {'POSTGRES_URL': 'test_url'})
    def setUp(self, mock_pool):
        self.mock_pool = mock_pool
        self.db = DB(1, 10)

    def test_init(self):
        self.mock_pool.assert_called_once_with(1, 10, dsn='test_url')

    def test_get_conn(self):
        self.db.get_conn()
        self.mock_pool.return_value.getconn.assert_called_once()

    def test_release_conn(self):
        mock_conn = MagicMock()
        self.db.release_conn(mock_conn)
        self.mock_pool.return_value.putconn.assert_called_once_with(mock_conn)
