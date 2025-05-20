python3 manage.py collectstatic

docker compose up --build -d

docker-compose exec backend python manage.py makemigrations hospital
docker-compose exec backend python manage.py migrate