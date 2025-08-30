"""Application factory for the Flask app.

This module sets up the Flask application, configures the SQLAlchemy
database and registers blueprints.  It intentionally avoids any heavy
business logic or side effects so that human developers can layer in
additional functionality later.
"""

from flask import Flask

from .models import db  # initialise the SQLAlchemy extension
from .routes import bp  # blueprint containing all routes


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        A configured :class:`flask.Flask` instance.
    """
    app = Flask(__name__)

    # Basic configuration.  The database lives in the project root and
    # file uploads are stored in the ``uploads`` directory.  A
    # development secret key is set for session cookies; production
    # deployments should override this via environment variables.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sandbox.db'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SECRET_KEY'] = 'dev'

    # Initialise the database extension and create tables on first boot.
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints defined in routes.py.  All routes live under
    # the main blueprint.
    app.register_blueprint(bp)

    return app