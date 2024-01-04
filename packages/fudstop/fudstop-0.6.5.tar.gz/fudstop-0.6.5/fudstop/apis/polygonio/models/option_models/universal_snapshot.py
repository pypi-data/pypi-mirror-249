import pandas as pd
from datetime import datetime, timedelta
import asyncpg
from asyncpg import pool
import asyncio
from apis.polygonio.mapping import option_condition_desc_dict,OPTIONS_EXCHANGES
indices_list = ["SPX", "SPXW", "NDX", "VIX", "VVIX"]



class UniversalSnapshot:
    def __init__(self, results):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        self.break_even_price = [i.get('session.break_even_price') for i in results]
        self.change = [i.get('session.change', None) for i in results]
        self.change_percent = [i.get('session.change_percent') for i in results]
        self.early_trading_change = [i.get('session.early_trading_change') for i in results]
        self.early_trading_change_percent = [i.get('session.early_trading_change_percent') for i in results]
        self.close = [i.get('session.close') for i in results]
        self.high = [i.get('session.high') for i in results]
        self.low = [i.get('session.low') for i in results]
        self.open = [i.get('session.open') for i in results]
        self.volume =[i.get('session.volume') for i in results]
        print(self.volume)
        self.prev_close = [i.get('session.previous_close') for i in results]


        self.strike = [i.get('details.strike_price') for i in results]
        self.expiry = [i.get('details.expiration_date') for i in results]
        self.contract_type = [i.get('details.contract_type') for i in results]
        self.exercise_style = [i.get('details.exercise_style') for i in results]
        self.ticker = [i.get('details.ticker') for i in results]

  
        self.theta_values = [i.get('greeks.theta') for i in results]
        self.gamma_values = [i.get('greeks.gamma') for i in results]
        self.vega_values = [i.get('greeks.vega') for i in results]
        self.delta_values = [i.get('greeks.delta') for i in results]

        
        self.implied_volatility = [i.get('implied_volatility') for i in results]
        self.open_interest = [i.get('open_interest') for i in results]

        #last_trade = [i.get('last_trade') for i in results]
        self.sip_timestamp = [i.get('last_trade.timestamp') for i in results]
        self.conditions = [i.get('last_trade.conditions') for i in results]
        self.trade_price = [i.get('last_trade.price') for i in results]
        self.trade_size = [i.get('last_trade.size') for i in results]
        self.exchange = [i.get('last_trade.exchange') for i in results]

    
        self.ask_prices = [i.get('last_quote.ask') for i in results]
        self.bid_prices = [i.get('last_qute.bid') for i in results]
        self.bid_sizes = [i.get('last_quote.bid_size') for i in results]
        self.ask_sizes = [i.get('last_quote.ask_size') for i in results]
        self.midpoints = [i.get('last_quote.midpoint') for i in results]

        self.name = [i.get('name') for i in results]
        self.market_status = [i.get('market_status') for i in results]
        self.ticker = [i.get('ticker') for i in results]
        self.type = [i.get('type') for i in results]


        self.change_to_breakeven = [i.get('underlying_asset.change_to_break_even') for i in results]
        self.underlying_ticker = [i.get('underlying_asset.ticker') for i in results]
        if self.underlying_ticker in indices_list:
            self.underlying_price = [i.get('underlying_asset.value') for i in results]
        else:
            self.underlying_price = [i.get('underlying_asset.price') for i in results]


        # expiry_series = pd.Series(self.expiry)
        # expiry_series = pd.to_datetime(expiry_series)
        # today = pd.Timestamp(datetime.today())
        # self.days_to_expiry = (expiry_series - today).dt.days
        # self.time_value = [p - s + k if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        # self.moneyness = [
        #     'Unknown' if u is None else (
        #         'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
        #             'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
        #         )
        #     ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        # ]


        self.data_dict = {
            
            'Change %': self.change_percent,
            'Close': self.close,
            'High': self.high,
            'Low': self.low,
            'Open': self.open,
            'Vol': self.volume,
            'Prev Close': self.prev_close,
            "call_put": self.contract_type,
            'Style': self.exercise_style,
            'Exp': self.expiry,
            'Skew': self.strike,
            'Strike': self.strike,
            'Delta': self.delta,
            'Gamma': self.gamma,
            'Theta': self.theta,
            'Vega': self.vega,
            'IV': self.implied_volatility,
            'Ask': self.ask,
            'Ask Size': self.ask_size,
            'Bid': self.bid,
            'Bid Size': self.bid_size,
            'Mid': self.midpoint,
            'Timestamp': self.sip_timestamp,
            'Conditions': self.conditions,
            'Trade Price': self.trade_price,
            'Size': self.trade_size,
            'Exchange': self.exchange,
            'OI': self.open_interest,
            'Price': self.underlying_price,
            'Sym': self.underlying_ticker,
            'Name': self.name,
            'Ticker': self.ticker,
            'Types': self.type,
        }
        self.database_data_dict = {
            'days_to_expiry': self.days_to_expiry,
            'moneyness': self.moneyness,
            'time_value': self.time_value,
            'break_even_price': self.break_even_price,
            'change_percent': self.change_percent,
            'early_trading_change': self.early_trading_change,
            'early_trading_change_percent': self.early_trading_change_percent,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'open': self.open,
            'volume': self.volume,
            'prev_close': self.prev_close,
            "call_put": self.contract_type,
            'style': self.exercise_style,
            'expiry': self.expiry,
            'strike': self.strike,  # Keep this line and remove the 'Skew' entry
            'delta': self.delta,
            'gamma': self.gamma,
            'theta': self.theta,
            'vega': self.vega,
            'iv': self.implied_volatility,
            'ask': self.ask,
            'ask_size': self.ask_size,
            'bid': self.bid,
            'bid_size': self.bid_size,
            'mid': self.midpoint,
            'timestamp': self.sip_timestamp,
            'conditions': self.conditions,
            'trade_price': self.trade_price,
            'trade_size': self.trade_size,
            'trade_exchange': self.exchange,
            'oi': self.open_interest,
            'underlying_price': self.underlying_price,
            'underlying_symbol': self.underlying_ticker,
            'change_to_break_even': self.change_to_breakeven,
            'change': self.change,
            'name': self.name,
            'ticker': self.ticker,
        }


        self.skew_dict = { 
            "call_put": self.contract_type,
            'iv': self.implied_volatility,
            'exp': self.expiry,
            'vol': self.volume,
            'oi': self.open_interest,
            'strike': self.strike,
}
        self.df = pd.DataFrame(self.data_dict)

        self.skew_df = pd.DataFrame(self.skew_dict)

    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value
    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration
