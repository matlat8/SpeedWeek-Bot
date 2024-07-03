import aiohttp

from core.logger import setup_logger
import core.iracing.utils as utils
from core.iracing.iracing_auth import authenticate

logger = setup_logger(__name__)

async def get_tracks():
    async with aiohttp.ClientSession(cookies=dict(await authenticate())) as session:
        url = "https://members-ng.iracing.com/data/track/get"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                tracks = await utils.forward_link(data['link'])
                return tracks
            else:
                logger.error(f"Failed to get tracks. Status code: {response.status} {await response.text()}")