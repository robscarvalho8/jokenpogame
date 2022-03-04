FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

COPY ./api /app/api
COPY main.py /app/main.py

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

ENV FLASK_APP=main.py

ENV PATH="/.venv/bin:$PATH"

CMD ["flask", "run", "-h", "0.0.0.0"]

EXPOSE 5000