import unittest
from unittest.mock import Mock
from bot.core.crud import utils

class TestFetchOneAsDict(unittest.TestCase):
    def test_single_row(self):
        # Mock a cursor object
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchone.return_value = (1, 'Test')

        result = utils.fetchone_as_dict(mock_cursor)

        self.assertEqual(result, {'id': 1, 'name': 'Test'})

    def test_no_row(self):
        # Mock a cursor object
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchone.return_value = None

        result = utils.fetchone_as_dict(mock_cursor)

        self.assertIsNone(result)
