release: python manage.py migrate
worker: celery -A tamarcado worker -Q celery --loglevel=info
web: gunicorn tamarcado.wsgi