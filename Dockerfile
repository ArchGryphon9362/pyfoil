FROM python:3.11.6

WORKDIR /app

COPY requirements.txt .

RUN mkdir /games

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "server.py" ]
