# pull official base image
FROM python:3.6

# set environment variables
# PYTHONDONTWRITEBYTECODE Prevents Python from writing pyc files to disc 
# PYTHONUNBUFFERED Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /apps/test_image

# install dependencies

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt 
