python manage.py migrate
python manage.py update_schedule &
gunicorn apps.wsgi --bind=0.0.0.0:80
