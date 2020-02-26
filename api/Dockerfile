FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python-dev mariadb-dev python3-dev gcc libc-dev

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=api.settings.development"]
