import numpy as np
from datetime import datetime
# In a real deployment, we would import the StateManager class
# from state_manager import StateManager

class WisdomBuilder:
    """
    The 'Neuroplasticity' Module.
    
    Function:
    Instead of just deleting old data (Data Cleansing), this module
    analyzes outcomes and updates the 'Strategy Vectors' in the Central Brain.
    
    It runs on a 'Spot Instance' (Low cost) at night.
    """
    
    def __init__(self, state_manager_instance):
        self.brain = state_manager_instance
        self.learning_rate = 0.1 # How fast the system adapts (Neuroplasticity rate)

    def reflect_on_trade(self, trade_result):
        """
        The 'Self-Reflect' Step.
        Analyzes a closed trade and mathematically adjusts the strategy's confidence vector.
        """
        strategy_id = trade_result['strategy']
        pnl = trade_result['pnl']
        
        # 1. Fetch current mental state (Vector)
        # Vector format: [Confidence (0-1), Aggression (0-1), Risk_Aversion (0-1)]
        current_vector = np.array(self.brain.get_strategy_vector(strategy_id))
        
        print(f"Reflecting on {strategy_id}. Outcome: {pnl}%. Current Mental State: {current_vector}")

        # 2. Calculate the 'Gradient' (Direction of improvement)
        # If Profitable: Increase Confidence, Maintain Aggression
        # If Loss: Decrease Confidence, Increase Risk_Aversion
        
        delta_vector = np.array([0.0, 0.0, 0.0])
        
        if pnl > 0:
            # Reward: Boost confidence significantly, slightly boost aggression
            reward = np.log1p(pnl) * 0.1 # Logarithmic reward scaling
            delta_vector = np.array([reward, reward * 0.5, -0.05])
        else:
            # Punishment: Penalize confidence, boost risk aversion
            punishment = np.abs(pnl) * 0.15
            delta_vector = np.array([-punishment, -punishment, punishment])

        # 3. Apply the update (Neuroplasticity)
        new_vector = current_vector + (delta_vector * self.learning_rate)
        
        # Clip values to keep them normalized (0.0 to 1.0)
        new_vector = np.clip(new_vector, 0.01, 0.99)

        # 4. Commit to Long-Term Memory (Redis)
        # We use the low-level serialize method here
        vectors = self.brain._deserialize(self.brain.redis.get(self.brain.K_STRATEGY_VECTORS)) or {}
        vectors[strategy_id] = new_vector.tolist()
        
        self.brain.redis.set(self.brain.K_STRATEGY_VECTORS, self.brain._serialize(vectors))
        
        print(f"-> Wisdom Updated. New Mental State: {new_vector}")
        
        return new_vector

    def nightly_vector_optimization(self):
        """
        The 'Deep Sleep' process.
        Runs permutations on the vectors to see if theoretical shifts would have performed better.
        (This mimics the 'Dreaming/Consolidation' phase of memory).
        """
        print("\n--- NIGHTLY DEEP SLEEP PHASE ---")
        # 1. Load all trades from the day (Mocking the fetch here)
        daily_trades = [
            {'strategy': 'A1_MR', 'pnl': 1.5},
            {'strategy': 'A1_MR', 'pnl': -0.5},
            {'strategy': 'A2_TF', 'pnl': 3.0}
        ]
        
        for trade in daily_trades:
            self.reflect_on_trade(trade)
            
        # 2. Pruning
        # If a strategy's confidence drops below 0.2, we flag it for manual review (Human Intervention)
        vectors = self.brain._deserialize(self.brain.redis.get(self.brain.K_STRATEGY_VECTORS))
        for strat, vec in vectors.items():
            if vec[0] < 0.2:
                print(f"WARNING: Strategy {strat} has lost System Confidence ({vec[0]:.2f}). Disabling...")
                # In a real app, we would set a flag in Redis to disable this strategy ID

# --- DEMO WRAPPER ---
if __name__ == "__main__":
    # Mock the StateManager for standalone testing
    class MockRedis:
        def __init__(self): self.data = {}
        def get(self, k): return self.data.get(k)
        def set(self, k, v): self.data[k] = v
    
    class MockStateManager:
        def __init__(self):
            self.redis = MockRedis()
            self.K_STRATEGY_VECTORS = "vectors"
        def get_strategy_vector(self, s): return [0.5, 0.5, 0.5]
        def _serialize(self, d): return d
        def _deserialize(self, d): return d

    print("Initializing Wisdom Builder...")
    mock_brain = MockStateManager()
    wisdom = WisdomBuilder(mock_brain)
    
    # Run the nightly routine
    wisdom.nightly_vector_optimization()