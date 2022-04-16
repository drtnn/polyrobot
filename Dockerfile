FROM python:3.9

EXPOSE 80

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install -r requirements.txt

CMD ["sh", "/usr/src/app/run.sh"]
