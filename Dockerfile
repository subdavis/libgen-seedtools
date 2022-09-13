FROM python:3.10-alpine
RUN apk add --no-cache transmission-daemon
## we need bash not sh for runnig the entrypoint script
## under sh, the job controll works with `compose run` yet not with `compose up`
RUN apk add --no-cache bash
## git is needed for pip from gh
RUN apk add --no-cache git

## pip version fails so installing version from github/main
## see: https://github.com/subdavis/libgen-seedtools/issues/6
## RUN pip install libgen-seedtools
RUN python3 -m pip install git+https://github.com/subdavis/libgen-seedtools/

ARG DATA_DIR=/opt/persistent/
ARG TD_DIR=${DATA_DIR}transmission-daemon/
ARG ST_DIR=${DATA_DIR}libgen-seedtools/
ARG ST_FILE=${ST_DIR}config.json

RUN mkdir ${DATA_DIR}
VOLUME ${DATA_DIR}

RUN mkdir ${TD_DIR}
COPY docker-assets/transmission-daemon/settings.json ${TD_DIR}

RUN mkdir ${ST_DIR}
COPY docker-assets/libgen-seedtools/config.json ${ST_FILE}

COPY docker-assets/docker-entrypoint.sh /opt/
RUN chmod +x /opt/docker-entrypoint.sh

## TBD: need to sort this out
## needed for listening port
## EXPOSE 51413/tcp 51413/udp

ENV TD_DIR=${TD_DIR}
ENV ST_DIR=${ST_DIR}
ENTRYPOINT /opt/docker-entrypoint.sh $TD_DIR $ST_DIR

