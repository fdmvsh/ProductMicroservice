FROM python:3.8.1-alpine3.11

WORKDIR /usr/src/app

EXPOSE 5000

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./micro.py" ]