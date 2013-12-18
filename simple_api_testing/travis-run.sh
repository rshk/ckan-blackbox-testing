#!/bin/bash

cd "$( dirname "$0" )"

export CKAN_VIRTUALENV=$VIRTUAL_ENV
export CKAN_POSTGRES_ADMIN=postgresql://postgres:pass@localhost/postgres
export CKAN_SOLR=http://localhost:8983/solr

exec python ./run_tests.py
#exec py.test --confcutdir="$PWD" --verbose -rsxX ./tests/
