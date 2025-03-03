FROM python:3.10
WORKDIR /bot
EXPOSE 8080
COPY . /bot
CMD python poteto.py
