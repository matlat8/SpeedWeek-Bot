import discord

class WeekEmbeds:

    def initial_laptime_msg(self, lap, position_plus_minus):
        msg = ''
        msg += f"New initial lap time for **{lap['driver']['firstName']} {lap['driver']['lastName']}**:\n"

        for position in position_plus_minus:
            if position[4] == f"{lap['driver']['firstName']} {lap['driver']['lastName']}":
                msg += f"\t**P{position[9]} {lap['driver']['firstName']} {lap['driver']['lastName']} - {lap['lapTime']:.3f}**\n"
            else: msg += f"*P{position[9]} {position[4]} - {position[5]:.3f}*\n"
            print('hit')
        #msg += f'Lap Time: {lap["lapTime"]:.3f}\n'
        #msg += f"Rank: {lap['rank']}"
        return msg

    def updated_laptime_msg(self, lap):
        msg = ''
        msg += f"Updated lap time for {lap['driver']['firstName']} {lap['driver']['lastName']}:\n"
        msg += f'Lap Time: {lap["lapTime"]:.3f}\n'
        msg += f"Rank: {lap['rank']}"
        return msg