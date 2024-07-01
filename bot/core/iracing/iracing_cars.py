import aiohttp

from core.iracing.iracing_auth import authenticate
from core.logger import setup_logger

logger = setup_logger(__name__)

async def get_cars():
    async with aiohttp.ClientSession(cookies=dict(await authenticate())) as session:
        url = "https://members-ng.iracing.com/data/car/get"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                cars = await forward_link(data['link']) 
                return cars
            else:
                logger.error(f"Failed to get cars. Status code: {response.status} {await response.text()}")

async def forward_link(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logger.error(f"Failed to forward iRacing link. Status code: {response.status} {await response.text()}")