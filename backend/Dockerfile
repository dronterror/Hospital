FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY manage.py ./manage.py

ENV DJANGO_SETTINGS_MODULE=hospital_website.settings
ENV PYTHONPATH=/app/backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/staticfiles /app/mediafiles

CMD ["uvicorn", "hospital_website.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
