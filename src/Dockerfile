FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y netcat

WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
CMD [ "./entrypoint.sh" ]
