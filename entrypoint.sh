#!/bin/sh

# Check if the migrations directory exists, if not, initialize it
if [ ! -d "migrations" ]; then
    echo "Migrations folder not found, initializing..."
    flask db init
    flask db migrate -m "Initial migration"
fi

# Apply any pending migrations
flask db upgrade

# return the command passed to the entrypoint
exec "$@"
