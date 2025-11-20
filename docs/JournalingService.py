
import json
from firebase_admin import credentials, initialize_app, firestore
from datetime import datetime
import os
import time

# --- Global Canvas Variables (Mandatory) ---
# NOTE: These variables are automatically provided by the Canvas environment.
# We include fallback values for local development testing.
__app_id = os.environ.get('CANVAS_APP_ID', 'default-algo-app')
__firebase_config = os.environ.get('FIREBASE_CONFIG_JSON', '{}')

class JournalingService:
    """
    Service responsible for persistent logging (memory and wisdom) via Firestore.
    
    This service tracks:
    1. Trade Events (Signals, Approvals, Fills, Exits)
    2. Wisdom Builder Memory (Strategy Performance, Parameter Adjustments)
    3. LLM Pattern Repository (External insights for experimentation)
    
    The architecture uses the artifacts/{appId}/users/{userId}/... structure 
    for personalized data storage.
    """
    
    def __init__(self):
        try:
            # 1. Initialize Firebase App (using provided config)
            self.firebase_config = json.loads(__firebase_config)
            if not self.firebase_config:
                raise ValueError("Firebase configuration not provided.")

            # Firebase Admin initialization requires a credential object, which is complex 
            # to mock perfectly in a script environment. For simplicity in this non-UI
            # Python service, we assume Firestore is externally initialized or we proceed 
            # with a mock DB to show the data structure required.
            
            # --- Mock Firestore Connection for Demonstration ---
            self.db = None # Placeholder for Firestore client
            print("[INFO] Journaling Service initialized with MOCK Firestore connection.")
            
            self.app_id = __app_id
            self.user_id = 'mock_user_id_123' # This would be fetched from the Auth token in a real service
            
            # Define secure, standardized paths
            self.BASE_PATH = f"artifacts/{self.app_id}/users/{self.user_id}"
            self.TRADE_JOURNAL_COLLECTION = f"{self.BASE_PATH}/trade_journal"
            self.WISDOM_MEMORY_COLLECTION = f"{self.BASE_PATH}/wisdom_memory"
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Journaling Service: {e}")
            self.db = None # Ensure DB is null on failure

    # --- Data Persistence (Mock DB for Demonstraton) ---
    def _mock_save(self, collection_path, data):
        """Simulates saving a document to Firestore."""
        doc_id = data.get('id', datetime.now().isoformat())
        print(f"[SAVE MOCK] Collection: {collection_path} | Doc ID: {doc_id} | Data: {list(data.keys())}")
        return doc_id

    def _mock_load_recent_trades(self, limit=10):
        """Simulates loading recent closed trades for the Nightly Review Agent."""
        print(f"[LOAD MOCK] Retrieving {limit} recent closed trades from: {self.TRADE_JOURNAL_COLLECTION}")
        
        # Mock data structure matching the Nightly Review Agent's expectation
        return [
            {'id': 'T001', 'ticker': 'AAPL', 'strategy': 'A1_MR', 'pnl': 4.5, 'status': 'Closed', 'exit_reason': 'TP Hit', 'timestamp': datetime(2025, 11, 15).isoformat()}, 
            {'id': 'T002', 'ticker': 'MSFT', 'strategy': 'A1_MR', 'pnl': -0.8, 'status': 'Closed', 'exit_reason': 'SL Hit', 'timestamp': datetime(2025, 11, 16).isoformat()},
            {'id': 'T003', 'ticker': 'GOOGL', 'strategy': 'A2_TF', 'pnl': 12.1, 'status': 'Closed', 'exit_reason': 'TP Hit', 'timestamp': datetime(2025, 11, 17).isoformat()},
            {'id': 'T004', 'ticker': 'BABA/JD', 'strategy': 'A3_SA', 'pnl': -3.2, 'status': 'Closed', 'exit_reason': 'Circuit Breaker', 'timestamp': datetime(2025, 11, 18).isoformat()}, # Loss for learning
        ]

    # --- Public Methods for Microservice Communication ---

    def log_trade_event(self, trade_data, event_type):
        """Logs every state change of a trade (Signal, Approval, Fill, Exit)."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'trade_details': trade_data,
            'source_service': 'StrategyEngine' if event_type == 'SIGNAL' else 'ExecutionManager'
        }
        return self._mock_save(self.TRADE_JOURNAL_COLLECTION, log_entry)

    def log_wisdom_adjustment(self, strategy_id, adjustment_type, old_value, new_value, reason):
        """Logs changes made by the E1 Adaptive Optimizer or E2 RL Agent."""
        wisdom_entry = {
            'timestamp': datetime.now().isoformat(),
            'strategy_id': strategy_id,
            'adjustment_type': adjustment_type, # e.g., 'E1_PARAM_TUNE', 'E2_REGIME_SWITCH'
            'old_value': old_value,
            'new_value': new_value,
            'reason': reason,
            'source_service': 'WisdomBuilder'
        }
        return self._mock_save(self.WISDOM_MEMORY_COLLECTION, wisdom_entry)
        
    def get_closed_trades_for_review(self, status='Closed', lookback_days=7):
        """Called by the Nightly Review Agent to fetch history for learning."""
        return self._mock_load_recent_trades()

    def log_pattern_suggestion(self, pattern_name, llm_criteria, backtest_result):
        """
        Stores patterns derived from the LLM/External analysis (Pattern Repository).
        This is for the 'experimentation' requirement.
        """
        pattern_entry = {
            'timestamp': datetime.now().isoformat(),
            'pattern_name': pattern_name,
            'llm_criteria': llm_criteria,
            'backtest_result': backtest_result,
            'status': 'Pending Verification'
        }
        return self._mock_save(f"{self.BASE_PATH}/pattern_repository", pattern_entry)

# --- DEMONSTRATION OF SERVICE USAGE ---
if __name__ == '__main__':
    journal = JournalingService()
    
    print("\n--- DEMO: Logging a New Trade Signal ---")
    mock_signal = {
        'id': 'T005', 
        'ticker': 'MSFT', 
        'action': 'BUY',
        'entryPrice': 400.00,
        'takeProfit': 408.00,
        'stopLoss': 398.00,
        'strategy': 'A2_TF'
    }
    journal.log_trade_event(mock_signal, 'SIGNAL_GENERATED')

    print("\n--- DEMO: Logging a Correction from the E1 Optimizer ---")
    journal.log_wisdom_adjustment(
        'A1_MR', 
        'E1_PARAM_TUNE', 
        old_value={'RSI_Threshold': 30}, 
        new_value={'RSI_Threshold': 28}, 
        reason='Nightly Review indicated lower RSI threshold needed for higher conviction.'
    )

    print("\n--- DEMO: Nightly Review Agent Requesting Data ---")
    review_data = journal.get_closed_trades_for_review()
    for trade in review_data:
        print(f"Reviewed Trade: {trade['ticker']} | PnL: {trade['pnl']}% | Exit: {trade['exit_reason']}")

    ## after more research this was provided as final version: 

    import json
from datetime import datetime
import os
import uuid

# --- Configuration & Mocking ---
# In a real deployment, these connect to GCP Firestore / AWS DynamoDB
__app_id = os.environ.get('CANVAS_APP_ID', 'trade-wisdom-app')

class JournalingService:
    """
    The Central Nervous System of the Trading Platform.
    
    Target Maturity Level: 4 (Managed)
    
    Responsibilities:
    1. Immutable Audit Trail: Logs every signal, order, and fill.
    2. Wisdom Generation: storage for Post-Mortems, Drift Detection, and Regime Tags.
    3. Shadow Mode Tracking: Separate collection for 'phantom' trades.
    """
    
    def __init__(self):
        self.app_id = __app_id
        self.user_id = 'user_default' # Multi-tenant ready
        print(f" Journaling Service initialized for App: {self.app_id}")
        
        # In-memory storage for demonstration (Would be Firestore/DynamoDB)
        self._db_mock = {
            'trade_journal':,
            'shadow_journal':,
            'wisdom_insights':,
            'system_health':
        }

    # --- Core Logging Methods ---

    def log_trade_event(self, trade_id, event_type, data, is_shadow=False):
        """
        Logs a trade event. 
        If is_shadow=True, logs to a separate 'Shadow Journal' to validate strategies 
        without risking capital.
        """
        entry = {
            'id': str(uuid.uuid4()),
            'trade_id': trade_id,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type, # SIGNAL, ORDER_SENT, FILL, CANCEL, REJECT
            'data': data,
            'market_regime': self._fetch_current_regime_tag() # Contextual awareness
        }
        
        collection = 'shadow_journal' if is_shadow else 'trade_journal'
        self._db_mock[collection].append(entry)
        
        print(f" {event_type} | Trade: {trade_id} | Regime: {entry['market_regime']}")
        return entry['id']

    def log_execution_metrics(self, trade_id, expected_price, fill_price, fill_time_ms):
        """
        [Maturity Level 4] Execution Quality Analysis.
        Logs slippage and latency to identify 'Infrastructure Alpha/Decay'.
        """
        slippage = fill_price - expected_price
        slippage_pct = (slippage / expected_price) * 100
        
        metric_entry = {
            'trade_id': trade_id,
            'type': 'EXECUTION_METRIC',
            'slippage_abs': slippage,
            'slippage_pct': slippage_pct,
            'latency_ms': fill_time_ms,
            'timestamp': datetime.utcnow().isoformat()
        }
        # Store in the wisdom/insights collection for the Nightly Review Agent
        self._db_mock['wisdom_insights'].append(metric_entry)
        print(f" Trade {trade_id} | Slippage: {slippage_pct:.4f}% | Latency: {fill_time_ms}ms")

    def log_post_mortem(self, trade_id, result_pnl, drift_score, root_cause):
        """
        [Maturity Level 4] Automated Post-Mortem.
        
        drift_score: Deviation from the Backtest Expected Value.
        root_cause: 'MARKET_SHIFT', 'INFRA_FAILURE', 'STRATEGY_DECAY', 'UNKNOWN'
        """
        insight = {
            'trade_id': trade_id,
            'type': 'POST_MORTEM',
            'pnl': result_pnl,
            'drift_score': drift_score, 
            'root_cause': root_cause,
            'timestamp': datetime.utcnow().isoformat()
        }
        self._db_mock['wisdom_insights'].append(insight)
        print(f" Post-Mortem Saved. Cause: {root_cause} | Drift: {drift_score}")

    # --- Context Helper Methods ---

    def _fetch_current_regime_tag(self):
        """
        Mock method to fetch the current 'State of the World' from the Data Service.
        Real implementation would check VIX, Moving Averages, etc.
        """
        # In a real system, this queries the Feature Store
        return "VOLATILE_SIDEWAYS" 

    # --- Query Methods for Wisdom Builder ---

    def get_recent_drift_stats(self, strategy_id):
        """
        Used by the 'Sidecar' Risk Manager. 
        If average drift > threshold, the Sidecar kills the strategy.
        """
        # Mock logic: calculate avg drift for last 10 trades
        return 0.15 # Example: 15% deviation from backtest

# --- DEMONSTRATION ---

if __name__ == "__main__":
    journal = JournalingService()
    
    # 1. Log a Live Signal (Context-Aware)
    t_id = "TRADE-001"
    journal.log_trade_event(t_id, "SIGNAL_GENERATED", {"ticker": "AAPL", "action": "BUY", "limit": 150.00})
    
    # 2. Log Execution (Measuring the infrastructure)
    # Scenario: We wanted 150.00, but got filled at 150.05 (Slippage) after 200ms
    journal.log_trade_event(t_id, "FILL_CONFIRMED", {"fill_price": 150.05, "qty": 10})
    journal.log_execution_metrics(t_id, expected_price=150.00, fill_price=150.05, fill_time_ms=200)
    
    # 3. Log a Shadow Mode Trade (Experimentation)
    journal.log_trade_event("SHADOW-001", "SIGNAL_GENERATED", {"ticker": "TSLA", "action": "SELL"}, is_shadow=True)
    
    # 4. Log a Post-Mortem (Learning)
    # Scenario: Trade closed with a loss. Backtest said 60% win chance. 
    journal.log_post_mortem(t_id, result_pnl=-50.00, drift_score=0.8, root_cause="MARKET_SHIFT")