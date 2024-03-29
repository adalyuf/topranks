FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV DockerHOME=/home/app/webapp  
RUN mkdir -p $DockerHOME
COPY . $DockerHOME
WORKDIR $DockerHOME

RUN sh ./install-nvm-aws.sh

RUN pip install -r requirements.txt
RUN echo "Starting new container"

EXPOSE 80
ENTRYPOINT ./start-production.sh