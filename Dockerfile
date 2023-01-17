FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python -m unittest discover

CMD [ "python3", "./src/polkadot.py"]
