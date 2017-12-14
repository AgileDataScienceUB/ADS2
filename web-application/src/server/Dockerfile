#FROM python:3-onbuild

# ensure local python is preferred over distribution python
#ENV PATH /usr/local/bin:$PATH
#
#RUN apt-get update && \
#    apt-get install -y python3 && \
#    apt-get install -y python3-pip
#
#ENV PATH /:$PATH

#
#COPY requirements.txt manage.py /server/
#COPY data /server/data/
#
#RUN pip3 install -r /server/requirements.txt \
#  && adduser app \
#  && mkdir -p /server  \
#  && chown -R app:app /server
#
#COPY flask_app /server/flask_app/
#
#VOLUME /tmp
#
#RUN chown -R app:app /server
#
#WORKDIR /server
#
#USER app
#
#EXPOSE 80
#
#CMD ["python3", "manage.py", "runserver"]

# Format: FROM    repository[:version]
FROM       ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY requirements.txt manage.py /server/
COPY data /server/data/
COPY flask_app /server/flask_app/
WORKDIR /server
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver"]

