
def test_root_hello(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_auth_register_and_login(client):
    r = client.post("/auth/register", json={
        "username": "prashanth", "email": "prashanth@gmail.com", "password": "pg123"
    })
    assert r.status_code == 201

    r = client.post("/auth/login", data={"username": "prashanth", "password": "pg123"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"


def test_movies_crud_flow(client):
    r = client.post("/movies/", json={"title": "Little Hearts", "genre": "Rom-Com"})
    assert r.status_code == 201
    movie_id = r.json()["id"]

    r = client.get("/movies/")
    assert r.status_code == 200

    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 200

    r = client.put(f"/movies/{movie_id}", json={"title": "Little Hearts", "genre": "Comedy"})
    assert r.status_code == 200
    assert r.json()["genre"] == "Comedy"

    r = client.delete(f"/movies/{movie_id}")
    assert r.status_code == 204

    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 404


def test_reviews_flow(client):
    # Create movie
    r = client.post("/movies/", json={"title": "Little Hearts"})
    movie_id = r.json()["id"]

    # Create review
    r = client.post(f"/movies/{movie_id}/reviews", json={"rating": 9.5, "comment": "Good movie"})
    assert r.status_code == 201
    review_id = r.json()["id"]

    # Duplicate should fail
    r = client.post(f"/movies/{movie_id}/reviews", json={"rating": 9.5})
    assert r.status_code == 400

    # List
    r = client.get(f"/movies/{movie_id}/reviews")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Get
    r = client.get(f"/reviews/{review_id}")
    assert r.status_code == 200

    # Update
    r = client.put(f"/reviews/{review_id}", json={"rating": 9.0})
    assert r.status_code == 200
    assert r.json()["rating"] == 9.0

    # Delete
    r = client.delete(f"/reviews/{review_id}")
    assert r.status_code == 204

    # After delete
    r = client.get(f"/reviews/{review_id}")
    assert r.status_code == 404
