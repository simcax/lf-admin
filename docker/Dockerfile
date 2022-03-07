FROM python:3.9.4
LABEL maintainer="carsten@skov.codes"
RUN apt update
RUN apt install -y gunicorn3 gcc python3-dev libpq-dev
# Upgrade pip 
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pip
RUN python -m venv /venv
COPY ./docker/requirements.txt /
RUN . venv/bin/activate && python -m pip install psycopg2 && python -m pip install -r requirements.txt
ENV SESSION_TYPE=redis
ENV REDIS_HOST=redis-lf-admin
ENV REDIS_PORT=6381
ENV FLASK_APP=app
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./app /app
COPY ./docker/config /config
COPY ./docker/docker_entrypoint.sh /
RUN chmod +x /docker_entrypoint.sh
WORKDIR /
EXPOSE 8000

ENTRYPOINT [ "./docker_entrypoint.sh" ]
CMD [ "/venv/bin/gunicorn", "-c", "python:config.gunicorn", "app.app:app" ]