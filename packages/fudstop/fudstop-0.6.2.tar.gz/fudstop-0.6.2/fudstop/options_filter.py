import disnake
from disnake import TextInputStyle
from disnake.ext import commands
import pandas as pd
from typing import List
from webull_options.webull_options import WebullOptions
import os
from tabulate import tabulate

from bot_menus.pagination import AlertMenus


from dotenv import load_dotenv
load_dotenv()
theta_em = "<a:_:1047010360554704977>"
gamma_em = "<a:_:1190024505700134973>"
delta_em = "<a:_:1044647851466182736>"
vega_em = "<a:_:1044647903009976372>"
rho_em = "<a:_:1044647745702596648>"
ticker_em = "<:_:1190025407815221270>"
volume_em = "🔊"
oi_em = "👥"
oi_change_em = "🔀"
iv_em="💉"
expiry_em="🗓️"
strike_em="🎳"
call_put_em="↕️"
change_ratio_em="➗"
start_over_em="<:_:1190026332248232126>"
open_em="<a:_:1044647404693106728>"
high_em="<a:_:1047010108930019340>"
low_em="<a:_:1044658254137008148>"
close_em="<a:_:1044647558133334126>"
underlying_price_em="💲"
from apis.polygonio.polygon_options import PolygonOptions

sdk = PolygonOptions(user='chuck', database='fudstop')

class FilterMenu(disnake.Embed):
    def __init__(self):
        super().__init__( 
            title=f"Options Filter Menu",
            description=f"```py\nMenu Buttons:```\n\n> {theta_em} - Theta\n> {delta_em} - Delta\n> {gamma_em} - Gamma\n> {vega_em} - Vega\n> {rho_em} - Rho\n\n> {iv_em} - IV\n> {volume_em} - Vol\n> {oi_em} - OI\n> {oi_change_em} - OI Change\n> {change_ratio_em} - Change%\n\n> {open_em} - Open\n> {high_em} - High\n> {low_em} - Low\n> {close_em} - Close\n> {underlying_price_em} - Underlying Price\n\n> {ticker_em} - Ticker\n> {strike_em} - Strike\n> {call_put_em} - Direction\n> {expiry_em} - Expiry\n\n> {start_over_em} - Clear"
        )


        self.set_footer(text=f"Implemented by FUDSTOP")
        self.add_field(namne="Extra Menu:", value=                "```py\nMenu Buttons:```\n\n"
                "> 💵 - Bid\n"
                "> 📊 - Bid Size\n"
                "> 💰 - Ask\n"
                "> 🎯 - Mid\n"
                "> 🔀 - Spread\n"
                "> 🔢 - Spread %\n"
                "> 🌊 - Vega Impact\n"
                "> ⚖️ - Delta Theta Ratio\n"
                "> ⚠️ - Gamma Risk\n"
                "> 🕒 - Theta Decay Rate\n"
                "> 🔍 - Sensitivity\n"
                "> 💨 - Velocity\n"
                "> 📈 - Profit Potential\n"
                "> 💎 - Intrinsic Value\n"
                "> 📅 - Extrinsic Value\n")
        self.add_field(name=f"Info:", value=f"> Select up to 5 attributes to query from the drop-down menu below.")




class QueryMenu(disnake.ui.Select):
    def __init__(self):
        # Use provided options if they are not None, otherwise default to an empty list


        super().__init__(custom_id='results', row=2, min_values=1, max_values=5, options= [ 
            disnake.SelectOption(label='ticker', description='Filter options based on the ticker name.',emoji=ticker_em),
            disnake.SelectOption(label='strike_price', description='Filter options by min/max strike price values.', emoji=strike_em),
            disnake.SelectOption(label='expiry', description='Filter options by expiration eact or min/max.', emoji=expiry_em),
            disnake.SelectOption(label='call_put', description='Filter options by calls or puts.', emoji=call_put_em),
            disnake.SelectOption(label='theta', description=f'Filter options by min / max theta values.', emoji=theta_em),
            disnake.SelectOption(label='gamma', description='Filter options by min/max gamma values.', emoji=gamma_em),
            disnake.SelectOption(label='vega', description='Filter options by min/max vega values.', emoji=vega_em),
            disnake.SelectOption(label='delta', description='Filter options by min/max vega values.', emoji=vega_em),
            disnake.SelectOption(label='iv', description='Filter options by min/max IV values.', emoji=delta_em),
            disnake.SelectOption(label='volume', description='Filter options by min/max volume values.', emoji=delta_em),
            disnake.SelectOption(label='oi', description='Filter options by min/max open interest values.', emoji=oi_em),
            disnake.SelectOption(label='open', description='Filter options by min/max open price values.', emoji=open_em),
            disnake.SelectOption(label='high', description='Filter options by min/max high price values.', emoji=high_em),
            disnake.SelectOption(label='low', description='Filter options by min/max low price values.', emoji=low_em),
            disnake.SelectOption(label='close', description='Filter options by min/max latest price values.', emoji=close_em),
            disnake.SelectOption(label='underlying_price', description='Filter options by min/max underlying price values.', emoji=underlying_price_em),


        ])

    async def callback(self, inter: disnake.AppCmdInter):
        text_inputs =[]
        for value in self._selected_values:
            
            components = [
            disnake.ui.TextInput(
                label=f"Filter by {value}",
                placeholder=f"The minimum {value} you wish the option to have.",
                custom_id=f"{value}",
                style=TextInputStyle.short
            )]

            text_inputs.append(components)

        await inter.response.send_modal(FilterModal(components=text_inputs))


