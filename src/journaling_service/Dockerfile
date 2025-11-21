FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY journaling_service.py main.py ./

EXPOSE 8084
ENV PORT=8084

CMD ["gunicorn", "--bind", "0.0.0.0:8084", "--workers", "2", "--timeout", "120", "main:app"]
