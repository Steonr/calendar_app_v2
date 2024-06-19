# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies and tzdata for timezone configuration
RUN apt-get update && apt-get install -y \
    tzdata

# Set the timezone
ENV TZ=Europe/Brussels

# Copy the requirements file into the container
COPY ../requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY .. .

# Ensure the secret file is copied to the correct location
COPY ../src/auth/Gmail/client_secretfile.json /app/src/auth/Gmail/client_secretfile.json

# Set the PYTHONPATH environment variable
ENV PYTHONPATH="/app"

# Run the application
CMD ["python", "-m", "src.main"]
