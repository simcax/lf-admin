#!/bin/bash
if [ `docker ps -a -f name=^redis|grep redis|wc -l` -eq 1 ];then 
    echo "Redis container exists"
    docker start redis
else
    echo "Starting redis"
    docker run -d -p 6379:6379 redis --name redis
fi
#source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
export RUN_ENVIRONMENT=Development
export REDIS_URL=redis://localhost:6379
export SESSION_TYPE=redis
export SESSION_COOKIE_SECURE=False
export SESSION_COOKIE_HTTPONLY=True
export FLASK_DEBUG=1
export COOKIE_DOMAIN=127.0.0.1
export SESSION_COOKIE_NAME=linux2.skov.run
export SECRET_KEY=NzRZHcNqyXGNaS1GcPqdJQ
export LOG_LEVEL=debug
export DB_HOST=localhost
flask run --host 0.0.0.0 --port 30000

