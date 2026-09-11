# The Auth System Â¶

## Overview Â¶

Swift supports a number of auth systems that share the following common
characteristics:

- The authentication/authorization part can be an external system or a
subsystem run within Swift as WSGI middleware

The authentication/authorization part can be an external system or a
subsystem run within Swift as WSGI middleware

- The user of Swift passes in an auth token with each request

The user of Swift passes in an auth token with each request

- Swift validates each token with the external auth system or auth subsystem
and caches the result

Swift validates each token with the external auth system or auth subsystem
and caches the result

- The token does not change from request to request, but does expire

The token does not change from request to request, but does expire

The token can be passed into Swift using the X-Auth-Token or the
X-Storage-Token header. Both have the same format: just a simple string
representing the token. Some auth systems use UUID tokens, some an MD5 hash of
something unique, some use âsomething elseâ but the salient point is that the
token is a string which can be sent as-is back to the auth system for
validation.

Swift will make calls to the auth system, giving the auth token to be
validated. For a valid token, the auth system responds with an overall
expiration time in seconds from now. To avoid the overhead in validating the same
token over and over again, Swift will cache the
token for a configurable time, but no longer than the expiration
time.

The Swift project includes two auth systems:

- TempAuth

TempAuth

- Keystone Auth

Keystone Auth

It is also possible to write your own auth system as described in Extending Auth .

## TempAuth Â¶

TempAuth is used primarily in Swiftâs functional test environment and can be
used in other test environments (such as SAIO (Swift All In One) ). It is not
recommended to use TempAuth in a production system. However, TempAuth is fully
functional and can be used as a model to develop your own auth system.

TempAuth has the concept of admin and non-admin users
within an account.  Admin users can do anything within the account.
Non-admin users can only perform read operations. However, some
privileged metadata such as X-Container-Sync-Key is not accessible to
non-admin users.

Users with the special group .reseller_admin can operate on any account.
For an example usage please see swift.common.middleware.tempauth .
If a request is coming from a reseller the auth system sets the request environ
reseller_request to True. This can be used by other middlewares.

Other users may be granted the ability to perform operations on
an account or container via ACLs. TempAuth supports two types of ACL:

- Per container ACLs based on the
containerâs X-Container-Read and X-Container-Write metadata. See Container ACLs for more information.

Per container ACLs based on the
containerâs X-Container-Read and X-Container-Write metadata. See Container ACLs for more information.

- Per account ACLs based on the accountâs X-Account-Access-Control metadata. For more information see Account ACLs .

Per account ACLs based on the accountâs X-Account-Access-Control metadata. For more information see Account ACLs .

TempAuth will now allow OPTIONS requests to go through without a token.

The TempAuth middleware is responsible for creating its own tokens. A user
makes a request containing their username and password and TempAuth
responds with a token. This token is then used to perform subsequent
requests on the userâs account, containers and objects.

## Keystone Auth Â¶

Swift is able to authenticate against OpenStack Keystone . In this
environment, Keystone is responsible for creating and validating
tokens. The KeystoneAuth middleware is responsible for
implementing the auth system within Swift as described here.

The KeystoneAuth middleware supports per container based ACLs on the
containerâs X-Container-Read and X-Container-Write metadata.
For more information see Container ACLs .

The account-level ACL is not supported by Keystone auth.

In order to use the keystoneauth middleware the auth_token middleware from KeystoneMiddleware will need to be configured.

The authtoken middleware performs the authentication token
validation and retrieves actual user authentication information. It
can be found in the KeystoneMiddleware distribution.

The KeystoneAuth middleware performs authorization and mapping the
Keystone roles to Swiftâs ACLs.

### Configuring Swift to use Keystone Â¶

Configuring Swift to use Keystone is relatively straightforward.  The first
step is to ensure that you have the auth_token middleware installed. It can
either be dropped in your python path or installed via the KeystoneMiddleware package.

You need at first make sure you have a service endpoint of type object-store in Keystone pointing to your Swift proxy. For example
having this in your /etc/keystone/default_catalog.templates

catalog.RegionOne.object_store.name = Swift Service
catalog.RegionOne.object_store.publicURL = http://swiftproxy:8080/v1/AUTH_$(tenant_id)s
catalog.RegionOne.object_store.adminURL = http://swiftproxy:8080/
catalog.RegionOne.object_store.internalURL = http://swiftproxy:8080/v1/AUTH_$(tenant_id)s

