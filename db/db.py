import asyncpg

pool = None


async def init_db(database_url: str):
    global pool
    pool = await asyncpg.create_pool(database_url)


async def close_db():
    global pool
    if pool:
        await pool.close()


async def fetch_properties(limit: int = 10):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                id,
                title,
                price,
                city,
                district,
                photo,
                description_ru,
                description_en,
                description_bg
            FROM properties
            ORDER BY id DESC
            LIMIT $1
            """,
            limit
        )
        return [dict(r) for r in rows]
