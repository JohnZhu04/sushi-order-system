FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py ./app/
COPY app/model.py ./app/
COPY app/db.py ./app/
