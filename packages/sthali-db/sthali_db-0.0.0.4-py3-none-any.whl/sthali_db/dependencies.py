from pydantic import NonNegativeInt


async def filter_parameters(skip: NonNegativeInt = 0, limit: NonNegativeInt = 100):
    return {"skip": skip, "limit": limit}
