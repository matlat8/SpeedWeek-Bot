

def get_leagues(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM leagues')
    leagues = cursor.fetchall()
    return leagues
