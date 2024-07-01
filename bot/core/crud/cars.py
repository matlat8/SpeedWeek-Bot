

def upsert_cars(conn, cars):
    insert_sql = """
    INSERT INTO cars (ir_id, car_make, car_model, car_name, car_name_abbreviated, car_categories, car_weight, free_with_subscription, has_headlights, has_multiple_dry_tire_types, has_rain_capable_tire_types, hp, is_ps_purchasable, price, rain_enabled)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (ir_id) DO UPDATE SET
    car_make = EXCLUDED.car_make,
    car_model = EXCLUDED.car_model,
    car_name = EXCLUDED.car_name,
    car_name_abbreviated = EXCLUDED.car_name_abbreviated,
    car_categories = EXCLUDED.car_categories,
    car_weight = EXCLUDED.car_weight,
    free_with_subscription = EXCLUDED.free_with_subscription,
    has_headlights = EXCLUDED.has_headlights,
    has_multiple_dry_tire_types = EXCLUDED.has_multiple_dry_tire_types,
    has_rain_capable_tire_types = EXCLUDED.has_rain_capable_tire_types,
    hp = EXCLUDED.hp,
    is_ps_purchasable = EXCLUDED.is_ps_purchasable,
    price = EXCLUDED.price,
    rain_enabled = EXCLUDED.rain_enabled;
    """
    with conn.cursor() as cursor:
        for car in cars:
            cursor.execute(insert_sql, (car['ir_id'], car['car_make'], car['car_model'], car['car_name'], car['car_name_abbreviated'], car['car_categories'], car['car_weight'], car['free_with_subscription'], car['has_headlights'], car['has_multiple_dry_tire_types'], car['has_rain_capable_tire_types'], car['hp'], car['is_ps_purchasable'], car['price'], car['rain_enabled']))
        conn.commit()