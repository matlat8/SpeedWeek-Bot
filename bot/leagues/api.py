import requests
import os


class LeagueAPI:
    async def search_by_team(self, team_id):
        url = 'https://garage61.net/api/v1/laps'
        header = {'Authorization': f'Bearer {os.environ.get("GARAGE61_API_KEY")}'}
        params = {'teams':[team_id]}
        response = requests.get(url, params=params, headers=header)

        if response.status_code != 200:
            print(f'G61 HTTP Error: {response.status_code}')
            return None
        
        data = response.json()
        print(data)

        return data

