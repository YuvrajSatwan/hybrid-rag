# Install and configure for Debian ¶

This section describes how to install and configure the Orchestration service
for Debian.

## Prerequisites ¶

Before you install and configure Orchestration, you must create a
database, service credentials, and API endpoints. Orchestration also
requires additional information in the Identity service.

- To create the database, complete these steps: Use the database access client to connect to the database
server as the root user: $ mysql -u root -p Create the heat database: CREATE DATABASE heat; Grant proper access to the heat database: GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'localhost' \ IDENTIFIED BY 'HEAT_DBPASS'; GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'%' \ IDENTIFIED BY 'HEAT_DBPASS'; Replace HEAT_DBPASS with a suitable password. Exit the database access client.

To create the database, complete these steps:

- Use the database access client to connect to the database
server as the root user: $ mysql -u root -p

Use the database access client to connect to the database
server as the root user:

$ mysql -u root -p

- Create the heat database: CREATE DATABASE heat;

Create the heat database:

CREATE DATABASE heat;

- Grant proper access to the heat database: GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'localhost' \ IDENTIFIED BY 'HEAT_DBPASS'; GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'%' \ IDENTIFIED BY 'HEAT_DBPASS'; Replace HEAT_DBPASS with a suitable password.

Grant proper access to the heat database:

GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'localhost' \ IDENTIFIED BY 'HEAT_DBPASS'; GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'%' \ IDENTIFIED BY 'HEAT_DBPASS';

Replace HEAT_DBPASS with a suitable password.

- Exit the database access client.

Exit the database access client.

- Source the admin credentials to gain access to
admin-only CLI commands: $ . admin-openrc

Source the admin credentials to gain access to
admin-only CLI commands:

$ . admin-openrc

- To create the service credentials, complete these steps: Create the heat user: $ openstack user create --domain default --password-prompt heat User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | e0353a670a9e496da891347c589539e9 | | enabled   | True                             | | id        | ca2e175b851943349be29a328cc5e360 | | name      | heat                             | +-----------+----------------------------------+ Add the admin role to the heat user: $ openstack role add --project service --user heat admin Note This command provides no output. Create the heat and heat-cfn service entities: $ openstack service create --name heat \ --description "Orchestration" orchestration +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | 727841c6f5df4773baa4e8a5ae7d72eb | | name        | heat                             | | type        | orchestration                    | +-------------+----------------------------------+ $ openstack service create --name heat-cfn \ --description "Orchestration" cloudformation +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | c42cede91a4e47c3b10c8aedc8d890c6 | | name        | heat-cfn                         | | type        | cloudformation                   | +-------------+----------------------------------+

To create the service credentials, complete these steps:

- Create the heat user: $ openstack user create --domain default --password-prompt heat User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | e0353a670a9e496da891347c589539e9 | | enabled   | True                             | | id        | ca2e175b851943349be29a328cc5e360 | | name      | heat                             | +-----------+----------------------------------+

Create the heat user:

$ openstack user create --domain default --password-prompt heat User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | e0353a670a9e496da891347c589539e9 | | enabled   | True                             | | id        | ca2e175b851943349be29a328cc5e360 | | name      | heat                             | +-----------+----------------------------------+

- Add the admin role to the heat user: $ openstack role add --project service --user heat admin Note This command provides no output.

Add the admin role to the heat user:

$ openstack role add --project service --user heat admin

Note

This command provides no output.

- Create the heat and heat-cfn service entities: $ openstack service create --name heat \ --description "Orchestration" orchestration +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | 727841c6f5df4773baa4e8a5ae7d72eb | | name        | heat                             | | type        | orchestration                    | +-------------+----------------------------------+ $ openstack service create --name heat-cfn \ --description "Orchestration" cloudformation +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | c42cede91a4e47c3b10c8aedc8d890c6 | | name        | heat-cfn                         | | type        | cloudformation                   | +-------------+----------------------------------+

Create the heat and heat-cfn service entities:

$ openstack service create --name heat \ --description "Orchestration" orchestration +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | 727841c6f5df4773baa4e8a5ae7d72eb | | name        | heat                             | | type        | orchestration                    | +-------------+----------------------------------+ $ openstack service create --name heat-cfn \ --description "Orchestration" cloudformation +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Orchestration                    | | enabled     | True                             | | id          | c42cede91a4e47c3b10c8aedc8d890c6 | | name        | heat-cfn                         | | type        | cloudformation                   | +-------------+----------------------------------+

