uvicorn api_app:app --port 5000 --reload
uvicorn web_app:app --port 5001 --reload
python3 serv.py

celery -A task.celery worker --loglevel=info
celery -A task.celery beat --loglevel=info
