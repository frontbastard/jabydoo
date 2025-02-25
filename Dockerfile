###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y cron && apt-get install -y gettext && \
    apt-get install -y --no-install-recommends gcc

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.4-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# copy entrypoint.sh and remove possible Windows line breaks
COPY ./entrypoint.sh $APP_HOME/entrypoint.sh
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh

# Set the correct permissions for the app directory
RUN chown -R app:app $APP_HOME

# Create the socket directory with appropriate permissions
RUN mkdir -p /home/app/web && chown -R app:app /home/app/web

# Change the user only after all file manipulations
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