- Create the Orchestration service API endpoints: $ openstack endpoint create --region RegionOne \ orchestration public http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 3f4dab34624e4be7b000265f25049609        | | interface    | public                                  | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+ $ openstack endpoint create --region RegionOne \ orchestration internal http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 9489f78e958e45cc85570fec7e836d98        | | interface    | internal                                | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+ $ openstack endpoint create --region RegionOne \ orchestration admin http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 76091559514b40c6b7b38dde790efe99        | | interface    | admin                                   | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+ $ openstack endpoint create --region RegionOne \ cloudformation public http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | b3ea082e019c4024842bf0a80555052c | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ cloudformation internal http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 169df4368cdc435b8b115a9cb084044e | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ cloudformation admin http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 3d3edcd61eb343c1bbd629aa041ff88b | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+

Create the Orchestration service API endpoints:

$ openstack endpoint create --region RegionOne \ orchestration public http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 3f4dab34624e4be7b000265f25049609        | | interface    | public                                  | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+ $ openstack endpoint create --region RegionOne \ orchestration internal http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 9489f78e958e45cc85570fec7e836d98        | | interface    | internal                                | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+ $ openstack endpoint create --region RegionOne \ orchestration admin http://controller:8004/v1/% \( tenant_id \) s +--------------+-----------------------------------------+ | Field        | Value                                   | +--------------+-----------------------------------------+ | enabled      | True                                    | | id           | 76091559514b40c6b7b38dde790efe99        | | interface    | admin                                   | | region       | RegionOne                               | | region_id    | RegionOne                               | | service_id   | 727841c6f5df4773baa4e8a5ae7d72eb        | | service_name | heat                                    | | service_type | orchestration                           | | url          | http://controller:8004/v1/%(tenant_id)s | +--------------+-----------------------------------------+

$ openstack endpoint create --region RegionOne \ cloudformation public http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | b3ea082e019c4024842bf0a80555052c | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ cloudformation internal http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 169df4368cdc435b8b115a9cb084044e | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ cloudformation admin http://controller:8000/v1 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 3d3edcd61eb343c1bbd629aa041ff88b | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | c42cede91a4e47c3b10c8aedc8d890c6 | | service_name | heat-cfn                         | | service_type | cloudformation                   | | url          | http://controller:8000/v1        | +--------------+----------------------------------+

- Orchestration requires additional information in the Identity service to
manage stacks. To add this information, complete these steps: Create the heat domain that contains projects and users
for stacks: $ openstack domain create --description "Stack projects and users" heat +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Stack projects and users         | | enabled     | True                             | | id          | 0f4d1bd326f2454dacc72157ba328a47 | | name        | heat                             | +-------------+----------------------------------+ Create the heat_domain_admin user to manage projects and users
in the heat domain: $ openstack user create --domain heat --password-prompt heat_domain_admin User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | 0f4d1bd326f2454dacc72157ba328a47 | | enabled   | True                             | | id        | b7bd1abfbcf64478b47a0f13cd4d970a | | name      | heat_domain_admin                | +-----------+----------------------------------+ Add the admin role to the heat_domain_admin user in the heat domain to enable administrative stack management
privileges by the heat_domain_admin user: $ openstack role add --domain heat --user-domain heat --user heat_domain_admin admin Note This command provides no output. Create the heat_stack_owner role: $ openstack role create heat_stack_owner +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 15e34f0c4fed4e68b3246275883c8630 | | name      | heat_stack_owner                 | +-----------+----------------------------------+ Add the heat_stack_owner role to the demo project and user to
enable stack management by the demo user: $ openstack role add --project demo --user demo heat_stack_owner Note This command provides no output. Note You must add the heat_stack_owner role to each user
that manages stacks. Create the heat_stack_user role: $ openstack role create heat_stack_user +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 88849d41a55d4d1d91e4f11bffd8fc5c | | name      | heat_stack_user                  | +-----------+----------------------------------+ Note The Orchestration service automatically assigns the heat_stack_user role to users that it creates
during stack deployment. By default, this role restricts
API <Application Programming Interface (API)> operations.
To avoid conflicts, do not add
this role to users with the heat_stack_owner role.

Orchestration requires additional information in the Identity service to
manage stacks. To add this information, complete these steps:

