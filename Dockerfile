# syntax=docker/dockerfile:1
FROM python:3.12-alpine

ENV PYTHONPATH=src
COPY requirements.txt /
COPY src/ /
COPY tests/utils/app.wsgi /src/app.wsgi

RUN pip install -r requirements.txt
RUN pip install waitress

EXPOSE 5000
CMD ["waitress-serve", "app:application"]