# Using service tokens Â¶

Warning

For all OpenStack releases after 2023-05-10, it is required that Nova be
configured to send a service token to Cinder and Cinder to receive it.  This
is required by the fix for CVE-2023-2088 .  See OSSA-2023-003 for details.

When a user initiates a request whose processing involves multiple services
(for example, a boot-from-volume request to the Compute Service will require
processing by the Block Storage Service, and may require processing by the
Image Service), the userâs token is handed from service to service.  This
ensures that the requestor is tracked correctly for audit purposes and also
guarantees that the requestor has the appropriate permissions to do what needs
to be done by the other services.

There are several instances where we want to differentiate between a request
coming from the user to one coming from another OpenStack service on behalf of
the user:

- For security reasons There are some operations in the Block Storage
service, required for normal operations, that could be exploited by a
malicious user to gain access to resources belonging to other users.  By
differentiating when the request comes directly from a user and when from
another OpenStack service the Cinder service can protect the deployment.

For security reasons There are some operations in the Block Storage
service, required for normal operations, that could be exploited by a
malicious user to gain access to resources belonging to other users.  By
differentiating when the request comes directly from a user and when from
another OpenStack service the Cinder service can protect the deployment.

- To prevent long-running job failures: If the chain of operations takes a long
time, the userâs token may expire before the action is completed, leading to
the failure of the userâs original request. One way to deal with this is to set a long token life in Keystone, and this
may be what you are currently doing.  But this can be problematic for
installations whose security policies prefer short user token lives.
Beginning with the Queens release, an alternative solution is available.  You
have the ability to configure some services (particularly Nova and Cinder) to
send a âservice tokenâ along with the userâs token.  When properly
configured, the Identity Service will validate an expired user token when it
is accompanied by a valid service token .  Thus if the userâs token expires
somewhere during a long running chain of operations among various OpenStack
services, the operations can continue.

To prevent long-running job failures: If the chain of operations takes a long
time, the userâs token may expire before the action is completed, leading to
the failure of the userâs original request.

One way to deal with this is to set a long token life in Keystone, and this
may be what you are currently doing.  But this can be problematic for
installations whose security policies prefer short user token lives.
Beginning with the Queens release, an alternative solution is available.  You
have the ability to configure some services (particularly Nova and Cinder) to
send a âservice tokenâ along with the userâs token.  When properly
configured, the Identity Service will validate an expired user token when it
is accompanied by a valid service token .  Thus if the userâs token expires
somewhere during a long running chain of operations among various OpenStack
services, the operations can continue.

Note

Thereâs nothing special about a service token.  Itâs a regular token
that has been requested by a service user.  And thereâs nothing special
about a service user, itâs just a user that has been configured in the
Identity Service to have specific roles that identify that user as
a service.

The key point here is that the âservice tokenâ doesnât need to have
an extra long life â it can have the same short life as all the
other tokens because it will be a fresh (and hence valid) token
accompanying the (possibly expired) userâs token.

## Configuration Â¶

To configure an OpenStack service that supports Service Tokens, like Nova and
Cinder, to send a âservice tokenâ along with the userâs token when it makes a
request to another service, you must do the following:

- Configure the âsenderâ services to send the token when calling other
OpenStack services.

Configure the âsenderâ services to send the token when calling other
OpenStack services.

- Configure each serviceâs user to have a service role in Keystone.

Configure each serviceâs user to have a service role in Keystone.

- Configure the âreceiverâ services to expect the token and validate it
appropriately on reception.

Configure the âreceiverâ services to expect the token and validate it
appropriately on reception.

### Send service token Â¶

To send the token we need to add to our configuration file the [service_user] section and fill it in with the appropriate configuration
for your service user ( username , project_name , etc.) and set the send_service_user_token option to true to tell the service to send the
token.

The configuration for the service user is basically the normal keystone user
configuration like we would have in the [keystone_authtoken] section, but
without the 2 configuration options weâll see in one of the next subsection to
configure the reception of service tokens.

In most cases we would use the same user we do in [keystone_authtoken] , for
example for the nova configuration we would have something like this:

[service_user] send_service_user_token = True # Copy following options from [keystone_authtoken] section project_domain_name = Default project_name = service user_domain_name = Default password = abc123 username = nova auth_url = http://192.168.121.66/identity auth_type = password

### Service role Â¶

A service role is nothing more than a Keystone role that allows a deployment to
identify a service without the need to make them admins, that way there is no
change in the privileges but we are able to identify that the request is
coming from another service and not a user.

The default service role is service , but we can use a different name or
even have multiple service roles.  For simplicityâs sake we recommend having
just one, service .

We need to make sure that the user configured in the [service_user] section
for a project has a service role.

Assuming our users are nova and cinder from the service project and
the service role is going to be the default service , we first check if the role exists or not :

$ openstack role show service

If it doesnât, we need to create it

$ openstack role create service

Check if the users have the roles assigned or not:

$ openstack role assignment list --user cinder --project service --names
$ openstack role assignment list --user nova --project service --names

And if they are not we assign the role to those users

$ openstack role add --user cinder --project service service
$ openstack role add --user nova --project service service

More information on creating service users can be found in the Keystone
documentation

### Receive service token Â¶

