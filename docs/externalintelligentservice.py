import os
import json
import time
import random
import redis
import msgpack
# In a real environment, you would install: pip install google-generativeai
import google.generativeai as genai 

# --- CONFIGURATION ---
# NOTE: The API Key is injected by the environment or config file
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '') 
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
APP_ID = os.environ.get('APP_ID', 'algo_brain_v1')

class ExternalIntelligence:
    """
    Service 5: The LLM Context & Catalyst Scanner.
    
    Role:
    1. Scans external data (News, Sentiment).
    2. Uses LLM (Gemini) to convert "Noise" into a "Regime Vector".
    3. Updates the Central Brain (Redis) with the new reality.
    
    Architecture:
    - Runs as a standalone process (loop).
    - Writes directly to the State Manager's memory.
    """

    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=6379, db=0)
        self.K_MARKET_STATE = f"{APP_ID}:market:state"
        
        # Initialize Gemini
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        else:
            self.model = None
            print("[WARN] No Gemini API Key found. Running in Mock Mode.")

    def fetch_market_news(self):
        """
        Simulates fetching 'Live' news from an API (e.g., Bloomberg, Reuters, Twitter).
        In a real app, this would hit a NewsAPI endpoint.
        """
        # MOCK DATA: Simulating different market scenarios
        scenarios = [
            "Fed Chair Powell suggests interest rate cuts may come sooner than expected due to cooling inflation.",
            "Tech sector sells off as major earnings reports miss expectations. VIX spikes to 22.",
            "Geopolitical tensions rise in the Middle East, oil prices surge 4%. Safe haven assets rallying.",
            "Job market report shows robust growth, signaling a 'Soft Landing' is achievable. S&P 500 hits new high."
        ]
        return random.choice(scenarios)

    def analyze_regime_with_llm(self, news_text):
        """
        The Core Intelligence: Converts text into a Mathematical Vector.
        Vector Format: [Bearish<->Bullish (-1 to 1), Volatility (0 to 1), Chaos_Factor (0 to 1)]
        """
        if not self.model:
            # Fallback Mock Logic if API is missing
            return self._mock_analysis(news_text)

        try:
            prompt = f"""
            Analyze the following market news and output a JSON object representing the market regime.
            News: "{news_text}"
            
            Output Format:
            {{
                "sentiment_score": (float, -1.0 to 1.0),
                "volatility_expectation": (float, 0.0 to 1.0),
                "regime_label": "Bull" | "Bear" | "Sideways" | "Crisis",
                "catalyst_detected": true/false
            }}
            Return ONLY the JSON.
            """
            response = self.model.generate_content(prompt)
            # Basic cleaning to ensure JSON
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"[ERROR] LLM Analysis Failed: {e}")
            return self._mock_analysis(news_text)

    def _mock_analysis(self, text):
        """Fallback logic to ensure system stability."""
        if "sell" in text.lower() or "miss" in text.lower() or "tensions" in text.lower():
            return {"sentiment_score": -0.6, "volatility_expectation": 0.8, "regime_label": "Bear/Crisis", "catalyst_detected": True}
        return {"sentiment_score": 0.7, "volatility_expectation": 0.3, "regime_label": "Bull", "catalyst_detected": False}

    def _serialize(self, data):
        return msgpack.packb(data, use_bin_type=True)

    def update_brain(self):
        """The Main Cycle."""
        print(f"[{time.strftime('%X')}] Scanning External World...")
        
        # 1. Sense
        news = self.fetch_market_news()
        print(f"   -> NEWS: {news}")
        
        # 2. Think (LLM)
        analysis = self.analyze_regime_with_llm(news)
        print(f"   -> INTEL: {analysis}")
        
        # 3. Act (Update Brain)
        # We fetch the existing state to preserve price data, only updating the 'regime'
        current_state_packed = self.redis.get(self.K_MARKET_STATE)
        state = msgpack.unpackb(current_state_packed, raw=False) if current_state_packed else {}
        
        # Merge the LLM insights
        state['regime'] = analysis
        state['last_updated'] = time.time()
        
        # Write back to Redis
        self.redis.set(self.K_MARKET_STATE, self._serialize(state))
        print("   -> Brain Updated with new Regime Context.")

    def start_loop(self, interval=300):
        """Runs the service indefinitely."""
        print("--- External Intelligence Service Started ---")
        while True:
            self.update_brain()
            time.sleep(interval)

if __name__ == "__main__":
    intel = ExternalIntelligence()
    # Run once for demo purposes
    intel.update_brain()