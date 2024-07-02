import aiohttp

import core.iracing.utils as utils
from core.iracing.iracing_auth import authenticate
from core.logger import setup_logger

logger = setup_logger(__name__)

async def get_cars():
    async with aiohttp.ClientSession(cookies=dict(await authenticate())) as session:
        url = "https://members-ng.iracing.com/data/car/get"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                cars = await utils.forward_link(data['link']) 
                return cars
            else:
                logger.error(f"Failed to get cars. Status code: {response.status} {await response.text()}")

