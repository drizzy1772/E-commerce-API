






async def get_products(db, query):
    result = await db.execute(query)
    return result.scalars().all()