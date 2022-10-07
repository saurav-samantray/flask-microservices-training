FROM python:3.10

#Install NGINX and Supervisor
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor

LABEL maintainer="saurav.samantray@gmail.com"
WORKDIR /user-management-service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# create a new user called nginx. Avoid using root
RUN useradd --no-create-home nginx

#Remove default ngnix configuration
RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

#Copy custom configuration to the image
COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

#Copy the source code from local to docker image
COPY . .

#Start the supervisord which will take care of starting ngnix and uWSGI server on container startup
CMD ["/usr/bin/supervisord"]