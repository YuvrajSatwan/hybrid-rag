# Install and configure (Red Hat) ¶

This section describes how to install and configure the Image service,
code-named glance, on the controller node. For simplicity, this
configuration stores images on the local file system.

## Prerequisites ¶

Before you install and configure the Image service, you must
create a database, service credentials, and API endpoints.

- To create the database, complete these steps: Use the database access client to connect to the database
server as the root user: $ mysql -u root -p Create the glance database: MariaDB [(none)]> CREATE DATABASE glance; Grant proper access to the glance database: MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \ IDENTIFIED BY 'GLANCE_DBPASS'; MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \ IDENTIFIED BY 'GLANCE_DBPASS'; Replace GLANCE_DBPASS with a suitable password. Exit the database access client.

To create the database, complete these steps:

- Use the database access client to connect to the database
server as the root user: $ mysql -u root -p

Use the database access client to connect to the database
server as the root user:

$ mysql -u root -p

- Create the glance database: MariaDB [(none)]> CREATE DATABASE glance;

Create the glance database:

MariaDB [(none)]> CREATE DATABASE glance;

- Grant proper access to the glance database: MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \ IDENTIFIED BY 'GLANCE_DBPASS'; MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \ IDENTIFIED BY 'GLANCE_DBPASS'; Replace GLANCE_DBPASS with a suitable password.

Grant proper access to the glance database:

MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \ IDENTIFIED BY 'GLANCE_DBPASS'; MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \ IDENTIFIED BY 'GLANCE_DBPASS';

Replace GLANCE_DBPASS with a suitable password.

- Exit the database access client.

Exit the database access client.

- Source the admin credentials to gain access to
admin-only CLI commands: $ . admin-openrc

Source the admin credentials to gain access to
admin-only CLI commands:

$ . admin-openrc

- To create the service credentials, complete these steps: Create the glance user: $ openstack user create --domain default --password-prompt glance User Password: Repeat User Password: +---------------------+----------------------------------+ | Field               | Value                            | +---------------------+----------------------------------+ | domain_id           | default                          | | enabled             | True                             | | id                  | 3f4e777c4062483ab8d9edd7dff829df | | name                | glance                           | | options             | {}                               | | password_expires_at | None                             | +---------------------+----------------------------------+ Add the admin role to the glance user and service project: $ openstack role add --project service --user glance admin Note This command provides no output. Create the glance service entity: $ openstack service create --name glance \ --description "OpenStack Image" image +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | OpenStack Image                  | | enabled     | True                             | | id          | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | name        | glance                           | | type        | image                            | +-------------+----------------------------------+

To create the service credentials, complete these steps:

- Create the glance user: $ openstack user create --domain default --password-prompt glance User Password: Repeat User Password: +---------------------+----------------------------------+ | Field               | Value                            | +---------------------+----------------------------------+ | domain_id           | default                          | | enabled             | True                             | | id                  | 3f4e777c4062483ab8d9edd7dff829df | | name                | glance                           | | options             | {}                               | | password_expires_at | None                             | +---------------------+----------------------------------+

Create the glance user:

$ openstack user create --domain default --password-prompt glance User Password: Repeat User Password: +---------------------+----------------------------------+ | Field               | Value                            | +---------------------+----------------------------------+ | domain_id           | default                          | | enabled             | True                             | | id                  | 3f4e777c4062483ab8d9edd7dff829df | | name                | glance                           | | options             | {}                               | | password_expires_at | None                             | +---------------------+----------------------------------+

- Add the admin role to the glance user and service project: $ openstack role add --project service --user glance admin Note This command provides no output.

Add the admin role to the glance user and service project:

$ openstack role add --project service --user glance admin

Note

This command provides no output.

- Create the glance service entity: $ openstack service create --name glance \ --description "OpenStack Image" image +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | OpenStack Image                  | | enabled     | True                             | | id          | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | name        | glance                           | | type        | image                            | +-------------+----------------------------------+

Create the glance service entity:

$ openstack service create --name glance \ --description "OpenStack Image" image +-------------+----------------------------------+ | Field       | Value                            | +-------------+----------------------------------+ | description | OpenStack Image                  | | enabled     | True                             | | id          | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | name        | glance                           | | type        | image                            | +-------------+----------------------------------+

- Create the Image service API endpoints: $ openstack endpoint create --region RegionOne \ image public http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 340be3625e9b4239a6415d034e98aace | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ image internal http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | a6e4b153c2ae4c919eccfdbb7dceb5d2 | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ image admin http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 0c37ed58103f4300a84ff125a539032d | | interface    | admin                            | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+

