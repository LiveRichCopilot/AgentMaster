# Use an official, secure, and slim Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first to leverage Docker layer caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the port the app runs on
ENV PORT 8080

# Define the command to run the application using a production-ready server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]