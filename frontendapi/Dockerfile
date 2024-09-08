FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /frontendapi

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .

COPY entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

