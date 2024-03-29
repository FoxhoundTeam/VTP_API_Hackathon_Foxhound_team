ARG PYTHON_VERSION=3.9.9-slim-buster

FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production
ENV UWSGI_PROFILE_OVERRIDE=ssl=true

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # git+https
  git \
  python3-dev \
  openssl \
  libssl-dev \
  pkg-config \
  unixodbc-dev

COPY ./websocket/requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/websocketapp

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


COPY ./compose/websocket/docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


COPY ./compose/websocket/commands/ /commands
RUN sed -i 's/\r$//g' /commands/*
RUN chmod +x -R /commands


COPY ./compose/websocket/uwsgi.ini /websocketapp/uwsgi.ini

# copy application code to WORKDIR
COPY ./websocket ${APP_HOME}

ENTRYPOINT ["/docker-entrypoint.sh"]