class QueryMenu2(disnake.ui.Select):
    def __init__(self):
        # Use provided options if they are not None, otherwise default to an empty list


        super().__init__(custom_id='results2', row=3, min_values=1, max_values=5, options= [ 
            disnake.SelectOption(label='bid', description='Filter options based on the min/max bid price.',emoji="💵"),
            disnake.SelectOption(label='bid_size', description='Filter options by min/max bid_size values.', emoji="📊"),
            disnake.SelectOption(label='ask', description=f'Filter options by min / max ask values.', emoji="💰"),
            disnake.SelectOption(label='mid', description='Filter options by min/max mid values.', emoji="🎯"),
            disnake.SelectOption(label='spread', description='Filter options by min/max bid/ask spread values.', emoji="🔀"),
            disnake.SelectOption(label='spread %', description='Filter options by min/max bid/ask spread percent values.', emoji="🔢"),
            disnake.SelectOption(label='vega impact', description='Filter options by min/max vega impact values.', emoji="🌊"),
            disnake.SelectOption(label='delta theta ratio', description='Filter options by min/max delta theta ratio values.', emoji="⚖️"),
            disnake.SelectOption(label='gamma risk', description='Filter options by min/max gamma risk values.', emoji="⚠️"),
            disnake.SelectOption(label='theta decay rate', description='Filter options by min/max theta decay rate values.', emoji="🕒"),
            disnake.SelectOption(label='sensitivity', description='Filter options by min/max sensitivity values.', emoji="🔍"),
            disnake.SelectOption(label='velocity', description='Filter options by min/max velocity values.', emoji="💨"),
            disnake.SelectOption(label='profit potential', description='Filter options by min/max profit potential values.', emoji="📈"),
            
            disnake.SelectOption(label='intrinsic value', description='Filter options by min/max strike price values.', emoji="💎"),
            disnake.SelectOption(label='extrinsic value', description='Filter options by expiration date - eact or min/max.', emoji="📅"),
       


        ])

    async def callback(self, inter: disnake.AppCmdInter):
        text_inputs =[]
        for value in self._selected_values:
            
            components = [
            disnake.ui.TextInput(
                label=f"Filter by {value}",
                placeholder=f"The minimum {value} you wish the option to have.",
                custom_id=f"{value}",
                style=TextInputStyle.short
            )]

            text_inputs.append(components)

        await inter.response.send_modal(FilterModal(components=text_inputs))

class FilterView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(QueryMenu())
        self.add_item(QueryMenu2())

       




# Subclassing the modal.
class FilterModal(disnake.ui.Modal):
    def __init__(self, components):
        self.components = components
        super().__init__(title="Create Tag", components=self.components)

    def chunk_string(self, string, size):
        """Yield successive size-sized chunks from string."""
        for i in range(0, len(string), size):
            yield string[i:i + size]

    async def callback(self, inter: disnake.ModalInteraction):
        conn = await sdk.connect()
        await inter.response.defer(ephemeral=True)
        # Operator mapping for different fields
        operator_mapping = {
            'expire_date': '=',
            'underlying_symbol': '=',
            'imp_vol': '>=',
            'open_int_change': '>=',
            'vega': '>=',
            'gamma': '>=',
            'delta': '>=',
            'volume': '>=',
            'open_interest': '>=',
            'strike_price': '='
            # Add other fields and their corresponding operators here
        }

        # Fields that need to be wrapped in single quotes
        quote_fields = ['ticker']

        # Prepare the base query and conditions
        query = "SELECT ticker, strike, call_put, expiry FROM opts WHERE "
        conditions = []

        for key, value in inter.text_values.items():
            # Choose operator based on the field, defaulting to '='
            operator = operator_mapping.get(key, '=')

            # Wrap value in quotes if the field is in quote_fields, else directly insert the value
            if key in quote_fields:
                formatted_value = f"'{value}'"
            else:
                formatted_value = value

            conditions.append(f"{key} {operator} {formatted_value}")

        # Combine conditions and finalize the query
        query += " AND ".join(conditions) + " LIMIT 25;"
        print(query)
        results = await conn.fetch(query)
        df = pd.DataFrame(results)
        print(df.columns)


        df = df.rename(columns={'ticker': 'sym', 'expiry': 'exp', "call_put": 'cp'})
        table = tabulate(df, headers=['sym', 'strike', 'cp', 'expiry', 'theta'], tablefmt='fancy', showindex=False)
        # Break apart data into chunks of 4000 characters
        chunks = self.chunk_string(table, 4000)
        embeds=[]
        # Create and send embeds for each chunk
        for chunk in chunks:
            embed = disnake.Embed(title="Option Filter Results", description=f"```py\n{chunk}```")
            embeds.append(embed)
        embed.add_field(name=f"Query:", value=f"```py\n{query}```")
        await inter.edit_original_message(embed=embeds[0],view=AlertMenus(embeds).add_item(QueryMenu()))  # Use send or edit_original_message as appropriate



