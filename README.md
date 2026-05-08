# Train Track Admin API

A FastAPI backend for managing trains, lines, and track segments with JWT authentication.

## Features

- CRUD operations for trains, lines, and tracks
- JWT authentication with bcrypt password hashing
- MongoDB with async Motor driver
- Input validation with Pydantic
- Aggregation endpoints for line summaries
- Comprehensive test suite with pytest
- Docker support

## Tech Stack

- FastAPI
- MongoDB / Motor
- Pydantic
- JWT (python-jose)
- bcrypt (passlib)
- pytest / httpx
- Docker

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── auth/         # JWT authentication
│   ├── models/       # Domain models
│   ├── schemas/      # Pydantic schemas
│   ├── repositories/ # Data access layer
│   ├── services/     # Business logic layer
│   ├── database/     # Database connection
│   ├── core/         # Configuration
│   └── main.py       # FastAPI app
├── tests/            # Test suite
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Setup

### Local Development

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start MongoDB (using Docker):
```bash
docker run -d -p 27017:27017 --name mongodb mongo:6
```

4. Run the API:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at http://localhost:8000

### Using Docker

```bash
docker-compose up --build
```

API will be available at http://localhost:8000

## API Endpoints

### Authentication

- `POST /auth/register` - Register a user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Trains (Protected)

- `POST /trains` - Create a train
- `GET /trains` - List all trains
- `GET /trains/{id}` - Get train details
- `PUT /trains/{id}` - Update a train
- `DELETE /trains/{id}` - Delete a train

### Lines (Protected)

- `POST /lines` - Create a line
- `GET /lines` - List all lines
- `GET /lines/{id}` - Get line details
- `PUT /lines/{id}` - Update a line
- `DELETE /lines/{id}` - Delete a line

### Tracks (Protected)

- `POST /tracks` - Create a track
- `GET /tracks` - List tracks (supports filters: line, elevation, bending)
- `GET /tracks/{id}` - Get track details
- `PUT /tracks/{id}` - Update a track
- `DELETE /tracks/{id}` - Delete a track
- `GET /lines/{id}/summary` - Get line summary (total length, avg elevation, max elevation, avg bending, track count)

## Running Tests

```bash
cd backend
pytest tests/ -v
```

## Domain Models

### Train
- `weight` (int, > 0)
- `train_cars` (int, > 0)

### Line
- `name` (string, unique, non-empty)

### Track
- `id_line` (UUID, must reference existing line)
- `length` (int, > 0)
- `bending` (int, >= 0)
- `elevation` (int, positive or negative)

## Validation

All inputs are validated using Pydantic models:
- Positive integer validation
- UUID validation
- String sanitization
- Duplicate line name prevention

## Error Handling

Standard error response format:
```json
{
  "detail": "Error description"
}
```

HTTP Status Codes:
- 200 - Success
- 201 - Created
- 400 - Validation Error
- 401 - Unauthorized
- 404 - Not Found
- 409 - Conflict
- 500 - Internal Server Error

## Security

- Passwords hashed with bcrypt
- JWT access tokens with configurable expiration
- Protected routes require valid Bearer token
- Role-ready architecture for future expansion

## Environment Variables

- `MONGODB_URL` - MongoDB connection string
- `DATABASE_NAME` - MongoDB database name
- `SECRET_KEY` - JWT signing secret
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## Performance

- Async API endpoints
- MongoDB indexes on frequently queried fields
- Optimized aggregation pipelines
- Designed for high concurrency

## License

MIT