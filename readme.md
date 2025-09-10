# Movie Review API

A comprehensive REST API for managing movies and user reviews, built with FastAPI and PostgreSQL, featuring a modern frontend for easy testing and interaction.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Movie Management**: Full CRUD operations for movies
- **Review System**: Users can create, read, update, and delete reviews for movies
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Security**: Password hashing with bcrypt, JWT tokens, input validation
- **Frontend**: Modern web interface built with vanilla HTML, CSS, and JavaScript
- **Documentation**: Automatic API documentation with Swagger/OpenAPI
- **Environment Configuration**: Production-ready environment variable management

## 📁 Project Structure

```
MovieReviewAPI/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and session management
├── models.py               # SQLAlchemy ORM models
├── schemas.py              # Pydantic schemas for request/response validation
├── dependencies.py         # FastAPI dependencies (authentication, etc.)
├── utils.py                # Utility functions (JWT, password hashing)
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── readme.md              # This file
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── movies.py          # Movie management routes
│   └── reviews.py         # Review management routes
└── frontend/              # Frontend application
    ├── index.html         # Complete frontend (HTML + CSS + JS)
    └── README.md          # Frontend documentation
```

## 🛠️ Setup

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

### Frontend Setup

**No installation required!** The frontend is a simple HTML file that can be opened directly in a browser.

1. **Open the Frontend**
   - Simply open `frontend/index.html` in your web browser
   - Or serve it with a simple HTTP server for better CORS handling:
     ```bash
     # Using Python 3
     cd frontend
     python3 -m http.server 3000
     ```

2. **Configure API URL** (if needed)
   - The default API URL is `http://localhost:8000`
   - You can change it in the frontend's API Configuration section

## 🌐 Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Frontend Interface**: Open `frontend/index.html` in your browser

## 📚 API Endpoints

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

## 🎯 Usage Examples

### Using the Frontend (Recommended)

1. **Start the backend**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Open the frontend**:
   - Open `frontend/index.html` in your browser
   - Or serve it with: `cd frontend && python3 -m http.server 3000`

3. **Use the application**:
   - Register a new user and login
   - Add movies and create reviews through the web interface

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

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Input Validation**: Pydantic schemas for request validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **Environment Variables**: Secure configuration management
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🗄️ Database Models

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

## 🎨 Frontend Features

- **Modern Design**: Clean, responsive interface with gradient backgrounds
- **Tabbed Interface**: Organized sections for Authentication, Movies, and Reviews
- **Real-time Feedback**: Status messages and error handling
- **JWT Management**: Automatic token handling and storage
- **API Integration**: Seamless communication with the backend
- **Mobile Responsive**: Works on desktop and mobile devices
- **No Dependencies**: Pure HTML, CSS, and JavaScript - no build tools needed

## 🚀 Development

### Backend Development
```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with specific environment
ENVIRONMENT=development uvicorn main:app --reload
```

### Frontend Development
```bash
# Serve the frontend with a local server (recommended for CORS)
cd frontend
python3 -m http.server 3000
```

## 📊 Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error

## 🔧 Production Deployment

1. **Set Environment Variables**:
   - Use strong, unique `SECRET_KEY`
   - Configure production `DATABASE_URL`
   - Set `ENVIRONMENT=production`

2. **Database**:
   - Use production PostgreSQL instance
   - Consider using database migrations for schema changes

3. **Security**:
   - Use HTTPS in production
   - Configure proper CORS origins
   - Set up proper logging and monitoring

4. **Frontend**:
   - Deploy to any static hosting service (GitHub Pages, Netlify, Vercel, etc.)
   - Update the API URL to point to your production backend
   - Configure backend CORS to allow your frontend domain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check `DATABASE_URL` in `.env`
   - Ensure database exists

2. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Frontend Not Loading**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Use a local server instead of opening the file directly

4. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify SECRET_KEY is set

5. **CORS Errors**
   - Use a local server for the frontend (not file://)
   - Ensure backend CORS includes your frontend URL
   - Check that the API URL is correct

### Getting Help

- Check the API documentation at `/docs`
- Review the logs for error messages
- Ensure all environment variables are set correctly
- Check browser console for frontend errors
