# Use an official Python runtime as a parent image
FROM python:3.9-slim AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Collect static files (they will be placed in /app/staticfiles)
RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expose port 8000 (the default port for Django)
EXPOSE 8000

USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run the Django application using gunicorn
CMD ["gunicorn", "GOBUS.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
