"""Entry point for launching the Flask application.

Running ``python -m app`` will execute this module and start the
development server.  The server binds to all interfaces on port 5000
by default.
"""

from . import create_app


app = create_app()


def main() -> None:
    """Run the Flask development server."""
    # When invoked as ``python -m app`` this function will be called to
    # start the built‑in development server.  In a production setting
    # this file would not be used; instead, a WSGI server such as
    # Gunicorn would load the ``app`` object directly.
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()