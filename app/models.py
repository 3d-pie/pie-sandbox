"""SQLAlchemy models for the Flask application.

This module defines the ``User`` and ``Item`` models that back the
authentication system and the uploaded items respectively.  The models
are intentionally simple and leave room for future migrations (e.g.
replacing boolean flags with proper role and permission tables).
"""

from flask_sqlalchemy import SQLAlchemy


# Instantiate a global SQLAlchemy object.  It will be bound to the
# Flask application in ``app/__init__.py`` via ``db.init_app(app)``.
db = SQLAlchemy()


class User(db.Model):
    """A user of the system.

    The model stores a username and password along with two legacy
    boolean flags.  These flags are intended to be replaced by a
    full role‑based access control implementation in a later
    migration.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # Legacy flags – will be migrated by a human developer
    is_admin = db.Column(db.Boolean, default=False)
    is_primary_admin = db.Column(db.Boolean, default=False)


class Item(db.Model):
    """An uploaded model or G‑Code file.

    ``filename`` stores the original file name supplied by the user.
    ``meta`` is a JSON column used to store arbitrary metadata such as
    G‑Code statistics or the relative path to a generated thumbnail.
    """

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    meta = db.Column(db.JSON, default=dict)  # holds gcode stats + thumb path