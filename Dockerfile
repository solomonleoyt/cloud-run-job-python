# Use Python 3.10.16-slim as base image
FROM python:3.10.16-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt and the Python script
COPY requirements.txt .
COPY main.py .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "main.py"]
