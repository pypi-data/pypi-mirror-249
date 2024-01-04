from openai import OpenAI
import os
import asyncio
from webull_options.webull_options import WebullOptions
from apis.polygonio.polygon_options import PolygonOptions
from list_sets.ticker_lists import most_active_tickers
sdk2 = PolygonOptions(user='postgres', database='fudstop')
import json
from dotenv import load_dotenv
load_dotenv()
import datetime
client = OpenAI(api_key=os.environ.get('YOUR_OPENAI_KEY'))
sdk = WebullOptions(access_token=os.environ.get('ACCESS_TOKEN'), osv=os.environ.get('OSV'), did=os.environ.get('DID'))
def serialize_record(record):
    """Convert asyncpg.Record to a dictionary, handling date serialization."""
    return {key: value.isoformat() if isinstance(value, datetime.date) else value 
            for key, value in dict(record).items()}

params_dict = { 
    
    "open": {
        "description": "Exact value for the opening price.",
        "min_max": "Minimum and maximum thresholds for the opening price."
    },
    "high": {
        "description": "Exact value for the highest price.",
        "min_max": "Minimum and maximum thresholds for the highest price."
    },
    "low": {
        "description": "Exact value for the lowest price.",
        "min_max": "Minimum and maximum thresholds for the lowest price."
    },
    "strike": {
        "description": "Exact strike price.",
        "min_max": "Minimum and maximum thresholds for the strike price."
    },
    "oi": {
        "description": "Exact open interest.",
        "min_max": "Minimum and maximum thresholds for open interest."
    },
    "vol": {
        "description": "Exact volume.",
        "min_max": "Minimum and maximum thresholds for volume."
    },
    "delta": {
        "description": "Exact delta value.",
        "min_max": "Minimum and maximum thresholds for delta value."
    },
    "vega": {
        "description": "Exact vega value.",
        "min_max": "Minimum and maximum thresholds for vega value."
    },
    "iv": {
        "description": "Exact implied volatility.",
        "min_max": "Minimum and maximum thresholds for implied volatility."
    },
    "gamma": {
        "description": "Exact gamma value.",
        "min_max": "Minimum and maximum thresholds for gamma value."
    },
    "theta": {
        "description": "Exact theta value.",
        "min_max": "Minimum and maximum thresholds for theta value."
    },
    "change_percent": {
        "description": "Maximum change value.",
        "min_max": "Minimum and maximum thresholds for maximum change value."
    },
    "expiry": {
        "description": "Expiration date of the option (YYYY-MM-DD).",
        "min_max": "Minimum and maximum thresholds for expiration date."
    },
    "call_put": {
        "description": "Type of option to filter ('call' or 'put').",
        "min_max": "No thresholds for this attribute."
    },
    "option_symbol": {
        "description": "Symbol of the option.",
        "min_max": "No thresholds for this attribute."
    },
    "ticker": {
        "description": "Underlying symbol for the option.",
        "min_max": "No thresholds for this attribute."
    },
    "underlying_price": {
        "description": "Exact underlying price.",
        "min_max": "Minimum and maximum thresholds for underlying price."
    },
    "underlying_price_min": {
        "description": "Minimum underlying price.",
        "min_max": "Minimum and maximum thresholds for underlying price."
    },
    "underlying_price_max": {
        "description": "Maximum underlying price.",
        "min_max": "Minimum and maximum thresholds for underlying price."
    },
    "volatility_score": {
        "description": "The volatility score quantifies the degree of price variation experienced over a specific period, reflecting the option's relative stability or instability.",
        "min_max": "Minimum and maximum thresholds for volatility score."
    },
    "implied_leverage": {
        "description": "Implied leverage measures the leverage inherent in the option's price relative to its delta, providing insights into the potential amplification of returns or losses.",
        "min_max": "Minimum and maximum thresholds for implied leverage."
    },
    "risk_exposure": {
        "description": "Risk exposure combines the gamma risk and theta decay rate to provide an overall sense of the option's risk exposure, considering both market movements and time decay.",
        "min_max": "Minimum and maximum thresholds for risk exposure."
    },
    "depth_volatility_ratio": {
        "description": "Depth volatility ratio compares market depth (as indicated by trade size) against volatility, providing a measure of how market depth is affected by or responds to volatility.",
        "min_max": "Minimum and maximum thresholds for depth volatility ratio."
    },
    "drift_rate": {
        "description": "Drift rate calculates the rate at which the underlying asset must move to reach the break-even point by expiry, offering insights into the expected asset movement needed for profitability.",
        "min_max": "Minimum and maximum thresholds for drift rate."
    },
    "price_stability": {
        "description": "Price stability metric evaluates the stability of the option's price based on the spread percentage and volume, indicating how consistently the option is priced over time.",
        "min_max": "Minimum and maximum thresholds for price stability."
    },
    "bid": {
        "description": "The bid price represents the maximum price that a buyer is willing to pay for an option.",
        "min_max": "Minimum and maximum thresholds for bid price."
    },
    "ask": {
        "description": "The ask price is the minimum price that a seller is willing to accept for an option.",
        "min_max": "Minimum and maximum thresholds for ask price."
    },
    "bid_size": {
        "description": "Bid size indicates the quantity of options that buyers are willing to purchase at the bid price, reflecting market demand at that price level.",
        "min_max": "Minimum and maximum thresholds for bid size."
    },
    "ask_size": {
        "description": "Ask size represents the quantity of options that sellers are ready to sell at the ask price, indicating market supply at that price level.",
        "min_max": "Minimum and maximum thresholds for ask size."
    },
    "mid": {
        "description": "The mid price, or midpoint, is calculated as the average of the bid and ask prices, providing a reference point for the current market price of an option.",
        "min_max": "Minimum and maximum thresholds for mid price."
    },
    "sensitivity": {
        "description": "Sensitivity measures the responsiveness of the option's price to underlying market changes, reflecting how quickly an option reacts to market movements.",
        "min_max": "Minimum and maximum thresholds for sensitivity."
    },
    "velocity": {
        "description": "Velocity refers to the rate of change in the option's price, capturing the speed at which the option's value is evolving over time.",
        "min_max": "Minimum and maximum thresholds for velocity."
    },
    "theta_decay_rate": {
        "description": "Theta decay rate measures the rate at which the option's time value decreases as it approaches expiration, indicating the effect of time decay on the option's price.",
        "min_max": "Minimum and maximum thresholds for theta decay rate."
    },
    "delta_theta_ratio": {
        "description": "Delta theta ratio compares the option's delta to its theta, providing a balance measure between directional exposure and time decay.",
        "min_max": "Minimum and maximum thresholds for delta theta ratio."
    },
    "delta_adjusted_liquidity": {
        "description": "Delta adjusted liquidity provides a measure of market liquidity adjusted for the option's directional risk, giving insights into how liquidity is influenced by market movements.",
        "min_max": "Minimum and maximum thresholds for delta adjusted liquidity."
    },
    "delta_weighted_time_value": {
        "description": "Delta weighted time value adjusts the time value of the option by its delta, providing a sense of the time value relative to the option's directional exposure.",
        "min_max": "Minimum and maximum thresholds for delta weighted time value."
    },
    "vol_oi_ratio": {
        "description": "Vol_oi_ratio indicates the ratio of trading volume to open interest, providing insight into trading activity relative to the number of open contracts.",
        "min_max": "Minimum and maximum thresholds for vol_oi_ratio."
    },
    "spread": {
        "description": "Spread represents the difference between the ask and bid prices of an option, indicating the transaction cost and liquidity of the option.",
        "min_max": "Minimum and maximum thresholds for spread."
    },
    "spread_pct": {
        "description": "Spread_pct measures the spread as a percentage of the mid-price, providing a relative view of the spread in terms of price.",
        "min_max": "Minimum and maximum thresholds for spread_pct."
    },
    "liquidity_oi_ratio": {
        "description": "Liquidity_oi_ratio compares the liquidity indicator with open interest, assessing market depth in relation to the number of open contracts.",
        "min_max": "Minimum and maximum thresholds for liquidity_oi_ratio."
    },
    "gamma_risk": {
        "description": "Gamma risk measures the rate of change in delta, indicating the option's sensitivity to movements in the underlying asset's price.",
        "min_max": "Minimum and maximum thresholds for gamma risk."
    },
    "intrinsic_value": {
        "description": "Intrinsic value is the inherent worth of an option, calculated as the difference between the underlying asset's price and the strike price.",
        "min_max": "Minimum and maximum thresholds for intrinsic value."
    },
    "extrinsic_value": {
        "description": "Extrinsic value represents the time value of an option, encompassing factors like time to expiry and volatility.",
        "min_max": "Minimum and maximum thresholds for extrinsic value."
    },
    "hedge_effectiveness": {
        "description": "Effectiveness of hedging.",
        "min_max": "Minimum and maximum thresholds for extrinsic value."
    }
}


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
                    "strike": {
                        "type": "integer",
                        "description": "Exact strike price.",
                    },
                    "strike_min": {
                        "type": "integer",
                        "description": "Minimum strike price.",
                    },
                    "strike_max": {
                        "type": "integer",
                        "description": "Maximum strike price.",
                    },
                    "oi_min": {
                        "type": "number",
                        "description": "Minimum open interest.",
                    },
                    "oi_max": {
                        "type": "number",
                        "description": "Maximum open interest.",
                    },
                    "oi": {
                        "type": "number",
                        "description": "Exact open interest.",
                    },
                    "vol_min": {
                        "type": "number",
                        "description": "Minimum volume.",
                    },
                    "vol_max": {
                        "type": "number",
                        "description": "Maximum volume.",
                    },
                    "vol": {
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
                    "iv_min": {
                        "type": "number",
                        "description": "Minimum implied volatility.",
                    },
                    "iv_max": {
                        "type": "number",
                        "description": "Maximum implied volatility.",
                    },
                    "iv": {
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
                    "change_percent": {
                        "type": "number",
                        "description": "Maximum change value.",
                    },
                    "change_percent_min": {
                        "type": "number",
                        "description": "Minimum change ratio.",
                    },
                    "change_percent_max": {
                        "type": "number",
                        "description": "Maximum change ratio.",
                    },
                    "expiry": {
                        "type": "string",
                        "description": "Expiration date of the option (YYYY-MM-DD).",
                    },
                    "expiry_min": {
                        "type": "string",
                        "description": "The minimum expiration date of the option (YYYY-MM-DD).",
                    },
                    "expiry_max": {
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
                    "ticker": {
                        "type": "string",
                        "description": "Underlying symbol for the option.",
                    },
                    "underlying_price_min": {
                        "type": "number",
                        "description": "Minimum underlying price.",
                    },
                    "underlying_price_max": {
                        "type": "number",
                        "description": "Maximum underlying price.",
                    },
                    "volatility_score": {
                        "type": "number",
                        "description": "The volatility score quantifies the degree of price variation experienced over a specific period, reflecting the option's relative stability or instability."
                    },
                    "volatility_score_min": {
                        "type": "number",
                        "description": "Minimum threshold for the volatility score, indicating the lower bound of the option's price variation."
                    },
                    "volatility_score_max": {
                        "type": "number",
                        "description": "Maximum threshold for the volatility score, indicating the upper bound of the option's price variation."
                    },
                    "implied_leverage": {
                        "type": "number",
                        "description": "Implied leverage measures the leverage inherent in the option's price relative to its delta, providing insights into the potential amplification of returns or losses."
                    },
                    "implied_leverage_min": {
                        "type": "number",
                        "description": "Minimum threshold for the implied leverage, representing the lower boundary of leverage impact in the option's pricing."
                    },
                    "implied_leverage_max": {
                        "type": "number",
                        "description": "Maximum threshold for the implied leverage, representing the upper boundary of leverage impact in the option's pricing."
                    },
                    "risk_exposure": {
                        "type": "number",
                        "description": "Risk exposure combines the gamma risk and theta decay rate to provide an overall sense of the option's risk exposure, considering both market movements and time decay."
                    },
                    "risk_exposure_min": {
                        "type": "number",
                        "description": "Minimum threshold for risk exposure, indicating the lower limit of combined market and time-based risks for the option."
                    },
                    "risk_exposure_max": {
                        "type": "number",
                        "description": "Maximum threshold for risk exposure, indicating the upper limit of combined market and time-based risks for the option."
                    },

                    "hedge_effectiveness": {
                        "type": "number",
                        "description": "Hedge effectiveness assesses how well the option serves as a hedging instrument against market movements, considering factors like delta and gamma."
                    },
                    "hedge_effectiveness_min": {
                        "type": "number",
                        "description": "Minimum threshold for hedge effectiveness, reflecting the lower limit of the option's capability to hedge against market fluctuations."
                    },
                    "hedge_effectiveness_max": {
                        "type": "number",
                        "description": "Maximum threshold for hedge effectiveness, reflecting the upper limit of the option's capability to hedge against market fluctuations."
                    },
                    "depth_volatility_ratio": {
                        "type": "number",
                        "description": "Depth volatility ratio compares market depth (as indicated by trade size) against volatility, providing a measure of how market depth is affected by or responds to volatility."
                    },
                    "depth_volatility_ratio_min": {
                        "type": "number",
                        "description": "Minimum threshold for depth volatility ratio, denoting the lower limit of the relationship between market depth and volatility."
                    },
                    "depth_volatility_ratio_max": {
                        "type": "number",
                        "description": "Maximum threshold for depth volatility ratio, denoting the upper limit of the relationship between market depth and volatility."
                    },
                    "drift_rate": {
                        "type": "number",
                        "description": "Drift rate calculates the rate at which the underlying asset must move to reach the break-even point by expiry, offering insights into the expected asset movement needed for profitability."
                    },
                    "drift_rate_min": {
                        "type": "number",
                        "description": "Minimum threshold for drift rate, indicating the lower boundary of the required rate of movement in the underlying asset for option profitability."
                    },
                    "drift_rate_max": {
                        "type": "number",
                        "description": "Maximum threshold for drift rate, indicating the upper boundary of the required rate of movement in the underlying asset for option profitability."
                    },
                    "price_stability": {
                        "type": "number",
                        "description": "Price stability metric evaluates the stability of the option's price based on the spread percentage and volume, indicating how consistently the option is priced over time."
                    },
                    "price_stability_min": {
                        "type": "number",
                        "description": "Minimum threshold for price stability, reflecting the lower bound of price consistency and predictability."
                    },
                    "price_stability_max": {
                        "type": "number",
                        "description": "Maximum threshold for price stability, reflecting the upper bound of price consistency and predictability."
                    },
                    "bid": {
                        "type": "number",
                        "description": "The bid price represents the maximum price that a buyer is willing to pay for an option."
                    },
                    "bid_min": {
                        "type": "number",
                        "description": "Minimum threshold for the bid price, indicating the lowest bid in the range."
                    },
                    "bid_max": {
                        "type": "number",
                        "description": "Maximum threshold for the bid price, indicating the highest bid in the range."
                    },
                    "ask": {
                        "type": "number",
                        "description": "The ask price is the minimum price that a seller is willing to accept for an option."
                    },
                    "ask_min": {
                        "type": "number",
                        "description": "Minimum threshold for the ask price, representing the lowest ask in the range."
                    },
                    "ask_max": {
                        "type": "number",
                        "description": "Maximum threshold for the ask price, representing the highest ask in the range."
                    },
                    "bid_size": {
                        "type": "number",
                        "description": "Bid size indicates the quantity of options that buyers are willing to purchase at the bid price, reflecting market demand at that price level."
                    },
                    "bid_size_min": {
                        "type": "number",
                        "description": "Minimum threshold for bid size, showing the lowest quantity of options buyers are willing to purchase."
                    },
                    "bid_size_max": {
                        "type": "number",
                        "description": "Maximum threshold for bid size, showing the highest quantity of options buyers are willing to purchase."
                    },
                    "ask_size": {
                        "type": "number",
                        "description": "Ask size represents the quantity of options that sellers are ready to sell at the ask price, indicating market supply at that price level."
                    },
                    "ask_size_min": {
                        "type": "number",
                        "description": "Minimum threshold for ask size, indicating the lowest quantity of options sellers are willing to sell."
                    },
                    "ask_size_max": {
                        "type": "number",
                        "description": "Maximum threshold for ask size, indicating the highest quantity of options sellers are willing to sell."
                    },

                    "mid": {
                        "type": "number",
                        "description": "The mid price, or midpoint, is calculated as the average of the bid and ask prices, providing a reference point for the current market price of an option."
                    },
                    "mid_min": {
                        "type": "number",
                        "description": "Minimum threshold for the mid price, representing the lower boundary of the average market price."
                    },
                    "mid_max": {
                        "type": "number",
                        "description": "Maximum threshold for the mid price, representing the upper boundary of the average market price."
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

                    "intrinsic_value": {
                        "type": "number",
                        "description": "Intrinsic value is the inherent worth of an option, calculated as the difference between the underlying asset's price and the strike price."
                    },
                    "intrinsic_value_min": {
                        "type": "number",
                        "description": "Minimum threshold for intrinsic value, indicating the lower bound of the option's inherent worth."
                    },
                    "intrinsic_value_max": {
                        "type": "number",
                        "description": "Maximum threshold for intrinsic value, indicating the upper bound of the option's inherent worth."
                    },

                    "extrinsic_value": {
                        "type": "number",
                        "description": "Extrinsic value represents the time value of an option, encompassing factors like time to expiry and volatility."
                    },
                    "extrinsic_value_min": {
                        "type": "number",
                        "description": "Minimum threshold for extrinsic value, indicating the lower time value of the option."
                    },
                    "extrinsic_value_max": {
                        "type": "number",
                        "description": "Maximum threshold for extrinsic value, indicating the higher time value of the option."
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
                    }










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
    query = f"SELECT ticker, strike, call_put, expiry, theta FROM public.opts WHERE "
    params = []
    param_index = 1

    # Mapping kwargs to database columns and expected types, including range filters
    column_types = {
        
        'high_min': ('high', 'float'),
        'high_max': ('high', 'float'),
        'high': ('high', 'float'),
        'low': ('low', 'float'),
        'low_min': ('low', 'float'),
        'low_max': ('low', 'float'),
        'strike': ('strike', 'int'),
        'strike_price_min': ('strike_price', 'int'),
        'strike_price_max': ('strike_price', 'int'),
        'oi': ('oi', 'float'),
        'oi_min': ('oi', 'float'),
        'oi_max': ('oi', 'float'),
        'vol_min': ('vol', 'float'),
        'vol_max': ('vol', 'float'),
        'vol': ('vol', 'float'),
        'delta': ('delta', 'float'),
        'delta_min': ('delta', 'float'),
        'delta_max': ('delta', 'float'),
        'vega': ('vega', 'float'),
        'vega_min': ('vega', 'float'),
        'vega_max': ('vega', 'float'),
        'iv_min': ('iv', 'float'),
        'iv_max': ('iv', 'float'),
        'iv': ('iv', 'float'),
        'ask': ('ask', 'float'),
        'ask_min': ('ask', 'float'),
        'ask_max': ('ask', 'float'),
        'bid': ('bid', 'float'),
        'bid_min': ('bid', 'float'),
        'bid_max': ('bid', 'float'),
        'mid': ('mid', 'float'),
        'mid_min': ('mid', 'float'),
        'mid_max': ('mid','float'),
        'gamma': ('gamma', 'float'),
        'gamma_min': ('gamma', 'float'),
        'gamma_max': ('gamma', 'float'),
        'theta': ('theta', 'max'),
        'theta_min': ('theta', 'float'),
        'theta_max': ('theta', 'float'),
        'theta_decay_rate': ('theta_decay_rate', 'float'),
        'theta_decay_rate_min': ('theta_decay_rate_min', 'float'),
        'theta_decaya_rate_max': ('theta_decay_rate_max', 'float'),
        'theta': ('theta', 'float'),
        'close': ('close', 'float'),
        'close_min': ('close', 'float'),
        'close_max': ('close', 'float'),
        'expiry_max': ('expiry', 'date'),
        'expiry': ('expiry', 'date'),
        'expiry_min': ('expiry', 'date'),
        'call_put': ('call_put', 'str'),
        'option_symbol': ('option_symbol', 'str'),
        'ticker': ('ticker', 'str'),
        'underlying_price_min': ('underlying_price', 'float'),
        'underlying_price_max': ('underlying_price', 'float'),
        'underlying_price': ('underlying_price', 'float'),
        'spread': ('spread', 'float'),
        'spread_min': ('spread', 'float'),
        'spread_max': ('spread', 'float'),
        'velocity': ('velocity', 'float'),
        'velocity_min': ('velocity_min', 'float'),
        'velocity_max': ('velocity_max', 'float'),
        'sensitivity': ('sensitivity', 'float'),
        'sensitivity_min': ('sensitivity', 'float'),
        'sensitivity_max': ('sensitivity', 'float'),
        'opp': ('opp', 'float'),
        'opp_min': ('opp', 'float'),
        'opp_max': ('opp', 'float'),
        'intrinsic_value': ('intrinsic_value', 'float'),
        'intrinsic_value_min': ('intrinsic_value', 'float'),
        'intrinsic_value_max': ('intrinsic_value', 'float'),
        'extrinsic_value': ('extrinsic_value', 'float'),
        'extrinsic_value_min': ('extrinsic_value', 'float'),
        'extrinsic_value_max': ('extrinsic_value', 'float'),
        'volume_oi_ratio': ('volume_oi_ratio', 'float'),
        'volume_oi_ratio_min': ('volume_oi_ratio', 'float'),
        'volume_oi_ratio_max': ('volume_oi_ratio', 'float'),

        'oi_change_impact': ('oi_change_impact', 'float'),
        'oi_change_impact_min': ('oi_change_impact', 'float'),
        'oi_change_impact_max': ('oi_change_impact', 'float'),

        'liquidity_volume_ratio': ('liquidity_volume_ratio', 'float'),
        'liquidity_volume_ratio_min': ('liquidity_volume_ratio', 'float'),
        'liquidity_volume_ratio_max': ('liquidity_volume_ratio', 'float'),
        'volatility_score': ('volatility_score', 'float'),
        'volatility_score_min': ('volatility_score', 'float'),
        'volatility_score_max': ('volatility_score', 'float'),
        'volatility_risk_premium': ('volatility_risk_premium', 'float'),
        'volatility_risk_premium_min': ('volatility_risk_premium', 'float'),
        'volatility_risk_premium_max': ('volatility_risk_premium', 'float'),
        'dte': ('dte', 'number'),
        'dte_min': ('dte', 'number'),
        'dte_max': ('dte', 'number'),

        'sentiment_index': ('sentiment_index', 'float'),
        'sentiment_index_min': ('sentiment_index', 'float'),
        'sentiment_index_max': ('sentiment_index', 'float'),

        'depth_volatility_ratio': ('depth_volatility_ratio', 'float'),
        'depth_volatility_ratio_min': ('depth_volatility_ratio', 'float'),
        'depth_volatility_ratio_max': ('depth_volatility_ratio', 'float'),

        'price_stability_index': ('price_stability_index', 'float'),
        'price_stability_index_min': ('price_stability_index', 'float'),
        'price_stability_index_max': ('price_stability_index', 'float'),

        'liquidity_oi_ratio': ('liquidity_oi_ratio', 'float'),
        'liquidity_oi_ratio_min': ('liquidity_oi_ratio', 'float'),
        'liquidity_oi_ratio_max': ('liquidity_oi_ratio', 'float'),

        'theta_vega_ratio': ('theta_vega_ratio', 'float'),
        'theta_vega_ratio_min': ('theta_vega_ratio', 'float'),
        'theta_vega_ratio_max': ('theta_vega_ratio', 'float'),

        'delta_weighted_time_value': ('delta_weighted_time_value', 'float'),
        'delta_weighted_time_value_min': ('delta_weighted_time_value', 'float'),
        'delta_weighted_time_value_max': ('delta_weighted_time_value', 'float'),

        'hedge_effectiveness': ('hedge_effectiveness', 'float'),
        'hedge_effectiveness_min': ('hedge_effectiveness', 'float'),
        'hedge_effectiveness_max': ('hedge_effectiveness', 'float'),

    }

    # Dynamically build query based on kwargs
    query = "SELECT ticker, strike, call_put, expiry FROM public.opts WHERE oi > 0"

    # Dynamically build query based on kwargs
    for key, value in kwargs.items():
        if key in column_types and value is not None:
            column, col_type = column_types[key]

            # Sanitize and format value for SQL query
            sanitized_value = sdk2.sanitize_value(value, col_type)

            if 'min' in key:
                query += f" AND {column} >= {sanitized_value}"
            elif 'max' in key:
                query += f" AND {column} <= {sanitized_value}"
            else:
                query += f" AND {column} = {sanitized_value}"
            print(query)
    query += " LIMIT 25"
    conn = await sdk2.connect()

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


