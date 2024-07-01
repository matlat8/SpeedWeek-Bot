CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    g61_id INTEGER,
    ir_id INTEGER UNIQUE,
    car_make VARCHAR(255),
    car_model VARCHAR(255),
    car_name VARCHAR(255),
    car_name_abbreviated VARCHAR(255),
    car_categories TEXT[],
    car_weight INTEGER,
    free_with_subscription BOOLEAN,
    has_headlights BOOLEAN,
    has_multiple_dry_tire_types BOOLEAN,
    has_rain_capable_tire_types BOOLEAN,
    hp INTEGER,
    is_ps_purchasable BOOLEAN,
    price FLOAT,
    rain_enabled BOOLEAN
);