FROM python:3.7-slim

# update the system and install system dependencis for packages like pandas and sklearn
RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

RUN mkdir /app

# make sure pipenv is installed in the system
RUN pip install pipenv

# copy both pipfiles to tmp directory of the system
COPY Pipfile* /tmp/

# cd intp the tmp directory and generate requirements.txt file from pipfile.lock file
RUN cd /tmp && pipenv lock --requirements > /app/requirements.txt

# cd back into the app directory
RUN cd /app

# set app directory as the working directory
WORKDIR /app

# install all required packages from generated requirements.txt file
RUN pip install -r /app/requirements.txt

# copy all source code to the container
COPY . .

# start the server
CMD gunicorn -b 0.0.0.0:8001 --access-logfile - "cctwin.app:create_app()"
