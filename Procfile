release: python manage.py migrate && python manage.py load_candidates test_candidates.csv
web: gunicorn voting_backend.wsgi --bind 0.0.0.0:$PORT --log-file -
