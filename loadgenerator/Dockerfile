FROM python:2.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends git

WORKDIR /opt/loadgen

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY locustfile.py ./
COPY loadgen.sh ./

ENTRYPOINT [ "./loadgen.sh" ]