- Create the heat domain that contains projects and users
for stacks: $ openstack domain create --description "Stack projects and users" heat +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Stack projects and users         | | enabled     | True                             | | id          | 0f4d1bd326f2454dacc72157ba328a47 | | name        | heat                             | +-------------+----------------------------------+

Create the heat domain that contains projects and users
for stacks:

$ openstack domain create --description "Stack projects and users" heat +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | Stack projects and users         | | enabled     | True                             | | id          | 0f4d1bd326f2454dacc72157ba328a47 | | name        | heat                             | +-------------+----------------------------------+

- Create the heat_domain_admin user to manage projects and users
in the heat domain: $ openstack user create --domain heat --password-prompt heat_domain_admin User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | 0f4d1bd326f2454dacc72157ba328a47 | | enabled   | True                             | | id        | b7bd1abfbcf64478b47a0f13cd4d970a | | name      | heat_domain_admin                | +-----------+----------------------------------+

Create the heat_domain_admin user to manage projects and users
in the heat domain:

$ openstack user create --domain heat --password-prompt heat_domain_admin User Password: Repeat User Password: +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | 0f4d1bd326f2454dacc72157ba328a47 | | enabled   | True                             | | id        | b7bd1abfbcf64478b47a0f13cd4d970a | | name      | heat_domain_admin                | +-----------+----------------------------------+

- Add the admin role to the heat_domain_admin user in the heat domain to enable administrative stack management
privileges by the heat_domain_admin user: $ openstack role add --domain heat --user-domain heat --user heat_domain_admin admin Note This command provides no output.

Add the admin role to the heat_domain_admin user in the heat domain to enable administrative stack management
privileges by the heat_domain_admin user:

$ openstack role add --domain heat --user-domain heat --user heat_domain_admin admin

Note

This command provides no output.

- Create the heat_stack_owner role: $ openstack role create heat_stack_owner +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 15e34f0c4fed4e68b3246275883c8630 | | name      | heat_stack_owner                 | +-----------+----------------------------------+

Create the heat_stack_owner role:

$ openstack role create heat_stack_owner +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 15e34f0c4fed4e68b3246275883c8630 | | name      | heat_stack_owner                 | +-----------+----------------------------------+

- Add the heat_stack_owner role to the demo project and user to
enable stack management by the demo user: $ openstack role add --project demo --user demo heat_stack_owner Note This command provides no output. Note You must add the heat_stack_owner role to each user
that manages stacks.

Add the heat_stack_owner role to the demo project and user to
enable stack management by the demo user:

$ openstack role add --project demo --user demo heat_stack_owner

Note

This command provides no output.

Note

You must add the heat_stack_owner role to each user
that manages stacks.

- Create the heat_stack_user role: $ openstack role create heat_stack_user +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 88849d41a55d4d1d91e4f11bffd8fc5c | | name      | heat_stack_user                  | +-----------+----------------------------------+ Note The Orchestration service automatically assigns the heat_stack_user role to users that it creates
during stack deployment. By default, this role restricts
API <Application Programming Interface (API)> operations.
To avoid conflicts, do not add
this role to users with the heat_stack_owner role.

Create the heat_stack_user role:

$ openstack role create heat_stack_user +-----------+----------------------------------+ | Field     | Value                            | +-----------+----------------------------------+ | domain_id | None                             | | id        | 88849d41a55d4d1d91e4f11bffd8fc5c | | name      | heat_stack_user                  | +-----------+----------------------------------+

Note

The Orchestration service automatically assigns the heat_stack_user role to users that it creates
during stack deployment. By default, this role restricts
API <Application Programming Interface (API)> operations.
To avoid conflicts, do not add
this role to users with the heat_stack_owner role.

## Install and configure components ¶

Note

Default configuration files vary by distribution. You might need
to add these sections and options rather than modifying existing
sections and options. Also, an ellipsis ( ... ) in the configuration
snippets indicates potential default configuration options that you
should retain.

- Install the packages: # apt-get install heat-api heat-api-cfn heat-engine

Install the packages:

# apt-get install heat-api heat-api-cfn heat-engine

