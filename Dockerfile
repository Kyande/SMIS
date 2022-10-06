FROM python:3.9

LABEL name="SMIS"
LABEL description="A system that helps run a school"

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements/base.txt /app/

RUN pip install -r base.txt

COPY . /app/
