FROM mcr.microsoft.com/playwright/python:v1.35.0-jammy

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install --with-deps chromium

COPY app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]