import pandas as pd
import numpy as np
from datetime import datetime
import talib # Technical Analysis library (standard in quant finance)
import random # Used for mock confidence scores
from scipy import stats

# Placeholder class for integration (assume DataHandler is running as a separate service)
class MockDataHandler:
    def get_current_data_snapshot(self):
        """Generates a mock data snapshot for the Strategy Engine to process."""
        data = {}
        assets = ['AAPL', 'MSFT', 'GOOGL', 'BABA', 'JD']
        date_range = pd.date_range(end=datetime.now(), periods=252, freq='B') 
        
        for ticker in assets:
            np.random.seed(hash(ticker) % 4294967295)
            # Create price series with a simulated mild trend or mean reversion tendency
            base_price = 100 + random.randint(10, 100)
            prices = base_price * (1 + np.cumsum(np.random.normal(0.0001, 0.005, size=len(date_range))))
            
            df = pd.DataFrame({
                'Adj Close': prices,
                'Volume': np.random.randint(500000, 5000000, size=len(date_range))
            }, index=date_range)
            
            data[ticker] = df.sort_index()
        
        # Inject a current signal for one ticker (e.g., AAPL is oversold)
        data['AAPL']['Adj Close'].iloc[-1] = data['AAPL']['Adj Close'].iloc[-1] * 0.95
        return data

# --- Core Service Class ---

