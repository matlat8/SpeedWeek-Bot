

def upsert_tracks(conn, tracks):
    upsert_sql = """
    INSERT INTO tracks (ir_id, category, track_name, config_name, is_dirt, is_oval, is_ps_purchasable, location, price, price_display, purchasable, track_config_length, free_with_subscription)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)
    ON CONFLICT (ir_id) DO UPDATE SET
    category = EXCLUDED.category,
    track_name = EXCLUDED.track_name,
    config_name = EXCLUDED.config_name,
    is_dirt = EXCLUDED.is_dirt,
    is_oval = EXCLUDED.is_oval,
    is_ps_purchasable = EXCLUDED.is_ps_purchasable,
    location = EXCLUDED.location,
    price = EXCLUDED.price,
    price_display = EXCLUDED.price_display,
    purchasable = EXCLUDED.purchasable,
    track_config_length = EXCLUDED.track_config_length,
    free_with_subscription = EXCLUDED.free_with_subscription;
    """
    with conn.cursor() as cursor:
        for track in tracks:
            cursor.execute(upsert_sql, (track['ir_id'], track['category'], track['track_name'], track['config_name'], track['is_dirt'], track['is_oval'], track['is_ps_purchasable'], track['location'], track['price'], track['price_display'], track['purchasable'], track['track_config_length'], track['free_with_subscription']))
        conn.commit()