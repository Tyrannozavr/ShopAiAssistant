FROM python:3.12

# Set working directory
WORKDIR /app

# Установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y libpq-dev gcc cron && \
    rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

RUN alembic upgrade head
ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
