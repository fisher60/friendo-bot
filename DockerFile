FROM python:3.8-slim

# Install dependencies for OpenCV
RUN apt-get update && apt-get -y install libgl1 libglib2.0-0 git

RUN mkdir /app

RUN pip install pipenv

COPY . /app/

WORKDIR /app/

RUN pipenv install --system --deploy

ENTRYPOINT ["python3"]
CMD ["-m", "bot"]
