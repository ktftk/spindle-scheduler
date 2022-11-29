FROM python:3.11

ENV PROJECT spinner_scheduler

WORKDIR /code

COPY . /code

RUN pip install -r /code/requirements.txt -e /code

WORKDIR /code/${PROJECT}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]