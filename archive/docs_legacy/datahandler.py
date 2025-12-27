import pandas as pd
import numpy as np
import time
from datetime import datetime
from collections import deque
import json
import random

# --- GLOBAL CONFIGURATION (MOCK/PLACEHOLDER FOR MICROSERVICE) ---
# In a real environment, these would be read from a config service or environment variables.
BROKER_API_KEY = "YOUR_BROKER_API_KEY"
DATA_VENDOR_API_KEY = "YOUR_DATA_VENDOR_API_KEY"
ASSETS_TO_TRACK = ['AAPL', 'MSFT', 'GOOGL', 'BABA', 'JD']

# --- BBO Handler Data Structure ---
# This dictionary simulates a real-time Level 1 quote feed, tracking Best Bid/Offer (BBO)
# and the mid-price, which is crucial for options and stat arb (A3) analysis.
BBO_DATA = {
    'AAPL': {'bid': 185.50, 'ask': 185.60, 'mid': 185.55, 'last_trade': 185.55, 'timestamp': time.time()},
    'MSFT': {'bid': 420.10, 'ask': 420.30, 'mid': 420.20, 'last_trade': 420.25, 'timestamp': time.time()},
    # ... other assets
}

# --- Core Service Class ---

class DataHandler:
    """
    The Data Ingestion and Normalization Service.
    
    This service is responsible for:
    1. Fetching raw historical and real-time data.
    2. Implementing the Data Normalization Layer (handling corporate actions).
    3. Implementing the BBO Handler for accurate mid-price calculation.
    4. Providing clean, standardized data to the Strategy Engine Service.
    """
    
    def __init__(self, assets=ASSETS_TO_TRACK):
        """Initializes data structures and mock connection settings."""
        self.assets = assets
        # Historical data storage (simulating a clean database)
        self.historical_data = self._load_mock_historical_data()
        # Real-time data queue (for BBO streaming)
        self.realtime_bbo_queues = {asset: deque(maxlen=100) for asset in assets}

    def _load_mock_historical_data(self):
        """
        [Data Normalization Layer]
        Simulates loading large historical datasets (Daily OHLCV) and
        applying crucial corporate action adjustments.
        
        In a real system, this would involve calling a data vendor API
        and adjusting for splits/dividends using provided metadata.
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Data Handler: Loading and normalizing mock historical data...")
        
        # Mock data generation
        data = {}
        date_range = pd.date_range(end=datetime.now(), periods=252, freq='B') # 1 year of business days
        
        for ticker in self.assets:
            # Generate random walk price data (Adjusted for Splits/Dividends)
            np.random.seed(hash(ticker) % 4294967295) # Seed for reproducible mock data
            prices = np.exp(np.cumsum(np.random.normal(0, 0.01, size=len(date_range)))) * (100 + random.randint(10, 50))
            
            df = pd.DataFrame({
                'Date': date_range,
                'Adj Close': prices,
                'Open': prices * (1 + np.random.normal(0, 0.005, size=len(date_range))),
                'High': prices * (1 + np.abs(np.random.normal(0, 0.01, size=len(date_range)))),
                'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, size=len(date_range)))),
                'Volume': np.random.randint(500000, 5000000, size=len(date_range))
            }).set_index('Date')
            
            data[ticker] = df.sort_index()
            
            # Simulated Corporate Action Adjustment (e.g., a simple 2:1 split 50 days ago)
            split_date = data[ticker].index[-50]
            if random.random() < 0.3: # Only simulate split for some tickers for complexity
                 data[ticker].loc[data[ticker].index < split_date, ['Open', 'High', 'Low', 'Adj Close']] /= 2
                 print(f"  -> {ticker}: Applied mock 2:1 split adjustment before {split_date.date()}")

        print("Data normalization complete.")
        return data

    def get_historical_data(self, ticker, lookback_days=252):
        """Retrieves cleaned historical data for a given ticker."""
        if ticker not in self.historical_data:
            print(f"Error: Historical data not found for {ticker}")
            return pd.DataFrame()
        
        # Return the last 'lookback_days' of clean, normalized data
        return self.historical_data[ticker].tail(lookback_days)

    # --- Real-Time BBO Handler (MOCK) ---
    def stream_and_process_bbo(self):
        """
        [BBO Handler]
        Simulates receiving a real-time market data feed (Bid, Ask, Mid-Price).
        In a real system, this would be a continuous websocket connection.
        """
        # Simulate a market tick for one random asset
        ticker = random.choice(self.assets)
        
        # Calculate new mock price based on current mid-price
        current_mid = BBO_DATA.get(ticker, {'mid': 100})['mid']
        
        # Apply a small random price change (simulating a tick)
        change = np.random.normal(0, 0.05) 
        new_mid = current_mid * (1 + change / 100)
        
        # Calculate new BBO based on the new mid-price (simulated spread of 0.05%)
        spread_pct = 0.0005
        new_bid = new_mid / (1 + spread_pct/2)
        new_ask = new_mid * (1 + spread_pct/2)
        
        # Update BBO_DATA dictionary
        BBO_DATA[ticker] = {
            'bid': round(new_bid, 2),
            'ask': round(new_ask, 2),
            'mid': round(new_mid, 2),
            'last_trade': round(new_mid + np.random.normal(0, 0.01), 2), # last trade slightly off mid
            'timestamp': time.time()
        }
        
        # Enqueue the latest mid-price for the SES (Strategy Engine Service)
        self.realtime_bbo_queues[ticker].append(BBO_DATA[ticker]['mid'])

        # Print update (for demonstration)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] BBO Update - {ticker}: Mid={BBO_DATA[ticker]['mid']} (Bid: {BBO_DATA[ticker]['bid']}, Ask: {BBO_DATA[ticker]['ask']})")
        
        return ticker, BBO_DATA[ticker]

    def get_latest_bbo(self, ticker):
        """Returns the latest BBO data for the requested ticker."""
        return BBO_DATA.get(ticker)

    def get_current_data_snapshot(self):
        """
        Returns a snapshot of the latest processed real-time data for all assets.
        This would be consumed by the Strategy Engine (SES).
        """
        snapshot = {}
        for ticker in self.assets:
            latest_data = self.get_latest_bbo(ticker)
            hist_data = self.get_historical_data(ticker, lookback_days=20) # Get 20 days for indicator calculation
            
            if not hist_data.empty and latest_data:
                # Append latest mid-price to the historical data as the "current" price point
                current_timestamp = datetime.fromtimestamp(latest_data['timestamp'])
                # Create a synthetic current day OHLCV for consistency
                current_day_data = pd.Series({
                    'Adj Close': latest_data['mid'],
                    'Open': hist_data['Adj Close'].iloc[-1], # Use yesterday's close as today's open mock
                    'High': max(latest_data['mid'], hist_data['High'].iloc[-1]),
                    'Low': min(latest_data['mid'], hist_data['Low'].iloc[-1]),
                    'Volume': 0 # Volume is difficult to mock accurately in ticks
                }, name=current_timestamp)

                # Combine historical data with the current snapshot (important for indicators)
                combined_data = pd.concat([hist_data, pd.DataFrame([current_day_data])])
                
                snapshot[ticker] = combined_data.tail(21) # Ensure we have enough data points (e.g., 20 days + current tick)
        
        return snapshot

# --- DEMONSTRATION OF SERVICE USAGE ---

if __name__ == '__main__':
    handler = DataHandler()
    
    print("\n--- DEMO: Fetching Cleaned Historical Data ---")
    aapl_hist = handler.get_historical_data('AAPL')
    print(f"AAPL Cleaned Data Head:\n{aapl_hist[['Adj Close', 'Volume']].head()}")
    print(f"AAPL Cleaned Data Tail:\n{aapl_hist[['Adj Close', 'Volume']].tail()}")
    
    print("\n--- DEMO: Real-Time BBO Stream (Simulated Ticks) ---")
    for _ in range(5):
        handler.stream_and_process_bbo()
        time.sleep(0.5)

    print("\n--- DEMO: Snapshot for Strategy Engine ---")
    snapshot = handler.get_current_data_snapshot()
    if 'MSFT' in snapshot:
        print(f"MSFT Snapshot for Strategy Engine (Last 5 points):\n{snapshot['MSFT']['Adj Close'].tail()}")