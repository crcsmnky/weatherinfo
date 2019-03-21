FROM python:2.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends git

WORKDIR /opt/weatherapp

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 5000
ENV PORT 5000

CMD python app.py