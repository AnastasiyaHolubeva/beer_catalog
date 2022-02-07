from app.db import db_session
from app.models import BeerORM
from tests.conftest import Beers


def test_beers_list(client):
    beer = BeerORM(name="Best beer ever", tagline="Test tagline")
    db_session.add(beer)
    db_session.commit()
    response = Beers(client).beers_list()
    assert response.status_code == 200
    assert b"Best beer ever" in response.data


def test_beers_get(client):
    beer = BeerORM(name="Best beer ever", tagline="Test tagline")
    db_session.add(beer)
    db_session.commit()
    response = Beers(client).beer_detail(beer.id)
    assert response.status_code == 200


def test_beers_get_not_found(client):
    response = Beers(client).beer_detail(1)
    assert response.status_code == 404


def test_beers_list_empty(client):
    response = Beers(client).beers_list()
    assert response.status_code == 200
    assert b"" is response.data
