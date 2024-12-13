FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["celery", "-A core.celery_app", "worker", "-l info", "--concurrency=4"]

CMD ["python",  "manage.py", "runserver", "0:8000"]

#CMD ["gunicorn", "-b 0:8000", "core.django_conf.wsgi", "--workers 8", "--threads 2"]
