FROM python:3.8-alpine AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create virtualenv path and add to front of $PATH
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /requirements.txt


WORKDIR /app

RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc && \
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home janus && \
    mkdir -p /vol/log && \
    mkdir -p /vol/static && \
    mkdir -p /vol/uploads && \
    mkdir -p /vol/admin/uploads&& \
    mkdir -p /vol/downloads && \
    chown -R janus:janus /app && \
    chown -R janus:janus /vol/static && \
    chown -R janus:janus /vol/uploads && \
    chown -R janus:janus /vol/admin/uploads && \
    chown -R janus:janus /vol/downloads && \
    chown -R janus:janus /vol/log

USER janus

COPY . /app

RUN /bin/cp -r /app/app/static/* /vol/static

VOLUME [ "/vol/downloads", "/vol/uploads", "/vol/admin/uploads", "/vol/static", "/vol/log" ]

# DEBUG BUILD
FROM base AS debug
USER root
COPY /dev-requirements.txt /dev-requirements.txt
RUN pip install -r /dev-requirements.txt
USER janus
ENTRYPOINT [ "python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "--host=0.0.0.0"  ]


# DEV BUILD
FROM base AS dev
ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

# PROD BUILD
FROM base AS prod
ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]