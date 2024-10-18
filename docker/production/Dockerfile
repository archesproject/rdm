FROM public.ecr.aws/l1p7h1f9/archesproject-fargeo:7.6.x-base-prod AS base
ENV APP_ROOT=${WEB_ROOT}/arches_rdm_example_project
WORKDIR ${WEB_ROOT}

COPY arches_rdm_example_project/arches_rdm_example_project/install/requirements.txt project-requirements.txt
COPY arches-rdm/ ${WEB_ROOT}/arches-rdm

RUN apt-get install nginx -y && source ENV/bin/activate && pip install -r project-requirements.txt && rm project-requirements.txt && pip install gunicorn botocore boto3 django-storages psutil && mkdir arches_rdm_example_project && cd arches-rdm && pip install .

COPY arches_rdm_example_project/docker/production/default.conf /etc/nginx/sites-available/default

RUN  apt-get install wget -y && wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg \
  && apt-get install apt-transport-https \
  && echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list \
  && apt-get update
RUN apt-get install sudo &&  echo 'Y' | adduser elasticsearch --disabled-password --ingroup "sudo" --gecos "First Last,RoomNumber,WorkPhone,HomePhone" && echo "elasticsearch ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers &&  su -c "sudo apt-get install elasticsearch" elasticsearch && exit 
RUN apt-get install postgresql-contrib-14 postgresql-14-postgis-3 -y && sed -i '1s/^/local all all trust\n/' /etc/postgresql/14/main/pg_hba.conf && (service postgresql start) \
  && echo "ALTER USER postgres WITH PASSWORD 'postgis';CREATE DATABASE template_postgis;CREATE EXTENSION postgis;\\q" | psql -Upostgres

COPY arches_rdm_example_project/arches_rdm_example_project ${WEB_ROOT}/arches_rdm_example_project/arches_rdm_example_project
COPY arches_rdm_example_project/manage.py ${WEB_ROOT}/arches_rdm_example_project/manage.py
WORKDIR ${APP_ROOT} 
RUN chown elasticsearch:elasticsearch /etc/elasticsearch -R && \
  chown elasticsearch:elasticsearch /usr/share/elasticsearch -R && \
  chown elasticsearch:elasticsearch /etc/default/elasticsearch && \
  cd arches_rdm_example_project && yarn install

RUN openssl ecparam -out /etc/ssl/private/nginx-selfsigned.key -name prime256v1 -genkey && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -key /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"

RUN ESPASSWORD='$(echo "y" | sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic | grep "New value:" | cut -d " " -f 3)' && export ES_JAVA_OPTS="-Xmx1g" && \
  sed -i 's/xpack.security.enabled: true/xpack.security.enabled: false/g' /etc/elasticsearch/elasticsearch.yml && \
  sed -i 's/xpack.security.enrollment.enabled: true/xpack.security.enrollment.enabled: false/g' /etc/elasticsearch/elasticsearch.yml && \
  (su -c "/usr/share/elasticsearch/bin/elasticsearch" elasticsearch>/dev/null 2>&1&) && \
  (service postgresql start) && sleep 30 && source ../ENV/bin/activate && (python3 manage.py setup_db --force) 

RUN source ../ENV/bin/activate && service postgresql start && \
  (/etc/init.d/nginx start&) && (gunicorn arches_rdm_example_project.wsgi&) && \
  cd arches_rdm_example_project && yarn run build_development && cd ../ && python3 manage.py collectstatic


FROM public.ecr.aws/l1p7h1f9/archesproject-fargeo:7.6.x-base-prod AS deploy 
USER root

## Setting default environment variables
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/arches-lingo
# Root project folder
ENV WHEELS=/wheels
ENV PYTHONUNBUFFERED=1

WORKDIR ${WEB_ROOT}

# Install the Arches application
# FIXME: ADD from github repository instead?

# From here, run commands from ARCHES_ROOT
RUN source /web_root/ENV/bin/activate && pip install gunicorn psutil botocore boto3 django-storages 

COPY docker/production/entrypoint.sh ${WEB_ROOT}/entrypoint.sh
RUN chmod -R 700 ${WEB_ROOT}/entrypoint.sh &&\
  dos2unix ${WEB_ROOT}/entrypoint.sh

COPY . ${WEB_ROOT}/arches-lingo

# Set default workdir
WORKDIR ${APP_ROOT}

RUN source /web_root/ENV/bin/activate && pip install -e .

# # Set entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["run_django_server"]

# Expose port 8000
EXPOSE 8000
