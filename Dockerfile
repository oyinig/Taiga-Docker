FROM python:3.5-alpine
MAINTAINER VGG Engineering Research <engineeringresearch@venturegardengroup.com>

# Define build arguments: Taiga version
ARG VERSION=4.2.5

# Install necessary packages
RUN apk update &&\
    apk add ca-certificates wget nginx git postgresql-dev musl-dev gcc jpeg-dev zlib-dev libxml2-dev libxslt-dev libffi-dev &&\
    update-ca-certificates

# Download taiga.io backend and frontend
RUN mkdir -p /taiga.io/
WORKDIR /taiga.io
RUN wget https://github.com/taigaio/taiga-back/archive/$VERSION.tar.gz
RUN tar xzf $VERSION.tar.gz
RUN ln -sf taiga-back-$VERSION taiga-back
RUN rm -f $VERSION.tar.gz
RUN wget https://github.com/taigaio/taiga-front-dist/archive/$VERSION-stable.tar.gz
RUN tar xzf $VERSION-stable.tar.gz
RUN ln -sf taiga-front-dist-$VERSION-stable taiga-front
RUN rm -f $VERSION-stable.tar.gz

# Install all required dependencies of the backend (we will check on container startup whether we need
# to setup the database first)
WORKDIR /taiga.io/taiga-back-$VERSION
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install taiga-contrib-ldap-auth
RUN pip install pem
RUN python manage.py collectstatic --noinput

# Setup default environment
ENV TAIGA_SSL "false"
ENV TAIGA_HOSTNAME "localhost"
ENV TAIGA_SECRET_KEY "!!!PLEASE-REPLACE-ME!!!"
ENV TAIGA_DB_HOST "localhost"
ENV TAIGA_DB_NAME "postgres"
ENV TAIGA_DB_USER "postgres"
ENV TAIGA_DB_PASSWORD "!!!PLEASE-REPLACE-ME!!!"
ENV TAIGA_PUBLIC_REGISTER_ENABLED "false"
ENV TAIGA_BACKEND_DEBUG "false"
ENV TAIGA_FRONTEND_DEBUG "false"
ENV TAIGA_FEEDBACK_ENABLED "false"
ENV TAIGA_DEFAULT_LANGUAGE "en"
ENV TAIGA_DEFAULT_THEME "material-design"
ENV LDAP_ENABLE "false"
ENV LDAP_SERVER ""
ENV LDAP_PORT 389
ENV LDAP_BIND_DN ""
ENV LDAP_BIND_PASSWORD ""
ENV LDAP_SEARCH_BASE ""
ENV LDAP_SEARCH_PROPERTY "sAMAccountName"
ENV LDAP_EMAIL_PROPERTY = 'mail'
ENV LDAP_FULL_NAME_PROPERTY = 'displayName'
ENV EMAIL_BACKEND  "django.core.mail.backends.smtp.EmailBackend"
ENV EMAIL_USE_TLS "False"
ENV EMAIL_HOST  ""
ENV EMAIL_PORT ""
ENV EMAIL_HOST_USER ""
ENV EMAIL_HOST_PASSWORD ""
ENV EMAIL_USE_SSL ""
ENV BACKEND_DEBUG "False"

ENV JIRA_IMPORTER_ACTIVE "True"
ENV JIRA_IMPORTER_CONSUMER_KEY "taiga"
ENV JIRA_IMPORTER_CERT ""
ENV JIRA_IMPORTER_PUB_CERT ""

ENV GITHUB_ACTIVE ""
ENV GITHUB_CLIENT_ID ""
ENV GIITHUB_CLIENT_SECRET ""

ENV TRELLO_ACTIVE ""
ENV TRELLO_API_KEY ""
ENV TRELLO_SECRET_KEY ""

ENV ASANA_ACTIVE ""
ENV ASANA_CALLBACK_URL ""
ENV ASANA_APP_ID ""
ENV ASANA_APP_SECERET ""

RUN mkdir /taiga.io/presets
COPY local.py /taiga.io/presets/local.py

# Setup Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Remove all packages that are not required anymore
RUN apk del gcc wget git musl-dev libxml2-dev
RUN apk add gettext

# Copy files for startup
COPY checkdb.py /taiga.io/checkdb.py
COPY private_key.pem /taiga.io/private_key.pem
COPY public_key.pem /taiga.io/public_key.pem
COPY entrypoint.sh /taiga.io/entrypoint.sh

# Create a data-directory into which the configuration files will be moved
RUN mkdir /taiga.io/data

# Startup
WORKDIR /taiga.io/taiga-back
ENTRYPOINT ["/taiga.io/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]