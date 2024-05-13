import requests
import os
import arrow


class LeagueAPI:
    async def search_for_team(self, team_id):
        url = 'https://garage61.net/api/v1/me'
        header = {'Authorization': f'Bearer {os.environ.get("GARAGE61_API_KEY")}'}
        response = requests.get(url, headers=header)

        if response.status_code != 200:
            print(f'G61 HTTP Error: {response.status_code}')
            return None
        
        data = response.json()
        print(data)

        return data

