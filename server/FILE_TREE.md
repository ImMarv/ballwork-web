# Server Directory Tree

```
server/
├── .env
├── .vscode/
├── __init__.py
├── __pycache__/
├── README.md
├── alembic.ini
├── alembic/
│   ├── README
│   ├── __pycache__/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── __pycache__/
├── app/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── core/
│   │   ├── __pycache__/
│   │   └── settings.py
│   ├── db.py
│   ├── db_base/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   └── base.py
│   ├── logging.py
│   ├── main.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── digest/
│   │   │   ├── __init__.py
│   │   │   └── models/
│   │   │       └── dto/
│   │   │           └── db/
│   │   ├── stats/
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── api.py
│   │   │   ├── deps.py
│   │   │   ├── mappers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   └── mappers.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── db/
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   └── dbmodels.py
│   │   │   │   └── dto/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── __pycache__/
│   │   │   │       ├── api_error.py
│   │   │   │       ├── competition.py
│   │   │   │       ├── country.py
│   │   │   │       ├── home_away.py
│   │   │   │       ├── player.py
│   │   │   │       └── team.py
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── api_football.py
│   │   │   │   └── ifootball_provider.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   └── users/
│   │       └── __init__.py
│   ├── requirements.txt
│   └── shared/
└── tests/
    ├── __init__.py
    ├── __pycache__/
    ├── digest/
    │   └── __init__.py
    ├── stats/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   ├── mock_204_response.json
    │   ├── mock_500_response.json
    │   ├── mock_competition_response.json
    │   ├── mock_country_response.json
    │   ├── mock_player_response.json
    │   ├── mock_provider.py
    │   ├── mock_team_response.json
    │   └── test_stats.py
    └── users/
        └── __init__.py
```

## Directory Summary

- **alembic/**: Database migration configuration and versions
- **app/**: Main application code
  - **core/**: Core settings and configuration
  - **db_base/**: Database base classes and models
  - **modules/**: Feature modules (digest, stats, users)
  - **shared/**: Shared utilities and helpers
- **tests/**: Test files organized by module
- **Configuration files**: `.env`, `alembic.ini`, `requirements.txt`
