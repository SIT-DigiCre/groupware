FROM python:latest

RUN pip install --upgrade
RUN pip install autopep8 flake8

COPY entrypoint.sh /entrypoint.sh
RUN chmod 700 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]