from flask import Flask, Response

from app.db import db_session


def create_app(test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(404)
    def page_not_found(error):
        return Response("Page not found.", status=404)

    # Init database
    from . import db
    db.init_app(app)

    # Register endpoint
    from . import beers
    app.register_blueprint(beers.bp)

    return app
