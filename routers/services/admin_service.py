from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models import Movie, User
from app.schemas import MovieCreate, MovieResponse
from app.database import get_db
from app.dependencies import require_role
from app.redis_client import clear_search_cache, invalidate_movie_cache
from sqlalchemy import func

router = APIRouter()

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role("admin"))
):
    new_movie = Movie(
        title=movie.title,
        description=movie.description,
        genre=movie.genre,
        release_year=movie.release_year
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    
    clear_search_cache()
    
    return new_movie

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, 
    movie: MovieCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    old_title = db_movie.title
    
    db_movie.title = movie.title
    db_movie.description = movie.description
    db_movie.genre = movie.genre
    db_movie.release_year = movie.release_year
    
    db.commit()
    db.refresh(db_movie)

    invalidate_movie_cache(old_title)
    if old_title != movie.title:
        invalidate_movie_cache(movie.title)
    
    return db_movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_title = movie.title
    
    db.delete(movie)
    db.commit()
    
    invalidate_movie_cache(movie_title)
    
    return None

