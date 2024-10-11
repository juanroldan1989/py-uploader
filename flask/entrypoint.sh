#!/bin/sh

# Check if the flask/uploads directory exists, if not, initialize it
if [ ! -d "flask/uploads" ]; then
  echo "Uploads folder not found, initializing..."
  cd flask
  mkdir uploads
  cd ..
  echo "Uploads folder created"
fi

# Check if the flask/migrations directory exists, if not, initialize it
if [ ! -d "flask/migrations" ]; then
  cd flask
  echo "Migrations folder not found, initializing..."
  flask db init
  flask db migrate -m "Initial migration"
  cd ..
  echo "Migrations folder created"
fi

# Apply any pending migrations
cd flask
flask db upgrade

# return the command passed to the entrypoint
exec "$@"
