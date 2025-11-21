"""
Wisdom Builder Flask API
"""

import os
import logging
import json
from flask import Flask, jsonify, request
from wisdom_builder import WisdomBuilder
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8082))
app = Flask(__name__)
wisdom = WisdomBuilder()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'wisdom-builder'}), 200


@app.route('/nightly-review', methods=['POST'])
def nightly_review():
    """
    Execute nightly learning review.
    Input: {'closed_trades': [...], 'current_vectors': {...}}
    Output: Updated strategy vectors
    """
    data = request.get_json() or {}
    try:
        closed_trades = data.get('closed_trades', [])
        current_vectors = data.get('current_vectors', {})
        
        updated_vectors = wisdom.nightly_review(closed_trades, current_vectors)
        
        return jsonify({
            'status': 'completed',
            'trades_analyzed': len(closed_trades),
            'updated_vectors': updated_vectors,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error during nightly review: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/reflect', methods=['POST'])
def reflect_trade():
    """Reflect on a single trade."""
    data = request.get_json() or {}
    try:
        trade_result = data.get('trade', {})
        current_vector = data.get('current_vector', [0.5, 0.5, 0.5])
        
        new_vector = wisdom.reflect_on_trade(trade_result, current_vector)
        
        return jsonify({
            'trade_pnl': trade_result.get('pnl'),
            'old_vector': current_vector,
            'new_vector': new_vector
        }), 200
    except Exception as e:
        logger.error(f"Error reflecting on trade: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info(f"Starting Wisdom Builder on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
