FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_handler.py main.py ./

EXPOSE 8085
ENV PORT=8085

CMD ["gunicorn", "--bind", "0.0.0.0:8085", "--workers", "2", "--timeout", "120", "main:app"]
