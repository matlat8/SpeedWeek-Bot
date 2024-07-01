import unittest
from unittest.mock import Mock, patch
from core.crud.notifications import get_notifications_for_league_for_laptime, insert_notification

class TestNotifications(unittest.TestCase):
    def setUp(self):
        self.conn = Mock()
        self.cursor = Mock()
        self.conn.cursor.return_value = self.cursor

    @patch('core.crud.notifications.fetchone_as_dict')
    def test_get_notifications_for_league_for_laptime(self, mock_fetch):
        mock_fetch.return_value = {'id': 1, 'league_id': 1}
        result = get_notifications_for_league_for_laptime(self.conn, 1)
        self.cursor.execute.assert_called_once()
        self.assertEqual(result, {'id': 1, 'league_id': 1})

    def test_insert_notification(self):
        self.cursor.fetchone.return_value = None
        insert_notification(self.conn, 1, 'type', 1, 1)
        self.assertEqual(self.cursor.execute.call_count, 2)

        self.cursor.fetchone.return_value = 1
        insert_notification(self.conn, 1, 'type', 1, 1)
        self.assertEqual(self.cursor.execute.call_count, 4)
