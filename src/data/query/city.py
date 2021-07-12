from ..db import execute_read_query


async def get_city(*, city_id=None, city_name=None):
    pass


async def get_cities():
    return await execute_read_query("SELECT * FROM cities;")


async def get_nation_cities(nation_id: int):
    return await execute_read_query(
        "SELECT * FROM cities WHERE nation_id = $1;", nation_id
    )