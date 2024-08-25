# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Gunicorn log setup. I have issues with gunicorn wiht docker for now
RUN mkdir -p /var/log/gunicorn /var/run/gunicorn && \
    touch /var/log/gunicorn/access.log /var/log/gunicorn/error.log && \
    chown -R www-data:www-data /var/log/gunicorn /var/run/gunicorn

# Create an entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run Gunicorn as the application server
#CMD ["gunicorn", "-c", "gunicorn.conf.py"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
