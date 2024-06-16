FROM python:3.10-slim-buster

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libreoffice \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Copy the credentials file (if needed for Google API)
COPY ./src/auth/Gmail/client_secretfile.json /app/src/auth/Gmail

# Run the application
CMD ["python", "read_excel.py"]
