FROM python:3.9-slim
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn (Fly.io uses $PORT)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "regulatory_intelligence.wsgi:application"]