class UniversalOptionSnapshot:
    def __init__(self, results):


        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]

        day = [i['day'] if 'day' in i else None for i in results]
        self.volume = [float(i['volume']) if 'volume' in i  else None for i in day]
        self.high = [float(i['high']) if 'high' in i else None for i in day]
        self.low = [float(i['low']) if 'low' in i else None for i in day]
        self.vwap = [float(i['vwap']) if 'vwap' in i else None for i in day]
        self.open = [float(i['open']) if 'open' in i else None for i in day]
        self.close = [float(i['close']) if 'close' in i else None for i in day]
        self.change_percent = [(float(c) - float(o)) / float(o) * 100.0 if o is not None and c is not None and o != 0 else None for o, c in zip(self.open, self.close)]
        self.change_percent = [round(item, 3) if item is not None else None for item in self.change_percent]




        details = [i['details'] for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

        greeks = [i['greeks'] if i['greeks'] is not None else None for i in results]
        self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
        self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
        self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
        self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]
        self.exchange = [OPTIONS_EXCHANGES.get(i) for i in self.exchange]

        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]

        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
        today = pd.Timestamp(datetime.today())
        
        
        self.days_to_expiry = (expiry_series - today).dt.days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
        self.option_velocity =[round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]
        #option_sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]
        #liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]
        #risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]
        #greeks-balance score - curated - finished
        self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]
        #options profit potential: FINAL - finished
        self.opp = [moneyness_score*oss*ltr*rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]



                        

        self.volatility_score = [(float(h) - float(l)) / float(o) if o is not None and h is not None and l is not None and o != 0 else None for h, l, o in zip(self.high, self.low, self.open)]
        self.volatility_score = [round(item, 3) if item is not None else None for item in self.volatility_score]


        self.implied_leverage = [float(d) / float(p) if d is not None and p is not None and p != 0 else None for d, p in zip(self.delta, self.trade_price)]
        self.implied_leverage = [round(item, 3) if item is not None else None for item in self.implied_leverage]
        self.risk_exposure = [abs(float(g)) + abs(float(t)) if g is not None and t is not None else None for g, t in zip(self.gamma_risk, self.theta_decay_rate)]
        self.risk_exposure = [round(item, 3) if item is not None else None for item in self.risk_exposure]

        self.price_movement_efficiency = [(float(p) - float(u)) / abs(float(u) - float(ul)) if p is not None and u is not None and ul is not None and ul != u else None for p, u, ul in zip(self.trade_price, self.underlying_price, [self.underlying_price[i - 1] if i > 0 else None for i in range(len(self.underlying_price))])]
        self.price_movement_efficiency = [round(item, 3) if item is not None else None for item in self.price_movement_efficiency]


        self.time_value_premium_ratio = [float(tv) / float(p) if tv is not None and p is not None and p != 0 else None for tv, p in zip(self.time_value, self.trade_price)]
        self.time_value_premium_ratio = [round(item, 3) if item is not None else None for item in self.time_value_premium_ratio]







        self.delta_adjusted_liquidity = [float(l) * abs(float(d)) if l is not None and d is not None else None for l, d in zip(self.liquidity_indicator, self.delta)]
        self.delta_adjusted_liquidity = [round(item, 3) if item is not None else None for item in self.delta_adjusted_liquidity]


        self.hedging_effectiveness = [abs(float(d)) + abs(float(g)) if d is not None and g is not None else None for d, g in zip(self.delta, self.gamma)]
        self.hedging_effectiveness = [round(item, 3) if item is not None else None for item in self.hedging_effectiveness]

        self.normalized_theta_vega_ratio = [abs(float(t)) / float(v) / float(p) if t is not None and v is not None and p is not None and v != 0 else None for t, v, p in zip(self.theta, self.vega, self.trade_price)]
        self.normalized_theta_vega_ratio = [round(item, 3) if item is not None else None for item in self.normalized_theta_vega_ratio]
        self.depth_volatility_ratio = [float(ts) / float(vol) if ts is not None and vol is not None and vol != 0 else None for ts, vol in zip(self.trade_size, self.volatility_score)]
        self.depth_volatility_ratio = [round(item, 3) if item is not None else None for item in self.depth_volatility_ratio]
        self.price_stability_index = [1 / (float(sp) * float(vol)) if sp is not None and vol is not None and sp * vol != 0 else None for sp, vol in zip(self.spread_pct, self.volume)]
        self.price_stability_index = [round(item, 3) if item is not None else None for item in self.price_stability_index]
        self.liquidity_oi_ratio = [float(liq) / float(oi) if liq is not None and oi is not None and oi != 0 else None for liq, oi in zip(self.liquidity_indicator, self.open_interest)]
        self.liquidity_oi_ratio = [round(item, 3) if item is not None else None for item in self.liquidity_oi_ratio]
        self.vol_oi_ratio = [float(vol) / float(oi) if vol is not None and oi is not None and oi != 0 else None for vol, oi in zip(self.volume, self.open_interest)]
        self.vol_oi_ratio = [round(item, 3) if item is not None else None for item in self.vol_oi_ratio]


        self.liquidity_volume_ratio = [float(liq) / float(vol) if liq is not None and vol is not None and vol != 0 else None for liq, vol in zip(self.liquidity_indicator, self.volume)]
        self.liquidity_volume_ratio = [round(item, 3) if item is not None else None for item in self.liquidity_volume_ratio]

        self.delta_weighted_time_value = [float(tv) * abs(float(d)) if tv is not None and d is not None else None for tv, d in zip(self.time_value, self.delta)]
        self.delta_weighted_time_value = [round(item, 3) if item is not None else None for item in self.delta_weighted_time_value]



        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'dte': self.days_to_expiry,
            'time_value': self.time_value,
            'moneyness': self.moneyness,
            'liquidity_score': self.liquidity_indicator,
            "call_put": self.contract_type,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'time_value_premium_ratio': self.time_value_premium_ratio,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'delta_adjusted_liquidity': self.delta_adjusted_liquidity,
            'delta_weighted_time_value': self.delta_weighted_time_value,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'theta_vega_ratio': self.normalized_theta_vega_ratio,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'liquidity_oi_ratio': self.liquidity_oi_ratio,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'intrinstic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'leverage_ratio': self.leverage_ratio,
            'vwap':self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'iv': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'vol_oi_ratio': self.vol_oi_ratio,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
            'return_on_risk': self.return_on_risk,
            'velocity': self.option_velocity,
            'sensitivity': self.oss,
            'greeks_balance': self.gbs,
            'opp': self.opp,
            'change_percent': self.change_percent,
            'volatility_score': self.volatility_score,
            'implied_leverage': self.implied_leverage,
            'risk_exposure': self.risk_exposure,

            'hedge_effectiveness': self.hedging_effectiveness,
            'depth_volatility_ratio': self.depth_volatility_ratio,
            'price_stability': self.price_stability_index,


            
        }


        # Create DataFrame from data_dict
        self.df = pd.DataFrame(self.data_dict)

    async def calculate_oi_change(self, pool):
        today = datetime.today().date()
        previous_day = today - timedelta(days=1)

        async with pool.acquire() as connection:
            # Fetch historical open interest data
            query = """
            SELECT option_symbol, open_interest, date
            FROM historical_table
            WHERE date = $1 OR date = $2
            """
            historical_data = await connection.fetch(query, previous_day, today)

        # Convert historical_data to a DataFrame
        df = pd.DataFrame(historical_data, columns=['option_symbol', 'open_interest', 'date'])
        df['open_interest'] = df['open_interest'].astype(float)

        # Pivot the DataFrame to get a column for each date's open interest
        pivot_df = df.pivot(index='option_symbol', columns='date', values='open_interest')

        # Ensure the DataFrame has both dates and fill missing values with 0
        pivot_df = pivot_df.reindex(columns=[previous_day, today], fill_value=0)

        # Calculate the change in open interest
        pivot_df['oi_change'] = pivot_df[today] - pivot_df[previous_day]

        # Reset index to convert 'option_symbol' back to a column
        pivot_df.reset_index(inplace=True)

        # Extract the relevant columns (option_symbol and oi_change)
        oi_change_df = pivot_df[['option_symbol', 'oi_change']]

        # Convert the DataFrame to a dictionary or another suitable format for your class
        oi_change = oi_change_df.to_dict('records')

        return oi_change
    def __repr__(self) -> str:
        return f"UniversalOptionSnapshot(break_even={self.break_even}, \
                implied_volatility={self.implied_volatility},\
                open_interest ={self.open_interest}, \
                change={self.exchange}, \
                expiry={self.expiry}, \
                ticker={self.ticker} \
                contract_type={self.contract_type}, \
                exercise_style={self.exercise_style}, \
                theta={self.theta}, \
                delta={self.delta}, \
                gamma={self.gamma}, \
                vega={self.vega}, \
                sip_timestamp={self.sip_timestamp}, \
                conditions={self.conditions}, \
                trade_price={self.trade_price}, \
                trade_size={self.trade_size}, \
                exchange={self.exchange}, \
                ask={self.ask}, \
                bid={self.bid}, \
                bid_size={self.bid_size}, \
                ask_size={self.ask_size}, \
                midpoint={self.midpoint}, \
                change_to_breakeven={self.change_to_breakeven}, \
                underlying_price={self.underlying_price}, \
                underlying_ticker={self.underlying_ticker})"
    
    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value
    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration

