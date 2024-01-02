import disnake
from disnake.ext import commands
from bot_menus.pagination import AlertMenus
import pandas as pd
import os
import asyncpg
from dotenv import load_dotenv
from datetime import datetime
from tabulate import tabulate
from schema import run_conversation, tools
from options_filter import FilterView, FilterMenu
load_dotenv()



class FilterCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.osv = os.environ.get('OSV')
        self.did = os.environ.get('DID')
        self.pool = None
        self.db_params = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'fud',
            'database': 'opts',
            'port': 5432
        }
        self.pool = None

    async def create_pool(self, min_size=1, max_size=10):
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(
                    min_size=min_size, 
                    max_size=max_size, 
                    **self.db_params
                )
            except Exception as e:
                print(f"Error creating connection pool: {e}")
                raise

    async def close_pool(self):
        if self.pool:
            await self.pool.close()

    def chunk_string(self, string, size):
        """Yield successive size-sized chunks from string."""
        for i in range(0, len(string), size):
            yield string[i:i + size]

    def sanitize_value(self, value, col_type):
        """Sanitize and format the value for SQL query."""
        if col_type == 'str':
            # For strings, add single quotes
            return f"'{value}'"
        elif col_type == 'date':
            # For dates, format as 'YYYY-MM-DD'
            if isinstance(value, str):
                try:
                    datetime.strptime(value, '%Y-%m-%d')
                    return f"'{value}'"
                except ValueError:
                    raise ValueError(f"Invalid date format: {value}")
            elif isinstance(value, datetime):
                return f"'{value.strftime('%Y-%m-%d')}'"
        else:
            # For other types, use as is
            return str(value)
    async def get_connection(self):
        if self.pool is None:
            await self.create_pool()

        return await self.pool.acquire()

    async def release_connection(self, connection):
        await self.pool.release(connection)
    async def filter_options(self, **kwargs):
        """
        Filters the options table based on provided keyword arguments.
        Usage example:
            await filter_options(strike_price_min=100, strike_price_max=200, call_put='call',
                                 expire_date='2023-01-01', delta_min=0.1, delta_max=0.5)
        """
        # Start with the base query
        query = f"SELECT underlying_symbol, strike_price, call_put, expire_date, theta FROM public.options WHERE "
        params = []
        param_index = 1

        # Mapping kwargs to database columns and expected types, including range filters
        column_types = {
            'ticker_id': ('ticker_id', 'int'),
            'belong_ticker_id': ('belong_ticker_id', 'int'),
            'open_min': ('open', 'float'),
            'open_max': ('open', 'float'),
            'high_min': ('high', 'float'),
            'high_max': ('high', 'float'),
            'low_min': ('low', 'float'),
            'low_max': ('low', 'float'),
            'strike_price_min': ('strike_price', 'int'),
            'strike_price_max': ('strike_price', 'int'),
            'pre_close_min': ('pre_close', 'float'),
            'pre_close_max': ('pre_close', 'float'),
            'open_interest_min': ('open_interest', 'float'),
            'open_interest_max': ('open_interest', 'float'),
            'volume_min': ('volume', 'float'),
            'volume_max': ('volume', 'float'),
            'latest_price_vol_min': ('latest_price_vol', 'float'),
            'latest_price_vol_max': ('latest_price_vol', 'float'),
            'delta_min': ('delta', 'float'),
            'delta_max': ('delta', 'float'),
            'vega_min': ('vega', 'float'),
            'vega_max': ('vega', 'float'),
            'imp_vol_min': ('imp_vol', 'float'),
            'imp_vol_max': ('imp_vol', 'float'),
            'gamma_min': ('gamma', 'float'),
            'gamma_max': ('gamma', 'float'),
            'theta_min': ('theta', 'float'),
            'theta_max': ('theta', 'float'),
            'rho_min': ('rho', 'float'),
            'rho_max': ('rho', 'float'),
            'close_min': ('close', 'float'),
            'close_max': ('close', 'float'),
            'change_min': ('change', 'float'),
            'change_max': ('change', 'float'),
            'change_ratio_min': ('change_ratio', 'float'),
            'change_ratio_max': ('change_ratio', 'float'),
            'expire_date': ('expire_date', 'date'),
            'open_int_change_min': ('open_int_change', 'float'),
            'open_int_change_max': ('open_int_change', 'float'),
            'active_level_min': ('active_level', 'float'),
            'active_level_max': ('active_level', 'float'),
            'cycle_min': ('cycle', 'float'),
            'cycle_max': ('cycle', 'float'),
            'call_put': ('call_put', 'str'),
            'option_symbol': ('option_symbol', 'str'),
            'underlying_symbol': ('underlying_symbol', 'str'),
            'underlying_price_min': ('underlying_price', 'float'),
            'underlying_price_max': ('underlying_price', 'float'),
        }

        # Dynamically build query based on kwargs
        query = "SELECT underlying_symbol, strike_price, call_put, expire_date, theta FROM public.options WHERE open_interest > 0"

        # Dynamically build query based on kwargs
        for key, value in kwargs.items():
            if key in column_types and value is not None:
                column, col_type = column_types[key]

                # Sanitize and format value for SQL query
                sanitized_value = self.sanitize_value(value, col_type)

                if 'min' in key:
                    query += f" AND {column} >= {sanitized_value}"
                elif 'max' in key:
                    query += f" AND {column} <= {sanitized_value}"
                else:
                    query += f" AND {column} = {sanitized_value}"
                print(query)
        conn = await self.get_connection()

        try:
            # Execute the query
            return await conn.fetch(query)
        except Exception as e:
            print(f"Error during query: {e}")
            return []
        finally:
            await conn.close()

    @commands.slash_command()
    async def filter(self, inter):
        pass

    @filter.sub_command()
    async def menu(self, inter:disnake.AppCmdInter):
        await inter.response.defer()
        await inter.edit_original_message(view=FilterView(), embed=FilterMenu())



    @filter.sub_command()
    async def low_theta(self, inter: disnake.AppCmdInter):
        await inter.response.defer()
        filtered_data = await self.filter_options(theta_max=-0.01, theta_min=-0.04)


        df = pd.DataFrame(filtered_data)
        print(df.columns)
        # Select only the specified columns

        df = df.rename(columns={'underlying_symbol': 'sym', 'strike_price':'strike', 'call_put': 'cp', 'expire_date': 'exp'})
        table = tabulate(df, headers=['sym', 'strike', 'cp', 'expiry', 'theta'], tablefmt='fancy', showindex=False)
        # Break apart data into chunks of 4000 characters
        chunks = self.chunk_string(table, 4000)
        embeds=[]
        # Create and send embeds for each chunk
        for chunk in chunks:
            embed = disnake.Embed(title="Low Theta Options", description=f"```py\n{chunk}```")
            embeds.append(embed)
        await inter.edit_original_message(embed=embeds[0],view=AlertMenus(embeds))  # Use send or edit_original_message as appropriate

    @filter.sub_command()
    async def ai(self, inter:disnake.AppCmdInter, filter_request:str):
        await inter.response.defer()
  
        results = await run_conversation(filter_request)
        results = results.choices[0].message.content
        embed = disnake.Embed(title=f"GPT AI - Options Filter", description=f"```py\n{results}```")

        await inter.edit_original_message(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(FilterCog(bot))

    print('Filter - READY!')

