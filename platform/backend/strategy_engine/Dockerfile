FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY strategy_engine.py main.py ./

EXPOSE 8081
ENV PORT=8081

CMD ["gunicorn", "--bind", "0.0.0.0:8081", "--workers", "2", "--timeout", "120", "main:app"]
