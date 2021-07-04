FROM python:3.9-slim

RUN mkdir /app

RUN pip install pipenv

COPY . /app/

WORKDIR /app/

RUN pipenv install --system --deploy

ENTRYPOINT ["python3"]
CMD ["-m", "bot"]
