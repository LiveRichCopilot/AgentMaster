# Use an official, secure, and slim Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first to leverage Docker layer caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# The CMD instruction will use the PORT variable provided by Cloud Run at runtime.
# We use the shell form of CMD to allow for environment variable substitution.
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}