class StrategyEngine:
    """
    The Strategy Engine Service (SES).
    
    Responsibilities include:
    1. Running multiple trading strategies (A1, A2, A3).
    2. Calculating technical indicators (TA-Lib).
    3. Filtering signals based on Expected Value (EV) and Risk.
    4. Implementing the Wisdom Builder's Nightly Review/Learning process.
    """

    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.strategies = {
            'A1_MR': self._mean_reversion_strategy,
            'A2_TF': self._trend_following_strategy,
            'A3_SA': self._statistical_arbitrage_strategy # Placeholder for actual pair data
        }
        # Mock historical performance metrics for EV calculation (Wisdom Builder memory)
        self.strategy_performance = {
            'A1_MR': {'win_rate': 0.65, 'avg_win': 0.03, 'avg_loss': 0.015, 'volatility_threshold': 2.0},
            'A2_TF': {'win_rate': 0.35, 'avg_win': 0.08, 'avg_loss': 0.02, 'fast_period': 50, 'slow_period': 200},
            'A3_SA': {'win_rate': 0.70, 'avg_win': 0.04, 'avg_loss': 0.01, 'z_score_limit': 2.0}
        }
        self.trade_suggestions = []


    # --- Wisdom Builder: Expected Value Filter (Strict Profit Mandate) ---
    
    def calculate_expected_value(self, strategy_id):
        """
        Calculates the expected profit/loss (EV) based on historical memory.
        EV = (Win Rate * Avg Win) - (Loss Rate * Avg Loss)
        """
        perf = self.strategy_performance.get(strategy_id)
        if not perf:
            return 0.0
            
        win_rate = perf['win_rate']
        loss_rate = 1.0 - win_rate
        avg_win = perf['avg_win']
        avg_loss = perf['avg_loss']
        
        expected_value = (win_rate * avg_win) - (loss_rate * avg_loss)
        return expected_value

    def _is_profitable(self, strategy_id):
        """Returns True only if EV > 0, enforcing the 'never losses' principle."""
        ev = self.calculate_expected_value(strategy_id)
        return ev > 0.005 # Require a slight margin above zero for resilience

    # --- Technical Analysis Functions ---
    
    def _calculate_indicators(self, data):
        """Calculate common indicators used across strategies."""
        close = data['Adj Close'].values
        # A. Mean Reversion Indicators
        data['RSI'] = talib.RSI(close, timeperiod=14)
        data['SMA20'] = talib.SMA(close, timeperiod=20)
        data['ATR'] = talib.ATR(data['High'].values, data['Low'].values, close, timeperiod=14)
        data['BB_StdDev'] = talib.STDDEV(close, timeperiod=20, nbdev=1)

        # B. Trend Following Indicators
        data['SMA50'] = talib.SMA(close, timeperiod=self.strategy_performance['A2_TF']['fast_period'])
        data['SMA200'] = talib.SMA(close, timeperiod=self.strategy_performance['A2_TF']['slow_period'])
        data['MACD'], data['MACDSignal'], _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        return data.iloc[-1] # Return latest indicator values

    # --- Strategy Implementations (A1, A2, A3) ---

    def _mean_reversion_strategy(self, ticker, indicators):
        """
        A1: Mean Reversion - Oversold/Overbought Signals.
        Entry: RSI < 30 AND price is 2 ATR away from SMA20.
        """
        if not self._is_profitable('A1_MR'):
            return None # Skip strategy if EV is negative

        # Entry Condition 1: Oversold (RSI < 30)
        is_oversold = indicators['RSI'] < 30 
        
        # Entry Condition 2 (Confirmation/Magnitude): Price deviation (2 ATR) from mean (SMA20)
        current_price = indicators['Adj Close']
        sma20 = indicators['SMA20']
        atr_distance = indicators['ATR'] * 2
        
        is_significant_deviation = (sma20 - current_price) > atr_distance # Price significantly below SMA

        if is_oversold and is_significant_deviation:
            # Calculate Risk/Reward based on current indicators and learned parameters
            take_profit = indicators['SMA20'] # TP is the mean (SMA20)
            stop_loss = current_price - (indicators['ATR'] * 1.5) # 1.5 ATR Trailing Stop initial
            
            return {
                'ticker': ticker,
                'strategy': 'A1: Mean Reversion',
                'action': 'BUY',
                'entryPrice': current_price,
                'takeProfit': take_profit,
                'stopLoss': stop_loss,
                'expected_return_pct': self.strategy_performance['A1_MR']['avg_win'],
                'rationale': f"Oversold (RSI:{indicators['RSI']:.2f}). Price is {atr_distance:.2f} below SMA20. High EV signal."
            }
        return None

    def _trend_following_strategy(self, ticker, indicators):
        """
        A2: Trend Following - Long-Term Trend Confirmation.
        Entry: SMA50 > SMA200 AND MACD crossing above signal line.
        """
        if not self._is_profitable('A2_TF'):
            return None 
            
        # Entry Condition 1: Long-term trend (Golden/Death Cross proxy)
        is_long_term_uptrend = indicators['SMA50'] > indicators['SMA200']
        
        # Entry Condition 2: Short-term momentum acceleration (MACD crossover)
        is_momentum_positive = indicators['MACD'] > indicators['MACDSignal'] and indicators['MACD'] > 0

        if is_long_term_uptrend and is_momentum_positive:
            current_price = indicators['Adj Close']
            # TP is based on a dynamic 3 ATR target
            take_profit = current_price + (indicators['ATR'] * 3)
            stop_loss = indicators['SMA200'] # Hard stop at the 200-day mean 

            return {
                'ticker': ticker,
                'strategy': 'A2: Trend Following',
                'action': 'BUY',
                'entryPrice': current_price,
                'takeProfit': take_profit,
                'stopLoss': stop_loss,
                'expected_return_pct': self.strategy_performance['A2_TF']['avg_win'],
                'rationale': f"Strong Uptrend (SMA50/200 cross) confirmed by MACD momentum. High EV signal."
            }
        return None

    def _statistical_arbitrage_strategy(self, ticker_pair_data):
        """
        A3: Statistical Arbitrage (Pairs Trading) - Placeholder for Z-Score Logic.
        In a real system, this requires historical co-integration analysis.
        """
        # Placeholder logic: Find a pair, calculate the spread, normalize (Z-score)
        
        # Mock Z-Score Calculation (assuming BABA/JD pair is the target)
        if 'BABA' not in ticker_pair_data or 'JD' not in ticker_pair_data:
            return None

        # Simulate Z-Score calculation based on historical data
        # In a real model, this would be complex regression
        mock_z_score = random.uniform(1.8, 2.8) # Simulate an extreme deviation

        if mock_z_score > self.strategy_performance['A3_SA']['z_score_limit']:
            # Signal: Short the stronger stock (BABA), Long the weaker stock (JD)
            current_baba_price = ticker_pair_data['BABA']['Adj Close'].iloc[-1]
            current_jd_price = ticker_pair_data['JD']['Adj Close'].iloc[-1]

            return {
                'ticker': 'BABA/JD',
                'strategy': 'A3: Statistical Arbitrage',
                'action': 'HEDGE (Short BABA, Long JD)',
                'entryPrice': mock_z_score, # Entry is the Z-Score value
                'takeProfit': 0.0,
                'stopLoss': self.strategy_performance['A3_SA']['z_score_limit'] + 1.0, # Stop at Z-score 3.0
                'expected_return_pct': self.strategy_performance['A3_SA']['avg_win'],
                'rationale': f"Pair Z-score hit {mock_z_score:.2f} (extreme deviation). Betting on spread mean reversion."
            }
        return None

    # --- Options Specialization (Early Quit/Take Profit) ---
    def _options_specialization(self, ticker, signal_data):
        """
        Generates a simplified Options trade structure (e.g., selling a put) 
        and applies the strict early-quit TP logic.
        """
        # This requires an Options Pricing Model (OPM) which is complex. We mock the output.
        
        if signal_data and signal_data['action'] == 'BUY':
            # Buy signal suggests being bullish, so we might sell a Cash-Secured Put (Short Put) 
            # to collect premium (Theta) with high probability of keeping the premium.
            
            # Mock Options Greeks and value calculation
            mock_premium = signal_data['entryPrice'] * 0.015 # 1.5% premium collection
            mock_delta = 0.35
            
            # Strict Profit Taker: Exit at 75% of max premium collected
            early_quit_premium = mock_premium * 0.75 
            
            return {
                'ticker': ticker,
                'strategy': 'Options: Short Put (Premium Collect)',
                'action': 'SELL_TO_OPEN (PUT)',
                'premium_received': mock_premium,
                'early_quit_TP': early_quit_premium,
                'delta': mock_delta,
                'rationale': f"High probability BUY signal utilized for premium collection. Target 75% profit ({early_quit_premium:.2f})."
            }
        return None


    # --- Wisdom Builder: Nightly Review Agent (Backtest-on-Actuals) ---
    
    def nightly_review_agent(self, trade_journal):
        """
        Runs daily/nightly analysis on completed trades (E1 learning).
        In a real environment, 'trade_journal' would come from the Journaling Service (Firestore).
        """
        print("\n--- WISDOM BUILDER: NIGHTLY REVIEW AGENT STARTING ---")
        closed_trades = [t for t in trade_journal if t['status'] == 'Closed']
        
        if not closed_trades:
            print("No closed trades to analyze. Learning skipped.")
            return

        win_count = sum(1 for t in closed_trades if t['pnl'] > 0)
        loss_count = len(closed_trades) - win_count
        
        new_win_rate = win_count / len(closed_trades) if closed_trades else 0.0

        print(f"Total Closed Trades Analyzed: {len(closed_trades)}. New Win Rate: {new_win_rate:.2f}")

        # E1: Adaptive Parameter Optimization - Adjusting Mean Reversion
        mr_performance = self.strategy_performance['A1_MR']
        
        # Simple Adaptive Logic: If the realized win rate is significantly lower than memory, 
        # tighten the volatility threshold for deviation.
        if new_win_rate < mr_performance['win_rate'] * 0.9:
            mr_performance['volatility_threshold'] *= 1.1 # Make it require a larger deviation (safer)
            mr_performance['win_rate'] = new_win_rate # Update memory
            print(f"-> E1 Adjustment: Mean Reversion strategy's volatility threshold adjusted to {mr_performance['volatility_threshold']:.2f} (due to poor performance).")

        # Backtest-on-Actuals: Simulate best/worst case scenario (Human-like memory)
        best_trade = max(closed_trades, key=lambda t: t['pnl'])
        worst_trade = min(closed_trades, key=lambda t: t['pnl'])

        print(f"\nWISDOM MEMORY:")
        print(f"  Best Trade: {best_trade['ticker']} | PnL: {best_trade['pnl']:.2f}% | What if we held longer? (Requires full backtest of the period)")
        print(f"  Worst Trade: {worst_trade['ticker']} | PnL: {worst_trade['pnl']:.2f}% | Could an earlier SL (e.g., 1.0 ATR) have saved us? (Requires full backtest of the period)")
        print("--- WISDOM BUILDER REVIEW ENDED ---")


    # --- Main Strategy Execution Loop ---
    
    def generate_signals(self):
        """
        The main function that is run periodically (e.g., every 15 minutes)
        to generate high-probability trade suggestions.
        """
        self.trade_suggestions = []
        
        # 1. Get Clean Data Snapshot
        data_snapshot = self.data_handler.get_current_data_snapshot()
        
        # 2. Run Strategies and Filter by EV
        for ticker, data in data_snapshot.items():
            if data.empty: continue
            
            # Calculate Indicators for the latest data point
            indicators = self._calculate_indicators(data)

            # A1: Mean Reversion
            mr_signal = self._mean_reversion_strategy(ticker, indicators)
            if mr_signal:
                self.trade_suggestions.append(mr_signal)

            # A2: Trend Following
            tf_signal = self._trend_following_strategy(ticker, indicators)
            if tf_signal:
                self.trade_suggestions.append(tf_signal)
            
            # Check for Options Specialization on any BUY signal
            if mr_signal or tf_signal:
                options_signal = self._options_specialization(ticker, mr_signal or tf_signal)
                if options_signal:
                    self.trade_suggestions.append(options_signal)
        
        # 3. Run A3 Stat Arb (requires cross-asset data, done separately)
        sa_signal = self._statistical_arbitrage_strategy(data_snapshot)
        if sa_signal:
             self.trade_suggestions.append(sa_signal)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Strategy Engine: Generated {len(self.trade_suggestions)} high-probability trade suggestions.")
        return self.trade_suggestions


