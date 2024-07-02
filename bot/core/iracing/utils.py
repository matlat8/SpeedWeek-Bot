import aiohttp

import core.iracing.utils as utils
from core.logger import setup_logger

logger = setup_logger(__name__)

async def forward_link(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logger.error(f"Failed to forward iRacing link. Status code: {response.status} {await response.text()}")