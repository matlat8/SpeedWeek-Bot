from discord.ext import tasks
from db import DB
from core.logger import setup_logger
from core.iracing.iracing_cars import get_cars
from core.iracing.tracks import get_tracks
from core.crud.cars import upsert_cars
from core.crud.tracks import upsert_tracks

logger = setup_logger(__name__)

@tasks.loop(hours=24)
async def load_tracks(bot):
    logger.debug('Start load_tracks task')
    
    db = DB(1,1)
    conn = db.get_conn()
    tracks = await get_tracks()

    if not tracks:
        logger.error('Failed to get tracks from iRacing API')
        return
    
    logger.debug(f'Found {len(tracks)} tracks from iRacing API')
    
    formatted_tracks = clean_tracks(tracks)

    logger.debug(f'Formatted {len(formatted_tracks)} tracks')
                 
    upsert_tracks(conn, formatted_tracks)
    
    logger.debug('Upserted tracks')

    conn.close()
    
    pass


def clean_tracks(tracks):
    formatted_tracks = []
    for track in tracks:
        formatted_track = {
            "ir_id": track.get("track_id"),
            "category": track.get("category"),
            "track_name": track.get("track_name"),
            "config_name": track.get("config_name"),
            "is_dirt": track.get("is_dirt"),
            "is_oval": track.get("is_oval"),
            "is_ps_purchasable": track.get("is_ps_purchasable"),
            "location": track.get("location"),
            "price": track.get("price"),
            "price_display": track.get("price_display"),
            "purchasable": track.get("purchasable"),
            "track_config_length": track.get("track_config_length"),
            "free_with_subscription": track.get("free_with_subscription")
        }
        formatted_tracks.append(formatted_track)
    return formatted_tracks