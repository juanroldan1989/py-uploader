# Py Uploader

The app interacts with a PostgreSQL database, stores files in an S3 bucket, and presents a UI to users.

## Startup

```ruby
$ docker-compose up
```

Access: `http://localhost:5000`

1. Upload file
2. Check S3 bucket
3. Adjust source code as needed
4. Run `docker-compose up` again

## ENV variables

You can set these in your environment or .env file.

```ruby
# Flask settings
FLASK_SECRET = 'flask_secret key'

# AWS credentials
AWS_ACCESS_KEY = 'aws_access_key'
AWS_SECRET_KEY = 'aws_secret_key'
S3_BUCKET_NAME = 's3_bucket_name'

# PostgreSQL settings
POSTGRES_USER = 'postgres_user'
POSTGRES_PASSWORD = 'postgres_password'
POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'postgres_db'
```

## S3 Bucket setup

Python script added `(scripts/check_s3_bucket.py)` to:

1. Check S3 Bucket presence
2. Create S3 Bucket if it does not exist yet
3. Return S3 Bucket location

### Usage

1. Make sure `boto3` is installed:

```ruby
pip install boto3
```

2. Trigger script:

```ruby
# Usage:
python check_s3_bucket.py

# Input:
Enter a unique bucket name: my-unique-bucket

# Output:
Checking if bucket 'my-unique-bucket' exists ...

Bucket 'my-unique-bucket' does not exist. Creating bucket ...
Bucket 'my-unique-bucket' created sucessfully.
Bucket URL: https://my-unique-bucket.s3.amazonaws.com/
```

## Flask Secret Key

- Always use a strong, unpredictable value for your SECRET_KEY. It should be a long string of random characters.

- You can generate a secret key using tools like Python's secrets module:

```ruby
import secrets

secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string
```

## Database

### Docker Compose

`docker-compose.yaml` file already provides everything needed for database setup

```ruby
$ docker-compose up
```

Access: `http://localhost:5000`

### Local setup

If `postgres_db` does not exist, you can create it manually. Open a terminal and connect to `PostgreSQL`:

```ruby
psql -U your_postgres_username
```

Then create the postgres_db:

```ruby
CREATE DATABASE postgres_db;
```

Then check for connection to the database:

```ruby
psql -U postgres_user -d postgres_db

postgres_db=# \dt
```

## WSGI

To improve the production-readiness of the `Flask` application, an `WSGI` server like `Gunicorn` is added.

Gunicorn is a Python WSGI HTTP server that serves Flask applications more efficiently in production environments.

1. Add `gunicorn==x.x.x` within `requirements.txt`
2. Add WSGI Entry point:

```ruby
# wsgi.py

from app import app

if __name__ = "__main__":
  app.run()
```
