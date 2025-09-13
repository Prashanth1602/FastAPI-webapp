# A script to seed the database with initial movie data from a JSON file.

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Movie
import json

def seed_movies():
    db: Session = SessionLocal()
    
    with open("app/movies.json", "r", encoding="utf-8") as f:
        movies_data = json.load(f)

    for movie in movies_data:
        exists = db.query(Movie).filter_by(title=movie["title"]).first()
        if not exists:  
            db.add(Movie(**movie))

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_movies()
    print("Seeding completed!")


    


