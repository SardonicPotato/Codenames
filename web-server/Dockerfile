FROM python:3.6-slim

WORKDIR /app

ADD . /app

RUN pip install -e .

EXPOSE 8080

CMD ["python", "scripts/launch_server.py", "./data"]
