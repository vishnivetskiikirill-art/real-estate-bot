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


async def get_user_lang(user_id: int):
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT lang FROM users WHERE user_id=$1", user_id)
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


async def get_user_filters(user_id: int):
    pool = _ensure_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT city, district, property_type
            FROM users
            WHERE user_id=$1
            """,
            user_id
        )
    return row or {"city": None, "district": None, "property_type": None}
