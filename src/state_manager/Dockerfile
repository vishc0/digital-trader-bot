FROM python:3.10-slim
RUN pip install flask gunicorn redis msgpack
COPY main.py .
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "main:app"]
