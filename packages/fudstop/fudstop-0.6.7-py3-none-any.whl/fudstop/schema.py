from openai import OpenAI
import os
import asyncio
from webull_options.webull_options import WebullOptions
from apis.polygonio.polygon_options import PolygonOptions
from list_sets.ticker_lists import most_active_tickers

import json
from dotenv import load_dotenv
load_dotenv()
import datetime
client = OpenAI(api_key=os.environ.get('YOUR_OPENAI_KEY'))
sdk = WebullOptions(access_token=os.environ.get('ACCESS_TOKEN'), osv=os.environ.get('OSV'), did=os.environ.get('DID'), user='postgres', database='fudstop')
def serialize_record(record):
    """Convert asyncpg.Record to a dictionary, handling date serialization."""
    return {key: value.isoformat() if isinstance(value, datetime.date) else value 
            for key, value in dict(record).items()}



tools = [
    {
        "type": "function",
        "function": {
            "name": "filter_options",
            "description": "Filter options based on several different keyword arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "open_min": {
                        "type": "number",
                        "description": "Minimum value for the opening price.",
                    },
                    "open_max": {
                        "type": "number",
                        "description": "Maximum value for the opening price.",
                    },
                    "open": {
                        "type": "number",
                        "description": "Exact value for the opening price.",
                    },
                    "high_min": {
                        "type": "number",
                        "description": "Minimum value for the highest price.",
                    },
                    "high_max": {
                        "type": "number",
                        "description": "Maximum value for the highest price.",
                    },
                    "high": {
                        "type": "number",
                        "description": "Exact value for the highest price.",
                    },
                    "low_min": {
                        "type": "number",
                        "description": "Minimum value for the lowest price.",
                    },
                    "low_max": {
                        "type": "number",
                        "description": "Maximum value for the lowest price.",
                    },
                    "low": {
                        "type": "number",
                        "description": "Exact value for the lowest price.",
                    },
                    "strike_price": {
                        "type": "integer",
                        "description": "Exact strike price.",
                    },
                    "strike_price_min": {
                        "type": "integer",
                        "description": "Minimum strike price.",
                    },
                    "strike_price_max": {
                        "type": "integer",
                        "description": "Maximum strike price.",
                    },
                    "open_interest_min": {
                        "type": "number",
                        "description": "Minimum open interest.",
                    },
                    "open_interest_max": {
                        "type": "number",
                        "description": "Maximum open interest.",
                    },
                    "open_interest": {
                        "type": "number",
                        "description": "Exact open interest.",
                    },
                    "open_int_change_min": {
                        "type": "number",
                        "description": "Minimum open interest change.",
                    },
                    "open_int_change_max": {
                        "type": "number",
                        "description": "Maximum open interest change.",
                    },
                    "open_int_change": {
                        "type": "number",
                        "description": "Exact open interest change.",
                    },
                    "volume_min": {
                        "type": "number",
                        "description": "Minimum volume.",
                    },
                    "volume_max": {
                        "type": "number",
                        "description": "Maximum volume.",
                    },
                    "volume": {
                        "type": "number",
                        "description": "Exact volume.",
                    },
                    "delta_min": {
                        "type": "number",
                        "description": "Minimum delta value.",
                    },
                    "delta_max": {
                        "type": "number",
                        "description": "Maximum delta value.",
                    },
                    "delta": {
                        "type": "number",
                        "description": "Exact delta value.",
                    },
                    "vega": {
                        "type": "number",
                        "description": "Exact vega value.",
                    },
                    "vega_min": {
                        "type": "number",
                        "description": "Minimum vega value.",
                    },
                    "vega_max": {
                        "type": "number",
                        "description": "Maximum vega value.",
                    },
                    "imp_vol_min": {
                        "type": "number",
                        "description": "Minimum implied volatility.",
                    },
                    "imp_vol_max": {
                        "type": "number",
                        "description": "Maximum implied volatility.",
                    },
                    "imp_vol": {
                        "type": "number",
                        "description": "Exact implied volatility.",
                    },
                    "gamma": {
                        "type": "number",
                        "description": "Exact gamma value.",
                    },
                    "gamma_min": {
                        "type": "number",
                        "description": "Minimum gamma value.",
                    },
                    "gamma_max": {
                        "type": "number",
                        "description": "Maximum gamma value.",
                    },
                    "theta_min": {
                        "type": "number",
                        "description": "Minimum theta value.",
                    },
                    "theta_max": {
                        "type": "number",
                        "description": "Maximum theta value.",
                    },
                    "change_ratio": {
                        "type": "number",
                        "description": "Maximum change value.",
                    },
                    "change_ratio_min": {
                        "type": "number",
                        "description": "Minimum change ratio.",
                    },
                    "change_ratio_max": {
                        "type": "number",
                        "description": "Maximum change ratio.",
                    },
                    "expire_date": {
                        "type": "string",
                        "description": "Expiration date of the option (YYYY-MM-DD).",
                    },
                    "expire_date_min": {
                        "type": "string",
                        "description": "The minimum expiration date of the option (YYYY-MM-DD).",
                    },
                    "expire_date_max": {
                        "type": "string",
                        "description": "The maximum expiration date of the option (YYYY-MM-DD).",
                    },
                    "call_put": {
                        "type": "string",
                        "description": "Type of option to filter ('call' or 'put').",
                    },
                    "option_symbol": {
                        "type": "string",
                        "description": "Symbol of the option.",
                    },
                    "underlying_symbol": {
                        "type": "string",
                        "description": "Underlying symbol for the option.",
                    },
                    "sensitivity": {
                        "type": "number",
                        "description": "Sensitivity measures the responsiveness of the option's price to underlying market changes, reflecting how quickly an option reacts to market movements."
                    },
                    "sensitivity_min": {
                        "type": "number",
                        "description": "Minimum threshold for sensitivity, indicating the lowest reactivity of the option to market changes."
                    },
                    "sensitivity_max": {
                        "type": "number",
                        "description": "Maximum threshold for sensitivity, indicating the highest reactivity of the option to market changes."
                    },
                    "velocity": {
                        "type": "number",
                        "description": "Velocity refers to the rate of change in the option's price, capturing the speed at which the option's value is evolving over time."
                    },
                    "velocity_min": {
                        "type": "number",
                        "description": "Minimum threshold for velocity, denoting the slowest rate of change in the option's price."
                    },
                    "velocity_max": {
                        "type": "number",
                        "description": "Maximum threshold for velocity, denoting the fastest rate of change in the option's price."
                    },
                    "theta_decay_rate": {
                        "type": "number",
                        "description": "Theta decay rate measures the rate at which the option's time value decreases as it approaches expiration, indicating the effect of time decay on the option's price."
                    },
                    "theta_decay_rate_min": {
                        "type": "number",
                        "description": "Minimum threshold for theta decay rate, showing the slowest rate of time value reduction."
                    },
                    "theta_decay_rate_max": {
                        "type": "number",
                        "description": "Maximum threshold for theta decay rate, showing the fastest rate of time value reduction."
                    },
                    "delta_theta_ratio": {
                        "type": "number",
                        "description": "Delta theta ratio compares the option's delta to its theta, providing a balance measure between directional exposure and time decay."
                    },
                    "delta_theta_ratio_min": {
                        "type": "number",
                        "description": "Minimum threshold for delta theta ratio, indicating a lower balance between directional exposure and time decay."
                    },
                    "delta_theta_ratio_max": {
                        "type": "number",
                        "description": "Maximum threshold for delta theta ratio, indicating a higher balance between directional exposure and time decay."
                    },
                    "delta_adjusted_liquidity": {
                        "type": "number",
                        "description": "Delta adjusted liquidity provides a measure of market liquidity adjusted for the option's directional risk, giving insights into how liquidity is influenced by market movements."
                    },
                    "delta_adjusted_liquidity_min": {
                        "type": "number",
                        "description": "Minimum threshold for delta adjusted liquidity, indicating lower liquidity adjusted for directional risk."
                    },
                    "delta_adjusted_liquidity_max": {
                        "type": "number",
                        "description": "Maximum threshold for delta adjusted liquidity, indicating higher liquidity adjusted for directional risk."
                    },
                    "delta_weighted_time_value": {
                        "type": "number",
                        "description": "Delta weighted time value adjusts the time value of the option by its delta, providing a sense of the time value relative to the option's directional exposure."
                    },
                    "delta_weighted_time_value_min": {
                        "type": "number",
                        "description": "Minimum threshold for delta weighted time value, indicating a lower adjusted time value for directional risk."
                    },
                    "delta_weighted_time_value_max": {
                        "type": "number",
                        "description": "Maximum threshold for delta weighted time value, indicating a higher adjusted time value for directional risk."
                    },

                    "vol_oi_ratio": {
                        "type": "number",
                        "description": "Vol_oi_ratio indicates the ratio of trading volume to open interest, providing insight into trading activity relative to the number of open contracts."
                    },
                    "vol_oi_ratio_min": {
                        "type": "number",
                        "description": "Minimum threshold for vol_oi_ratio, indicating a lower level of trading activity relative to open interest."
                    },
                    "vol_oi_ratio_max": {
                        "type": "number",
                        "description": "Maximum threshold for vol_oi_ratio, indicating a higher level of trading activity relative to open interest."
                    },

                    "spread": {
                        "type": "number",
                        "description": "Spread represents the difference between the ask and bid prices of an option, indicating the transaction cost and liquidity of the option."
                    },
                    "spread_min": {
                        "type": "number",
                        "description": "Minimum threshold for spread, indicating a narrower difference between ask and bid prices."
                    },
                    "spread_max": {
                        "type": "number",
                        "description": "Maximum threshold for spread, indicating a wider difference between ask and bid prices."
                    },

                    "spread_pct": {
                        "type": "number",
                        "description": "Spread_pct measures the spread as a percentage of the mid-price, providing a relative view of the spread in terms of price."
                    },
                    "spread_pct_min": {
                        "type": "number",
                        "description": "Minimum threshold for spread_pct, indicating a lower relative difference between ask and bid prices."
                    },
                    "spread_pct_max": {
                        "type": "number",
                        "description": "Maximum threshold for spread_pct, indicating a higher relative difference between ask and bid prices."
                    },

                    "liquidity_oi_ratio": {
                        "type": "number",
                        "description": "Liquidity_oi_ratio compares the liquidity indicator with open interest, assessing market depth in relation to the number of open contracts."
                    },
                    "liquidity_oi_ratio_min": {
                        "type": "number",
                        "description": "Minimum threshold for liquidity_oi_ratio, indicating lower market depth relative to open interest."
                    },
                    "liquidity_oi_ratio_max": {
                        "type": "number",
                        "description": "Maximum threshold for liquidity_oi_ratio, indicating higher market depth relative to open interest."
                    },

                    "gamma_risk": {
                        "type": "number",
                        "description": "Gamma risk measures the rate of change in delta, indicating the option's sensitivity to movements in the underlying asset's price."
                    },
                    "gamma_risk_min": {
                        "type": "number",
                        "description": "Minimum threshold for gamma risk, indicating a lower sensitivity to changes in the underlying asset's price."
                    },
                    "gamma_risk_max": {
                        "type": "number",
                        "description": "Maximum threshold for gamma risk, indicating a higher sensitivity to changes in the underlying asset's price."
                    },
                    "dte": {
                        "type": "number",
                        "description": "Minimum days to expiry."
                    },
                    "dte_min": {
                        "type": "number",
                        "description": "Exact number of days until expiry."
                    },
                    "dte_max": {
                        "type": "number",
                        "description": "Maximum threshold for days to expiry."
                    },

                    "oi_weighted_delta": {
                        "type": "number",
                        "description": "Weighted delta in terms of open interest."
                    },
                    "oi_weighted_delta_min": {
                        "type": "number",
                        "description": "Minimum threshold for weighted delta in terms of open interest."
                    },
                    "oi_weighted_delta_max": {
                        "type": "number",
                        "description": "Maximum threshold for weighted delta in terms of open interest."
                    },
                    "iv_spread": {
                        "type": "number",
                        "description": "Implied volatility spread."
                    },
                    "iv_spread_min": {
                        "type": "number",
                        "description": "Minimum threshold for implied volatility spread."
                    },
                    "iv_spread_max": {
                        "type": "number",
                        "description": "Maximum threshold for implied volatility spread."
                    },
                    "oi_change_vol_adjusted": {
                        "type": "number",
                        "description": "Volume-adjusted change in open interest."
                    },
                    "oi_change_vol_adjusted_min": {
                        "type": "number",
                        "description": "Minimum threshold for volume-adjusted change in open interest."
                    },
                    "oi_change_vol_adjusted_max": {
                        "type": "number",
                        "description": "Maximum threshold for volume-adjusted change in open interest."
                    },
                    "oi_pcr": {
                        "type": "number",
                        "description": "Open interest put/call ratio."
                    },
                    "oi_pcr_min": {
                        "type": "number",
                        "description": "Minimum threshold for open interest put/call ratio."
                    },
                    "oi_pcr_max": {
                        "type": "number",
                        "description": "Maximum threshold for open interest put/call ratio."
                    },
                    "volume_pcr": {
                        "type": "number",
                        "description": "Volume put/call ratio."
                    },
                    "volume_pcr_min": {
                        "type": "number",
                        "description": "Minimum threshold for volume put/call ratio."
                    },
                    "volume_pcr_max": {
                        "type": "number",
                        "description": "Maximum threshold for volume put/call ratio."
                    },
                    "vega_weighted_maturity": {
                        "type": "number",
                        "description": "Vega-weighted maturity of the option."
                    },
                    "vega_weighted_maturity_min": {
                        "type": "number",
                        "description": "Minimum threshold for vega-weighted maturity."
                    },
                    "vega_weighted_maturity_max": {
                        "type": "number",
                        "description": "Maximum threshold for vega-weighted maturity."
                    },
                    "theta_decay_rate": {
                        "type": "number",
                        "description": "Rate of time decay (theta) of the option."
                    },
                    "theta_decay_rate_min": {
                        "type": "number",
                        "description": "Minimum threshold for the rate of time decay."
                    },
                    "theta_decay_rate_max": {
                        "type": "number",
                        "description": "Maximum threshold for the rate of time decay."
                    },










                },
                "required": [],  # Add required fields here if any
            },
        }
    }
]
async def filter_options(**kwargs):
    """
    Filters the options table based on provided keyword arguments.
    Usage example:
        await filter_options(strike_price_min=100, strike_price_max=200, call_put='call',
                                expire_date='2023-01-01', delta_min=0.1, delta_max=0.5)
    """
    # Start with the base query
    query = f"SELECT underlying_symbol, strike_price, call_put, expire_date FROM wb_opts WHERE "
    params = []
    param_index = 1

    # Mapping kwargs to database columns and expected types, including range filters
        # Mapping kwargs to database columns and expected types, including range filters
    column_types = {
            'ticker_id': ('ticker_id', 'int'),
            'belong_ticker_id': ('belong_ticker_id', 'int'),
            'open_min': ('open', 'float'),
            'open_max': ('open', 'float'),
            'open': ('open', 'float'),
            'high_min': ('high', 'float'),
            'high_max': ('high', 'float'),
            'high': ('high', 'float'),
            'low_min': ('low', 'float'),
            'low_max': ('low', 'float'),
            'low': ('low', 'float'),
            'strike_price_min': ('strike_price', 'int'),
            'strike_price_max': ('strike_price', 'int'),
            'strike_price': ('strike_price', 'int'),
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
            'delta': ('delta', 'float'),
            'vega_min': ('vega', 'float'),
            'vega_max': ('vega', 'float'),
            'imp_vol': ('imp_vol', 'float'),
            'imp_vol_min': ('imp_vol', 'float'),
            'imp_vol_max': ('imp_vol', 'float'),
            'gamma_min': ('gamma', 'float'),
            'gamma_max': ('gamma', 'float'),
            'gamma': ('gamma', 'float'),
            'theta': ('theta', 'float'),
            'theta_min': ('theta', 'float'),
            'theta_max': ('theta', 'float'),
            'rho_min': ('rho', 'float'),
            'rho_max': ('rho', 'float'),
            'close_min': ('close', 'float'),
            'close': ('close', 'float'),
            'close_max': ('close', 'float'),
            'change_min': ('change', 'float'),
            'change_max': ('change', 'float'),
            'change_ratio_min': ('change_ratio', 'float'),
            'change_ratio_max': ('change_ratio', 'float'),
            'change_ratio': ('change_ratio', 'float'),
            'expire_date_min': ('expire_date', 'date'),
            'expire_date_max': ('expire_date', 'date'),
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
            'oi_weighted_delta_min': ('oi_weighted_delta', 'float'),
            'oi_weighted_delta_max': ('oi_weighted_delta', 'float'),
            'iv_spread_min': ('iv_spread', 'float'),
            'iv_spread_max': ('iv_spread', 'float'),
            'oi_change_vol_adjusted_min': ('oi_change_vol_adjusted', 'float'),
            'oi_change_vol_adjusted_max': ('oi_change_vol_adjusted', 'float'),
            'oi_pcr_min': ('oi_pcr', 'float'),
            'oi_pcr_max': ('oi_pcr', 'float'),
            'oc_pcr': ('oi_pcr', 'float'),
            'volume_pcr_min': ('volume_pcr', 'float'),
            'volume_pcr_max': ('volume_pcr', 'float'),
            'volume_pcr': ('volume_pcr', 'float'),
            'vega_weighted_maturity_min': ('vega_weighted_maturity', 'float'),
            'vega_weighted_maturity_max': ('vega_weighted_maturity', 'float'),
            'theta_decay_rate_min': ('theta_decay_rate', 'float'),
            'theta_decay_rate_max': ('theta_decay_rate', 'float'),
            'velocity_min': ('velocity', 'float'),
            'velocity_max': ('velocity', 'float'),
            'gamma_risk_min': ('gamma_risk', 'float'),
            'gamma_risk_max': ('gamma_risk', 'float'),
            'delta_to_theta_ratio_min': ('delta_to_theta_ratio', 'float'),
            'delta_to_theta_ratio_max': ('delta_to_theta_ratio', 'float'),
            'liquidity_theta_ratio_min': ('liquidity_theta_ratio', 'float'),
            'liquidity_theta_ratio_max': ('liquidity_theta_ratio', 'float'),
            'sensitivity_score_min': ('sensitivity_score', 'float'),
            'sensitivity_score_max': ('sensitivity_score', 'float'),
            'dte_min': ('dte', 'int'),
            'dte_max': ('dte', 'int'),
            'dte': ('dte', 'int'),
            'time_value_min': ('time_value', 'float'),
            'time_value_max': ('time_value', 'float'),
            'time_value': ('time_value', 'float'),
            'moneyness': ('moneyness', 'str')
        }

    # Dynamically build query based on kwargs
    query = "SELECT underlying_symbol, strike_price, call_put, expire_date FROM wb_opts WHERE open_interest > 0"

    # Dynamically build query based on kwargs
    for key, value in kwargs.items():
        if key in column_types and value is not None:
            column, col_type = column_types[key]

            # Sanitize and format value for SQL query
            sanitized_value = sdk.sanitize_value(value, col_type)

            if 'min' in key:
                query += f" AND {column} >= {sanitized_value}"
            elif 'max' in key:
                query += f" AND {column} <= {sanitized_value}"
            else:
                query += f" AND {column} = {sanitized_value}"
            print(query)
    query += " LIMIT 25"
    conn = await sdk.db_manager.get_connection()

    try:
        # Execute the query
        return await conn.fetch(query)
    except Exception as e:
        print(f"Error during query: {e}")
        return []
    finally:
        await conn.close()
async def run_conversation(query: str):
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": f"{query}?? Please response in tabulated format for ease of readability and give a summary underneath it. Use 'fancy' Ensure to only return options that expire past today's date.. and return the query you used."}]
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "filter_options": filter_options,  # Assuming filter_options is an async function
        }

        messages.append(response_message)  # extend conversation with assistant's reply

        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            records = await function_to_call(**function_args)

            # Process each record for serialization
            processed_records = [serialize_record(record) for record in records]

            # Serialize the list of processed records
            serialized_response = json.dumps(processed_records)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": serialized_response,
            })

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response


