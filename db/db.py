import asyncpg
from typing import Optional, Any, Dict, List

_pool: Optional[asyncpg.Pool] = None


def _ensure_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        raise RuntimeError("DB pool is not initialized. Call init_db() first.")
    return _pool


async def init_db(dsn: str) -> None:
    global _pool
    _pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)

    async with _pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                lang TEXT,
                city TEXT,
                district TEXT,
                property_type TEXT
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id SERIAL PRIMARY KEY,
                property_type TEXT,
                city TEXT,
                district TEXT,
                price NUMERIC,
                description_ru TEXT,
                description_en TEXT,
                description_bg TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        )


async def close_db() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


# ---------- user settings ----------

async def set_user_lang(user_id: int, lang: str) -> None:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, lang)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET lang = EXCLUDED.lang;
            """,
            user_id, lang
        )


async def get_user_lang(user_id: int) -> Optional[str]:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT lang FROM users WHERE user_id = $1;",
            user_id
        )
    return row["lang"] if row else None


async def set_user_city(user_id: int, city: str) -> None:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, city)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET city = EXCLUDED.city;
            """,
            user_id, city
        )


async def set_user_district(user_id: int, district: str) -> None:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, district)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET district = EXCLUDED.district;
            """,
            user_id, district
        )


async def set_user_property_type(user_id: int, property_type: str) -> None:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, property_type)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET property_type = EXCLUDED.property_type;
            """,
            user_id, property_type
        )


async def get_user_filters(user_id: int) -> Dict[str, Optional[str]]:
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT city, district, property_type
            FROM users
            WHERE user_id = $1;
            """,
            user_id
        )
    if not row:
        return {"city": None, "district": None, "property_type": None}
    return dict(row)


# ---------- properties ----------

async def fetch_properties(
    limit: int = 5,
    city: Optional[str] = None,
    district: Optional[str] = None,
    property_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    pool = _ensure_pool()

    query = """
        SELECT id, property_type, city, district, price,
               description_ru, description_en, description_bg,
               created_at
        FROM properties
        WHERE 1=1
    """
    params: List[Any] = []
    i = 1

    if city:
        query += f" AND city = ${i}"
        params.append(city)
        i += 1

    if district:
        query += f" AND district = ${i}"
        params.append(district)
        i += 1

    if property_type:
        query += f" AND property_type = ${i}"
        params.append(property_type)
        i += 1

    query += f" ORDER BY created_at DESC LIMIT ${i}"
    params.append(limit)

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [dict(r) for r in rows]
