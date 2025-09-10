from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Review, Movie, User
from schemas import ReviewCreate, ReviewOut, ReviewUpdate
from database import get_db
from dependencies import get_current_user

router = APIRouter()

@router.post("/movies/{movie_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    movie_id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing_review = db.query(Review).filter(
        Review.movie_id == movie_id, 
        Review.user_id == current_user.id
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=400, 
            detail="You have already reviewed this movie. Update your existing review instead."
        )

    if review_in.rating < 0 or review_in.rating > 10:
        raise HTTPException(
            status_code=400, 
            detail="Rating must be between 0 and 10"
        )

    new_review = Review(
        user_id=current_user.id,
        movie_id=movie_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/movies/{movie_id}/reviews", response_model=List[ReviewOut])
def get_movie_reviews(
    movie_id: int, 
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 20
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    reviews = (
        db.query(Review)
        .filter(Review.movie_id == movie_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return reviews

@router.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/reviews/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only update your own reviews"
        )

    if review_in.rating is not None:
        if review_in.rating < 0 or review_in.rating > 10:
            raise HTTPException(
                status_code=400, 
                detail="Rating must be between 0 and 10"
            )
        review.rating = review_in.rating
    
    if review_in.comment is not None:
        review.comment = review_in.comment

    db.commit()
    db.refresh(review)
    return review

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only delete your own reviews"
        )

    db.delete(review)
    db.commit()
    return None
