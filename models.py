CREATE_PROPERTIES = """
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    city TEXT,
    district TEXT,
    photo TEXT
);
"""

CREATE_REQUESTS = """
CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    property_id INT,
    user_id BIGINT,
    username TEXT
);
"""