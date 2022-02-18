import click
from flask.cli import with_appcontext
from pydantic import parse_raw_as
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, registry

from app.config import SQLALCHEMY_DATABASE_URI
from app.utils.scraper import get_beers

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base: registry = declarative_base()
Base.query = db_session.query_property()


def init_db() -> None:
    import app.models
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    import app.models
    db_session.remove()
    Base.metadata.drop_all(bind=engine)


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('upload-data')
@with_appcontext
def upload_data_command() -> None:
    """Fill database with data."""
    from app.models import BeerModel
    from app.models import BeerORM

    # Upload objects from external API
    beers_bytes = get_beers()
    beers_list = parse_raw_as(list[BeerModel], beers_bytes)
    beers = [BeerORM(**beer.dict()) for beer in beers_list]
    try:
        db_session.bulk_save_objects(beers)
    except IntegrityError:
        click.echo("Data already uploaded.")
    else:
        db_session.commit()
        click.echo('Data was successfully uploaded.')


def init_app(app) -> None:
    app.cli.add_command(init_db_command)
    app.cli.add_command(upload_data_command)
