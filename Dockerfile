# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Redis server and its client tools
# apt-get update is necessary before installing new packages
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed Python packages
# Now including prometheus_client and redis-py for connecting to Redis
RUN pip install -r requirements.txt --no-cache-dir

# Make port 5000 (Flask) and 6379 (Redis) available to the world outside this container
EXPOSE 5000
EXPOSE 6379

# Use a wrapper script to start both Gunicorn and Redis server
# This is a common pattern when running multiple processes in a single container
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Run the start.sh script when the container launches
CMD ["/usr/local/bin/start.sh"]
