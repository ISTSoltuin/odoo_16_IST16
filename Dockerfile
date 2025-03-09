FROM odoo:16
# Copy entrypoint script and Odoo configuration file
USER root

RUN apt-get update && apt-get install -y \
    libffi-dev \
    libxmlsec1-dev \
    libxml2-dev \
    libxslt1-dev \
    libxml2 \
    libxmlsec1 \
    python3-dev \
    pkg-config

COPY ./extra-addons /usr/lib/python3/dist-packages/odoo/extra-addons

WORKDIR /usr/lib/python3/dist-packages/odoo/extra-addons
RUN pip3 install --upgrade pip wheel setuptools \
    && pip3 install -r ./requirements.txt

# Ajustar permissões na pasta do filestore
RUN chmod -R 777 /var/lib/odoo /usr/lib/python3/dist-packages/odoo


COPY ./odoo.conf /etc/odoo/
