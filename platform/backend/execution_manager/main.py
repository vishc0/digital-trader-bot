"""
Execution Manager Flask API

Exposes endpoints to place orders in `paper` or `live` mode.
"""
import os
import logging
from flask import Flask, jsonify, request
from execution_manager import ExecutionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8086))
EXECUTION_MODE = os.environ.get('EXECUTION_MODE', 'paper')

app = Flask(__name__)
manager = ExecutionManager(mode=EXECUTION_MODE)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'execution-manager', 'mode': manager.mode}), 200


@app.route('/place-order', methods=['POST'])
def place_order():
    """Place an order. Request JSON example:
    {
      "ticker": "AAPL",
      "side": "buy",
      "qty": 10,
      "price": 150.0,
      "order_type": "limit"
    }
    """
    data = request.get_json() or {}
    idempotency_key = request.headers.get('Idempotency-Key')
    try:
        order = data
        result = manager.place_order(order, idempotency_key=idempotency_key)
        return jsonify({'status': 'ok', 'result': result}), 200
    except Exception as e:
        logger.error(f'Error placing order: {e}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info(f'Starting Execution Manager on port {PORT} (mode={EXECUTION_MODE})')
    app.run(host='0.0.0.0', port=PORT, debug=False)