Now we need to make the services validate the service token on reception, this
part is crucial.

The 2 configuration options in [keystone_authoken] related to receiving
service tokens are service_token_roles and service_token_roles_required .

The service_token_roles contains a list of roles that we consider to belong
to services.  The service user must belong to at least one of them to be
considered a valid service token.  The value defaults to service , so we
donât need to set it if thatâs the value we are using.

Now we need to tell the keystone middleware to actually validate the service
token and confirm that itâs not only a valid token, but that it has one of the
roles set in service_token_roles . We do this by setting service_token_roles_required to true .

So we would have something like this in our [keystone_authtoken] section:

[keystone_authtoken] service_token_roles = service service_token_roles_required = true

## Troubleshooting Â¶

If youâve configured this feature and are still having long-running
job failures, there are basically three degrees of freedom to take into
account: (1) each source service, (2) each receiving service, and (3) the
Identity Service (Keystone).

- Each source service (basically, Nova and Cinder) must have the [service_user] section in the source service configuration
file filled in as described in the Configuration section above. Note As of the 2023.1 release, Glance does not have the ability to pass
service tokens. It can receive them, though.  The place where you may
still see a long running failure is when Glance is using a backend that
requires Keystone validation (for example, the Swift backend) and the
user token has expired.

Each source service (basically, Nova and Cinder) must have the [service_user] section in the source service configuration
file filled in as described in the Configuration section above.

Note

As of the 2023.1 release, Glance does not have the ability to pass
service tokens. It can receive them, though.  The place where you may
still see a long running failure is when Glance is using a backend that
requires Keystone validation (for example, the Swift backend) and the
user token has expired.

- There are several things to pay attention to in Keystone: When service_token_roles_required is enabled you must make sure that
any service user who will be contacting that receiving service (and for
whom you want to enable âservice tokenâ usage) has one of the roles
specified in the receiving servicesâs service_token_roles setting.
(This is a matter of creating and assigning roles using the Identity
Service API, itâs not a configuration file issue.) Even with a service token, an expired user token cannot be used
indefinitely.  Thereâs a Keystone configuration setting that controls
this: [token]/allow_expired_window in the Keystone configuration
file.  The default setting is 2 days, so some security teams may want to
lower this just on general principles.  You need to make sure itâs not
set too low to be completely ineffective. If you are using Fernet tokens, you need to be careful with your Fernet
key rotation period.  Whoever sets up the key rotation has to pay
attention to the [token]/allow_expired_window setting as well as the
obvious [token]/expiration setting.  If keys get rotated faster than expiration + allow_expired_window seconds, an expired user
token might not be decryptable, even though the request using it is
being made within allow_expired_window seconds.

There are several things to pay attention to in Keystone:

- When service_token_roles_required is enabled you must make sure that
any service user who will be contacting that receiving service (and for
whom you want to enable âservice tokenâ usage) has one of the roles
specified in the receiving servicesâs service_token_roles setting.
(This is a matter of creating and assigning roles using the Identity
Service API, itâs not a configuration file issue.)

When service_token_roles_required is enabled you must make sure that
any service user who will be contacting that receiving service (and for
whom you want to enable âservice tokenâ usage) has one of the roles
specified in the receiving servicesâs service_token_roles setting.
(This is a matter of creating and assigning roles using the Identity
Service API, itâs not a configuration file issue.)

- Even with a service token, an expired user token cannot be used
indefinitely.  Thereâs a Keystone configuration setting that controls
this: [token]/allow_expired_window in the Keystone configuration
file.  The default setting is 2 days, so some security teams may want to
lower this just on general principles.  You need to make sure itâs not
set too low to be completely ineffective.

Even with a service token, an expired user token cannot be used
indefinitely.  Thereâs a Keystone configuration setting that controls
this: [token]/allow_expired_window in the Keystone configuration
file.  The default setting is 2 days, so some security teams may want to
lower this just on general principles.  You need to make sure itâs not
set too low to be completely ineffective.

- If you are using Fernet tokens, you need to be careful with your Fernet
key rotation period.  Whoever sets up the key rotation has to pay
attention to the [token]/allow_expired_window setting as well as the
obvious [token]/expiration setting.  If keys get rotated faster than expiration + allow_expired_window seconds, an expired user
token might not be decryptable, even though the request using it is
being made within allow_expired_window seconds.

If you are using Fernet tokens, you need to be careful with your Fernet
key rotation period.  Whoever sets up the key rotation has to pay
attention to the [token]/allow_expired_window setting as well as the
obvious [token]/expiration setting.  If keys get rotated faster than expiration + allow_expired_window seconds, an expired user
token might not be decryptable, even though the request using it is
being made within allow_expired_window seconds.

To summarize, you need to be aware of:

- Keystone: must allow a decent sized allow_expired_window (default is 2
days)

Keystone: must allow a decent sized allow_expired_window (default is 2
days)

- Each source service: must be configured to be able to create and send
service tokens (default is OFF)

Each source service: must be configured to be able to create and send
service tokens (default is OFF)

- Each receiving service: has to be configured to accept service tokens
(default is ON) and require role verification (default is OFF)

Each receiving service: has to be configured to accept service tokens
(default is ON) and require role verification (default is OFF)
