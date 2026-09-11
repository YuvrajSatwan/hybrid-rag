# Install and configure Placement from PyPI ¶

The section describes how to install and configure the placement service using
packages from PyPI . Placement works with Python version 2.7, but version 3.6
or higher is recommended.

This document assumes you have a working MySQL server and a working Python
environment, including the pip package installer. Depending on
your environment, you may wish to install placement in a virtualenv .

This document describes how to run placement with uwsgi as its web server.
This is but one of many different ways to host the service. Placement is a
well-behaved WSGI application so should be straightforward to host with any
WSGI server.

If using placement in an OpenStack environment, you will need to ensure it is
up and running before starting services that use it but after services it uses.
That means after Keystone , but before anything else.

## Prerequisites ¶

Before installing the service, you will need to create the database, service
credentials, and API endpoints, as described in the following sections.

### pip ¶

Install pip from PyPI .

Note

Examples throughout this reference material use the pip command.
This may need to be pathed or spelled differently (e.g. pip3 )
depending on your installation and Python version.

### python-openstackclient ¶

If not already installed, install the openstack command line tool:

# pip install python-openstackclient

### Create Database ¶

Placement is primarily tested with MySQL/MariaDB so that is what is described
here. It also works well with PostgreSQL and likely with many other databases
supported by sqlalchemy .

To create the database, complete these steps:

- Use the database access client to connect to the database server as the root user or by using sudo as appropriate: # mysql

Use the database access client to connect to the database server as the root user or by using sudo as appropriate:

# mysql

- Create the placement database: MariaDB [(none)]> CREATE DATABASE placement;

Create the placement database:

MariaDB [(none)]> CREATE DATABASE placement;

- Grant proper access to the database: MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' \ IDENTIFIED BY 'PLACEMENT_DBPASS'; MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' \ IDENTIFIED BY 'PLACEMENT_DBPASS'; Replace PLACEMENT_DBPASS with a suitable password.

Grant proper access to the database:

MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' \ IDENTIFIED BY 'PLACEMENT_DBPASS'; MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' \ IDENTIFIED BY 'PLACEMENT_DBPASS';

Replace PLACEMENT_DBPASS with a suitable password.

- Exit the database access client.

Exit the database access client.

### Configure User and Endpoints ¶

Note

If you are not using Keystone, you can skip the steps below but will
need to configure the api.auth_strategy setting
with a value of noauth2 . See also Quick Placement Development .

Note

You will need to authenticate to Keystone as an admin before
making these calls. There are many different ways to do this,
depending on how your system was set up. If you do not have an admin-openrc file, you will have something similar.

Important

These documents use an endpoint URL of http://controller:8778/ as an example only. You should
configure placement to use whatever hostname and port works best
for your environment. Using SSL on the default port, with either
a domain or path specific to placement, is recommended. For
example: https://mygreatcloud.com/placement or https://placement.mygreatcloud.com/ .

- Source the admin credentials to gain access to admin-only CLI commands: $ . admin-openrc

Source the admin credentials to gain access to admin-only CLI commands:

$ . admin-openrc

- Create a Placement service user using your chosen PLACEMENT_PASS : $ openstack user create --domain default --password-prompt placement User Password: Repeat User Password: +---------------------+----------------------------------+ | Field               | Value                            | +---------------------+----------------------------------+ | domain_id           | default                          | | enabled             | True                             | | id                  | fa742015a6494a949f67629884fc7ec8 | | name                | placement                        | | options             | {}                               | | password_expires_at | None                             | +---------------------+----------------------------------+

Create a Placement service user using your chosen PLACEMENT_PASS :

$ openstack user create --domain default --password-prompt placement User Password: Repeat User Password: +---------------------+----------------------------------+ | Field               | Value                            | +---------------------+----------------------------------+ | domain_id           | default                          | | enabled             | True                             | | id                  | fa742015a6494a949f67629884fc7ec8 | | name                | placement                        | | options             | {}                               | | password_expires_at | None                             | +---------------------+----------------------------------+

- Add the Placement user to the service project with the admin role: $ openstack role add --project service --user placement admin Note This command provides no output.

Add the Placement user to the service project with the admin role:

$ openstack role add --project service --user placement admin

Note

This command provides no output.

- Create the Placement API entry in the service catalog: $ openstack service create --name placement \ --description "Placement API" placement +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Placement API                    | | enabled     | True                             | | id          | 2d1a27022e6e4185b86adac4444c495f | | name        | placement                        | | type        | placement                        | +-------------+----------------------------------+

Create the Placement API entry in the service catalog:

$ openstack service create --name placement \ --description "Placement API" placement +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Placement API                    | | enabled     | True                             | | id          | 2d1a27022e6e4185b86adac4444c495f | | name        | placement                        | | type        | placement                        | +-------------+----------------------------------+

- Create the Placement API service endpoints: Note Depending on your environment, the URL for the endpoint will vary
by port (possibly 8780 instead of 8778, or no port at all) and
hostname. You are responsible for determining the correct URL. $ openstack endpoint create --region RegionOne \ placement public http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 2b1b2637908b4137a9c2e0470487cbc0 | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ placement internal http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 02bcda9a150a4bd7993ff4879df971ab | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ placement admin http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 3d71177b9e0f406f98cbff198d74b182 | | interface    | admin                            | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+

Create the Placement API service endpoints:

Note

Depending on your environment, the URL for the endpoint will vary
by port (possibly 8780 instead of 8778, or no port at all) and
hostname. You are responsible for determining the correct URL.

