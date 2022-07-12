FROM python:3
USER root

RUN apt-get update && apt-get install -y git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools

RUN python -m pip install ecdsa asn1tools pymysql utils flask python-dotenv requests

# RUN git clone https://github.com/endlessbaum/eSIM-OTA-SMDP.git

# WORKDIR /eSIM-OTA-SMD/api

ADD ./ /api
WORKDIR /api
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--no-debugger", "--host", "0.0.0.0","--port", "5000"]