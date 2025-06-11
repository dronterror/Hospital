#!/bin/sh

# Wait for postgres
echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
END

# Set up initial Wagtail pages
python manage.py setup_initial_data

echo "Migrations and initial setup completed successfully" 