#!/bin/bash

# Test script for SAP Webhooks API
# This script demonstrates all RESTful endpoints

# Default values
DEFAULT_PROTOCOL="http"
DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT="9001"
DEFAULT_API_KEY="nL/jnMd+IHCTk8M1vZPGgA=="

# Help message
show_help() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -s, --https         Use HTTPS instead of HTTP"
  echo "  -h, --host HOST     API host (default: $DEFAULT_HOST)"
  echo "  -p, --port PORT     API port (default: $DEFAULT_PORT)"
  echo "  -k, --key KEY       API key (default: $DEFAULT_API_KEY)"
  echo "  --help              Show this help message"
  echo ""
  echo "Examples:"
  echo "  $0 -h api.example.com -p 8080"
  echo "  $0 -s -h secure-api.example.com -p 443"
  echo "  $0 -k 'your-custom-api-key'"
}

# Parse command line arguments
PROTOCOL=$DEFAULT_PROTOCOL
HOST=$DEFAULT_HOST
PORT=$DEFAULT_PORT
API_KEY=$DEFAULT_API_KEY

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--https)
      PROTOCOL="https"
      shift
      ;;
    -h|--host)
      HOST="$2"
      shift 2
      ;;
    -p|--port)
      PORT="$2"
      shift 2
      ;;
    -k|--key)
      API_KEY="$2"
      shift 2
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Configuration
API_BASE_URL="${PROTOCOL}://${HOST}:${PORT}/api/webhooks"
API_URL="${API_BASE_URL}/"

# Color formatting
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}  SAP Webhooks API Test Script${NC}"
echo -e "${BLUE}  Protocol: ${PROTOCOL}, Host: ${HOST}, Port: ${PORT}${NC}"
echo -e "${BLUE}==========================================${NC}"

# 1. GET all webhooks
echo -e "\n${GREEN}GET all webhooks:${NC}"
curl -s -H "X-API-KEY: $API_KEY" $API_URL | jq

# 2. POST a new webhook
echo -e "\n${GREEN}POST a new webhook:${NC}"
curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "event_type": "order.created",
    "entity_id": "order-123456",
    "data": {
      "order_id": "ORD-123456",
      "customer_id": "CUST-789",
      "items": [
        {"product_id": "PROD-001", "quantity": 2, "price": 19.99},
        {"product_id": "PROD-002", "quantity": 1, "price": 29.99}
      ],
      "total": 69.97
    }
  }' | jq

# 3. GET a specific webhook by ID
echo -e "\n${GREEN}GET a specific webhook by ID:${NC}"
curl -s -H "X-API-KEY: $API_KEY" "${API_BASE_URL}/webhook123" | jq

# 4. PUT (full update) a webhook
echo -e "\n${GREEN}PUT (full update) a webhook:${NC}"
curl -s -X PUT "${API_BASE_URL}/webhook123" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "event_type": "order.updated",
    "entity_id": "order-123456",
    "data": {
      "order_id": "ORD-123456",
      "status": "processed",
      "updated_at": "2023-09-15T14:30:00Z",
      "updated_by": "system"
    }
  }' | jq

# 5. PATCH (partial update) a webhook
echo -e "\n${GREEN}PATCH (partial update) a webhook:${NC}"
curl -s -X PATCH "${API_BASE_URL}/webhook123" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "event_type": "order.processed",
    "data": {
      "status": "shipped",
      "tracking_number": "TRK123456789"
    }
  }' | jq

# 6. DELETE a webhook
echo -e "\n${GREEN}DELETE a webhook:${NC}"
curl -s -X DELETE "${API_BASE_URL}/webhook123" \
  -H "X-API-KEY: $API_KEY" \
  -v 2>&1 | grep "< HTTP"

# 7. Health check endpoint
echo -e "\n${GREEN}Health Check:${NC}"
curl -s "${PROTOCOL}://${HOST}:${PORT}/healthz" | jq

echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  Test Script Completed${NC}"
echo -e "${BLUE}==========================================${NC}" 