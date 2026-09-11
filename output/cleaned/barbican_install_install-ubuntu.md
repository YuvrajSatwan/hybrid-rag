# Install and configure for Ubuntu ¶

This section describes how to install and configure the Key Manager
service for Ubuntu 14.04 (LTS).

## Prerequisites ¶

Before you install and configure the Key Manager service,
you must create a database, service credentials, and API endpoints.

- To create the database, complete these steps: Use the database access client to connect to the database
server as the root user: # mysql Create the barbican database: CREATE DATABASE barbican; Grant proper access to the barbican database: GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'localhost' \ IDENTIFIED BY 'BARBICAN_DBPASS'; GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'%' \ IDENTIFIED BY 'BARBICAN_DBPASS'; Replace BARBICAN_DBPASS with a suitable password. Exit the database access client. exit;

To create the database, complete these steps:

- Use the database access client to connect to the database
server as the root user: # mysql

Use the database access client to connect to the database
server as the root user:

# mysql

- Create the barbican database: CREATE DATABASE barbican;

Create the barbican database:

CREATE DATABASE barbican;

- Grant proper access to the barbican database: GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'localhost' \ IDENTIFIED BY 'BARBICAN_DBPASS'; GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'%' \ IDENTIFIED BY 'BARBICAN_DBPASS'; Replace BARBICAN_DBPASS with a suitable password.

Grant proper access to the barbican database:

GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'localhost' \ IDENTIFIED BY 'BARBICAN_DBPASS'; GRANT ALL PRIVILEGES ON barbican.* TO 'barbican'@'%' \ IDENTIFIED BY 'BARBICAN_DBPASS';

Replace BARBICAN_DBPASS with a suitable password.

- Exit the database access client. exit;

Exit the database access client.

exit;

- Source the admin credentials to gain access to
admin-only CLI commands: $ source admin-openrc

Source the admin credentials to gain access to
admin-only CLI commands:

$ source admin-openrc

- To create the service credentials, complete these steps: Create the barbican user: $ openstack user create --domain default --password-prompt barbican Add the admin role to the barbican user: $ openstack role add --project service --user barbican admin Create the creator role: $ openstack role create creator Add the creator role to the barbican user: $ openstack role add --project service --user barbican creator Create the barbican service entities: $ openstack service create --name barbican --description "Key Manager" key-manager

To create the service credentials, complete these steps:

- Create the barbican user: $ openstack user create --domain default --password-prompt barbican

Create the barbican user:

$ openstack user create --domain default --password-prompt barbican

- Add the admin role to the barbican user: $ openstack role add --project service --user barbican admin

Add the admin role to the barbican user:

$ openstack role add --project service --user barbican admin

- Create the creator role: $ openstack role create creator

Create the creator role:

$ openstack role create creator

- Add the creator role to the barbican user: $ openstack role add --project service --user barbican creator

Add the creator role to the barbican user:

$ openstack role add --project service --user barbican creator

- Create the barbican service entities: $ openstack service create --name barbican --description "Key Manager" key-manager

Create the barbican service entities:

$ openstack service create --name barbican --description "Key Manager" key-manager

- Create the Key Manager service API endpoints: $ openstack endpoint create --region RegionOne \ key-manager public http://controller:9311 $ openstack endpoint create --region RegionOne \ key-manager internal http://controller:9311 $ openstack endpoint create --region RegionOne \ key-manager admin http://controller:9311

Create the Key Manager service API endpoints:

$ openstack endpoint create --region RegionOne \ key-manager public http://controller:9311 $ openstack endpoint create --region RegionOne \ key-manager internal http://controller:9311 $ openstack endpoint create --region RegionOne \ key-manager admin http://controller:9311

## Install and configure components ¶

- Install the packages: # apt-get update # apt-get install barbican-api barbican-keystone-listener barbican-worker

Install the packages:

# apt-get update # apt-get install barbican-api barbican-keystone-listener barbican-worker

- Edit the /etc/barbican/barbican.conf file and complete the following
actions: In the [DEFAULT] section, configure database access: [DEFAULT] ... sql_connection = mysql+pymysql://barbican:BARBICAN_DBPASS@controller/barbican Replace BARBICAN_DBPASS with the password you chose for the
Key Manager service database. In the [DEFAULT] section,
configure RabbitMQ message queue access: [DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ . In the [keystone_authtoken] section, configure Identity
service access: [keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = barbican password = BARBICAN_PASS Replace BARBICAN_PASS with the password you chose for the barbican user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section.

Edit the /etc/barbican/barbican.conf file and complete the following
actions:

- In the [DEFAULT] section, configure database access: [DEFAULT] ... sql_connection = mysql+pymysql://barbican:BARBICAN_DBPASS@controller/barbican Replace BARBICAN_DBPASS with the password you chose for the
Key Manager service database.

In the [DEFAULT] section, configure database access:

[DEFAULT] ... sql_connection = mysql+pymysql://barbican:BARBICAN_DBPASS@controller/barbican

Replace BARBICAN_DBPASS with the password you chose for the
Key Manager service database.

- In the [DEFAULT] section,
configure RabbitMQ message queue access: [DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ .

In the [DEFAULT] section,
configure RabbitMQ message queue access:

[DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller

Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ .

- In the [keystone_authtoken] section, configure Identity
service access: [keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = barbican password = BARBICAN_PASS Replace BARBICAN_PASS with the password you chose for the barbican user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section.

In the [keystone_authtoken] section, configure Identity
service access:

[keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = barbican password = BARBICAN_PASS

Replace BARBICAN_PASS with the password you chose for the barbican user in the Identity service.

Note

Comment out or remove any other options in the [keystone_authtoken] section.

- Populate the Key Manager service database: If you wish the Key Manager service to automatically populate the
database when the service is first started, set db_auto_create to
True in the [DEFAULT] section. By default this will not be active
and you can populate the database manually as below: $ su -s /bin/sh -c "barbican-manage db upgrade" barbican Note Ignore any deprecation messages in this output.

Populate the Key Manager service database:

If you wish the Key Manager service to automatically populate the
database when the service is first started, set db_auto_create to
True in the [DEFAULT] section. By default this will not be active
and you can populate the database manually as below:

$ su -s /bin/sh -c "barbican-manage db upgrade" barbican

Note

Ignore any deprecation messages in this output.

- Barbican has a plugin architecture which allows the deployer to store secrets in
a number of different back-end secret stores.  By default, Barbican is configured to
store secrets in a basic file-based keystore.  This key store is NOT safe for
production use. For a list of supported plugins and detailed instructions on how to configure them,
see Configure Secret Store Back-end

Barbican has a plugin architecture which allows the deployer to store secrets in
a number of different back-end secret stores.  By default, Barbican is configured to
store secrets in a basic file-based keystore.  This key store is NOT safe for
production use.

For a list of supported plugins and detailed instructions on how to configure them,
see Configure Secret Store Back-end

## Finalize installation ¶

Restart the Key Manager services:

# service barbican-keystone-listener restart # service barbican-worker restart # service apache2 restart
