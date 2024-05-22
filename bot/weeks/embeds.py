import discord

class WeekEmbeds:

    def initial_laptime_msg(self, lap):
        msg = ''
        msg += f"New initial lap time for {lap['driver']['firstName']} {lap['driver']['lastName']}:\n"
        msg += f'Lap Time: {lap["lapTime"]:.3f}\n'
        msg += f"Rank: {lap['rank']}"
        return msg

    def updated_laptime_msg(self, lap):
        msg = ''
        msg += f"Updated lap time for {lap['driver']['firstName']} {lap['driver']['lastName']}:\n"
        msg += f'Lap Time: {lap["lapTime"]:.3f}\n'
        msg += f"Rank: {lap['rank']}"
        return msg