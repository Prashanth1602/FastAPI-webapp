from fastapi import FastAPI
from routers import auth, movies, reviews

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/movies", tags=["movies"])
app.include_router(reviews.router)

@app.get("/")
def hello():
    return {"message": "Hello, World....This is Prashanth Surapaneni!"}
