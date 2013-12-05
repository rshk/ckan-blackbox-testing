# API Testing

## Strategy

We need:

* A virtualenv containing a Ckan installation
* A clean database (better: a user that can create databases)
* A clean Solr index, with the Ckan schema (todo: how to recreate indices?)
* Access to paster commands to setup users etc.
* To launch a subprocess running Ckan
