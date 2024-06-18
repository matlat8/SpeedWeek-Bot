from discord import Embed


def view_leagues_basic_embed(leagues):
    embed = Embed(title='Leagues', color=0x00ff00)
    for league in leagues:
        embed.add_field(name=league['name'], value=f"Team ID: {league['g61_team_id']}\nLeague ID: {league['id']}", inline=False)
    return embed