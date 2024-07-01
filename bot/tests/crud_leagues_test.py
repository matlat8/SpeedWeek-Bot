import unittest
from unittest.mock import Mock, call
from core.crud import leagues

class TestLeagues(unittest.TestCase):
    def setUp(self):
        self.conn = Mock()
        self.cursor = Mock()
        self.conn.cursor.return_value = self.cursor

    def test_get_id_name_from_leagues(self):
        leagues.fetchall_as_dict = Mock(return_value='result')
        result = leagues.get_id_name_from_leagues(self.conn)
        self.cursor.execute.assert_called_once_with('SELECT id, name FROM leagues')
        self.assertEqual(result, 'result')

    def test_get_leagues(self):
        leagues.fetchall_as_dict = Mock(return_value='result')
        result = leagues.get_leagues(self.conn)
        self.cursor.execute.assert_called_once_with('SELECT * FROM leagues')
        self.assertEqual(result, 'result')

    def test_new_league(self):
        leagues.new_league(self.conn, 'league_name', 'team_id')
        self.cursor.execute.assert_called_once_with('INSERT INTO leagues (name, g61_team_id, first_day_of_week) values (%s, %s, %s)', ('league_name', 'team_id', 1))