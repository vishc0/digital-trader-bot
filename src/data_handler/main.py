"""
Data Handler Flask API
"""

import os
import logging
import json
from flask import Flask, jsonify, request
from data_handler import DataHandler
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8085))
app = Flask(__name__)
handler = DataHandler()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'data-handler'}), 200


@app.route('/historical/<ticker>', methods=['GET'])
def get_historical(ticker):
    """Get historical data for a ticker."""
    lookback = request.args.get('lookback_days', default=252, type=int)
    data = handler.get_historical_data(ticker, lookback)
    
    if data.empty:
        return jsonify({'error': f'No data for {ticker}'}), 404
    
    return jsonify({
        'ticker': ticker,
        'data': data.tail(10).to_dict('records'),
        'count': len(data)
    }), 200


@app.route('/bbo/<ticker>', methods=['GET'])
def get_bbo(ticker):
    """Get best bid/offer for a ticker."""
    bbo = handler.get_bbo(ticker)
    
    if not bbo:
        return jsonify({'error': f'No BBO for {ticker}'}), 404
    
    return jsonify(bbo), 200


@app.route('/bbo/<ticker>', methods=['POST'])
def update_bbo(ticker):
    """Update BBO for a ticker."""
    data = request.get_json() or {}
    handler.update_bbo(
        ticker,
        data.get('bid', 0),
        data.get('ask', 0),
        data.get('last_trade', 0)
    )
    return jsonify({'status': 'updated', 'ticker': ticker}), 200


@app.route('/snapshot', methods=['GET'])
def get_snapshot():
    """Get full market snapshot."""
    lookback = request.args.get('lookback_days', default=20, type=int)
    snapshot = handler.get_data_snapshot(lookback)
    
    # Convert DataFrames to JSON
    result = {}
    for ticker, df in snapshot.items():
        result[ticker] = df.tail(5).to_dict('records')
    
    return jsonify({'snapshot': result, 'timestamp': datetime.utcnow().isoformat()}), 200


if __name__ == '__main__':
    logger.info(f"Starting Data Handler on port {PORT}")
    handler.generate_mock_historical_data()  # Pre-load data
    app.run(host='0.0.0.0', port=PORT, debug=False)
