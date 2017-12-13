web: gunicorn auction.wsgi --log-file -
worker: celery worker -A auction -l info
beat: celery -A auction beat -S django
release: python manage.py migrate

