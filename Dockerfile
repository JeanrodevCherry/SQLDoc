FROM python:3-slim
COPY requirements.txt /app/requirements.txt
WORKDIR /app/
RUN apt update && apt upgrade -y
RUN pip install -r ./requirements.txt