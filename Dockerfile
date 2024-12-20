FROM debian:11

ENV TZ="America/Sao_Paulo"

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

RUN python3 -m pip install  mysql-connector-python==8.0.29 \
    numpy==1.23.2 \
    pandas==1.4.4 \
    protobuf==4.21.5 \
    python-dateutil==2.8.2 \
    python-dotenv==0.21.0 \
    pytz==2022.2.1 \
    six==1.16.0 \
    dnspython==2.2.1 \
    pymongo==4.3.2 



COPY . .

CMD ["python3", "main.py", "load-onus"]
