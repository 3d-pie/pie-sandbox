# Use a slim Python base image.  Python 3.12 is required by the
# application.  Slim reduces the image size by omitting build tools.
FROM python:3.11-slim

# Set the working directory inside the container.  All subsequent
# commands operate relative to this directory.
WORKDIR /app

# Install system dependencies.  These are kept minimal; add additional
# packages here if your future implementation requires them (e.g.
# build tools for ``trimesh`` or ``Pillow`` may be necessary).
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification and install Python packages.  Installing
# requirements up front takes advantage of Docker layer caching when
# source files change.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source into the image.  This includes
# Python code, templates, migrations and any static files.
COPY . .

# Expose the port that the Flask development server listens on.
EXPOSE 5000

# Set the default command to run the application using the module
# syntax.  The entrypoint script in ``app/__main__.py`` will start
# the Flask development server.
CMD ["python", "-m", "app"]