Create the Image service API endpoints:

$ openstack endpoint create --region RegionOne \ image public http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 340be3625e9b4239a6415d034e98aace | | interface    | public                           | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ image internal http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | a6e4b153c2ae4c919eccfdbb7dceb5d2 | | interface    | internal                         | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+ $ openstack endpoint create --region RegionOne \ image admin http://controller:9292 +--------------+----------------------------------+ | Field        | Value                            | +--------------+----------------------------------+ | enabled      | True                             | | id           | 0c37ed58103f4300a84ff125a539032d | | interface    | admin                            | | region       | RegionOne                        | | region_id    | RegionOne                        | | service_id   | 8c2c7f1b9b5049ea9e63757b5533e6d2 | | service_name | glance                           | | service_type | image                            | | url          | http://controller:9292           | +--------------+----------------------------------+

- Register quota limits (optional): If you decide to use per-tenant quotas in Glance, you must register
the limits in Keystone first: $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 1000 --region RegionOne image_size_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 1000                             | | description   | None                             | | id            | 9cedfc5de80345a9b13ed00c2b5460f2 | | region_id     | RegionOne                        | | resource_name | image_size_total                 | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 1000 --region RegionOne image_stage_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 1000                             | | description   | None                             | | id            | 5a68712b6ba6496d823d0c66e5e860b9 | | region_id     | RegionOne                        | | resource_name | image_stage_total                | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 100 --region RegionOne image_count_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 100                              | | description   | None                             | | id            | beb91b043296499f8e6268f29d8b2749 | | region_id     | RegionOne                        | | resource_name | image_count_total                | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 100 --region RegionOne \ image_count_uploading +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 100                              | | description   | None                             | | id            | fc29649c047a45bf9bc03ec4a7bcb8af | | region_id     | RegionOne                        | | resource_name | image_count_uploading            | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ Be sure to also set use_keystone_limits=True in your glance-api.conf file.

Register quota limits (optional):

If you decide to use per-tenant quotas in Glance, you must register
the limits in Keystone first:

$ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 1000 --region RegionOne image_size_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 1000                             | | description   | None                             | | id            | 9cedfc5de80345a9b13ed00c2b5460f2 | | region_id     | RegionOne                        | | resource_name | image_size_total                 | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 1000 --region RegionOne image_stage_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 1000                             | | description   | None                             | | id            | 5a68712b6ba6496d823d0c66e5e860b9 | | region_id     | RegionOne                        | | resource_name | image_stage_total                | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 100 --region RegionOne image_count_total +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 100                              | | description   | None                             | | id            | beb91b043296499f8e6268f29d8b2749 | | region_id     | RegionOne                        | | resource_name | image_count_total                | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+ $ openstack --os-cloud devstack-system-admin registered limit create \ --service glance --default-limit 100 --region RegionOne \ image_count_uploading +---------------+----------------------------------+ | Field         | Value                            | +---------------+----------------------------------+ | default_limit | 100                              | | description   | None                             | | id            | fc29649c047a45bf9bc03ec4a7bcb8af | | region_id     | RegionOne                        | | resource_name | image_count_uploading            | | service_id    | e38c84a2487f49fd9864193bdc8a3174 | +---------------+----------------------------------+

Be sure to also set use_keystone_limits=True in your glance-api.conf file.

## Install and configure components ¶

Note

Default configuration files vary by distribution. You might need
to add these sections and options rather than modifying existing
sections and options. Also, an ellipsis ( ... ) in the configuration
snippets indicates potential default configuration options that you
should retain.

- Install the packages: # dnf install openstack-glance

Install the packages:

# dnf install openstack-glance

