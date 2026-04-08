FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores para playwright y dependencias de sistema
RUN playwright install --with-deps chromium

COPY . .

CMD ["python", "app.py"]
