FROM python:3.11

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY prisma ./prisma

RUN prisma generate

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]