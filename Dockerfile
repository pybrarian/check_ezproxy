FROM python:3.6.6-slim-jessie
ADD . /app
WORKDIR /app
RUN python setup.py install
ENTRYPOINT ["check_ezproxy"]