- Edit the /etc/glance/glance-api.conf file and complete the
following actions: In the [database] section, configure database access: [database] # ... connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance Replace GLANCE_DBPASS with the password you chose for the
Image service database. In the [keystone_authtoken] and [paste_deploy] sections,
configure Identity service access: [keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = glance password = GLANCE_PASS [paste_deploy] # ... flavor = keystone Replace GLANCE_PASS with the password you chose for the glance user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section. In the [glance_store] section, configure the local file
system store and location of image files: [DEFAULT] # ... enabled_backends = fs:file [glance_store] # ... default_backend = fs [fs] filesystem_store_datadir = /var/lib/glance/images/ In the [oslo_limit] section, configure access to keystone: [oslo_limit] auth_url = http://controller:5000 auth_type = password user_domain_id = default username = glance system_scope = all password = GLANCE_PASS endpoint_id = ENDPOINT_ID region_name = RegionOne Replace GLANCE_PASS with the password you chose for the glance user in the Identity service. Replace ENDPOINT_ID with the ID of the image endpoint you
created earlier (in our case, this would be
340be3625e9b4239a6415d034e98aace), and that you may find by running: $ openstack endpoint list --service glance --region RegionOne Make sure that the glance account has reader access to
system-scope resources (like limits): $ openstack role add --user glance --user-domain Default --system all reader See the oslo_limit docs for more information about configuring the unified limits client. In the [DEFAULT] section, optionally enable per-tenant quotas: [DEFAULT] use_keystone_limits = True Note that you must have created the registered limits as
described above if this is enabled.

Edit the /etc/glance/glance-api.conf file and complete the
following actions:

- In the [database] section, configure database access: [database] # ... connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance Replace GLANCE_DBPASS with the password you chose for the
Image service database.

In the [database] section, configure database access:

[database] # ... connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance

Replace GLANCE_DBPASS with the password you chose for the
Image service database.

- In the [keystone_authtoken] and [paste_deploy] sections,
configure Identity service access: [keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = glance password = GLANCE_PASS [paste_deploy] # ... flavor = keystone Replace GLANCE_PASS with the password you chose for the glance user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section.

In the [keystone_authtoken] and [paste_deploy] sections,
configure Identity service access:

[keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = Default user_domain_name = Default project_name = service username = glance password = GLANCE_PASS [paste_deploy] # ... flavor = keystone

Replace GLANCE_PASS with the password you chose for the glance user in the Identity service.

Note

Comment out or remove any other options in the [keystone_authtoken] section.

- In the [glance_store] section, configure the local file
system store and location of image files: [DEFAULT] # ... enabled_backends = fs:file [glance_store] # ... default_backend = fs [fs] filesystem_store_datadir = /var/lib/glance/images/

In the [glance_store] section, configure the local file
system store and location of image files:

[DEFAULT] # ... enabled_backends = fs:file [glance_store] # ... default_backend = fs [fs] filesystem_store_datadir = /var/lib/glance/images/

- In the [oslo_limit] section, configure access to keystone: [oslo_limit] auth_url = http://controller:5000 auth_type = password user_domain_id = default username = glance system_scope = all password = GLANCE_PASS endpoint_id = ENDPOINT_ID region_name = RegionOne Replace GLANCE_PASS with the password you chose for the glance user in the Identity service. Replace ENDPOINT_ID with the ID of the image endpoint you
created earlier (in our case, this would be
340be3625e9b4239a6415d034e98aace), and that you may find by running: $ openstack endpoint list --service glance --region RegionOne Make sure that the glance account has reader access to
system-scope resources (like limits): $ openstack role add --user glance --user-domain Default --system all reader See the oslo_limit docs for more information about configuring the unified limits client.

In the [oslo_limit] section, configure access to keystone:

[oslo_limit] auth_url = http://controller:5000 auth_type = password user_domain_id = default username = glance system_scope = all password = GLANCE_PASS endpoint_id = ENDPOINT_ID region_name = RegionOne

Replace GLANCE_PASS with the password you chose for the glance user in the Identity service.

Replace ENDPOINT_ID with the ID of the image endpoint you
created earlier (in our case, this would be
340be3625e9b4239a6415d034e98aace), and that you may find by running:

$ openstack endpoint list --service glance --region RegionOne

Make sure that the glance account has reader access to
system-scope resources (like limits):

$ openstack role add --user glance --user-domain Default --system all reader

See the oslo_limit docs for more information about configuring the unified limits client.

- In the [DEFAULT] section, optionally enable per-tenant quotas: [DEFAULT] use_keystone_limits = True Note that you must have created the registered limits as
described above if this is enabled.

In the [DEFAULT] section, optionally enable per-tenant quotas:

[DEFAULT] use_keystone_limits = True

Note that you must have created the registered limits as
described above if this is enabled.

- Populate the Image service database: # su -s /bin/sh -c "glance-manage db_sync" glance Note Ignore any deprecation messages in this output.

Populate the Image service database:

# su -s /bin/sh -c "glance-manage db_sync" glance

Note

Ignore any deprecation messages in this output.

## Finalize installation ¶

- Start the Image services and configure them to start when
the system boots: # systemctl enable openstack-glance-api.service # systemctl start openstack-glance-api.service

Start the Image services and configure them to start when
the system boots:

# systemctl enable openstack-glance-api.service # systemctl start openstack-glance-api.service