- Edit the /etc/heat/heat.conf file and complete the following
actions: In the [database] section, configure database access: [database] ... connection = mysql+pymysql://heat:HEAT_DBPASS@controller/heat Replace HEAT_DBPASS with the password you chose for the
Orchestration database. In the [DEFAULT] section,
configure RabbitMQ message queue access: [DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ . In the [keystone_authtoken] , [trustee] and [clients_keystone] sections,
configure Identity service access: [keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = heat password = HEAT_PASS [trustee] ... auth_type = password auth_url = http://controller:5000 username = heat password = HEAT_PASS user_domain_name = Default [clients_keystone] ... auth_uri = http://controller:5000 Replace HEAT_PASS with the password you chose for the heat user in the Identity service. In the [DEFAULT] section, configure the metadata and
wait condition URLs: [DEFAULT] ... heat_metadata_server_url = http://controller:8000 heat_waitcondition_server_url = http://controller:8000/v1/waitcondition In the [DEFAULT] section, configure the stack domain and
administrative credentials: [DEFAULT] ... stack_domain_admin = heat_domain_admin stack_domain_admin_password = HEAT_DOMAIN_PASS stack_user_domain_name = heat Replace HEAT_DOMAIN_PASS with the password you chose for the heat_domain_admin user in the Identity service.

Edit the /etc/heat/heat.conf file and complete the following
actions:

- In the [database] section, configure database access: [database] ... connection = mysql+pymysql://heat:HEAT_DBPASS@controller/heat Replace HEAT_DBPASS with the password you chose for the
Orchestration database.

In the [database] section, configure database access:

[database] ... connection = mysql+pymysql://heat:HEAT_DBPASS@controller/heat

Replace HEAT_DBPASS with the password you chose for the
Orchestration database.

- In the [DEFAULT] section,
configure RabbitMQ message queue access: [DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ .

In the [DEFAULT] section,
configure RabbitMQ message queue access:

[DEFAULT] ... transport_url = rabbit://openstack:RABBIT_PASS@controller

Replace RABBIT_PASS with the password you chose for the openstack account in RabbitMQ .

- In the [keystone_authtoken] , [trustee] and [clients_keystone] sections,
configure Identity service access: [keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = heat password = HEAT_PASS [trustee] ... auth_type = password auth_url = http://controller:5000 username = heat password = HEAT_PASS user_domain_name = Default [clients_keystone] ... auth_uri = http://controller:5000 Replace HEAT_PASS with the password you chose for the heat user in the Identity service.

In the [keystone_authtoken] , [trustee] and [clients_keystone] sections,
configure Identity service access:

[keystone_authtoken] ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = heat password = HEAT_PASS [trustee] ... auth_type = password auth_url = http://controller:5000 username = heat password = HEAT_PASS user_domain_name = Default [clients_keystone] ... auth_uri = http://controller:5000

Replace HEAT_PASS with the password you chose for the heat user in the Identity service.

- In the [DEFAULT] section, configure the metadata and
wait condition URLs: [DEFAULT] ... heat_metadata_server_url = http://controller:8000 heat_waitcondition_server_url = http://controller:8000/v1/waitcondition

In the [DEFAULT] section, configure the metadata and
wait condition URLs:

[DEFAULT] ... heat_metadata_server_url = http://controller:8000 heat_waitcondition_server_url = http://controller:8000/v1/waitcondition

- In the [DEFAULT] section, configure the stack domain and
administrative credentials: [DEFAULT] ... stack_domain_admin = heat_domain_admin stack_domain_admin_password = HEAT_DOMAIN_PASS stack_user_domain_name = heat Replace HEAT_DOMAIN_PASS with the password you chose for the heat_domain_admin user in the Identity service.

In the [DEFAULT] section, configure the stack domain and
administrative credentials:

[DEFAULT] ... stack_domain_admin = heat_domain_admin stack_domain_admin_password = HEAT_DOMAIN_PASS stack_user_domain_name = heat

Replace HEAT_DOMAIN_PASS with the password you chose for the heat_domain_admin user in the Identity service.

- Populate the Orchestration database: # su -s /bin/sh -c "heat-manage db_sync" heat Note Ignore any deprecation messages in this output.

Populate the Orchestration database:

# su -s /bin/sh -c "heat-manage db_sync" heat

Note

Ignore any deprecation messages in this output.

## Finalize installation ¶

- Restart the Orchestration services: # service heat-api restart # service heat-api-cfn restart # service heat-engine restart

Restart the Orchestration services:

# service heat-api restart # service heat-api-cfn restart # service heat-engine restart
