# Ballwork Web - Server

A FastAPI-based backend for football (soccer) statistics tracking and analysis. This application uses a modular architecture to fetch, manage, and serve football player and team statistics from external APIs.

## Getting Started

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. Navigate to the server directory:
```bash
cd server
```

2. Install dependencies:
```bash
pip install -r app/requirements.txt
```

3. Create a `.env` file in the `server/` directory with your configuration:
```env
API_FOOTBALL_KEY=your_api_key_here
```

### Running the Application

Start the development server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Modules

### Stats Module

Handles football statistics retrieval and management.

**Endpoints:**
- `GET /stats/players/{player_id}` - Get player statistics
- `GET /stats/teams/{team_id}` - Get team statistics

**Providers:**
- **ApiFootball** - External provider for football statistics
- Custom providers can implement the `IFootballProvider` interface

### Digest Module

Manages statistics digests and summaries.

### Users Module

Handles user management and authentication.

## Testing

Run the test suite:
```bash
pytest server/tests/
```

Run specific module tests:
```bash
pytest server/tests/stats/
```

With coverage:
```bash
pytest --cov=app server/tests/
```

## Configuration

Configuration is managed through environment variables in the `.env` file:

- `API_FOOTBALL_KEY` - API key for external football statistics provider
- `DEBUG` - Enable debug mode (optional)

See [core/settings.py](app/core/settings.py) for all available settings.

## Development Guidelines

### Adding New Modules

1. Create a new directory under `app/modules/<module_name>`
2. Implement the module structure following the modulith pattern:
   - `api.py` - Route handlers
   - `service.py` - Business logic
   - `repository.py` - Data access
   - `models/` - Data models
   - `providers/` - External integrations (if needed)

3. Register the router in `app/main.py`

### Code Organization

- **Keep modules independent** - No cross-module imports
- **Business logic in services** - API handlers should be thin
- **Data access through repositories** - No direct DB calls elsewhere
- **External integrations as providers** - Keep them abstracted behind interfaces

## Dependencies

See [requirements.txt](app/requirements.txt) for the complete list:
- `fastapi` - Web framework
- `httpx` - Async HTTP client
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variable loading

## Troubleshooting

### Import Errors

If you encounter import errors when running tests:
- Ensure `__init__.py` files exist in all Python packages
- Use relative imports in test modules: `from .mock_provider import ...`
- Make sure the project root is in your Python path

### API Football Provider Issues

- Verify `API_FOOTBALL_KEY` is set in your `.env` file
- Check API rate limits and quota
- Review API documentation at [api-football.com](https://www.api-football.com/)

## License

See [LICENSE](../LICENSE) for details.

## Contributing

When contributing, maintain adherence to the architectural rules and testing standards outlined in this document.
