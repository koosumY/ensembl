FROM python:3.5.9-alpine

RUN mkdir /app
WORKDIR /app/

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY code /app/code

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "code/app.py" ]
