# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# psycopg2 needs to compile against PostgreSQL libraries to provide necessary headers and configurations for this compilation
# And also install system dependencies required to build psycopg2 from source
RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  python3-dev \
  build-essential

# Copy the requirements file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the current directory contents into the container
ADD . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
