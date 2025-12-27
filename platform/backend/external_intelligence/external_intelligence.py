"""
External Intelligence Service - Market Regime Detection

Responsibilities:
- Scans news and market data
- Uses LLM (Gemini) to extract sentiment and regime
- Updates market regime vectors
"""

import os
import json
import logging
import time
import random
from datetime import datetime

logger = logging.getLogger(__name__)


class ExternalIntelligence:
    """
    LLM-based market context and regime detection.
    """

    def __init__(self):
        """Initialize LLM connection."""
        self.model_name = 'gemini-2.5-flash'
        logger.info(f"External Intelligence initialized with {self.model_name}")

    def fetch_market_news(self):
        """Simulate fetching latest market news."""
        scenarios = [
            "Fed signals interest rate cuts may come sooner due to cooling inflation.",
            "Tech earnings miss expectations. VIX spikes to 22.",
            "Geopolitical tensions rise. Oil prices surge 4%.",
            "Job market robust. S&P 500 hits new high.",
            "Central bank emergency measures fuel risk-on sentiment."
        ]
        return random.choice(scenarios)

    def analyze_regime_with_llm(self, news_text):
        """
        Convert news into market regime vector.
        Format: [Sentiment (-1 to 1), Volatility (0 to 1), Regime label]
        """
        # In production, call actual Gemini API
        # For now, mock based on keywords
        
        sentiment_keywords = {
            'positive': ['rally', 'surge', 'gain', 'high', 'peak', 'robust'],
            'negative': ['crash', 'miss', 'decline', 'tension', 'emergency']
        }
        
        text_lower = news_text.lower()
        sentiment_score = 0.0
        
        for word in sentiment_keywords['positive']:
            if word in text_lower:
                sentiment_score += 0.2
        for word in sentiment_keywords['negative']:
            if word in text_lower:
                sentiment_score -= 0.2
        
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Determine regime label
        if sentiment_score > 0.3:
            regime = 'Bull'
        elif sentiment_score < -0.3:
            regime = 'Bear'
        else:
            regime = 'Sideways'
        
        volatility = abs(sentiment_score) * 0.5 + 0.3  # Range 0-1
        
        return {
            'sentiment_score': round(sentiment_score, 2),
            'volatility_expectation': round(volatility, 2),
            'regime_label': regime,
            'catalyst_detected': abs(sentiment_score) > 0.5
        }

    def update_market_context(self):
        """Main cycle: sense, think, act."""
        logger.info("Scanning external market context...")
        
        # 1. Fetch news
        news = self.fetch_market_news()
        logger.info(f"News: {news}")
        
        # 2. Analyze with LLM
        regime_vector = self.analyze_regime_with_llm(news)
        logger.info(f"Regime: {regime_vector}")
        
        return {
            'news': news,
            'regime': regime_vector,
            'timestamp': datetime.utcnow().isoformat()
        }
