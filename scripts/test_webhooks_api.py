#!/usr/bin/env python3
"""
Test script for SAP Webhooks API.
This script demonstrates all RESTful endpoints.
"""
import json
import requests
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init()


def print_header(text):
    """Print a formatted header text."""
    print(f"\n{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}  {text}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}")


def print_request_info(method, path):
    """Print formatted request information."""
    print(f"\n{Fore.GREEN}{method} {path}{Style.RESET_ALL}")


def print_response(response):
    """Print formatted response."""
    print(f"Status: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)
    print()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test SAP Webhooks API")
    parser.add_argument(
        "-H", "--host",
        default="127.0.0.1",
        help="API host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "-p", "--port",
        default="9001",
        help="API port (default: 9001)"
    )
    return parser.parse_args()


def main():
    """Run the test script."""
    # Parse command-line arguments
    args = parse_args()

    # Configuration
    base_url = f"http://{args.host}:{args.port}/api/webhooks/"
    api_key = "nL/jnMd+IHCTk8M1vZPGgA=="
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print_header(f"SAP Webhooks API Test Script - {args.host}:{args.port}")

    # 1. GET all webhooks
    print_request_info("GET", "/api/webhooks/")
    response = requests.get(base_url, headers=headers)
    print_response(response)

    # 2. POST a new webhook
    print_request_info("POST", "/api/webhooks/")
    payload = {
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
    }
    response = requests.post(base_url, headers=headers, json=payload)
    print_response(response)

    # 3. GET a specific webhook by ID
    webhook_id = "webhook123"
    print_request_info("GET", f"/api/webhooks/{webhook_id}")
    response = requests.get(
        f"{base_url.rstrip('/')}/{webhook_id}", headers=headers)
    print_response(response)

    # 4. PUT (full update) a webhook
    print_request_info("PUT", f"/api/webhooks/{webhook_id}")
    payload = {
        "event_type": "order.updated",
        "entity_id": "order-123456",
        "data": {
            "order_id": "ORD-123456",
            "status": "processed",
            "updated_at": "2023-09-15T14:30:00Z",
            "updated_by": "system"
        }
    }
    response = requests.put(
        f"{base_url.rstrip('/')}/{webhook_id}", headers=headers, json=payload)
    print_response(response)

    # 5. PATCH (partial update) a webhook
    print_request_info("PATCH", f"/api/webhooks/{webhook_id}")
    payload = {
        "event_type": "order.processed",
        "data": {
            "status": "shipped",
            "tracking_number": "TRK123456789"
        }
    }
    response = requests.patch(
        f"{base_url.rstrip('/')}/{webhook_id}", headers=headers, json=payload)
    print_response(response)

    # 6. DELETE a webhook
    print_request_info("DELETE", f"/api/webhooks/{webhook_id}")
    response = requests.delete(
        f"{base_url.rstrip('/')}/{webhook_id}", headers=headers)
    print_response(response)

    print_header("Test Script Completed")


if __name__ == "__main__":
    main()
