# Dockerfile enhances security while keeping the image size small.

# Non-root User:
# The nonrootuser is created with its own home directory.
# The application will run as this non-root user,
# which is a standard security measure to prevent privilege escalation in the event of an exploit.

# Controlled Permissions:
# The COPY command uses --chown to ensure that the non-root user owns the application files.
# This helps avoid issues where root is the owner but
# the application is running as a non-root user.

# Reduced apt-get usage:
# Installed only necessary packages (e.g., libpq5) in the final image,
# ensuring minimal exposure to security vulnerabilities in unused packages.

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

# Copy the requirements file (`flask` folder) and install dependencies
COPY /flask/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r /app/requirements.txt

# Stage 2: Final stage with only the necessary components
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group, and set permissions
RUN useradd -m -d /home/nonrootuser nonrootuser
USER nonrootuser

# Copy only the installed dependencies from the builder stage, adjust ownership
COPY --from=builder --chown=nonrootuser:nonrootuser /install /usr/local

# Copy the application code (`flask` folder) and set correct ownership and permissions
COPY --chown=nonrootuser:nonrootuser /flask /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Use non-root user to run the application
USER nonrootuser

# Set the entrypoint to run the script
ENTRYPOINT ["/app/entrypoint.sh"]

# Run the Flask application
# CMD ["flask", "run"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