On your Swift proxy server you will want to adjust your main pipeline
and add auth_token and keystoneauth in your /etc/swift/proxy-server.conf like this

[ pipeline : main ] pipeline = [ .... ] authtoken keystoneauth proxy - logging proxy - server

add the configuration for the authtoken middleware:

[ filter : authtoken ] paste . filter_factory = keystonemiddleware . auth_token : filter_factory www_authenticate_uri = http : // keystonehost : 5000 / auth_url = http : // keystonehost : 5000 / auth_plugin = password project_domain_id = default user_domain_id = default project_name = service username = swift password = password cache = swift . cache include_service_catalog = False delay_auth_decision = True

The actual values for these variables will need to be set depending on
your situation, but in short:

- www_authenticate_uri should point to a Keystone service from which users may
retrieve tokens. This value is used in the WWW-Authenticate header that
auth_token sends with any denial response.

www_authenticate_uri should point to a Keystone service from which users may
retrieve tokens. This value is used in the WWW-Authenticate header that
auth_token sends with any denial response.

- auth_url points to the Keystone Admin service. This information is
used by the middleware to actually query Keystone about the validity of the
authentication tokens. It is not necessary to append any Keystone API version
number to this URI.

auth_url points to the Keystone Admin service. This information is
used by the middleware to actually query Keystone about the validity of the
authentication tokens. It is not necessary to append any Keystone API version
number to this URI.

- The auth credentials ( project_domain_id , user_domain_id , username , project_name , password ) will be used to retrieve an
admin token. That token will be used to authorize user tokens behind the
scenes. These credentials must match the Keystone credentials for the Swift
service. The example values shown here assume a user named âswiftâ with admin
role on a project named âserviceâ, both being in the Keystone domain with id
âdefaultâ. Refer to the KeystoneMiddleware documentation for other examples.

The auth credentials ( project_domain_id , user_domain_id , username , project_name , password ) will be used to retrieve an
admin token. That token will be used to authorize user tokens behind the
scenes. These credentials must match the Keystone credentials for the Swift
service. The example values shown here assume a user named âswiftâ with admin
role on a project named âserviceâ, both being in the Keystone domain with id
âdefaultâ. Refer to the KeystoneMiddleware documentation for other examples.

- cache is set to swift.cache . This means that the middleware
will get the Swift memcache from the request environment.

cache is set to swift.cache . This means that the middleware
will get the Swift memcache from the request environment.

- include_service_catalog defaults to True if not set. This means
that when validating a token, the service catalog is retrieved
and stored in the X-Service-Catalog header. This is required if you use
access-rules in Application Credentials. You may also need to increase max_header_size .

include_service_catalog defaults to True if not set. This means
that when validating a token, the service catalog is retrieved
and stored in the X-Service-Catalog header. This is required if you use
access-rules in Application Credentials. You may also need to increase max_header_size .

Note

The authtoken config variable delay_auth_decision must be set to True . The default is False , but that breaks public access, StaticWeb , FormPost , TempURL , and authenticated
capabilities requests (using Discoverability ).

and you can finally add the keystoneauth configuration. Here is a simple
configuration:

[ filter : keystoneauth ] use = egg : swift #keystoneauth operator_roles = admin , swiftoperator

Use an appropriate list of roles in operator_roles. For example, in
some systems, the role _member_ or Member is used to indicate
that the user is allowed to operate on project resources.

#### OpenStack Service Using Composite Tokens Â¶

Some OpenStack services such as Cinder and Glance may use
a âservice accountâ. In this mode, you configure a separate account where
the service stores project data that it manages. This account is not used
directly by the end-user. Instead, all access is done through the service.

To access the âserviceâ account, the service must present two tokens: one from
the end-user and another from its own service user. Only when both tokens are
present can the account be accessed. This section describes how to set the
configuration options to correctly control access to both the ânormalâ and
âserviceâ accounts.

In this example, end users use the AUTH_ prefix in account names,
whereas services use the SERVICE_ prefix:

[ filter : keystoneauth ] use = egg : swift #keystoneauth reseller_prefix = AUTH , SERVICE operator_roles = admin , swiftoperator SERVICE_service_roles = service

The actual values for these variable will need to be set depending on your
situation as follows:

