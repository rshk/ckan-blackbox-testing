#!/bin/bash

## Wrapper script to run tests under Travis CI
## We need to:
## - install solr
## - install Ckan in a virtualenv

cd "$( dirname "$0" )"

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual env not set"
    exit 1
fi

if [ -z "$REPO_URL" ]; then
    REPO_URL=https://github.com/okfn/ckan
fi
if [ -z "$REPO_BRANCH" ]; then
    REPO_BRANCH=master
fi


## Set password for postgres user
##------------------------------------------------------------
sudo -u postgres -H psql -c "ALTER USER postgres PASSWORD 'pass'"


## Install Solr
##------------------------------------------------------------
apt-get install solr-jetty
service jetty stop

cat > /etc/default/jetty <<EOF
NO_START=0
JETTY_HOST=127.0.0.1
JETTY_PORT=8983
JAVA_HOME=${JAVA_HOME}
EOF


## Download Ckan
##------------------------------------------------------------
mkdir -p ${VIRTUAL_ENV}/src
mkdir -p ${VIRTUAL_ENV}/etc/ckan
git clone "$REPO_URL" -b "$REPO_BRANCH" --depth=0 "$VIRTUAL_ENV"/src/ckan

cp "$VIRTUAL_ENV"/src/ckan/ckan/config/solr/schema-2.0.xml /etc/solr/conf/schema.xml
service jetty start

cp "$VIRTUAL_ENV"/src/ckan/ckan/config/who.ini ${VIRTUAL_ENV}/etc/ckan/

pip install -r ./simple_api_testing/requirements.txt
pip install -r "$VIRTUAL_ENV"/src/ckan/requirements.txt
cd "$VIRTUAL_ENV"/src/ckan/ && python setup.py install
