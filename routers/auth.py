from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User, RefreshToken
from app.schemas import UserCreate, UserOut, Token, TokenRequest, TokenResponse
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.token_cleanup import cleanup_expired_tokens, cleanup_revoked_tokens, get_token_stats
from app.dependencies import get_current_user, require_role

router = APIRouter()

@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

   user = db.query(User).filter(User.username == form_data.username).first()

   if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )   

   access_token = create_access_token(data={"sub": str(user.id)})
   refresh_token = create_refresh_token(data={"sub": str(user.id)})

   db_refresh_token = RefreshToken(
       user_id=user.id,
       token=refresh_token
   )
   db.add(db_refresh_token)
   db.commit()

   return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(request: TokenRequest, db: Session = Depends(get_db)):

    token_str = request.refresh_token

    token_in_db = db.query(RefreshToken).filter_by(token=token_str).first()
    if not token_in_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    try:
        payload = decode_refresh_token(token_str)
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})

    token_in_db.token = new_refresh_token
    db.commit()

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    

@router.post("/auth/logout")
def logout_user(request: TokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    token_in_db = db.query(RefreshToken).filter_by(token=request.refresh_token).first()

    token_in_db.revoked = True
    db.commit()
    return {"message": "Logged out successfully"}

@router.post("/auth/cleanup-tokens")
def cleanup_tokens_endpoint(current_user: User = Depends(require_role("admin"))):
    try:
        expired_count = cleanup_expired_tokens()
        revoked_count = cleanup_revoked_tokens()
        stats = get_token_stats()
        
        return {
            "message": "Token cleanup completed successfully",
            "expired_tokens_removed": expired_count,
            "revoked_tokens_removed": revoked_count,
            "current_stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token cleanup failed: {str(e)}"
        )

@router.get("/auth/token-stats")
def get_token_statistics(current_user: User = Depends(require_role("admin"))):
  
    try:
        stats = get_token_stats()
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve token statistics"
            )
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get token stats: {str(e)}"
        )