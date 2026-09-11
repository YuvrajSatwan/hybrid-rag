# Installation Â¶

Note

Before the Stein release the placement code was in Nova alongside
the compute REST API code (nova-api). Make sure that the release
version of this document matches the release version you want to
deploy.

## Steps Overview Â¶

This subsection gives an overview of the process without going into detail
on the methods used.

1. Deploy the API service

Placement provides a placement-api WSGI script for running the service with
Apache, nginx or other WSGI-capable web servers. Depending on what packaging
solution is used to deploy OpenStack, the WSGI script may be in /usr/bin or /usr/local/bin .

placement-api , as a standard WSGI script, provides a module level application attribute that most WSGI servers expect to find. This means it
is possible to run it with lots of different servers, providing flexibility in
the face of different deployment scenarios. Common scenarios include:

- apache2 with mod_wsgi

apache2 with mod_wsgi

- apache2 with mod_proxy_uwsgi

apache2 with mod_proxy_uwsgi

- nginx with uwsgi

nginx with uwsgi

- nginx with gunicorn

nginx with gunicorn

In all of these scenarios the host, port and mounting path (or prefix) of the
application is controlled in the web serverâs configuration, not in the
configuration ( placement.conf ) of the placement application.

When placement was first added to DevStack it used the mod_wsgi style.
Later it was updated to use mod_proxy_uwsgi . Looking at those changes can
be useful for understanding the relevant options.

DevStack is configured to host placement at /placement on either the
default port for http or for https ( 80 or 443 ) depending on whether TLS
is being used. Using a default port is desirable.

By default, the placement application will get its configuration for settings
such as the database connection URL from /etc/placement/placement.conf .
The directory the configuration file will be found in can be changed by setting OS_PLACEMENT_CONFIG_DIR in the environment of the process that starts the
application. With recent releases of oslo.config , configuration options may
also be set in the environment .

Note

When using uwsgi with a front end (e.g., apache2 or nginx) something
needs to ensure that the uwsgi process is running. In DevStack this is done
with systemd . This is one of many different ways to manage uwsgi.

This document refrains from declaring a set of installation instructions for
the placement service. This is because a major point of having a WSGI
application is to make the deployment as flexible as possible. Because the
placement API service is itself stateless (all state is in the database), it is
possible to deploy as many servers as desired behind a load balancing solution
for robust and simple scaling. If you familiarize yourself with installing
generic WSGI applications (using the links in the common scenarios list,
above), those techniques will be applicable here.

2. Synchronize the database

The placement service uses its own database, defined in the placement_database section of configuration. The placement_database.connection option must be set or
the service will not start. The command line tool placement-manage can be used to migrate the database tables to their correct form, including
creating them. The database described by the connection option must
already exist and have appropriate access controls defined.

Another option for synchronization is to set placement_database.sync_on_startup to True in
configuration. This will perform any missing database migrations as the
placement web service starts. Whether you choose to sync automaticaly or use
the command line tool depends on the constraints of your environment and
deployment tooling.

3. Create accounts and update the service catalog

Create a placement service user with an admin role in Keystone.

The placement API is a separate service and thus should be registered under
a placement service type in the service catalog. Clients of placement, such
as the resource tracker in the nova-compute node, will use the service catalog
to find the placement endpoint.

See Configure User and Endpoints for examples of creating the service user
and catalog entries.

Devstack sets up the placement service on the default HTTP port (80) with a /placement prefix instead of using an independent port.

## Installation Packages Â¶

This section provides instructions on installing placement from Linux
distribution packages.

Warning

These installation documents are a work in progress. Some of the
distribution packages mentioned are not yet available so the
instructions will not work .

The placement service provides an HTTP API used to track resource provider
inventories and usages. More detail can be found at the placement
overview .

Placement operates as a web service over a data model. Installation involves
creating the necessary database and installing and configuring the web service.
This is a straightforward process, but there are quite a few steps to integrate
placement with the rest of an OpenStack cloud.

Note

Placement is required by some of the other OpenStack services,
notably nova, therefore it should be installed before those other
services but after Identity (keystone).

- Install and configure Placement from PyPI

- Install and configure Placement for Red Hat Enterprise Linux and CentOS Stream

- Install and configure Placement for Ubuntu

- Verify Installation
