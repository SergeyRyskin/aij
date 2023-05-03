FROM ubuntu:latest
LABEL authors="Yilmaz Mustafa <dev@mail.be>"
LABEL description="AI Journalist Backend Services Dockerfile"

RUN apt-get update && apt-get install -y \
    curl \
    git \
    htop \
    nano \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade wheel

# Install RabbitMQ and enable management console
RUN apt-get update && apt-get install -y \
    rabbitmq-server \
    && rm -rf /var/lib/apt/lists/*

RUN rabbitmq-plugins enable rabbitmq_management

# Install SQLite
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Start RabbitMQ
RUN service rabbitmq-server start

# Create user and vhost
RUN rabbitmqctl add_user admin admin
RUN rabbitmqctl add_vhost admin_vhost
RUN rabbitmqctl set_user_tags admin administrator
RUN rabbitmqctl set_permissions -p admin_vhost admin ".*" ".*" ".*"

# Create user and vhost
RUN rabbitmqctl add_user user user
RUN rabbitmqctl add_vhost user_vhost
RUN rabbitmqctl set_user_tags user user

# Create user and vhost
RUN rabbitmqctl add_user guest guest
RUN rabbitmqctl add_vhost guest_vhost
RUN rabbitmqctl set_user_tags guest guest

# Create user and vhost
RUN rabbitmqctl add_user test test
RUN rabbitmqctl add_vhost test_vhost
RUN rabbitmqctl set_user_tags test test

# Start SQLite
RUN service sqlite3 start

# Create database
RUN sqlite3 /app/database.db < /app/database.sql

# copy all files from current directory to working directory in container
COPY . /app

# set working directory to /app/
WORKDIR /app

# Install pipenv globally
RUN pip3 install pipenv

# install dependencies
RUN pipenv install --system --deploy

# Expose RabbitMQ, SQLite and FastAPI ports
EXPOSE 5672
EXPOSE 15672
EXPOSE 3306
EXPOSE 8000

# run command on container start
CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]

# docker build -t ai-journalist-backend .