- The first item in the reseller_prefix list must match Keystoneâs endpoint
(see /etc/keystone/default_catalog.templates above). Normally
this is AUTH .

The first item in the reseller_prefix list must match Keystoneâs endpoint
(see /etc/keystone/default_catalog.templates above). Normally
this is AUTH .

- The second item in the reseller_prefix list is the prefix used by the
OpenStack services(s). You must configure this value ( SERVICE in the
example) with whatever the other OpenStack service(s) use.

The second item in the reseller_prefix list is the prefix used by the
OpenStack services(s). You must configure this value ( SERVICE in the
example) with whatever the other OpenStack service(s) use.

- Set the operator_roles option to contain a role or roles that end-userâs
have on projectâs they use.

Set the operator_roles option to contain a role or roles that end-userâs
have on projectâs they use.

- Set the SERVICE_service_roles value to a role or roles that only the
OpenStack service user has. Do not use a role that is assigned to
ânormalâ end users. In this example, the role service is used.
The service user is granted this role to a single project only. You do
not need to make the service user a member of every project.

Set the SERVICE_service_roles value to a role or roles that only the
OpenStack service user has. Do not use a role that is assigned to
ânormalâ end users. In this example, the role service is used.
The service user is granted this role to a single project only. You do
not need to make the service user a member of every project.

This configuration works as follows:

- The end-user presents a user token to an OpenStack service. The service
then makes a Swift request to the account with the SERVICE prefix.

The end-user presents a user token to an OpenStack service. The service
then makes a Swift request to the account with the SERVICE prefix.

- The service forwards the original user token with the request. It also
adds itâs own service token.

The service forwards the original user token with the request. It also
adds itâs own service token.

- Swift validates both tokens. When validated, the user token gives the admin or swiftoperator role(s). When validated, the service token
gives the service role.

Swift validates both tokens. When validated, the user token gives the admin or swiftoperator role(s). When validated, the service token
gives the service role.

- Swift interprets the above configuration as follows: Did the user token provide one of the roles listed in operator_roles? Did the service token have the service role as described by the SERVICE_service_roles options.

Swift interprets the above configuration as follows:

- Did the user token provide one of the roles listed in operator_roles?

Did the user token provide one of the roles listed in operator_roles?

- Did the service token have the service role as described by the SERVICE_service_roles options.

Did the service token have the service role as described by the SERVICE_service_roles options.

- If both conditions are met, the request is granted. Otherwise, Swift
rejects the request.

If both conditions are met, the request is granted. Otherwise, Swift
rejects the request.

In the above example, all services share the same account. You can separate
each service into its own account. For example, the following provides a
dedicated account for each of the Glance and Cinder services. In addition,
you must assign the glance_service and cinder_service to the
appropriate service users:

[ filter : keystoneauth ] use = egg : swift #keystoneauth reseller_prefix = AUTH , IMAGE , VOLUME operator_roles = admin , swiftoperator IMAGE_service_roles = glance_service VOLUME_service_roles = cinder_service

### Access control using keystoneauth Â¶

By default the only users able to perform operations (e.g. create a container)
on an account are those having a Keystone role for the corresponding Keystone
project that matches one of the roles specified in the operator_roles option.

Users who have one of the operator_roles will be able to set container ACLs
to grant other users permission to read and/or write objects in specific
containers, using X-Container-Read and X-Container-Write headers
respectively. In addition to the ACL formats described here , keystoneauth supports ACLs using the
format:

other_project_id : other_user_id .

where other_project_id is the UUID of a Keystone project and other_user_id is the UUID of a Keystone user. This will allow the other
user to access a container provided their token is scoped on the other
project. Both other_project_id and other_user_id may be replaced with
the wildcard character * which will match any project or user respectively.

Be sure to use Keystone UUIDs rather than names in container ACLs.

Note

For backwards compatibility, keystoneauth will by default grant container
ACLs expressed as other_project_name:other_user_name (i.e. using
Keystone names rather than UUIDs) in the special case when both the other
project and the other user are in Keystoneâs default domain and the project
being accessed is also in the default domain.

For further information see KeystoneAuth

Users with the Keystone role defined in reseller_admin_role ( ResellerAdmin by default) can operate on any account. The auth system
sets the request environ reseller_request to True if a request is coming
from a user with this role. This can be used by other middlewares.

### Troubleshooting tips for keystoneauth deployment Â¶

