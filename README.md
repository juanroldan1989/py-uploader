# Py Uploader

The app interacts with a PostgreSQL database, stores files in an S3 bucket, and presents a UI to users.

## S3 Bucket setup

Python script added `(scripts/check_s3_bucket.py)` to:

1. Check S3 Bucket presence
2. Create S3 Bucket if it does not exist yet
3. Return S3 Bucket location

### Usage

1. Environment Variables: The script reads the AWS access key, secret key, and S3 bucket name from environment variables. You can set these in your environment or .env file.

```ruby
export AWS_ACCESS_KEY='your_access_key'
export AWS_SECRET_KEY='your_secret_key'
export S3_BUCKET_NAME='your_bucket_name'
```

2. or set those up within an `.env` file.

3. Make sure `boto3` is installed:

```
pip install boto3
```

4. Trigger script:

```
python check_create_s3_bucket.py
```

## Flask Secret Key

- Always use a strong, unpredictable value for your SECRET_KEY. It should be a long string of random characters.

- You can generate a secret key using tools like Python's secrets module:

```ruby
import secrets

secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string
```

## ENV variables

There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.
