FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python",  "manage.py", "runserver", "0:8000"]

#CMD ["gunicorn", "-b 0:8000", "core.django_conf.wsgi", "--workers 4", "--threads 2"]
