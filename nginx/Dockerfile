FROM nginx:latest

COPY default1.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]