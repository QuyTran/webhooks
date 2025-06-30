# SAP Webhooks API

A Python FastAPI application for handling SAP webhooks.

## Features

- RESTful API endpoints for receiving SAP webhook data
- Authentication with API keys
- Configurable via environment variables
- API documentation with Swagger/OpenAPI

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/sap-webhooks.git
cd sap-webhooks
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on the example:

```bash
cp .env.example .env
# Edit .env with your settings
```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or use the Python module:

```bash
python -m app.main
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Webhooks

- `POST /api/webhooks/` - Receive webhook data
- `GET /api/webhooks/` - List recent webhooks

## Configuration

Configuration is managed through environment variables or a `.env` file:

- `API_HOST`: Host to bind the server (default: "0.0.0.0")
- `API_PORT`: Port to run the server (default: 8000)
- `LOG_LEVEL`: Logging level (default: "info")
- `API_KEY`: API key for authentication
- `SECRET_KEY`: Secret key for token generation

### Custom Headers

Custom headers are loaded from the `app/custom_headers.json` file. This file contains a list of headers that will be added to all API responses. The format is:

```json
[
  {"name": "header-name", "value": "header-value"},
  {"name": "another-header", "value": "another-value"}
]
```

To modify the headers, simply edit this file and restart the application.

## Security

- API Key authentication is required for all endpoints
- CORS middleware is configured but should be restricted in production

## License

[MIT](LICENSE) 