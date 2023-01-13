FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]