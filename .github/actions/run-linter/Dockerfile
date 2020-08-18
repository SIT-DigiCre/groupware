FROM python:latest

RUN pip install --upgrade pip
RUN pip install flake8

COPY entrypoint.sh /entrypoint.sh
RUN chmod 700 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]