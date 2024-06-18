
from core.crud.utils import fetchone_as_dict

def get_notifications_for_league_for_laptime(conn):
    cursor = conn.cursor()
    sql = "SELECT id, league_id, notification_type, guild_id, channel_id, last_modified from notifications WHERE league_id = %s AND notification_type =  'lap_time'"
    cursor.execute(sql, (league_id,))
    notifications = fetchone_as_dict(cursor)
    return notifications

def insert_notification(conn, league_id, notification_type, guild_id, channel_id):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notifications (league_id, notification_type, guild_id, channel_id) values (%s, %s, %s, %s)', (league_id, notification_type, guild_id, channel_id))
    return
