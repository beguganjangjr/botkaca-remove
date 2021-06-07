FROM alpine:latest as prepare_env
WORKDIR /app

RUN apk --no-cache -q add \
    python3 python3-dev py3-pip libffi libffi-dev musl-dev gcc \
    build-base zlib-dev jpeg-dev libxml2-dev libxslt-dev

RUN pip3 install -q --ignore-installed distlib pipenv
RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH" VIRTUAL_ENV="/app/venv"

COPY requirements.txt .
RUN pip3 install -q -r requirements.txt


FROM alpine:latest as execute
WORKDIR /app

ENV PATH="/app/venv/bin:$PATH" VIRTUAL_ENV="/app/venv"

RUN apk --update --no-cache -q add \
    python3 libffi \
    ffmpeg bash unzip curl wget
COPY setup.sh .
RUN bash setup.sh
RUN apk del bash unzip curl wget
COPY --from=prepare_env /app/venv venv
