FROM python:3.11

WORKDIR /code

COPY . /code

RUN pip install -r /code/requirements.txt -e /code

CMD ["uvicorn", "spinner_scheduler.app.main:app", "--host", "0.0.0.0", "--port", "8080"]