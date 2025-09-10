# Movie Review API

A comprehensive REST API for managing movies and user reviews, built with FastAPI and PostgreSQL, featuring a modern frontend for easy testing and interaction.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Movie Management**: Full CRUD operations for movies
- **Review System**: Users can create, read, update, and delete reviews for movies
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Security**: Password hashing with bcrypt, JWT tokens, input validation

## Setup

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Copy the environment template
   cp env.example .env
   
   # Edit .env with your actual values
   DATABASE_URL=postgresql://username:password@localhost/moviedb
   SECRET_KEY=your-super-secret-key-here
   ```

3. **Database Setup**
   - Create a PostgreSQL database named `moviedb`
   - Update the `DATABASE_URL` in your `.env` file
   - The application will automatically create tables on startup

4. **Run the Backend**
   ```bash
   uvicorn main:app --reload
   ```

## Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Movies
- `GET /movies/` - Get all movies (paginated)
- `POST /movies/` - Create a new movie (requires authentication)
- `GET /movies/{movie_id}` - Get a specific movie
- `PUT /movies/{movie_id}` - Update a movie (requires authentication)
- `DELETE /movies/{movie_id}` - Delete a movie (requires authentication)

### Reviews
- `POST /reviews/movies/{movie_id}/reviews` - Create a review for a movie (requires authentication)
- `GET /reviews/movies/{movie_id}/reviews` - Get all reviews for a movie
- `GET /reviews/reviews/{review_id}` - Get a specific review
- `PUT /reviews/reviews/{review_id}` - Update a review (requires authentication, owner only)
- `DELETE /reviews/reviews/{review_id}` - Delete a review (requires authentication, owner only)

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/moviedb

# Security Configuration
SECRET_KEY=your-super-secret-key-here

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
ENVIRONMENT=development

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Using the API Directly

#### Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "email": "john@example.com", "password": "password123"}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123"
```

#### Create a Movie (with authentication)
```bash
curl -X POST "http://localhost:8000/movies/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "The Matrix", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality.", "genre": "Sci-Fi", "release_year": 1999}'
```

#### Add a Review
```bash
curl -X POST "http://localhost:8000/reviews/movies/1/reviews" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"rating": 9.5, "comment": "Amazing movie with groundbreaking special effects!"}'
```

## Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Input Validation**: Pydantic schemas for request validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **Environment Variables**: Secure configuration management
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Timestamp

### Movie
- `id`: Primary key
- `title`: Movie title
- `description`: Movie description
- `genre`: Movie genre
- `release_year`: Year of release
- `created_at`: Timestamp

### Review
- `id`: Primary key
- `user_id`: Foreign key to User
- `movie_id`: Foreign key to Movie
- `rating`: Rating (0-10)
- `comment`: Review comment
- `created_at`: Timestamp

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error


## License

This project is open source and available under the MIT License.

