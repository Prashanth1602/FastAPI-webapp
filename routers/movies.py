from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Movie, User
from app.schemas import MovieCreate, MovieResponse, MovieSearchResponse
from app.database import get_db
from app.dependencies import get_current_user, require_role
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
    return new_movie

@router.get("/", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@router.get("/search", response_model=List[MovieSearchResponse])
def search_movies(db: Session = Depends(get_db), q: str = Query(..., min_length=1)):
    ts_query = func.plainto_tsquery(q)

    results = db.query(
        Movie,
        func.coalesce(
            func.ts_rank_cd(Movie.search_vector, ts_query),
            func.similarity(Movie.title, q)
        ).label("score")
    ).filter(
        (Movie.search_vector.op('@@')(ts_query)) |
        (Movie.title.ilike(f"%{q}%")) |
        (func.similarity(Movie.title, q) > 0.2)
    ).order_by(
        func.coalesce(
            func.ts_rank_cd(Movie.search_vector, ts_query),
            func.similarity(Movie.title, q)
        ).desc()
    ).all()

    if not results:
        raise HTTPException(status_code=404, detail="No movies found matching")

    return [r[0] for r in results]

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

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
    
    db_movie.title = movie.title
    db_movie.description = movie.description
    db_movie.genre = movie.genre
    db_movie.release_year = movie.release_year
    
    db.commit()
    db.refresh(db_movie)
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
    
    db.delete(movie)
    db.commit()
    return None

