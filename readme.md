# Movie Review API

A production-ready REST API for managing movies and user reviews, built with FastAPI and PostgreSQL, including advanced authentication features with JWT, refresh token rotation, secure session management, and role-based access control.

## Features

* **User Authentication**: JWT-based authentication with registration and login
* **Role-Based Access Control**: Admin and regular user roles, restricting movie management operations
* **Refresh Token Rotation**: Stateful refresh tokens with automatic rotation and revocation
* **Logout**: Endpoint to revoke all refresh tokens for a user
* **Movie Management**: Full CRUD operations for movies (restricted by role)
* **Advanced Search**: Multi-layered search with full-text search, fuzzy matching, and relevance ranking
* **Review System**: Users can create, read, update, and delete reviews for movies
* **Database**: PostgreSQL with SQLAlchemy ORM and optimized search indexes
* **Security**: Password hashing with bcrypt, JWT tokens, refresh token storage, input validation, CORS protection
* **Testing**: Comprehensive test suite with pytest

## Setup

### Backend Setup

1. **Install Dependencies**

   ```bash
   # Install in editable mode (recommended)
   pip install -e .

   # OR install from requirements.txt
   pip install -r requirements.txt
   ```

2. **Environment Configuration**

   ```bash
   cp env.example .env

   # Edit .env with your actual values
   DATABASE_URL=postgresql://username:password@localhost/moviedb
   SECRET_KEY=your-super-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

3. **Database Setup**

   * Create a PostgreSQL database named `moviedb`
   * Apply migrations with Alembic: `alembic upgrade head`
   * Seed the database with sample movies: `python -m app.seeding.seed`

4. **Run the Backend**

   ```bash
   uvicorn app.main:app --reload
   ```

### Testing

```bash
pytest -v
```

Includes:

* Root endpoint testing
* User authentication (register/login)
* Movie CRUD operations
* Review CRUD operations

### Database Migrations (Alembic)

```bash
alembic upgrade head
```

## API Endpoints

### Authentication

* `POST /auth/register` - Register a new user
* `POST /auth/login` - Login and get access token and refresh token
* `POST /auth/refresh` - Refresh access token using a refresh token (rotation enabled)
* `POST /auth/logout` - Revoke all refresh tokens for the current user

### Movies

* `GET /movies/` - Get all movies (paginated)
* `GET /movies/search?q={query}` - Search movies with advanced full-text search
* `POST /movies/` - Create a new movie (requires admin role)
* `GET /movies/{movie_id}` - Get a specific movie
* `PUT /movies/{movie_id}` - Update a movie (requires admin role)
* `DELETE /movies/{movie_id}` - Delete a movie (requires admin role)

### Reviews

* `POST /movies/{movie_id}/reviews` - Create a review for a movie (requires authentication)
* `GET /movies/{movie_id}/reviews` - Get all reviews for a movie
* `GET /reviews/{review_id}` - Get a specific review
* `PUT /reviews/{review_id}` - Update a review (requires authentication, owner only)
* `DELETE /reviews/{review_id}` - Delete a review (requires authentication, owner only)

## Advanced Search Functionality

The API includes a sophisticated search system that combines multiple search techniques for optimal results:

### Search Features

* **Full-Text Search**: PostgreSQL's built-in full-text search with ranking
* **Fuzzy Matching**: Trigram similarity for handling typos and partial matches
* **Case-Insensitive Search**: ILIKE fallback for basic pattern matching
* **Relevance Ranking**: Results ordered by relevance score (best matches first)

### Search Implementation

* **Search Vector**: Automatically generated from movie title, genre, and description
* **GIN Index**: High-performance index for fast full-text search queries
* **Multi-layered Search**: Combines three search methods for comprehensive results
* **Minimum Query Length**: Requires at least 1 character to prevent empty searches

### Usage Examples

```bash
# Search for movies by title
GET /movies/search?q=baahubali

# Search for movies by genre
GET /movies/search?q=action

# Search with partial matches
GET /movies/search?q=rrr

# Search with typos (fuzzy matching)
GET /movies/search?q=bahubali
```

### Search Response

Returns a list of movies matching the search query, ordered by relevance:

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

## Security Features

* **Password Hashing**: bcrypt for secure password storage
* **JWT Tokens**: Stateless access tokens
* **Refresh Token Rotation**: Stored in DB, revoked after use
* **Role-Based Access Control**: Restrict movie management actions to admin users
* **Logout**: Revoke all refresh tokens
* **Input Validation**: Pydantic schemas
* **CORS Protection**: Configurable origins
* **SQL Injection Protection**: SQLAlchemy ORM

## Database Models

### User

* `id`: Primary key
* `username`: Unique username
* `email`: Unique email address
* `password_hash`: Hashed password
* `role`: User role (e.g., 'admin', 'user')
* `created_at`: Timestamp

### Movie

* `id`: Primary key
* `title`: Movie title
* `description`: Movie description
* `genre`: Movie genre
* `release_year`: Year of release
* `created_at`: Timestamp

### Review

* `id`: Primary key
* `user_id`: Foreign key to User
* `movie_id`: Foreign key to Movie
* `rating`: Rating (0-10)
* `comment`: Review comment
* `created_at`: Timestamp

### RefreshToken

* `id`: Primary key
* `user_id`: Foreign key to User
* `token`: JWT string
* `created_at`: Timestamp
* `expires_at`: Expiration timestamp
* `revoked`: Boolean flag

## Project Structure

```
MovieReviewAPI/
├── app/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── seeding/
│   │   ├── movies.json
│   │   └── seed.py
│   └── utils.py
├── routers/
│   ├── auth.py
│   ├── movies.py
│   └── reviews.py
├── tests/
├── alembic/
├── Dockerfile
├── env.example
├── pyproject.toml
├── readme.md
└── requirements.txt
```

## Docker

```bash
docker build -t movie-review-api .
docker run --env-file .env -p 8000:8000 movie-review-api
```

## Contributing

We welcome contributions! Follow the steps below to contribute:

### 1. Fork the Repository

* Click the Fork button on the top-right corner of this repo (on GitHub).
* This creates a copy of the project under your GitHub account.

### 2. Clone Your Fork

Clone your forked repository to your local machine:

```bash
git clone https://github.com/<your-username>/FastAPI-webapp.git
cd FastAPI-webapp
```

### 3. Create a New Branch

Always create a new branch before making changes:

```bash
git checkout -b feature/my-feature
```

Replace `feature/my-feature` with something descriptive, like `feature/movie-search` or `bugfix/login-error`.

### 4. Make Your Changes

* Add your new code or fix bugs.
* Stage your changes:

```bash
git add .
```

* Commit with a meaningful message:

```bash
git commit -m "Add movie search functionality with pagination"
```

### 5. Push to Your Fork

Push your branch to your forked repo:

```bash
git push origin feature/my-feature
```

### 6. Open a Pull Request

1. Go to your fork on GitHub.
2. You’ll see a prompt to Open a Pull Request (PR).
3. Select your branch (`feature/my-feature`) and create a PR into the `main` branch of this repository.
4. Add a clear title and description of your changes.

### 7. Code Review & Merge

* The project maintainer (me) will review your PR.
* If everything looks good, it will be merged into the main branch.

### 8. (Optional) Cleanup

After your branch is merged, you can delete it to keep things tidy:

```bash
# Delete branch locally
git branch -d feature/my-feature

# Delete branch from your fork on GitHub
git push origin --delete feature/my-feature
```

---

That’s it! Thanks for contributing to **Movie Review API**

## License

This project is open source and available under the MIT License.
