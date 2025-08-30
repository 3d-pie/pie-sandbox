"""Alembic environment configuration.

This file configures Alembic for the Flask application.  It exposes
``target_metadata`` from the application's SQLAlchemy models and
provides offline and online migration runners.  The environment is
generated manually to keep the scaffold lean; real migrations should
be authored by a human using the Alembic CLI.
"""

from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.models import db


# Load configuration from the Alembic ``alembic.ini`` file.  This
# configuration is not included in the scaffold; instead, the
# ``sqlalchemy.url`` option is pulled from the Flask config via an
# environment variable when running migrations.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata for 'autogenerate' support
target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be
    available.

    Calls to ``context.execute()`` here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        # Fall back to the default SQLite database used by the app
        url = "sqlite:///sandbox.db"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    configuration = config.get_section(config.config_ini_section) or {}
    url = configuration.get("sqlalchemy.url") or os.getenv("SQLALCHEMY_URL")
    if not url:
        # Default to the application's SQLite DB
        url = "sqlite:///sandbox.db"
    configuration["sqlalchemy.url"] = url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()