FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install requests

# Buat volume untuk database SQLite
RUN mkdir -p /data

CMD ["python", "app.py"]
