
from core.crud.utils import fetchone_as_dict
from core.logger import setup_logger

logger = setup_logger(__name__)

def get_notifications_for_league_for_laptime(conn):
    cursor = conn.cursor()
    sql = "SELECT id, league_id, notification_type, guild_id, channel_id, last_modified from notifications WHERE league_id = %s AND notification_type =  'lap_time'"
    cursor.execute(sql, (league_id,))
    notifications = fetchone_as_dict(cursor)
    return notifications

def insert_notification(conn, league_id, notification_type, guild_id, channel_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notifications WHERE league_id = %s AND notification_type = %s AND guild_id = %s AND channel_id = %s', (league_id, notification_type, guild_id, channel_id))
    if cursor.fetchone():
        logger.debug('Updating notification')
        cursor.execute('UPDATE notifications SET last_modified = NOW(), channel_id = %s WHERE league_id = %s AND notification_type = %s AND guild_id = %s', (channel_id, league_id, notification_type, guild_id))
    else:
        logger.debug('Inserting new notification')
        cursor.execute('INSERT INTO notifications (league_id, notification_type, guild_id, channel_id) values (%s, %s, %s, %s)', (league_id, notification_type, guild_id, channel_id))
    return
