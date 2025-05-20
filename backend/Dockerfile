FROM python:3.11-slim

WORKDIR /app

COPY manage.py .

COPY backend backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=hospital_website.settings
ENV PYTHONPATH=/app
ENV PYTHONPATH=/app/backend

RUN python manage.py collectstatic --noinput

CMD ["uvicorn", "hospital_website.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
