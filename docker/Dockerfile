FROM python:3.9-alpine

RUN apk add --update --no-cache \
    chromium-chromedriver \
    chromium

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
WORKDIR /home/appuser

# TODO use poetry
# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN pip install selenium

COPY app/ ./app

CMD ["app/healthcheck_selenium.py"]
ENTRYPOINT ["python"]
