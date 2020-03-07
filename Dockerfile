FROM python:3.8-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]
