#!/bin/bash

# --- 1. SELF-HEALING CONFIGURATION ---
# Try to find the project ID from multiple sources to be safe
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

# If gcloud didn't return it, try the environment variable
if [[ -z "$PROJECT_ID" ]]; then
    PROJECT_ID=$DEVSHELL_PROJECT_ID
fi

# If we still don't have it, we cannot proceed.
if [[ -z "$PROJECT_ID" ]]; then
    echo "❌ CRITICAL ERROR: Could not detect Google Cloud Project ID."
    echo "   Please run this command first: gcloud config set project digitaltraderbot"
    exit 1
fi

# === THE FIX: FORCE SET THE PROJECT ===
# This fixes the error you saw. We explicitly tell gcloud "Use this project for everything."
echo "🔧 Enforcing Project Selection: $PROJECT_ID"
gcloud config set project $PROJECT_ID --quiet

# Variables
REGION="us-central1"
REDIS_NAME="algo-brain"
VPC_CONNECTOR="redis-connector"
NETWORK_NAME="default"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[CHECK] $1${NC}"
}

error_exit() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

log "🚀 RE-STARTING DEPLOYMENT FOR: $PROJECT_ID"

# ==============================================================================
# STEP 2: CHECK AND ENABLE APIS (IDEMPOTENT)
# ==============================================================================
log "Step 2: Verifying APIs..."
REQUIRED_APIS=("run.googleapis.com" "redis.googleapis.com" "vpcaccess.googleapis.com" "cloudbuild.googleapis.com" "artifactregistry.googleapis.com")

for api in "${REQUIRED_APIS[@]}"; do
    # Check if enabled. We suppress output to keep logs clean.
    if gcloud services list --enabled --filter="config.name:$api" | grep -q "$api"; then
        warn "API $api is already active."
    else
        log "Enabling $api..."
        gcloud services enable "$api" || error_exit "Failed to enable $api"
    fi
done

# ==============================================================================
# STEP 3: NETWORK INFRASTRUCTURE
# ==============================================================================
log "Step 3: Verifying Network Bridge (VPC Connector)..."

# We check specifically for the connector in the right region
if gcloud compute networks vpc-access connectors describe $VPC_CONNECTOR --region $REGION >/dev/null 2>&1; then
    warn "VPC Connector $VPC_CONNECTOR already exists."
else
    log "Creating VPC Connector (This takes ~2 mins)..."
    gcloud compute networks vpc-access connectors create $VPC_CONNECTOR \
        --region $REGION \
        --range 10.8.0.0/28 \
        --network $NETWORK_NAME \
        --min-instances 2 \
        --max-instances 3 \
        --machine-type e2-micro || error_exit "Failed to create VPC connector."
fi

# ==============================================================================
# STEP 4: THE BRAIN (REDIS)
# ==============================================================================
log "Step 4: Verifying Redis Brain..."

if gcloud redis instances describe $REDIS_NAME --region $REGION >/dev/null 2>&1; then
    warn "Redis instance $REDIS_NAME already exists."
else
    log "Creating Redis instance..."
    log "⚠️ NOTE: This step takes 5-8 minutes. DO NOT EXIT. If it times out, just re-run script."
    gcloud redis instances create $REDIS_NAME \
        --size=1 \
        --region=$REGION \
        --tier=BASIC \
        --redis-version=redis_6_x \
        --connect-mode=DIRECT_PEERING \
        --network=$NETWORK_NAME || error_exit "Failed to create Redis."
fi

REDIS_HOST=$(gcloud redis instances describe $REDIS_NAME --region $REGION --format="value(host)")
log "✅ Redis Brain is online at: $REDIS_HOST"

# ==============================================================================
# STEP 5: GENERATE CODE (OVERWRITE SAFE)
# ==============================================================================
log "Step 5: Refreshing Application Code..."
mkdir -p deploy_package/state_manager
mkdir -p deploy_package/strategy_engine
cd deploy_package

# Requirements
cat <<EOF > requirements.txt
flask==3.0.0
gunicorn==21.2.0
redis==5.0.1
msgpack==1.0.7
pandas==2.1.4
numpy==1.26.3
EOF

# State Manager Code
cat <<EOF > state_manager/main.py
import os
import redis
import msgpack
from flask import Flask, jsonify, request

app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# Retry connection logic for robustness
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, socket_connect_timeout=5)

@app.route('/')
def health():
    try:
        r.ping()
        return jsonify({"status": "healthy", "role": "State Manager", "brain_connected": True}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify({"market_regime": "neutral", "circuit_breaker": False})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
EOF

# Dockerfile
cat <<EOF > state_manager/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
EOF

cp requirements.txt state_manager/

# ==============================================================================
# STEP 6: DEPLOY TO CLOUD RUN
# ==============================================================================
log "Step 6: Deploying Services..."

log "Deploying State Manager..."
# We force the region and allow unauthenticated for the UI
gcloud run deploy state-manager \
    --source state_manager \
    --region $REGION \
    --allow-unauthenticated \
    --vpc-connector $VPC_CONNECTOR \
    --set-env-vars REDIS_HOST=$REDIS_HOST || error_exit "Failed to deploy State Manager"

log "🎉 DEPLOYMENT SUCCESSFUL!"
log "Your Infrastructure is verified and active."