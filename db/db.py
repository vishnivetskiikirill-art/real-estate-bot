import asyncpg
from typing import Optional, List, Dict, Any

pool: Optional[asyncpg.Pool] = None


CREATE_PROPERTIES_SQL = """
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    property_type TEXT,
    city TEXT,
    district TEXT,
    price INT,
    photo TEXT,
    description_ru TEXT
);
"""


async def init_db(database_url: str) -> None:
    """
    Создаём пул и таблицы.
    """
    global pool
    pool = await asyncpg.create_pool(database_url)
    async with pool.acquire() as conn:
        await conn.execute(CREATE_PROPERTIES_SQL)


async def close_db() -> None:
    global pool
    if pool:
        await pool.close()
        pool = None


async def fetch_properties(
    property_type: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    district: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Достаём объявления по фильтрам.
    """
    if pool is None:
        raise RuntimeError("DB pool is not initialized. Call init_db() first.")

    conditions = []
    params = []

    if property_type:
        params.append(property_type)
        conditions.append(f"property_type = ${len(params)}")

    if city:
        params.append(city)
        conditions.append(f"city = ${len(params)}")

    if district:
        params.append(district)
        conditions.append(f"district = ${len(params)}")

    if min_price is not None:
        params.append(min_price)
        conditions.append(f"price >= ${len(params)}")

    if max_price is not None:
        params.append(max_price)
        conditions.append(f"price <= ${len(params)}")

    where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    params.append(limit)

    query = f"""
        SELECT id, property_type, city, district, price, photo, description_ru
        FROM properties
        {where_sql}
        ORDER BY id DESC
        LIMIT ${len(params)}
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [dict(r) for r in rows]
