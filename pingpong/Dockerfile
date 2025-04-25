FROM python:3.9-slim
WORKDIR /app
COPY pingpong.py .
RUN pip install flask psycopg2-binary
CMD ["python", "pingpong.py"]
