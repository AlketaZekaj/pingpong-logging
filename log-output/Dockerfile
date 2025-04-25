FROM python:3.9-slim

WORKDIR /app

COPY log-output.py .

RUN pip install requests flask

CMD ["python", "log-output.py"]
