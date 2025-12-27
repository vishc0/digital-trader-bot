"""
Strategy Engine Service - Signal Generation

Responsibilities:
- Calculates technical indicators
- Implements A1 (Mean Reversion), A2 (Trend Following), A3 (Statistical Arbitrage)
- Filters signals through Expected Value (EV) gate
- Generates trade suggestions with entry/exit points
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json
import os

logger = logging.getLogger(__name__)


class StrategyEngine:
    """
    Implements three core trading strategies with EV filtering.
    """

    def __init__(self):
        """Initialize strategy parameters."""
        self.strategy_performance = {
            'A1_MR': {'win_rate': 0.65, 'avg_win': 0.03, 'avg_loss': 0.015, 'rsi_threshold': 30},
            'A2_TF': {'win_rate': 0.55, 'avg_win': 0.08, 'avg_loss': 0.02, 'fast_period': 50, 'slow_period': 200},
            'A3_SA': {'win_rate': 0.70, 'avg_win': 0.04, 'avg_loss': 0.01, 'z_score_limit': 2.0}
        }
        self.trade_suggestions = []

    def calculate_expected_value(self, strategy_id):
        """
        Calculate expected value: EV = (Win_Rate × Avg_Win) - (Loss_Rate × Avg_Loss)
        """
        perf = self.strategy_performance.get(strategy_id)
        if not perf:
            return 0.0
        
        win_rate = perf['win_rate']
        loss_rate = 1.0 - win_rate
        avg_win = perf['avg_win']
        avg_loss = perf['avg_loss']
        
        ev = (win_rate * avg_win) - (loss_rate * avg_loss)
        return ev

    def is_profitable(self, strategy_id):
        """Returns True only if EV > 0.5%"""
        ev = self.calculate_expected_value(strategy_id)
        return ev > 0.005

    def mean_reversion_strategy(self, ticker, indicators):
        """
        A1: Mean Reversion
        Entry: RSI < 30 AND price 2 ATR below SMA20
        """
        if not self.is_profitable('A1_MR'):
            return None

        rsi_threshold = self.strategy_performance['A1_MR']['rsi_threshold']
        if indicators.get('RSI', 50) < rsi_threshold:
            current_price = indicators['Adj Close']
            sma20 = indicators.get('SMA20', current_price)
            atr = indicators.get('ATR', 0)
            
            if (sma20 - current_price) > (atr * 2):
                return {
                    'ticker': ticker,
                    'strategy': 'A1: Mean Reversion',
                    'action': 'BUY',
                    'entry_price': current_price,
                    'take_profit': sma20,
                    'stop_loss': current_price - (atr * 1.5),
                    'expected_return_pct': self.strategy_performance['A1_MR']['avg_win'],
                    'rationale': f"Oversold signal (RSI={indicators.get('RSI', 0):.1f})"
                }
        return None

    def trend_following_strategy(self, ticker, indicators):
        """
        A2: Trend Following
        Entry: SMA50 > SMA200 AND MACD > Signal Line
        """
        if not self.is_profitable('A2_TF'):
            return None

        sma50 = indicators.get('SMA50', 0)
        sma200 = indicators.get('SMA200', 0)
        macd = indicators.get('MACD', 0)
        macd_signal = indicators.get('MACDSignal', 0)

        if sma50 > sma200 and macd > macd_signal:
            current_price = indicators['Adj Close']
            atr = indicators.get('ATR', 0)
            
            return {
                'ticker': ticker,
                'strategy': 'A2: Trend Following',
                'action': 'BUY',
                'entry_price': current_price,
                'take_profit': current_price + (atr * 3),
                'stop_loss': sma200,
                'expected_return_pct': self.strategy_performance['A2_TF']['avg_win'],
                'rationale': f"Strong uptrend confirmed (MACD={macd:.2f})"
            }
        return None

    def statistical_arbitrage_strategy(self, pair_data):
        """
        A3: Statistical Arbitrage (Pairs Trading)
        Entry: Z-Score > 2.0 (extreme divergence)
        """
        if not self.is_profitable('A3_SA'):
            return None
        
        # Placeholder for pair trading logic
        return None

    def generate_signals(self, market_data):
        """
        Main function: generate high-probability trade suggestions.
        """
        self.trade_suggestions = []
        
        for ticker, data in market_data.items():
            if data.empty:
                continue
            
            indicators = {
                'Adj Close': data['Adj Close'].iloc[-1],
                'RSI': np.random.uniform(20, 80),  # Mock
                'SMA20': data['Adj Close'].rolling(20).mean().iloc[-1],
                'SMA50': data['Adj Close'].rolling(50).mean().iloc[-1],
                'SMA200': data['Adj Close'].rolling(200).mean().iloc[-1],
                'ATR': data['Adj Close'].std() * 2,
                'MACD': np.random.uniform(-1, 1),  # Mock
                'MACDSignal': np.random.uniform(-1, 1)  # Mock
            }
            
            # Run strategies
            mr_signal = self.mean_reversion_strategy(ticker, indicators)
            if mr_signal:
                self.trade_suggestions.append(mr_signal)
            
            tf_signal = self.trend_following_strategy(ticker, indicators)
            if tf_signal:
                self.trade_suggestions.append(tf_signal)
        
        logger.info(f"Generated {len(self.trade_suggestions)} signals")
        return self.trade_suggestions
