"""
External Intelligence Flask API
"""

import os
import logging
import json
from flask import Flask, jsonify, request
from external_intelligence import ExternalIntelligence
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8083))
app = Flask(__name__)
intel = ExternalIntelligence()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'external-intelligence'}), 200


@app.route('/market-context', methods=['GET'])
def get_market_context():
    """Fetch latest market context and regime."""
    try:
        context = intel.update_market_context()
        return jsonify(context), 200
    except Exception as e:
        logger.error(f"Error fetching market context: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze-news', methods=['POST'])
def analyze_news():
    """Analyze provided news text for regime."""
    data = request.get_json() or {}
    news_text = data.get('news', '')
    
    if not news_text:
        return jsonify({'error': 'No news provided'}), 400
    
    try:
        regime = intel.analyze_regime_with_llm(news_text)
        return jsonify({
            'news': news_text,
            'regime': regime,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error analyzing news: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info(f"Starting External Intelligence on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
