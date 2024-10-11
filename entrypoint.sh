#!/bin/sh

# Check if the uploads directory exists, if not, initialize it
if [ ! -d "uploads" ]; then
  echo "Uploads folder not found, initializing..."
  cd flask
  mkdir uploads
fi

# Check if the migrations directory exists, if not, initialize it
if [ ! -d "migrations" ]; then
  echo "Migrations folder not found, initializing..."
  cd flask
  flask db init
  flask db migrate -m "Initial migration"
fi

# Apply any pending migrations
flask db upgrade

# return the command passed to the entrypoint
exec "$@"
