FROM zenika/alpine-maven

USER root

# Install python and pip
RUN apk add --update --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && apk add --update --no-cache py-setuptools \
  && pip3 install virtualenv \
  && rm -rf /var/cache/apk/*



ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD ./ /opt/webapp/
WORKDIR /opt/webapp

# Expose is NOT supported by Heroku
#EXPOSE 5000

# Run the image as a non-root user
RUN adduser -D myuser
RUN chmod -R 777 .
USER myuser

CMD gunicorn --bind 0.0.0.0:8080 --timeout 60000 wsgi