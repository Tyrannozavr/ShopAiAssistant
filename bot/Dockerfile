FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip

COPY . .
RUN pip install -r requirements.txt

# Set the PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app
CMD ["python", "app/main.py"]
