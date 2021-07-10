FROM python:3.9-slim

RUN apt-get update && apt-get -y install git

RUN mkdir /app

RUN pip install pipenv

COPY . /app/

WORKDIR /app/

RUN pipenv install --system --deploy

ENTRYPOINT ["python3"]
CMD ["-m", "bot"]