class CallsOrPuts:
    def __init__(self, data):
        self.cfi = [i['cfi'] if 'cfi' in i else None for i in data]
        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in data]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in data]
        self.expiration_date = [i['expiration_date'] if 'expiration_date' in i else None for i in data]
        self.primary_exchange = [i['primary_exchange'] if 'primary_exchange' in i else None for i in data]
        self.shares_per_contract = [i['shares_per_contract'] if 'shares_per_contract' in i else None for i in data]
        self.strike_price = [i['strike_price'] if 'strike_price' in i else None for i in data]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in data]
        self.underlying_ticker = [i['underlying_ticker'] if 'underlying_ticker' in i else None for i in data]


        self.data_dict = { 
            'ticker': self.ticker,
            'strike': self.strike_price,
            'expiry': self.expiration_date

        }


        self.df = pd.DataFrame(self.data_dict).sort_values(by='expiry')

class MultipleUniversalOptionSnapshot:
    def __init__(self, results):
        self.break_even = results.get('break_even_price', None)
     
        self.implied_volatility = results.get('implied_volatility', None)
        self.open_interest = results.get('open_interest', None)

        day = results.get('day', None)
        self.volume = day.get('volume', None)
        self.high = day.get('high', None)
        self.low = day.get('low', None)
        self.vwap = day.get('vwap', None)
        self.open = day.get('open', None)
        self.close = day.get('close', None)




        details = results.get('details', None)
        self.strike = details.get('strike_price', None)
        self.expiry =  details.get('expiration_date', None)
        self.contract_type =  details.get('contract_type', None)
        self.exercise_style =  details.get('exercise_style', None)
        self.ticker =  details.get('ticker', None)

        greeks = results.get('greeks', None)
        self.theta = greeks.get('theta', None)
        self.delta = greeks.get('delta', None)
        self.gamma = greeks.get('gamma', None)
        self.vega = greeks.get('vega', None)


        last_trade = results.get('last_trade', None)
        self.sip_timestamp = last_trade.get('sip_timestamp', None)
        self.conditions = last_trade.get('conditions', None)
        self.trade_price = last_trade.get('price', None)
        self.trade_size = last_trade.get('size', None)
        self.exchange = last_trade.get('exchange', None)

        last_quote = results.get('last_quote', None)
        self.ask = last_quote.get('ask', None)
        self.bid = last_quote.get('bid', None)
        self.bid_size = last_quote.get('bid_size', None)
        self.ask_size = last_quote.get('ask_size', None)
        self.midpoint = last_quote.get('midpoint', None)


        underlying_asset = results.get('underlying_asset', None)
        self.change_to_breakeven = underlying_asset.get('change_to_breakeven', None)
        self.underlying_price = underlying_asset.get('underlying_price', None)
        self.underlying_ticker = underlying_asset.get('underlying_ticker', None)

        self.data_dict = {
            'strike': self.strike,
            'exp': self.expiry,
            'type': self.contract_type,
            'exercise_style': self.exercise_style,
            'ticker': self.ticker,
            'theta': self.theta,
            'delta': self.delta,
            'gamma': self.gamma,
            'vega': self.vega,
            'sip_timestamp': self.sip_timestamp,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'vwap':self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'Size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'IV': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'entryCost': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'price': self.underlying_price,
            'sym': self.underlying_ticker
        }

        self.df = pd.DataFrame(self.data_dict)
