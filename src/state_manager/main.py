import os
import redis
import msgpack
from flask import Flask, jsonify

app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# Robust connection with timeout
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, socket_connect_timeout=5)

@app.route('/')
def health():
    try:
        r.ping()
        return jsonify({"status": "healthy", "role": "Brain", "connected": True}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
***************************

import redis
import msgpack  # Efficient binary serialization (The 80/20 optimization)
import time
import json
import os

# --- CONFIGURATION (Injected by Environment) ---
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
APP_ID = os.environ.get('APP_ID', 'algo_brain_v1')

class CircuitBreakerOpen(Exception):
    """Raised when the system attempts to trade while risk limits are breached."""
    pass

class StateManager:
    """
    The Single Source of Truth.
    
    Design Principles:
    1. Tight Coupling via Data: All services read/write to this, avoiding chatty HTTP chains.
    2. Binary Protocol: Uses MsgPack for low latency/high throughput.
    3. Safety First: Hard-coded logic checks (Circuit Breakers) embedded in the state layer.
    """

    def __init__(self):
        # Connection pool for efficient resource usage
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.redis = redis.Redis(connection_pool=self.pool)
        
        # Keys
        self.K_CIRCUIT_BREAKER = f"{APP_ID}:risk:circuit_breaker"
        self.K_STRATEGY_VECTORS = f"{APP_ID}:wisdom:vectors"
        self.K_MARKET_STATE = f"{APP_ID}:market:state"
        self.K_DAILY_PNL = f"{APP_ID}:finance:daily_pnl"

    def _serialize(self, data):
        """Compresses data using MsgPack (Efficiency optimization)."""
        return msgpack.packb(data, use_bin_type=True)

    def _deserialize(self, data):
        if not data: return None
        return msgpack.unpackb(data, raw=False)

    # --- SAFETY LAYER (The "Never Loss" Mandate) ---

    def check_circuit_breaker(self):
        """
        The absolute gatekeeper. If this returns False, NO trade can physically execute.
        This protects against AI hallucinations or infinite loops.
        """
        status = self._deserialize(self.redis.get(self.K_CIRCUIT_BREAKER))
        
        if status and status.get('triggered', False):
            raise CircuitBreakerOpen(f"SYSTEM HALTED: {status.get('reason')}")
        
        # Check Daily Loss Limit (Hard Coded Safety)
        daily_pnl = float(self.redis.get(self.K_DAILY_PNL) or 0.0)
        MAX_DAILY_LOSS = -500.00 # Example: $500 Max Loss
        
        if daily_pnl <= MAX_DAILY_LOSS:
            self.trigger_circuit_breaker("Daily Loss Limit Hit")
            raise CircuitBreakerOpen("Daily Loss Limit Hit")

        return True

    def trigger_circuit_breaker(self, reason):
        """ pulls the plug on the system. """
        print(f"!!! CRITICAL: TRIGGERING CIRCUIT BREAKER: {reason} !!!")
        data = {'triggered': True, 'reason': reason, 'timestamp': time.time()}
        self.redis.set(self.K_CIRCUIT_BREAKER, self._serialize(data))

    def reset_system_state(self):
        """Called manually or by Wisdom module after Nightly Review."""
        self.redis.delete(self.K_CIRCUIT_BREAKER)
        self.redis.set(self.K_DAILY_PNL, 0.0)

    # --- WISDOM ACCESS (Vector Retrieval) ---

    def get_strategy_vector(self, strategy_id):
        """
        Retrieves the 'Confidence Vector' for a strategy.
        Default vector implies neutral confidence.
        """
        vectors = self._deserialize(self.redis.get(self.K_STRATEGY_VECTORS)) or {}
        # Default: [Confidence, Volatility_Tolerance, Regime_Alignment]
        return vectors.get(strategy_id, [0.5, 0.5, 0.5]) 

    def update_market_state(self, snapshot):
        """
        Updates the shared 'consciousness' of the market.
        Services read this instead of fetching external APIs (Cost Optimization).
        """
        # 1 Hour TTL (Time To Live) - data shouldn't be stale
        self.redis.setex(self.K_MARKET_STATE, 3600, self._serialize(snapshot))

    def get_market_state(self):
        return self._deserialize(self.redis.get(self.K_MARKET_STATE))

# --- DEMO USAGE ---
if __name__ == "__main__":
    brain = StateManager()
    
    # 1. Simulate a healthy state check
    try:
        brain.check_circuit_breaker()
        print("System Health: GREEN")
    except CircuitBreakerOpen as e:
        print(f"System Health: RED - {e}")

    # 2. Simulate a Market Update (Efficient Write)
    market_data = {'AAPL': 185.50, 'VIX': 14.2, 'Regime': 'Bull'}
    brain.update_market_state(market_data)
    print("Market State Updated.")

    # 3. Simulate a Catastrophic Loss
    brain.redis.set(brain.K_DAILY_PNL, -600.00)
    try:
        brain.check_circuit_breaker()
    except CircuitBreakerOpen as e:
        print(f"Safety Net Caught: {e}")