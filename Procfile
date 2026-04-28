web: python manage.py migrate && python manage.py load_candidates test_candidates.csv --force && gunicorn voting_backend.wsgi --bind 0.0.0.0:$PORT --timeout 300 --log-file -
