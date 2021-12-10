web: gunicorn DummyCSV.wsgi & celery --app=DummyCSV worker & wait -n
release: python manage.py migrate
