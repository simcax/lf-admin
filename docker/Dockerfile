FROM python:3.9.4 
RUN apt update
# Upgrade pip 
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
COPY ./docker/docker_entrypoint.sh /
RUN chmod +x /docker_entrypoint.sh
WORKDIR /
EXPOSE 8000

ENTRYPOINT [ "./docker_entrypoint.sh" ]
CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "8000" ]