FROM python:3.10-slim

WORKDIR /app

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.py .

ENTRYPOINT ["python", "/app/entrypoint.py"]