# --- DEMONSTRATION OF SERVICE USAGE ---

if __name__ == '__main__':
    # Initialize services
    data_handler = MockDataHandler()
    engine = StrategyEngine(data_handler)

    print("--- DEMO 1: Signal Generation & EV Filter ---")
    signals = engine.generate_signals()
    
    # Display signals that passed the strict EV filter
    for i, signal in enumerate(signals):
        print(f"\nSignal #{i+1} | Ticker: {signal['ticker']}")
        print(f"  Strategy: {signal['strategy']} | Action: {signal['action']}")
        print(f"  Entry: ${signal['entryPrice']:.2f} | TP: ${signal.get('takeProfit'):.2f} | SL: ${signal.get('stopLoss'):.2f}")
        print(f"  Expected Return: {signal['expected_return_pct']*100:.2f}%")
        print(f"  Rationale: {signal['rationale']}")
    
    print("\n--- DEMO 2: Wisdom Builder Nightly Review (Learning from Mock Trades) ---")
    
    # Mock data from the Journaling Service (simulating live performance)
    MOCK_CLOSED_TRADES = [
        {'ticker': 'AAPL', 'strategy': 'A1_MR', 'pnl': 4.5, 'status': 'Closed'}, # Win
        {'ticker': 'MSFT', 'strategy': 'A1_MR', 'pnl': -0.8, 'status': 'Closed'}, # Loss (small)
        {'ticker': 'GOOGL', 'strategy': 'A2_TF', 'pnl': 12.1, 'status': 'Closed'}, # Big Win
        {'ticker': 'BABA/JD', 'strategy': 'A3_SA', 'pnl': 2.3, 'status': 'Closed'}, # Win
        {'ticker': 'AAPL', 'strategy': 'A1_MR', 'pnl': -3.2, 'status': 'Closed'}, # Big Loss
    ]
    
    engine.nightly_review_agent(MOCK_CLOSED_TRADES)