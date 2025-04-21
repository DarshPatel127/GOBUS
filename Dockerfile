# Use an official Python runtime as a parent image
FROM python:3.9-slim

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

# Expose port 8000 (the default port for Django)
EXPOSE 8000

# Run the Django application using gunicorn
CMD ["gunicorn", "P2.wsgi:application", "--bind", "0.0.0.0:8000","--workers", "3"]
