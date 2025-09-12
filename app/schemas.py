from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    rating: float
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    comment: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class TokenRequest(BaseModel):
    refresh_token: str
