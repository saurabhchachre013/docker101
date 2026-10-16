FROM ubuntu

USER root

RUN apt-get update && apt-get install -y iputils-ping

ENTRYPOINT ["ping", "-c", "3"]
CMD ["google.com"]

