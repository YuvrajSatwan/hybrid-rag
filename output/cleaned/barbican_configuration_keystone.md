# Using Keystone Middleware with Barbican Â¶

## Prerequisites Â¶

To enable Keystone integration with Barbican youâll need a relatively current
version of Keystone. It is sufficient if you are installing an OpenStack cloud
where all services including Keystone and Barbican are from the same release.
If you donât have an instance of Keystone available, you can use one of the
following ways to setup your own.

- Simple Dockerized Keystone

Simple Dockerized Keystone

- Installing Keystone

Installing Keystone

- An OpenStack cloud with Keystone (Devstack in the simplest case)

An OpenStack cloud with Keystone (Devstack in the simplest case)

## Hooking up Barbican to Keystone Â¶

Assuming that youâve already setup your Keystone instance, connecting
Barbican to Keystone is quite simple. When completed, Barbican should
require a valid X-Auth-Token to be provided with all API calls except
the get version call.

- Turn off any active instances of Barbican

Turn off any active instances of Barbican

- Edit /etc/barbican/barbican-api-paste.ini Change the pipeline /v1 value from unauthenticated barbican_api to the authenticated barbican-api-keystone . This step will not be
necessary on barbican from OpenStack Newton or higher, since barbican
will default to using Keystone authentication as of OpenStack Newton. [composite:main] use = egg:Paste #urlmap / : barbican_version /v1 : barbican-api-keystone Replace authtoken filter values to match your Keystone
setup [filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 Alternatively, you can shorten this to [filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory and store Barbicanâs Keystone credentials in the [keystone_authtoken] section of /etc/barbican/barbican.conf [keystone_authtoken] auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3

Edit /etc/barbican/barbican-api-paste.ini

- Change the pipeline /v1 value from unauthenticated barbican_api to the authenticated barbican-api-keystone . This step will not be
necessary on barbican from OpenStack Newton or higher, since barbican
will default to using Keystone authentication as of OpenStack Newton. [composite:main] use = egg:Paste #urlmap / : barbican_version /v1 : barbican-api-keystone

Change the pipeline /v1 value from unauthenticated barbican_api to the authenticated barbican-api-keystone . This step will not be
necessary on barbican from OpenStack Newton or higher, since barbican
will default to using Keystone authentication as of OpenStack Newton.

[composite:main] use = egg:Paste #urlmap / : barbican_version /v1 : barbican-api-keystone

- Replace authtoken filter values to match your Keystone
setup [filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 Alternatively, you can shorten this to [filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory and store Barbicanâs Keystone credentials in the [keystone_authtoken] section of /etc/barbican/barbican.conf [keystone_authtoken] auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3

Replace authtoken filter values to match your Keystone
setup

[filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3

Alternatively, you can shorten this to

[filter:authtoken] paste.filter_factory = keystonemiddleware.auth_token:filter_factory

and store Barbicanâs Keystone credentials in the [keystone_authtoken] section of /etc/barbican/barbican.conf

[keystone_authtoken] auth_plugin = password username = {YOUR_KEYSTONE_USERNAME} password = {YOUR_KEYSTONE_PASSWORD} user_domain_id = {YOUR_KEYSTONE_USER_DOMAIN} project_name = {YOUR_KEYSTONE_PROJECT} project_domain_id = {YOUR_KEYSTONE_PROJECT_DOMAIN} www_authenticate_uri = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3 auth_url = http://{YOUR_KEYSTONE_ENDPOINT}:5000/v3

- Start Barbican {barbican_home}/bin/barbican.sh start

Start Barbican {barbican_home}/bin/barbican.sh start
