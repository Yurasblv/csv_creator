web: gunicorn DummyCSV.wsgi
release: python manage.py migrate
worker: celery -A DummyCSV worker -B --loglevel=info


