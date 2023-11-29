celery -A src.celery.app worker  -l info --concurrency=2 &
celery -A src.celery.app flower -l info & celery -A src.celery.app beat -l INFO &
uvicorn app.main:app --host 0.0.0.0 --reload --workers 2