import asyncpg

pool: asyncpg.Pool | None = None


async def init_db(database_url: str):
    global pool
    pool = await asyncpg.create_pool(database_url)


async def close_db():
    global pool
    if pool:
        await pool.close()


async def fetch_properties(
    property_type: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    district: str | None = None,
):
    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if property_type:
        params.append(property_type)
        query += f" AND type = ${len(params)}"

    if min_price:
        params.append(min_price)
        query += f" AND price >= ${len(params)}"

    if max_price:
        params.append(max_price)
        query += f" AND price <= ${len(params)}"

    if district:
        params.append(district)
        query += f" AND district = ${len(params)}"

    async with pool.acquire() as conn:
        return await conn.fetch(query, *params)
