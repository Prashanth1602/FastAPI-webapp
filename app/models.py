from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Index, Boolean
from datetime import timedelta  
from sqlalchemy.types import DateTime
from datetime import datetime

from sqlalchemy.dialects.postgresql import TSVECTOR

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='user')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Create an index on username and email for faster lookups
    # This improves performance for login and user search operations
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
    )

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True, index=True)
    release_year = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    search_vector = Column(TSVECTOR)

    # Create indexes for commonly searched fields
    __table_args__ = (
        Index('idx_movie_title', 'title'),
        Index('idx_movie_genre', 'genre'),
        Index('idx_movie_year', 'release_year'),
    )

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Create indexes for foreign keys and commonly queried fields
    # Composite index for finding reviews by movie and user
    __table_args__ = (
        Index('idx_review_user', 'user_id'),
        Index('idx_review_movie', 'movie_id'),
        Index('idx_review_movie_user', 'movie_id', 'user_id'),  # Composite index
        Index('idx_review_rating', 'rating'),
        Index('idx_review_created', 'created_at'),
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    revoked = Column(Boolean, default=False)