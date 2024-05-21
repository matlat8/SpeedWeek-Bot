import aiohttp
import os

class WeeksAPI:

    async def get_week_laps(self, track_id, car_id, team_id):
        async with aiohttp.ClientSession() as session:

            url = f"https://garage61.net/api/v1/laps?tracks={track_id}&cars={car_id}&teams={team_id}"
            headers = {'Authorization': f'Bearer {os.environ.get("GARAGE61_API_KEY")}'}
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Failed to get week laps. Status code: {response.status}\n{await response.text()}")