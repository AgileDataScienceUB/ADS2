
#FROM buildpack-deps:stretch
#
## ensure local python is preferred over distribution python
#ENV PATH /usr/local/bin:$PATH
#
#RUN apt-get update && \
#    apt-get install -y python3
#
#ENV PATH /:$PATH
#
## FROM mhart/alpine-node:6.4.0
#
#RUN mkdir -p /client
#
#
#COPY package.json /client/
#COPY data /client/data/
#COPY fonts /client/fonts/
#COPY images /client/images/
#COPY scripts /client/scripts/
#COPY styles /client/styles/
#COPY views /client/views/
#COPY favicon.ico /client/
#COPY index.html /client/
#
#WORKDIR /client
#
#
#
#EXPOSE 3000
#
#CMD ["python3", "-m", "http.server", "3000"]

FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y nodejs
RUN apt-get install -y npm

COPY package.json /client/
COPY data /client/data/
COPY fonts /client/fonts/
COPY images /client/images/
COPY scripts /client/scripts/
COPY styles /client/styles/
COPY views /client/views/
COPY favicon.ico /client/
COPY index.html /client/

WORKDIR /client



RUN npm install -g http-server

CMD ["http-server", "-p", "8080"]

