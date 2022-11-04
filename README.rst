***************************
Emporia Energy Vue Exporter
***************************

This is an application for exporting usage metrics from the Emporia Energy Vue units.
This exporter utilizes the Emporia Energy Cloud, and the `PyEmVue`_ module.

.. _PyEmVue: https://github.com/magico13/PyEmVue

Installation
============

Easiest usage of this is to use the container image!

```
docker run -it \
  -e EMVUE_EXPORTER_USERNAME=yourusernamehere \
  -e EMVUE_EXPORTER_PASSWORD=yourpasswordhere \
  -p 10110:10110 \
  registry.gitlab.com/shouptech/emvue_exporter
```

Then, point prometheus to your container host, at port 10110.

Configuration
=============

Configuration is done through environment variables.

* ``EMVUE_EXPORTER_USERNAME`` - *Required*, username to access the Emporia Energy portal.
* ``EMVUE_EXPORTER_PASSWORD`` - *Required*, password to access the Emporia Energy portal.
* ``EMVUE_EXPORTER_LOG_LEVEL`` - Logging level. Defaults to INFO.
* ``EMVUE_EXPORTER_PORT`` - Port number to listen on. Defaults to 10110.
* ``EMVUE_EXPORTER_POLL_DELAY`` - Delay in seconds between polls of the API. Defaults to 60.

Changelog
=========

0.1
----

Initial release
