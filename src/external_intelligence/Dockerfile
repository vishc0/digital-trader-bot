FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY external_intelligence.py main.py ./

EXPOSE 8083
ENV PORT=8083

CMD ["gunicorn", "--bind", "0.0.0.0:8083", "--workers", "1", "--timeout", "120", "main:app"]
