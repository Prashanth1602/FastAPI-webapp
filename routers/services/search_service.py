
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Movie
from app.schemas import MovieSearchResponse
from app.database import get_db
from sqlalchemy import func
from app.redis_client import get_cached, set_cache

router = APIRouter()

@router.get("/", response_model=List[MovieSearchResponse])
def search_movies(db: Session = Depends(get_db), q: str = Query(..., min_length=1)):

    cached = get_cached(q.lower())
    if cached:
        return cached

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

    movies =  [r[0] for r in results]

    set_cache(q.lower(), [MovieSearchResponse.from_orm(m).dict() for m in movies])

    return movies