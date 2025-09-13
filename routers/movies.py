from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Movie
from app.schemas import MovieResponse
from app.database import get_db
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

