FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
# Copy built static files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy templated nginx config and entrypoint
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default environment (can be overridden in Cloud Run)
ENV PORT=8080
ENV API_GATEWAY_URL="http://localhost:8000"

EXPOSE 8080
CMD ["/entrypoint.sh"]
