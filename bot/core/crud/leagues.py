from core.crud.utils import fetchall_as_dict

def get_id_name_from_leagues(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM leagues')
    leagues = fetchall_as_dict(cursor)
    return leagues

def get_leagues(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leagues')
    leagues = fetchall_as_dict(cursor)
    return leagues

def new_league(conn, league_name, team_id):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leagues (name, g61_team_id, first_day_of_week) values (%s, %s, %s)', (league_name, team_id, 1))
    return