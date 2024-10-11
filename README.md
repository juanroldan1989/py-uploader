# Py Uploader

The app interacts with a PostgreSQL database, stores files in an S3 bucket, and presents a UI to users.

# Automation pipeline

Deployment is **automated** through **Github Actions** with:

![Screenshot 2024-10-11 at 13 48 52](https://github.com/user-attachments/assets/8412832d-31c8-41fe-8474-d5282280539a)

<img width="1143" alt="Screenshot 2024-10-11 at 13 50 02" src="https://github.com/user-attachments/assets/cba352ae-d3f5-48dc-a19d-314b9ba6cc4f">

1. Flask source code **linting** validation and **tests**
2. Infrastructure provisioning through **Terraform**
3. **Networking** (VPC + Subnets + ALB)
4. **AWS ECS Fargate**: 2 ECS Services with 1 ECS Task each.
5. Docker images **build/tag** process
6. Docker images **validation** through **Trivy** (security) and **Dockle** (best practices)
7. **ECR (Elastic Container Registry)** storing each image with versioning: **py-uploader-flask** and **py-uploader-nginx**
8. **Health checks** included after deployment.
9. **Slack** notifications for success/failures scenarios on Docker images **build/push** workflows.
10. **Slack** notifications for success/failures scenarios on Docker images security and best practices.
11. **Slack** notifications for success/failures scenarios on Deployment.

## Provision Infrastructure

### Docker Images (build/push)

1. Build `nginx` image and push to Docker Hub (or other registry like `ECR`)

```ruby
$ cd nginx

$ docker build -t <username>/py-uploader-nginx .
$ docker push <username>/py-uploader-nginx:latest
```

2. Build `py-uploader` image and push to Docker Hub (or other registry like `ECR`)

```ruby
$ docker build -t <username>/py-uploader-flask .
$ docker push <username>/py-uploader-flask:latest
```

### Terraform

1. Change dir to a project `infra`
2. Run commands:

```ruby
$ terraform init
$ terraform apply
```

3. Check `output` section

```ruby
alb_dns_name = "ecs-alb-<account-id>.<region-id>.elb.amazonaws.com"
```

4. Available endpoints are:

- `GET /upload` -> Upload files to S3 Bucket

- `GET /files` -> List of files uploaded

5. Delete infrastructure

To remove all infrastructure managed by Terraform:

```ruby
$ terraform destroy
```

# Dockerfile

- `docker` folder contains iterations of Dockerfiles with improvements on each step

- `Dockerfile` located at `root` path is the latest and best version because:

1. Enhances security using `nonroot` user and `controlled permissions`.
2. Keeps the image size small implementing a `multi-stage` build and reduced `apt-get` usage.

# Development

```ruby
$ docker-compose up
```

Access: `http://localhost:5000`

1. Upload file
2. Check S3 bucket
3. Adjust source code as needed within `flask` folder.
4. Run `docker-compose up` again

### ENV variables

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

### S3 Bucket setup

Python script added `(scripts/check_s3_bucket.py)` to:

1. Check S3 Bucket presence
2. Create S3 Bucket if it does not exist yet
3. Return S3 Bucket location

#### Usage

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

### Database

#### Docker Compose

`docker-compose.yaml` file already provides everything needed for database setup

```ruby
$ docker-compose up
```

Access: `http://localhost:5000`

#### Local setup

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

### WSGI

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

### Flask Secret Key

- Always use a strong, unpredictable value for your SECRET_KEY. It should be a long string of random characters.

- You can generate a secret key using tools like Python's secrets module:

```ruby
import secrets

secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string
```
