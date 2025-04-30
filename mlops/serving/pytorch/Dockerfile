FROM python:3.12-slim

WORKDIR /app
COPY tmp/app.py .
COPY tmp/model.pt .

RUN pip install torch fastapi uvicorn

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]