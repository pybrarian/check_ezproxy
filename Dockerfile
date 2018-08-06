FROM python:3.6.6-slim-jessie
ADD . /app
WORKDIR /app
RUN python setup.py install
ENV EZPROXY_PREFIX="Change" \
    LIBGUIDES_API_URL="Change" \
    EZPROXY_ERROR_TEXT="Change" \
    KB_WSKEY="Change" \
    KB_COLLECTIONS="Change"
ENTRYPOINT ["check_ezproxy"]