web: gunicorn DummyCSV.wsgi & celery --app=DummyCSV worker & wait -n
release: heroku run rake db:migrate
