FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wisdom_builder.py main.py ./

EXPOSE 8082
ENV PORT=8082

CMD ["gunicorn", "--bind", "0.0.0.0:8082", "--workers", "1", "--timeout", "120", "main:app"]
