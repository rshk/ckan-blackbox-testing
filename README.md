# Ckan black-box testing

[![Build Status](https://travis-ci.org/rshk/ckan-blackbox-testing.png?branch=master)](https://travis-ci.org/rshk/ckan-blackbox-testing)

"Black-box" test suite for [Ckan](https://github.com/okfn/ckan).


## Running tests

Requirements:

- Python virtualenv, with Ckan installed
- PostgreSQL instance, with administrative access
- Solr instance, with Ckan schema installed

Running this:

```
export CKAN_VIRTUALENV=$VIRTUAL_ENV
export CKAN_POSTGRES_ADMIN=postgresql://postgres:pass@localhost/postgres
export CKAN_SOLR=http://127.0.0.1:8983/solr

python ./simple_api_testing/run_tests.py
```

(Have a look at the ``simple_api_testing/travis-*.sh`` scripts for more examples)


## How does it work?

We provide a bunch of py.test fixtures that will:

- create / drop postgresql user and database for each test module run
- flush the solr index on each module run
- provide facilities for running / stopping the ``paster serve`` process


## TodoList

- Figure out a nice way to trigger builds "the other way round", i.e.
  when a change is pushed on the ckan repository (in any branch, ...)
- Write complete test suite for Ckan API
- Maybe, add tests for the web pages too


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/rshk/ckan-blackbox-testing/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

