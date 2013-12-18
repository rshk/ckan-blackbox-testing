#!/bin/bash

export CKAN_VIRTUALENV=$VIRTUAL_ENV
export CKAN_POSTGRES_ADMIN=postgresql://postgres:pass@database.local/postgres
export CKAN_SOLR=http://localhost:8983/solr/ckan-2.0
exec python ./run_tests.py
