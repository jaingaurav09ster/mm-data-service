FROM python:3.6
LABEL maintainer="Lorem Ipsum"
RUN apt-get update  &&  \
    apt-get install -y python  && \
    apt-get install -y python-pip  && \
    pip install Flask  && \
    apt-get install -y curl  && \
    mkdir files
COPY docker /files/docker
RUN pip install -r /files/docker/requirements.txt
ENV FLASK_APP /files/docker/app.py
EXPOSE 2231
CMD flask run --host=0.0.0.0 --port 2231