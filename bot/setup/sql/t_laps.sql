CREATE TABLE IF NOT EXISTS laps (
    id SERIAL PRIMARY KEY,
    week_id INTEGER,
    g61_lap_id VARCHAR(255) NOT NULL,
    driver_name VARCHAR(255),
    event_id VARCHAR(255),
    session INTEGER,
    sessionType INTEGER,
    car_id INTEGER,
    track_id INTEGER,
    startTime TIMESTAMP,
    lapNumber INTEGER,
    lapTime FLOAT(9),
    clean BOOLEAN,
    joker BOOLEAN,
    discontinuity BOOLEAN,
    missing BOOLEAN,
    incomplete BOOLEAN,
    offtrack BOOLEAN,
    pitlane BOOLEAN,
    pinIn BOOLEAN,
    pinOut BOOLEAN,
    trackTemp FLOAT(9),
    trackUsage INTEGER,
    trackWetness INTEGER,
    airTemp FLOAT(9),
    clouds INTEGER,
    airDensity FLOAT(9),
    airPressure FLOAT(9),
    windVel FLOAT(9),
    windDir FLOAT(9),
    relativeHumidity FLOAT(9),
    fogLevel FLOAT(9),
    precipitation FLOAT(9),
    sectors json,
    fuelLevel FLOAT(9),
    fuelUsed FLOAT(9)
)