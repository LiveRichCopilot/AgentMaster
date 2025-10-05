# Use an official, secure, and slim Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the application source code
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "streaming-live-api-server.py"]
