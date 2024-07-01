from discord.ext import tasks
from db import DB
from core.logger import setup_logger
from core.iracing.iracing_cars import get_cars
from core.crud.cars import upsert_cars

logger = setup_logger(__name__)

@tasks.loop(hours=24)
async def load_cars(bot):
    logger.debug('Start load_cars task')
    
    db = DB(1,1)
    conn = db.get_conn()
    cars = await get_cars()
    
    logger.debug(f'Found {len(cars)} cars from iRacing API')
    
    formatted_cars = clean_cars(cars)

    logger.debug(f'Formatted {len(formatted_cars)} cars')
                 
    upsert_cars(conn, formatted_cars)
    
    logger.debug('Upserted cars')
    
    pass


def clean_cars(cars):
    formatted_cars = []
    for car in cars:
        formatted_car = {
            "ir_id": car.get("car_id"),
            "car_make": None,  # The API response does not contain a direct match for car_make
            "car_model": None,  # The API response does not contain a direct match for car_model
            "car_name": car.get("car_name"),
            "car_name_abbreviated": car.get("car_name_abbreviated"),
            "car_categories": car.get("categories", []),
            "car_weight": car.get("car_weight"),
            "free_with_subscription": car.get("free_with_subscription"),
            "has_headlights": car.get("has_headlights"),
            "has_multiple_dry_tire_types": car.get("has_multiple_dry_tire_types"),
            "has_rain_capable_tire_types": car.get("has_rain_capable_tire_types"),
            "hp": car.get("hp"),
            "is_ps_purchasable": car.get("is_ps_purchasable"),
            "price": car.get("price"),
            "rain_enabled": car.get("rain_enabled"),
        }
        formatted_cars.append(formatted_car)
    return formatted_cars