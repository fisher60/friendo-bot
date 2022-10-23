FROM python:3.9-slim

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIPENV_NOSPIN=1

WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy deps and lockfile
COPY Pipfile Pipfile.lock /app/

# Install project deps
RUN pipenv install --system --deploy

# Set SHA build argument
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Copy in rest of code last, for caching
COPY . /app/

CMD ["python3", "-m", "bot"]
