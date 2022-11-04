FROM python:3.10

COPY . /app
RUN cd /app && pip install . && cd / && rm -rf /app

CMD ["/usr/local/bin/emvue_exporter"]
