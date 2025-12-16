import os
import asyncpg

pool = None

async def connect_db():
    global pool
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    pool = await asyncpg.create_pool(database_url)


async def execute(query, *args):
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)


async def fetch(query, *args):
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)
