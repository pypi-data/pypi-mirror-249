import os
from dotenv import load_dotenv
load_dotenv()
import disnake
from disnake.ext import commands

from apis.polygonio.polygon_options import PolygonOptions
from webull_options.webull_options import WebullOptions

wb_opts = WebullOptions(access_token=os.environ.get('ACCESS_TOKEN'), osv=os.environ.get('OSV'), did=os.environ.get('DID'))

opts = PolygonOptions(user='postgres', database='fudstop')


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