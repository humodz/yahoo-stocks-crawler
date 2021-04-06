# https://pythonspeed.com/articles/alpine-docker-python/
FROM python:3.9-slim as base

COPY docker/install-packages.sh .
RUN ./install-packages.sh chromium chromium-driver

RUN groupadd appgroup --system && useradd appuser -g appgroup --create-home
USER appuser
WORKDIR /home/appuser

# TODO use poetry
# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN pip install selenium

COPY app/ ./app

CMD ["app/healthcheck_selenium.py"]
ENTRYPOINT ["python"]
