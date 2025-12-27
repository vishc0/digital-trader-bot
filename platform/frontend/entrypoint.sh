#!/bin/sh
set -e

# Ensure required env vars have defaults
: "${PORT:=8080}"
: "${API_GATEWAY_URL:=http://localhost:8000}"

# Render nginx config from template using environment variables
envsubst '${API_GATEWAY_URL} ${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

echo "Starting Nginx on port ${PORT}, proxying /api to ${API_GATEWAY_URL}"
exec nginx -g 'daemon off;'
