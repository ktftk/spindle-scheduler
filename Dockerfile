FROM python:3.11

ENV PROJECT spinner_schduler

WORKDIR /code

COPY . /code

RUN pip install -r /code/requirements.txt --no-cache-dir /code

CMD ["uvicorn", "${PROJECT}.app.main:app", "--host", "0.0.0.0", "--port", "8080"]