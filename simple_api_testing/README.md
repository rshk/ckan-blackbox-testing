# Simple tests for CKAN API

This test suite will run a bunch of simple tests on a running Ckan instance.

The database is assumed to be empty, and the Ckan instance running with
default privileges.

The only requirements are, passed as environment variables:

* ``CKAN_URL`` URL pointing to the running Ckan instance
* ``CKAN_API_KEY`` API key to be used for requests. It is assumed to belong
  to a superuser.


## Setting up the instance

* Install ckan
* Create configuration file
* Create database
* Make sure we have access to a Solr index
* Create user, make it sysadmin
* Run the tests
