import disnake
from disnake.ext import commands

from apis.polygonio.polygon_options import PolygonOptions


opts = PolygonOptions()


class PlaysCOG(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    @commands.slash_command()
    async def plays(self, inter):
        pass



    @plays.sub_command()
    async def easy_mode(self, inter:disnake.AppCmdInter, type:str=commands.Param(choices=['calls', 'puts'])):
        await inter.response.defer()
        await inter.edit_original_message(f"Finding plays...")

        if type == 'calls':
            calls, puts = await opts.find_plays()
            

            
            await inter.edit_original_message(file=disnake.File(calls.to_csv('calls.csv')))

        elif type =='puts':
            calls, puts = await opts.find_plays()
            await inter.edit_original_message(file=disnake.File(puts.to_csv('puts.csv')))



def setup(bot: commands.Bot):
    bot.add_cog(PlaysCOG(bot))
    print('PLAYS READY')