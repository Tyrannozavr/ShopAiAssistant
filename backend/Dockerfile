FROM python:3.12

# Set working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc cron postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Wait for the database to be ready before running migrations
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
CMD ["/bin/sh", "-c", "/wait-for-it.sh db alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
#CMD ["/bin/sh", "-c", "/wait-for-it.sh db alembic upgrade head"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]