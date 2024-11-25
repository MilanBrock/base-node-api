# Dockerfile
FROM python:3.8-slim

# Install dependencies
RUN pip install openai loguru requests click

# Copy your Python script into the container
COPY script.py /app/script.py

# Set the working directory
WORKDIR /app

# Set the entrypoint
ENTRYPOINT ["python", "script.py"]
