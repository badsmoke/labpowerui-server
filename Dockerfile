FROM python:3.13-slim-bullseye


LABEL maintainer="dockerhub@badcloud.eu"
LABEL description="labpowerui-server"


WORKDIR /usr/src/app




RUN apt update \
  && apt install nano -y \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY ./src/requirements.txt ./
#RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src ./
COPY ./src/main.py ./psu-server.py

#COPY ./src/owon_psu /usr/local/lib/python3.13/site-packages/owon_psu/__init__.py
CMD [ "python","-u","/usr/src/app/psu-server.py" ]