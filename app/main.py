from fastapi import FastAPI
from routers import auth, movies, reviews
from routers.services import search_service, admin_service

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/movies")
app.include_router(reviews.router)
app.include_router(search_service.router, prefix="/search")
app.include_router(admin_service.router, prefix="/movies")

@app.get("/")
def hello():
    return {"message": "Hello, World....This is Prashanth Surapaneni!"}
