from collections import namedtuple
import pandas as pd
# Named tuples for various sections
Details = namedtuple('Details', ['strike', 'expiry', 'contract_type', 'exercise_style', 'ticker'])
Greeks = namedtuple('Greeks', ['theta', 'delta', 'theta_decay_rate', 'vega_impact', 'delta_impact', 'gamma_risk'])
LastTrade = namedtuple('LastTrade', ['timestamp', 'conditions', 'price', 'size', 'exchange'])
LastQuote = namedtuple('LastQuote', ['ask', 'bid', 'midpoint', 'ask_size', 'bid_size'])
MarketStatus = namedtuple('MarketStatus', ['oi', 'volume', 'high', 'low', 'vwap', 'open', 'close', 'change_ratio'])
UnderlyingAsset = namedtuple('UnderlyingAsset', ['change_to_breakeven', 'price', 'ticker'])
OptionAnalytics = namedtuple('OptionAnalytics', ['implied_volatility', 'dte', 'time_value', 'moneyness', 'liquidity_indicator', 'spread', 'intrinsic_value', 'extrinsic_value', 'leverage_ratio', 'spread_pct'])
TradeAnalytics = namedtuple('TradeAnalytics', ['trade_price', 'trade_size', 'ask', 'bid', 'bid_size', 'ask_size', 'midpoint'])
RiskMetrics = namedtuple('RiskMetrics', ['return_on_risk', 'option_velocity', 'gamma_risk', 'theta_decay_rate', 'vega_impact', 'delta_to_theta_ratio'])
ScoringMetrics = namedtuple('ScoringMetrics', ['oss', 'ltr', 'rrs', 'gbs', 'opp', 'volatility_score', 'implied_leverage', 'risk_exposure', 'price_movement_efficiency', 'time_value_premium_ratio'])
LiquidityMetrics = namedtuple('LiquidityMetrics', ['delta_adjusted_liquidity', 'hedging_effectiveness', 'theta_vega_ratio', 'depth_volatility_ratio', 'price_stability_index', 'liquidity_oi_ratio', 'vol_oi_ratio', 'liquidity_volume_ratio', 'delta_weighted_time_value'])



