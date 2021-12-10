web: gunicorn DummyCSV.wsgi & celery --app=DummyCSV worker & wait -n
release: rake db:migrate
