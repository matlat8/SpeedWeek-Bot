import discord

class WeekEmbeds:

    def initial_laptime_msg(self, lap):
        msg = ''
        msg += f"New initial lap time for {lap['driver']['firstName']} {lap['driver']['lastName']}:\n"
        msg += f'Lap Time: {lap["lapTime"]:.3f}\n'
        msg += f"Rank: {lap['rank']}"
        return msg

    def lap_embed(self, lap):
        embed = discord.Embed(
            title=f"New Lap Time for Week {lap['week_num']}",
            description=f"Driver: {lap['driver']}\nLap Time: {lap['lap_time']}\n",
            color=discord.Color.green()
        )
        return embed