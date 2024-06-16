

def get_active_season_for_league(conn, league_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM seasons WHERE league_id = %s AND end_date >= now()', (league_id,))
    season_id = cursor.fetchone()
    return season_id