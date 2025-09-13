
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import RefreshToken
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_expired_tokens():
  
    db: Session = SessionLocal()
    try:
        current_time = datetime.utcnow()

        expired_tokens = db.query(RefreshToken).filter(
            RefreshToken.expires_at < current_time
        ).all()
        
        if expired_tokens:
            for token in expired_tokens:
                db.delete(token)
            
            db.commit()
            logger.info(f"Cleaned up {len(expired_tokens)} expired refresh tokens")
            return len(expired_tokens)
        else:
            logger.info("No expired tokens found")
            return 0
            
    except Exception as e:
        logger.error(f"Error during token cleanup: {e}")
        db.rollback()
        return -1
    finally:
        db.close()

def cleanup_revoked_tokens():

    db: Session = SessionLocal()
    try:
        revoked_tokens = db.query(RefreshToken).filter(
            RefreshToken.revoked == True
        ).all()
        
        if revoked_tokens:
            for token in revoked_tokens:
                db.delete(token)
            
            db.commit()
            logger.info(f"Cleaned up {len(revoked_tokens)} revoked refresh tokens")
            return len(revoked_tokens)
        else:
            logger.info("No revoked tokens found")
            return 0
            
    except Exception as e:
        logger.error(f"Error during revoked token cleanup: {e}")
        db.rollback()
        return -1
    finally:
        db.close()

def get_token_stats():

    db: Session = SessionLocal()
    try:
        current_time = datetime.utcnow()
        
        total_tokens = db.query(RefreshToken).count()
        expired_tokens = db.query(RefreshToken).filter(
            RefreshToken.expires_at < current_time
        ).count()
        revoked_tokens = db.query(RefreshToken).filter(
            RefreshToken.revoked == True
        ).count()
        active_tokens = total_tokens - expired_tokens - revoked_tokens
        
        stats = {
            "total_tokens": total_tokens,
            "active_tokens": active_tokens,
            "expired_tokens": expired_tokens,
            "revoked_tokens": revoked_tokens
        }
        
        logger.info(f"Token statistics: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Error getting token stats: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting token cleanup...")
    expired_count = cleanup_expired_tokens()
    revoked_count = cleanup_revoked_tokens()
    stats = get_token_stats()
    
    print(f"Cleanup completed:")
    print(f"- Expired tokens removed: {expired_count}")
    print(f"- Revoked tokens removed: {revoked_count}")
    print(f"- Current stats: {stats}")
