FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir debugpy

COPY . .


EXPOSE 8001
EXPOSE 5679


CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5679", "manage.py", "runserver", "0.0.0.0:8001", "--nothreading", "--noreload"]

