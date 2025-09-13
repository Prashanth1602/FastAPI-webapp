# Movie Review API

A **production-ready REST API** for managing movies and user reviews, built with **FastAPI** and **PostgreSQL**, featuring advanced authentication, refresh token rotation, secure session management, role-based access control, and high-performance search capabilities.

![Architecture Diagram](architecture.png)

---

## Badges

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![Redis](https://img.shields.io/badge/Redis-7+-red)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://github.com/actions/workflows/tests.yml/badge.svg)

---

## Features

* **User Authentication**: JWT-based authentication with registration and login
* **Role-Based Access Control**: Admin vs. user privileges
* **Refresh Token Rotation**: Secure session handling with revocation
* **Logout**: Revoke all refresh tokens per user
* **Movie Management**: Full CRUD (Create, Read, Update, Delete) for movies
* **Advanced Search**: Full-text, fuzzy matching, case-insensitive search with Redis caching
* **Redis Caching**: High-performance caching with smart invalidation
* **Review System**: Users can create, edit, and delete reviews
* **Database**: PostgreSQL with SQLAlchemy ORM and optimized search indexes
* **Security**: bcrypt password hashing, JWT tokens, input validation, CORS protection
* **Testing**: Comprehensive test suite with `pytest`

---

## Setup

### 1. Install Dependencies

```bash
# Recommended (editable mode)
pip install -e .

# Or from requirements.txt
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp env.example .env

# Edit .env with your values
DATABASE_URL=postgresql://username:password@localhost/moviedb
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Database Setup

* Create PostgreSQL DB: `moviedb`
* Apply migrations: `alembic upgrade head`
* Seed DB with sample data: `python -m app.seeding.seed`

### 4. Redis Setup

```bash
# macOS
brew install redis
redis-server

# Ubuntu
sudo apt-get install redis-server
redis-server

# Install Redis client
pip install redis
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

### 6. Testing

```bash
pytest -v
```

---

## API Endpoints

### Authentication

* `POST /auth/register` → Register user
* `POST /auth/login` → Login with JWT tokens
* `POST /auth/refresh` → Refresh access token
* `POST /auth/logout` → Logout & revoke tokens
* `POST /auth/cleanup-tokens` → Admin cleanup expired tokens
* `GET /auth/token-stats` → Admin token statistics

### Movies

* `GET /movies/` → List movies (paginated)
* `GET /movies/{id}` → Get movie details
* `POST /movies/` → Add movie (admin only)
* `PUT /movies/{id}` → Update movie (admin only)
* `DELETE /movies/{id}` → Delete movie (admin only)

### Search

* `GET /search?q={query}` → Advanced search (FTS + fuzzy + caching)

### Reviews

* `POST /movies/{id}/reviews` → Add review (auth required)
* `GET /movies/{id}/reviews` → Get all reviews for a movie
* `GET /reviews/{id}` → Get specific review
* `PUT /reviews/{id}` → Update review (owner only)
* `DELETE /reviews/{id}` → Delete review (owner only)

---

## Advanced Search

* **Full-Text Search**: PostgreSQL’s FTS with ranking
* **Fuzzy Matching**: Trigram similarity for typos
* **Case-Insensitive Search**: ILIKE fallback
* **Relevance Ranking**: Results ordered by score
* **Redis Caching**: 5-minute TTL cache

**Example:**

```bash
GET /search?q=baahubali
GET /search?q=rrr
GET /search?q=bahubali   # typo handled
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Baahubali: The Beginning",
    "description": "An adventurous story of two brothers vying for the throne.",
    "genre": "Action/Drama",
    "release_year": 2015
  }
]
```

---

## Architecture

### Module Organization

* **Movies Module** → CRUD + admin ops
* **Search Module** → FTS + fuzzy search + caching
* **Auth Module** → JWT + refresh token handling
* **Reviews Module** → CRUD with ownership validation

**Integration:**

```python
app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/movies")
app.include_router(search_service.router, prefix="/search")
app.include_router(admin_service.router, prefix="/movies")
app.include_router(reviews.router)
```

### Project Structure

```
MovieReviewAPI/
├── app/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── redis_client.py
│   ├── schemas.py
│   ├── seeding/
│   ├── token_cleanup.py
│   └── utils.py
├── routers/
│   ├── auth.py
│   ├── movies.py
│   ├── reviews.py
│   └── services/
│       ├── admin_service.py
│       └── search_service.py
├── tests/
├── alembic/
├── Dockerfile
├── env.example
├── pyproject.toml
├── readme.md
└── requirements.txt
```

---

## Docker Setup

```bash
docker build -t movie-review-api .
docker run --env-file .env -p 8000:8000 movie-review-api
```

---

## Contributing

We welcome contributions from the community! To maintain quality and consistency, please follow these steps:

### 1. Fork the Repository

* Click the **Fork** button on GitHub to create a copy under your account.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/MovieReviewAPI.git
cd MovieReviewAPI
```

### 3. Create a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

* Write clean, modular, and tested code.
* Ensure code follows PEP8 guidelines.
* Add or update relevant tests in `tests/`.

### 5. Commit Changes

```bash
git add .
git commit -m "Add <short-description-of-change>"
```

### 6. Push Changes

```bash
git push origin feature/your-feature-name
```

### 7. Open a Pull Request (PR)

* Go to your fork on GitHub.
* Click **Compare & pull request**.
* Provide a **clear description** of your changes and why they are needed.
* Reference related issues (if any).

### 8. Code Review & Merge

* Your PR will be reviewed by maintainers.
* Suggested changes should be addressed promptly.
* Once approved, it will be merged into the `main` branch.

### 9. Cleanup (Optional)

After merge, clean up your local and remote branches:

```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## License

This project is licensed under the **MIT License**.
