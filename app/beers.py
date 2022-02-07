from flask import (
    Blueprint, Response
)
from werkzeug.exceptions import NotFound

from app.db import db_session
from app.models import BeerORM, BeerList, BeerModel

bp = Blueprint('beers', __name__, url_prefix='/beers')


@bp.route('/', methods=('GET',))
def beers_list() -> Response:
    """Get beers list response."""
    beers = db_session.query(BeerORM).all()
    if not beers:
        return Response()
    beer_obj_list = BeerList.from_orm(beers)
    response = Response(beer_obj_list.json())
    return response


@bp.route('/<int:pk>/', methods=('GET',))
def beer_detail(pk: int) -> Response:
    """Get beers detail response."""
    beer = db_session.query(BeerORM).get(pk)
    if not beer:
        raise NotFound
    beer_obj = BeerModel.from_orm(beer)
    response = Response(beer_obj.json())
    return response
