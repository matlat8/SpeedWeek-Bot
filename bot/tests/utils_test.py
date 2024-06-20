import unittest
from unittest.mock import Mock
from core.crud import utils

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
    def test_mismatched_row_and_description(self):
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchone.return_value = (1, 'Test', 'Extra')

        result = utils.fetchone_as_dict(mock_cursor)

        self.assertEqual(result, {'id': 1, 'name': 'Test'})

    def test_empty_description(self):
        mock_cursor = Mock()
        mock_cursor.description = []
        mock_cursor.fetchone.return_value = (1,)

        result = utils.fetchone_as_dict(mock_cursor)

        self.assertEqual(result, {})

    def test_empty_description_and_row(self):
        mock_cursor = Mock()
        mock_cursor.description = []
        mock_cursor.fetchone.return_value = ()

        result = utils.fetchone_as_dict(mock_cursor)

        self.assertEqual(result, None)