Some common mistakes can result in API requests failing when first deploying
keystone with Swift:

- Incorrect configuration of the Swift endpoint in the Keystone service. By default, keystoneauth expects the account part of a URL to have the form AUTH_<keystone_project_id> . Sometimes the AUTH_ prefix is missed when
configuring Swift endpoints in Keystone, as described in the Install  Guide . This is easily diagnosed by inspecting the
proxy-server log file for a failed request URL and checking that the URL
includes the AUTH_ prefix (or whatever reseller prefix may have been
configured for keystoneauth): GOOD : proxy - server : 127.0.0.1 127.0.0.1 07 / Sep / 2016 / 16 / 06 / 58 HEAD / v1 / AUTH_cfb8d9d45212408b90bc0776117aec9e HTTP / 1.0 204 ... BAD : proxy - server : 127.0.0.1 127.0.0.1 07 / Sep / 2016 / 16 / 07 / 35 HEAD / v1 / cfb8d9d45212408b90bc0776117aec9e HTTP / 1.0 403 ...

Incorrect configuration of the Swift endpoint in the Keystone service.

By default, keystoneauth expects the account part of a URL to have the form AUTH_<keystone_project_id> . Sometimes the AUTH_ prefix is missed when
configuring Swift endpoints in Keystone, as described in the Install  Guide . This is easily diagnosed by inspecting the
proxy-server log file for a failed request URL and checking that the URL
includes the AUTH_ prefix (or whatever reseller prefix may have been
configured for keystoneauth):

GOOD : proxy - server : 127.0.0.1 127.0.0.1 07 / Sep / 2016 / 16 / 06 / 58 HEAD / v1 / AUTH_cfb8d9d45212408b90bc0776117aec9e HTTP / 1.0 204 ... BAD : proxy - server : 127.0.0.1 127.0.0.1 07 / Sep / 2016 / 16 / 07 / 35 HEAD / v1 / cfb8d9d45212408b90bc0776117aec9e HTTP / 1.0 403 ...

- Incorrect configuration of the authtoken middleware options in the Swift
proxy server. The authtoken middleware communicates with the Keystone service to
validate tokens that are presented with client requests. To do this authtoken must authenticate itself with Keystone using the credentials
configured in the [filter:authtoken] section of /etc/swift/proxy-server.conf . Errors in these credentials can result in authtoken failing to validate tokens and may be revealed in the proxy
server logs by a message such as: proxy - server : Identity server rejected authorization Note More detailed log messaging may be seen by setting the authtoken option log_level = debug . The authtoken configuration options may be checked by attempting to use
them to communicate directly with Keystone using an openstack command
line. For example, given the authtoken configuration sample shown in Configuring Swift to use Keystone , the following command should return a
service catalog: openstack -- os - identity - api - version = 3 -- os - auth - url = http : // keystonehost : 5000 / \ -- os - username = swift -- os - user - domain - id = default \ -- os - project - name = service -- os - project - domain - id = default \ -- os - password = password catalog show object - store If this openstack command fails then it is likely that there is a problem
with the authtoken configuration.

Incorrect configuration of the authtoken middleware options in the Swift
proxy server.

The authtoken middleware communicates with the Keystone service to
validate tokens that are presented with client requests. To do this authtoken must authenticate itself with Keystone using the credentials
configured in the [filter:authtoken] section of /etc/swift/proxy-server.conf . Errors in these credentials can result in authtoken failing to validate tokens and may be revealed in the proxy
server logs by a message such as:

proxy - server : Identity server rejected authorization

Note

More detailed log messaging may be seen by setting the authtoken option log_level = debug .

The authtoken configuration options may be checked by attempting to use
them to communicate directly with Keystone using an openstack command
line. For example, given the authtoken configuration sample shown in Configuring Swift to use Keystone , the following command should return a
service catalog:

openstack -- os - identity - api - version = 3 -- os - auth - url = http : // keystonehost : 5000 / \ -- os - username = swift -- os - user - domain - id = default \ -- os - project - name = service -- os - project - domain - id = default \ -- os - password = password catalog show object - store

If this openstack command fails then it is likely that there is a problem
with the authtoken configuration.

## Extending Auth Â¶

TempAuth is written as wsgi middleware, so implementing your own auth is as
easy as writing new wsgi middleware, and plugging it in to the proxy server.

See Auth Server and Middleware for detailed information on extending the
auth system.
