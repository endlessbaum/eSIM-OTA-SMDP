FROM python:3
USER root

RUN apt-get update
RUN apt-get install -y git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools

RUN python -m pip install ecdsa asn1tools pymysql utils flask python-dotenv requests

# RUN git clone https://github.com/endlessbaum/eSIM-OTA-SMDP.git

# WORKDIR /eSIM-OTA-SMD/edgeserver

ADD ./ /edgeserver
WORKDIR /edgeserver

EXPOSE 5001
ENTRYPOINT ["flask", "run", "--no-debugger", "--host", "0.0.0.0", "--port", "5001"]