$ openstack endpoint create --region RegionOne \ placement public http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 2b1b2637908b4137a9c2e0470487cbc0 | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ placement internal http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 02bcda9a150a4bd7993ff4879df971ab | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ placement admin http://controller:8778 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 3d71177b9e0f406f98cbff198d74b182 | | interface    | admin                            | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 2d1a27022e6e4185b86adac4444c495f | | service_name | placement                        | | service_type | placement                        | | url          | http://controller:8778           | +--------------+----------------------------------+

## Install and configure components ¶

The default location of the placement configuration file is /etc/placement/placement.conf . A different directory may be chosen by
setting OS_PLACEMENT_CONFIG_DIR in the environment. It is also possible to
run the service with a partial or no configuration file and set some options
in the environment . See Configuration Guide for additional
configuration settings not mentioned here.

Note

In the steps below, controller is used as a stand in for the
hostname of the hosts where keystone, mysql, and placement are
running. These may be distinct. The keystone host (used for auth_url and www_authenticate_uri ) should be the unversioned
public endpoint for the Identity service.

- Install placement and required database libraries: # pip install openstack-placement pymysql

Install placement and required database libraries:

# pip install openstack-placement pymysql

- Create the /etc/placement/placement.conf file and complete the following
actions: Create a [placement_database] section and configure database access: [placement_database] connection = mysql+pymysql://placement:PLACEMENT_DBPASS@controller/placement Replace PLACEMENT_DBPASS with the password you chose for the placement
database. Create [api] and [keystone_authtoken] sections, configure Identity
service access: [api] auth_strategy = keystone # use noauth2 if not using keystone [keystone_authtoken] www_authenticate_uri = http://controller:5000/ auth_url = http://controller:5000/ memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = placement password = PLACEMENT_PASS Replace PLACEMENT_PASS with the password you chose for the placement user in the Identity service. Note The value of user_name , password , project_domain_name and user_domain_name need to be in sync with your keystone config. You may wish to set the debug option to True to
produce more verbose log output.

Create the /etc/placement/placement.conf file and complete the following
actions:

- Create a [placement_database] section and configure database access: [placement_database] connection = mysql+pymysql://placement:PLACEMENT_DBPASS@controller/placement Replace PLACEMENT_DBPASS with the password you chose for the placement
database.

Create a [placement_database] section and configure database access:

[placement_database] connection = mysql+pymysql://placement:PLACEMENT_DBPASS@controller/placement

Replace PLACEMENT_DBPASS with the password you chose for the placement
database.

- Create [api] and [keystone_authtoken] sections, configure Identity
service access: [api] auth_strategy = keystone # use noauth2 if not using keystone [keystone_authtoken] www_authenticate_uri = http://controller:5000/ auth_url = http://controller:5000/ memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = placement password = PLACEMENT_PASS Replace PLACEMENT_PASS with the password you chose for the placement user in the Identity service. Note The value of user_name , password , project_domain_name and user_domain_name need to be in sync with your keystone config.

Create [api] and [keystone_authtoken] sections, configure Identity
service access:

[api] auth_strategy = keystone # use noauth2 if not using keystone [keystone_authtoken] www_authenticate_uri = http://controller:5000/ auth_url = http://controller:5000/ memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = placement password = PLACEMENT_PASS

Replace PLACEMENT_PASS with the password you chose for the placement user in the Identity service.

Note

The value of user_name , password , project_domain_name and user_domain_name need to be in sync with your keystone config.

- You may wish to set the debug option to True to
produce more verbose log output.

You may wish to set the debug option to True to
produce more verbose log output.

- Populate the placement database: $ placement-manage db sync Note An alternative is to use the placement_database.sync_on_startup option.

Populate the placement database:

$ placement-manage db sync

Note

An alternative is to use the placement_database.sync_on_startup option.

## Finalize installation ¶

Now that placement itself has been installed we need to launch the service in a
web server. What follows provides a very basic web server that, while
relatively performant, is not set up to be easy to manage. Since there are many
web servers and many ways to manage them, such things are outside the scope of
this document.

Install and run the web server:

- Install the uwsgi package (these instructions are against version
2.0.18): # pip install uwsgi

Install the uwsgi package (these instructions are against version
2.0.18):

# pip install uwsgi

- Run the server with the placement WSGI application in a terminal window: Warning Make sure you are using the correct uwsgi binary. It may
be in multiple places in your path. The wrong version will
fail and complain about bad arguments. # uwsgi -M --http :8778 --wsgi-file /usr/local/bin/placement-api \ --processes 2 --threads 10

Run the server with the placement WSGI application in a terminal window:

Warning

Make sure you are using the correct uwsgi binary. It may
be in multiple places in your path. The wrong version will
fail and complain about bad arguments.

# uwsgi -M --http :8778 --wsgi-file /usr/local/bin/placement-api \ --processes 2 --threads 10

- In another terminal confirm the server is running using curl . The URL
should match the public endpoint set in Configure User and Endpoints . $ curl http://controller:8778/ The output will look something like this: { "versions" : [ { "id" : "v1.0" , "max_version" : "1.31" , "links" : [ { "href" : "" , "rel" : "self" } ], "min_version" : "1.0" , "status" : "CURRENT" } ] } Further interactions with the system can be made with osc-placement .

In another terminal confirm the server is running using curl . The URL
should match the public endpoint set in Configure User and Endpoints .

$ curl http://controller:8778/

The output will look something like this:

{ "versions" : [ { "id" : "v1.0" , "max_version" : "1.31" , "links" : [ { "href" : "" , "rel" : "self" } ], "min_version" : "1.0" , "status" : "CURRENT" } ] }

Further interactions with the system can be made with osc-placement .
