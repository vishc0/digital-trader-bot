"""
Wisdom Builder Service - Nightly Learning Engine

Responsibilities:
- Analyzes closed trades (backtest-on-actuals)
- Updates strategy confidence vectors
- Implements E1 adaptive parameter optimization
- Detects drift and performance decay
"""

import numpy as np
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class WisdomBuilder:
    """
    The Learning Engine - Neuroplasticity Module
    Runs nightly to optimize strategy parameters based on realized performance.
    """

    def __init__(self, learning_rate=0.1):
        """Initialize learning rate."""
        self.learning_rate = learning_rate
        logger.info(f"Wisdom Builder initialized with learning_rate={learning_rate}")

    def reflect_on_trade(self, trade_result, current_vector):
        """
        Analyze a closed trade and update strategy confidence vector.
        
        Vector: [Confidence, Aggression, Risk_Aversion]
        """
        pnl = trade_result.get('pnl', 0.0)
        
        # Calculate gradient based on outcome
        if pnl > 0:
            # Reward: boost confidence
            reward = np.log1p(abs(pnl)) * 0.1
            delta = np.array([reward, reward * 0.5, -0.05])
        else:
            # Punishment: reduce confidence, increase risk aversion
            punishment = abs(pnl) * 0.15
            delta = np.array([-punishment, -punishment, punishment])
        
        # Apply learning
        new_vector = np.array(current_vector) + (delta * self.learning_rate)
        new_vector = np.clip(new_vector, 0.01, 0.99)  # Normalize
        
        return new_vector.tolist()

    def nightly_review(self, closed_trades, strategy_vectors):
        """
        Nightly analysis and learning from all closed trades.
        
        Returns updated strategy vectors.
        """
        if not closed_trades:
            logger.info("No closed trades to analyze")
            return strategy_vectors
        
        logger.info(f"Analyzing {len(closed_trades)} closed trades")
        
        # Group trades by strategy
        trades_by_strategy = {}
        for trade in closed_trades:
            strategy_id = trade.get('strategy', 'UNKNOWN')
            if strategy_id not in trades_by_strategy:
                trades_by_strategy[strategy_id] = []
            trades_by_strategy[strategy_id].append(trade)
        
        # Update vectors for each strategy
        updated_vectors = dict(strategy_vectors)
        
        for strategy_id, trades in trades_by_strategy.items():
            current_vector = updated_vectors.get(strategy_id, [0.5, 0.5, 0.5])
            
            # Calculate average performance
            avg_pnl = np.mean([t.get('pnl', 0) for t in trades])
            win_count = sum(1 for t in trades if t.get('pnl', 0) > 0)
            win_rate = win_count / len(trades)
            
            logger.info(f"{strategy_id}: Win Rate={win_rate:.1%}, Avg PnL={avg_pnl:.2f}%")
            
            # Update vector based on aggregate performance
            for trade in trades:
                new_vector = self.reflect_on_trade(trade, current_vector)
                current_vector = new_vector
            
            updated_vectors[strategy_id] = current_vector
            logger.info(f"{strategy_id} updated: {[f'{v:.2f}' for v in current_vector]}")
        
        return updated_vectors