class UniversalOptionSnapshot:
    def __init__(self, results):
        # Initialize lists to store named tuples
        self.details_list = []
        self.greeks_list = []
        self.last_trades_list = []
        self.last_quotes_list = []
        self.market_status_list = []
        self.underlying_assets_list = []
        self.option_analytics_list = []
        self.trade_analytics_list = []
        self.risk_metrics_list = []
        self.scoring_metrics_list = []
        self.liquidity_metrics_list = []

        for item in results:
            # Extract data for Details
            details_item = item.get('details', {})
            self.details_list.append(Details(
                strike=float(details_item.get('strike_price', None)),
                expiry=details_item.get('expiration_date', None),
                contract_type=details_item.get('contract_type', None),
                exercise_style=details_item.get('exercise_style', None),
                ticker=details_item.get('ticker', None)
            ))

            # Extract data for Greeks
            greeks_item = item.get('greeks', {})
            self.greeks_list.append(Greeks(
                theta=greeks_item.get('theta', None),
                delta=greeks_item.get('delta', None),
                theta_decay_rate=greeks_item.get('theta_decay_rate', None),
                vega_impact=greeks_item.get('vega_impact', None),
                delta_impact=greeks_item.get('delta_impact', None),
                gamma_risk=greeks_item.get('gamma_risk', None)
            ))

            # Extract data for LastTrade
            last_trade_item = item.get('last_trade', {})
            self.last_trades_list.append(LastTrade(
                timestamp=last_trade_item.get('timestamp', None),
                conditions=last_trade_item.get('conditions', None),
                price=last_trade_item.get('price', None),
                size=last_trade_item.get('size', None),
                exchange=last_trade_item.get('exchange', None)
            ))
           # Extract data for LastQuote
            last_quote_item = item.get('last_quote', {})
            self.last_quotes_list.append(LastQuote(
                ask=last_quote_item.get('ask', None),
                bid=last_quote_item.get('bid', None),
                midpoint=last_quote_item.get('midpoint', None),
                ask_size=last_quote_item.get('ask_size', None),
                bid_size=last_quote_item.get('bid_size', None)
            ))

            # Extract data for MarketStatus
            market_status_item = item.get('session', {})
            self.market_status_list.append(MarketStatus(
                oi=item.get('open_interest', None),
                volume=market_status_item.get('volume', None),
                high=market_status_item.get('high', None),
                low=market_status_item.get('low', None),
                vwap=market_status_item.get('vwap', None),
                open=market_status_item.get('open', None),
                close=market_status_item.get('close', None),
                change_ratio=market_status_item.get('change_percent', None)
            ))

            # Extract data for UnderlyingAsset
            underlying_asset_item = item.get('underlying_asset', {})
            self.underlying_assets_list.append(UnderlyingAsset(
                change_to_breakeven=underlying_asset_item.get('change_to_break_even', None),
                price=underlying_asset_item.get('price', None),
                ticker=underlying_asset_item.get('ticker', None)
            ))

            # Extract data for OptionAnalytics
            option_analytics_item = item  # Assuming OptionAnalytics data is at the top level of item
            self.option_analytics_list.append(OptionAnalytics(
                implied_volatility=option_analytics_item.get('implied_volatility', None),
                dte=option_analytics_item.get('dte', None),
                time_value=option_analytics_item.get('time_value', None),
                moneyness=option_analytics_item.get('moneyness', None),
                liquidity_indicator=option_analytics_item.get('liquidity_indicator', None),
                spread=option_analytics_item.get('spread', None),
                intrinsic_value=option_analytics_item.get('intrinsic_value', None),
                extrinsic_value=option_analytics_item.get('extrinsic_value', None),
                leverage_ratio=option_analytics_item.get('leverage_ratio', None),
                spread_pct=option_analytics_item.get('spread_pct', None)
            ))

            # Extract data for TradeAnalytics
            trade_analytics_item = item  # Assuming TradeAnalytics data is at the top level of item
            self.trade_analytics_list.append(TradeAnalytics(
                trade_price=trade_analytics_item.get('trade_price', None),
                trade_size=trade_analytics_item.get('trade_size', None),
                ask=trade_analytics_item.get('ask', None),
                bid=trade_analytics_item.get('bid', None),
                bid_size=trade_analytics_item.get('bid_size', None),
                ask_size=trade_analytics_item.get('ask_size', None),
                midpoint=trade_analytics_item.get('midpoint', None)
            ))

            # Extract data for RiskMetrics
            risk_metrics_item = item  # Assuming RiskMetrics data is at the top level of item
            self.risk_metrics_list.append(RiskMetrics(
                return_on_risk=risk_metrics_item.get('return_on_risk', None),
                option_velocity=risk_metrics_item.get('option_velocity', None),
                gamma_risk=risk_metrics_item.get('gamma_risk', None),
                theta_decay_rate=risk_metrics_item.get('theta_decay_rate', None),
                vega_impact=risk_metrics_item.get('vega_impact', None),
                delta_to_theta_ratio=risk_metrics_item.get('delta_to_theta_ratio', None)
            ))

            # Extract data for ScoringMetrics
            scoring_metrics_item = item  # Assuming ScoringMetrics data is at the top level of item
            self.scoring_metrics_list.append(ScoringMetrics(
                oss=scoring_metrics_item.get('oss', None),
                ltr=scoring_metrics_item.get('ltr', None),
                rrs=scoring_metrics_item.get('rrs', None),
                gbs=scoring_metrics_item.get('gbs', None),
                opp=scoring_metrics_item.get('opp', None),
                volatility_score=scoring_metrics_item.get('volatility_score', None),
                implied_leverage=scoring_metrics_item.get('implied_leverage', None),
                risk_exposure=scoring_metrics_item.get('risk_exposure', None),
                price_movement_efficiency=scoring_metrics_item.get('price_movement_efficiency', None),
                time_value_premium_ratio=scoring_metrics_item.get('time_value_premium_ratio', None)
            ))

            # Extract data for LiquidityMetrics
            liquidity_metrics_item = item  # Assuming LiquidityMetrics data is at the top level of item
            self.liquidity_metrics_list.append(LiquidityMetrics(
                delta_adjusted_liquidity=liquidity_metrics_item.get('delta_adjusted_liquidity', None),
                hedging_effectiveness=liquidity_metrics_item.get('hedging_effectiveness', None),
                theta_vega_ratio=liquidity_metrics_item.get('theta_vega_ratio', None),
                depth_volatility_ratio=liquidity_metrics_item.get('depth_volatility_ratio', None),
                price_stability_index=liquidity_metrics_item.get('price_stability_index', None),
                liquidity_oi_ratio=liquidity_metrics_item.get('liquidity_oi_ratio', None),
                vol_oi_ratio=liquidity_metrics_item.get('vol_oi_ratio', None),
                liquidity_volume_ratio=liquidity_metrics_item.get('liquidity_volume_ratio', None),
                delta_weighted_time_value=liquidity_metrics_item.get('delta_weighted_time_value', None)
            ))


    def create_dataframe(self):
        # Combine all named tuples into a single DataFrame
        data = {
            'Details': self.details_list,
            'Greeks': self.greeks_list,
            'LastTrade': self.last_trades_list,
            'LastQuote': self.last_quotes_list,
            'MarketStatus': self.market_status_list,
            'UnderlyingAsset': self.underlying_assets_list,
            'OptionAnalytics': self.option_analytics_list,
            'TradeAnalytics': self.trade_analytics_list,
            'RiskMetrics': self.risk_metrics_list,
            'ScoringMetrics': self.scoring_metrics_list,
            'LiquidityMetrics': self.liquidity_metrics_list
        }

        # Create a DataFrame from the data
        self.dataframe = pd.DataFrame(data)



import asyncio
async def main():
    # Usage example
    results = []  # Assuming this is your input data
    snapshot = UniversalOptionSnapshot(results)
    snapshot.create_dataframe()