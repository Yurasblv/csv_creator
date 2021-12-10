web: gunicorn DummyCSV.wsgi
celery: celery -A DummyCSV worker -l INFO
release: python manage.py migrate
