import pytest
from fastapi.testclient import TestClient

from app.core.exceptions import MovieAlreadyExistsException
from app.main import app
from app.models.movie import MovieSchema
from app.services.movies_services import MovieService

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_movie_success(mocker):
    mock_movie = MovieSchema(id=1, title="Test Movie", genre="Horror", director="Test Director", release_year=2021)
    mocker.patch.object(MovieService, 'create_movie', return_value=mock_movie)
    response = client.post("/v1/movies/", json={"id": 1, "title": "Test Movie", "genre": "Horror", "director": "Test Director", "release_year": 2021})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Movie",
        "genre": "Horror",
        "director": "Test Director",
        "release_year": 2021
    }

@pytest.mark.asyncio
async def test_create_movie_already_exists(mocker):
    mocker.patch.object(MovieService, 'create_movie', side_effect=MovieAlreadyExistsException("Test Movie"))
    response = client.post("/v1/movies/", json={"id": 1, "title": "Test Movie", "genre": "Horror", "director": "Test Director", "release_year": 2021})
    assert response.status_code == 400
    assert response.json() == {'detail': "Movie 'Test Movie' already exists."}

@pytest.mark.asyncio
async def test_get_movie_by_id_success(mocker):
    mock_movie = MovieSchema(id=1, title="Test Movie", genre="Horror", director="Test Director", release_year=2021)
    mocker.patch.object(MovieService, 'get_movie_by_id', return_value=mock_movie)
    response = client.get("/v1/movies/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Movie",
        "genre": "Horror",
        "director": "Test Director",
        "release_year": 2021
    }

@pytest.mark.asyncio
async def test_get_movie_by_id_not_found(mocker):
    mocker.patch.object(MovieService, 'get_movie_by_id', return_value=None)
    response = client.get("/v1/movies/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie with ID 1 not found."}

@pytest.mark.asyncio
async def test_update_movie_success(mocker):
    mock_movie = MovieSchema(id=1, title="Test Movie", genre="Horror", director="Test Director", release_year=2021)
    mocker.patch.object(MovieService, 'update_movie', return_value=mock_movie)
    response = client.put("/v1/movies/1", json={"id": 1, "title": "Test Movie", "genre": "Horror", "director": "Test Director", "release_year": 2021})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Movie",
        "genre": "Horror",
        "director": "Test Director",
        "release_year": 2021
    }

@pytest.mark.asyncio
async def test_update_movie_not_found(mocker):
    mocker.patch.object(MovieService, 'update_movie', return_value=None)
    response = client.put("/v1/movies/1", json={"id": 1, "title": "Test Movie", "genre": "Horror", "director": "Test Director", "release_year": 2021})
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie with ID 1 not found."}

@pytest.mark.asyncio
async def test_delete_movie_success(mocker):
    mock_response = {"message": "Movie deleted successfully"}
    mocker.patch.object(MovieService, 'delete_movie', return_value=mock_response)
    response = client.delete("/v1/movies/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Movie deleted successfully"}

@pytest.mark.asyncio
async def test_delete_movie_not_found(mocker):
    mocker.patch.object(MovieService, 'delete_movie', return_value=None)
    response = client.delete("/v1/movies/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie with ID 1 not found."}

@pytest.mark.asyncio
async def test_get_all_movies_success(mocker):
    mock_movies = [
        MovieSchema(id=1, title="Test Movie 1", genre="Horror", director="Test Director", release_year=2021),
        MovieSchema(id=2, title="Test Movie 2", genre="Comedy", director="Test Director", release_year=2021),
    ]
    mocker.patch.object(MovieService, 'get_all_movies', return_value=mock_movies)
    response = client.get("/v1/movies/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Movie 1",
            "genre": "Horror",
            "director": "Test Director",
            "release_year": 2021
        },
        {
            "id": 2,
            "title": "Test Movie 2",
            "genre": "Comedy",
            "director": "Test Director",
            "release_year": 2021
        }
    ]

@pytest.mark.asyncio
async def test_get_all_movies_empty(mocker):
    mocker.patch.object(MovieService, 'get_all_movies', return_value=[])
    response = client.get("/v1/movies/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_movies_by_genre_success(mocker):
    mock_movies = [
        MovieSchema(id=1, title="Test Movie 1", genre="Horror", director="Test Director", release_year=2021),
        MovieSchema(id=2, title="Test Movie 2", genre="Horror", director="Test Director", release_year=2021),
    ]
    mocker.patch.object(MovieService, 'get_movies_by_genre', return_value=mock_movies)
    response = client.get("/v1/movies/genre/Horror")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Movie 1",
            "genre": "Horror",
            "director": "Test Director",
            "release_year": 2021
        },
        {
            "id": 2,
            "title": "Test Movie 2",
            "genre": "Horror",
            "director": "Test Director",
            "release_year": 2021
        }
    ]