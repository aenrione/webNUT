FROM python:3.6
MAINTAINER Alfredo Enrione <aenrione@aenrione.xyz>

RUN mkdir /app && \
cd /app && \
git clone https://github.com/rshipp/python-nut2.git && \
cd python-nut2 && \
python setup.py install && \
cd ..

COPY . /app/webNUT
RUN pip install -e /app/webNUT


COPY /docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app/webNUT

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 6543
