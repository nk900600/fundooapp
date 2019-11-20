FROM python:latest


RUN mkdir /fundoo
WORKDIR /fundoo
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev libmcrypt-dev default-mysql-client
RUN pip install --upgrade pip setuptools wheel


COPY  requirement.txt ./

RUN  pip install -r requirement.txt


COPY . ./
EXPOSE 8000


