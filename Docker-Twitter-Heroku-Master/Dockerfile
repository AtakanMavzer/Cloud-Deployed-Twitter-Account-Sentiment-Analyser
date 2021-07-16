FROM zenika/alpine-chrome:89-with-node-14
USER root
RUN mkdir /app
WORKDIR /app
#COPY ./code /code
ENV PYTHONUNBUFFERED 1

#ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Installs latest Chromium (89) package.

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
RUN ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools


RUN pip3 install Flask==2.0.1
RUN pip3 install Flask-RESTful==0.3.9
RUN pip3 install pymongo==3.11.4
RUN pip3 install python-dotenv==0.17.1
RUN pip3 install textblob==0.15.3
RUN pip3 install dnspython
RUN pip install Flask-HTTPAuth
RUN pip install Werkzeug
#
RUN apk add --no-cache \
	  nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs \
	  npm

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.

# Puppeteer v6.0.0 works with Chromium 89.
RUN npm i puppeteer


RUN npm i mongodb
# Add user so we don't need --no-sandbox.
# Run everything after as non-privileged user.



COPY . .
#CMD [ "python3", "-m" , "flask", "run"]
#CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload
CMD [ "python3", "wsgi.py"]