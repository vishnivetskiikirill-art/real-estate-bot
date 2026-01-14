import asyncpg
from typing import Any, Optional

_pool: Optional[asyncpg.Pool] = None


async def init_db(database_url: str) -> None:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=database_url, min_size=1, max_size=5)


async def close_db() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def fetch_properties(limit: int = 10) -> list[dict[str, Any]]:
    assert _pool is not None, "DB not initialized"

    rows = await _pool.fetch(
        """
        SELECT id, title, price, city, district, photo,
               description_ru, description_en, description_bg
        FROM properties
        ORDER BY id DESC
        LIMIT $1
        """,
        limit,
    )
    return [dict(r) for r in rows]
