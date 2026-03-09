"""
Data Handler Service - Data Ingestion & Normalization

Responsibilities:
- Fetches historical and real-time market data
- Applies corporate action adjustments
- Implements BBO (Best Bid/Offer) handler
- Provides clean data snapshots to Strategy Engine
"""

import json
import logging
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
import pandas as pd
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
        self.market_data_provider = os.environ.get('MARKET_DATA_PROVIDER', 'mock').lower()
        self.twelve_data_api_key = os.environ.get('TWELVE_DATA_API_KEY', '').strip()
        self.api_key_configured = bool(self.twelve_data_api_key)
        self.historical_cache_meta = {}
        self.quote_cache_meta = {}
        self.historical_cache_ttl_seconds = int(os.environ.get('HISTORICAL_CACHE_TTL_SECONDS', 300))
        self.quote_cache_ttl_seconds = int(os.environ.get('QUOTE_CACHE_TTL_SECONDS', 15))
        logger.info(f"Data Handler initialized with assets: {assets}")

    def _utcnow(self):
        return datetime.utcnow()

    def _cache_is_fresh(self, cache_meta, key, ttl_seconds):
        cached_at = cache_meta.get(key)
        if not cached_at:
            return False
        return (self._utcnow() - cached_at).total_seconds() < ttl_seconds

    def _fetch_json(self, base_url, params):
        url = f"{base_url}?{urlencode(params)}"
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))

    def _normalize_twelve_data_timeseries(self, values):
        if not values:
            return pd.DataFrame()

        df = pd.DataFrame(values)
        rename_map = {
            'datetime': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }
        df = df.rename(columns=rename_map)
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        df['Adj Close'] = df['Close']
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
        return df.sort_index()

    def _fetch_twelve_data_historical_data(self, ticker, lookback_days=252):
        if not self.api_key_configured:
            raise RuntimeError('TWELVE_DATA_API_KEY is not configured')

        try:
            payload = self._fetch_json(
                'https://api.twelvedata.com/time_series',
                {
                    'symbol': ticker,
                    'interval': '1day',
                    'outputsize': max(lookback_days, 30),
                    'apikey': self.twelve_data_api_key,
                    'format': 'JSON'
                }
            )
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f'Twelve Data historical request failed: {exc}') from exc

        if payload.get('status') == 'error':
            raise RuntimeError(payload.get('message', 'Unknown Twelve Data error'))

        values = payload.get('values', [])
        df = self._normalize_twelve_data_timeseries(values)
        if df.empty:
            raise RuntimeError(f'No Twelve Data historical values returned for {ticker}')

        self.historical_data[ticker] = df
        self.historical_cache_meta[ticker] = self._utcnow()
        return df.tail(lookback_days)

    def _fetch_twelve_data_quote(self, ticker):
        if not self.api_key_configured:
            raise RuntimeError('TWELVE_DATA_API_KEY is not configured')

        try:
            payload = self._fetch_json(
                'https://api.twelvedata.com/quote',
                {
                    'symbol': ticker,
                    'apikey': self.twelve_data_api_key,
                    'format': 'JSON'
                }
            )
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f'Twelve Data quote request failed: {exc}') from exc

        if payload.get('status') == 'error':
            raise RuntimeError(payload.get('message', 'Unknown Twelve Data error'))

        bid = float(payload.get('bid') or payload.get('close') or payload.get('previous_close') or 0)
        ask = float(payload.get('ask') or payload.get('close') or payload.get('previous_close') or bid)
        last_trade = float(payload.get('close') or payload.get('previous_close') or bid)
        self.update_bbo(ticker, bid, ask, last_trade)
        self.quote_cache_meta[ticker] = self._utcnow()
        return self.bbo_data[ticker]

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
        if self.market_data_provider == 'twelve_data' and self.api_key_configured:
            if ticker in self.historical_data and self._cache_is_fresh(
                self.historical_cache_meta,
                ticker,
                self.historical_cache_ttl_seconds
            ):
                return self.historical_data[ticker].tail(lookback_days)
            try:
                return self._fetch_twelve_data_historical_data(ticker, lookback_days)
            except Exception as exc:
                logger.warning('Falling back to mock historical data for %s: %s', ticker, exc)

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
        if self.market_data_provider == 'twelve_data' and self.api_key_configured:
            if ticker in self.bbo_data and self._cache_is_fresh(
                self.quote_cache_meta,
                ticker,
                self.quote_cache_ttl_seconds
            ):
                return self.bbo_data[ticker]
            try:
                return self._fetch_twelve_data_quote(ticker)
            except Exception as exc:
                logger.warning('Falling back to cached/mock BBO for %s: %s', ticker, exc)

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

    def get_provider_status(self):
        """Return provider configuration and readiness."""
        return {
            'provider': self.market_data_provider,
            'api_key_configured': self.api_key_configured,
            'assets': self.assets,
            'historical_cache_size': len(self.historical_data),
            'bbo_cache_size': len(self.bbo_data)
        }
