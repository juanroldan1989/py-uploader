# Dockerfile uses a multi-stage build to separate the build dependencies
# from the runtime dependencies.

# The first stage, named `builder`:
# - installs the build dependencies and
# - copies the requirements file into the container.

# It then installs the Python dependencies into a separate directory (`/install`)
# using the --prefix option for pip.

# This isolates the installed dependencies from the rest of the system
# and allows you to copy only the necessary components to the final image.

# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set the working directory
WORKDIR /app

# Install build dependencies for psycopg2 and other compiled libraries
RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r /app/requirements.txt

# Stage 2: Final stage with only the necessary components
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
