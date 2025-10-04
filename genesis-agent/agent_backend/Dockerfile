
# Stage 1: Build the React frontend
FROM node:18-alpine AS build

# Set the working directory for the frontend build
WORKDIR /app/frontend

# Copy package files first to leverage Docker layer caching
COPY switch-live-agent/frontend/package.json ./package.json
COPY switch-live-agent/frontend/yarn.lock ./yarn.lock

# Install dependencies
RUN yarn install

# Copy the rest of the frontend source code
COPY switch-live-agent/frontend/ ./

# Build the frontend application
RUN yarn build

# --- VERIFICATION STEP ---
# This command will cause the build to fail if the 'build' directory was not created.
RUN ls /app/frontend/build


# Stage 2: The final production image
FROM python:3.9-slim

# Set the working directory for the final application
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the verified frontend build assets from the previous stage
COPY --from=build /app/frontend/build ./build

# Copy the backend requirements and source code
COPY live-agent-source/requirements.txt .
COPY live-agent-source/streaming-live-api-server.py .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the server will run on
EXPOSE 8080

# Command to run the backend server
CMD ["uvicorn", "streaming-live-api-server:app", "--host", "0.0.0.0", "--port", "8080"]
