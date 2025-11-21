"""
Data Handler Service - Data Ingestion & Normalization

Responsibilities:
- Fetches historical and real-time market data
- Applies corporate action adjustments
- Implements BBO (Best Bid/Offer) handler
- Provides clean data snapshots to Strategy Engine
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DataHandler:
    """
    Data ingestion and normalization service.
    """

    def __init__(self, assets=['AAPL', 'MSFT', 'GOOGL', 'BABA', 'JD']):
        """Initialize data handler."""
        self.assets = assets
        self.historical_data = {}
        self.bbo_data = {}
        logger.info(f"Data Handler initialized with assets: {assets}")

    def generate_mock_historical_data(self, lookback_days=252):
        """Generate mock historical OHLCV data."""
        logger.info(f"Generating mock historical data for {len(self.assets)} assets")
        
        data = {}
        date_range = pd.date_range(end=datetime.now(), periods=lookback_days, freq='B')
        
        for ticker in self.assets:
            np.random.seed(hash(ticker) % 4294967295)
            
            # Generate random walk prices
            base_price = 100 + np.random.randint(10, 100)
            returns = np.random.normal(0.0001, 0.01, size=len(date_range))
            prices = base_price * np.exp(np.cumsum(returns))
            
            df = pd.DataFrame({
                'Adj Close': prices,
                'Open': prices * (1 + np.random.normal(0, 0.005, len(date_range))),
                'High': prices * (1 + np.abs(np.random.normal(0, 0.01, len(date_range)))),
                'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, len(date_range)))),
                'Volume': np.random.randint(500000, 5000000, len(date_range))
            }, index=date_range)
            
            data[ticker] = df.sort_index()
        
        self.historical_data = data
        return data

    def get_historical_data(self, ticker, lookback_days=252):
        """Retrieve historical data for a ticker."""
        if not self.historical_data:
            self.generate_mock_historical_data()
        
        if ticker not in self.historical_data:
            logger.warning(f"Historical data not found for {ticker}")
            return pd.DataFrame()
        
        return self.historical_data[ticker].tail(lookback_days)

    def update_bbo(self, ticker, bid, ask, last_trade):
        """Update best bid/offer for a ticker."""
        mid = (bid + ask) / 2
        self.bbo_data[ticker] = {
            'bid': bid,
            'ask': ask,
            'mid': mid,
            'last_trade': last_trade,
            'timestamp': datetime.utcnow().isoformat(),
            'spread': ask - bid,
            'spread_pct': ((ask - bid) / mid * 100) if mid != 0 else 0
        }

    def get_bbo(self, ticker):
        """Get latest BBO for a ticker."""
        if ticker not in self.bbo_data:
            return None
        return self.bbo_data[ticker]

    def get_data_snapshot(self, lookback_days=20):
        """Get combined historical + real-time snapshot for Strategy Engine."""
        if not self.historical_data:
            self.generate_mock_historical_data()
        
        snapshot = {}
        
        for ticker in self.assets:
            hist = self.get_historical_data(ticker, lookback_days)
            
            if hist.empty:
                continue
            
            # Get latest BBO
            bbo = self.get_bbo(ticker)
            
            if bbo:
                # Append current mid as latest close
                current_row = pd.Series({
                    'Adj Close': bbo['mid'],
                    'Open': hist['Adj Close'].iloc[-1],
                    'High': max(bbo['mid'], hist['High'].iloc[-1]),
                    'Low': min(bbo['mid'], hist['Low'].iloc[-1]),
                    'Volume': 0
                }, name=datetime.utcnow())
                
                snapshot[ticker] = pd.concat([hist, pd.DataFrame([current_row])])
            else:
                snapshot[ticker] = hist
        
        return snapshot
