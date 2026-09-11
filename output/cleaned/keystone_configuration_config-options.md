# API Configuration options Â¶

## Configuration Â¶

The Identity service is configured in the /etc/keystone/keystone.conf file.

The following tables provide a comprehensive list of the Identity
service options.

For a sample configuration file, refer to keystone.conf .

### DEFAULT Â¶

string

<None>

Using this feature is NOT recommended. Instead, use the keystone-manage bootstrap command. The value of this option is treated as a âshared secretâ that can be used to bootstrap Keystone through the API. This âtokenâ does not represent a user (it has no identity), and carries no explicit authorization (it effectively bypasses most authorization checks). If set to None , the value is ignored and the admin_token middleware is effectively disabled.

URI

<None>

The base public endpoint URL for Keystone that is advertised to clients (NOTE: this does NOT affect how Keystone listens for connections). Defaults to the base host URL of the request. For example, if keystone receives a request to http://server:5000/v3/users , then this will option will be automatically treated as http://server:5000 . You should only need to set option if either the value of the base URL contains a path that keystone does not automatically infer ( /prefix/v3 ), or if the endpoint should be found on a different host.

integer

5

Maximum depth of the project hierarchy, excluding the project acting as a domain at the top of the hierarchy. WARNING: Setting it to a large value may adversely impact performance.

integer

64

Limit the sizes of user & project ID/names.

Warning

This option is deprecated for removal since 2025.1.
Its value may be silently ignored 
in the future.

This option has had no effect.

integer

255

Similar to [DEFAULT] max_param_size , but provides an exception for token values. With Fernet tokens, this can be set as low as 255.

integer

<None>

The maximum number of entities that will be returned in a collection. This global limit may be then overridden for a specific driver, by specifying a list_limit in the appropriate section (for example, [assignment] ). No limit is set by default. In larger deployments, it is recommended that you set this to a reasonable number to prevent operations like listing all users and projects from placing an unnecessary load on the system.

integer

1000

0

As a query can potentially return many thousands of items, you can limit the maximum number of items in a single response by setting this option. While list_limit is used to set the default page size this parameter sets global maximum that cannot be exceded.

boolean

False

If set to true, strict password length checking is performed for password manipulation. If a password exceeds the maximum length, the operation will fail with an HTTP 403 Forbidden error. If set to false, passwords are automatically truncated to the maximum length.

boolean

False

If set to true, then the server will return information in HTTP responses that may allow an unauthenticated or authenticated user to get more information than normal, such as additional details about why authentication failed. This may be useful for debugging but is insecure.

string

<None>

Default publisher_id for outgoing notifications. If left undefined, Keystone will default to using the serverâs host name.

string

cadf

basic, cadf

Define the notification format for identity service events. A basic notification only has information about the resource being operated on. A cadf notification has the same information, as well as information about the initiator of the event. The cadf option is entirely backwards compatible with the basic option, but is fully CADF-compliant, and is recommended for auditing use cases.

multi-valued

identity.authenticate.success

identity.authenticate.pending

You can reduce the number of notifications keystone emits by explicitly opting out. Keystone will not emit notifications that match the patterns expressed in this list. Values are expected to be in the form of identity.<resource_type>.<operation> . By default, all notifications related to authentication are automatically suppressed. This field can be set multiple times in order to opt-out of multiple notification topics. For example, the following suppresses notifications describing user creation or successful authentication events: notification_opt_out=identity.user.create notification_opt_out=identity.authenticate.success

boolean

False

This option can be changed without restarting.

If set to true, the logging level will be set to DEBUG instead of the default INFO level.

string

<None>

This option can be changed without restarting.

The name of a logging configuration file. This file is appended to any existing logging configuration files. For details about logging configuration files, see the Python logging module documentation. Note that when logging configuration files are used then all logging configuration is set in the configuration file and other logging configuration options are ignored (for example, log-date-format).

Deprecated Variations Â¶ Group Name DEFAULT log-config DEFAULT log_config

Group

Name

DEFAULT

log-config

DEFAULT

log_config

string

%Y-%m-%d %H:%M:%S

Defines the format string for %(asctime)s in log records. Default: the value above . This option is ignored if log_config_append is set.

string

<None>

(Optional) Name of log file to send logging output to. If no default is set, logging will go to stderr as defined by use_stderr. This option is ignored if log_config_append is set.

Deprecated Variations Â¶ Group Name DEFAULT logfile

Group

Name

DEFAULT

logfile

string

<None>

(Optional) The base directory used for relative log_file  paths. This option is ignored if log_config_append is set.

Deprecated Variations Â¶ Group Name DEFAULT logdir

Group

Name

DEFAULT

logdir

boolean

False

Use syslog for logging. Existing syslog format is DEPRECATED and will be changed later to honor RFC5424. This option is ignored if log_config_append is set.

boolean

False

Enable journald for logging. If running in a systemd environment you may wish to enable journal support. Doing so will use the journal native protocol which includes structured metadata in addition to log messages.This option is ignored if log_config_append is set.

string

LOG_USER

Syslog facility to receive log lines. This option is ignored if log_config_append is set.

boolean

False

Use JSON formatting for logging. This option is ignored if log_config_append is set.

boolean

False

Log output to standard error. This option is ignored if log_config_append is set.

boolean

False

(Optional) Set the âcolorâ key according to log levels. This option takes effect only when logging to stderr or stdout is used. This option is ignored if log_config_append is set.

integer

1

The amount of time before the log files are rotated. This option is ignored unless log_rotation_type is set to âintervalâ.

string

days

Seconds, Minutes, Hours, Days, Weekday, Midnight

Rotation interval type. The time of the last file change (or the time when the service was started) is used when scheduling the next rotation.

integer

30

Maximum number of rotated log files.

integer

200

Log file maximum size in MB. This option is ignored if âlog_rotation_typeâ is not set to âsizeâ.

string

none

interval, size, none

Log rotation type.

Possible values

Rotate logs at predefined time intervals.

Rotate logs once they reach a predefined size.

Do not rotate log files.

string

%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(global_request_id)s %(request_id)s %(user_identity)s] %(instance)s%(message)s

Format string to use for log messages with context. Used by oslo_log.formatters.ContextFormatter

string

%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s

Format string to use for log messages when context is undefined. Used by oslo_log.formatters.ContextFormatter

string

%(funcName)s %(pathname)s:%(lineno)d

Additional data to append to log message when logging level for the message is DEBUG. Used by oslo_log.formatters.ContextFormatter

string

%(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s

Prefix each line of exception output with this format. Used by oslo_log.formatters.ContextFormatter

string

%(user)s %(project)s %(domain)s %(system_scope)s %(user_domain)s %(project_domain)s

Defines the format string for %(user_identity)s that is used in logging_context_format_string. Used by oslo_log.formatters.ContextFormatter

list

INFO

List of package logging levels in logger=LEVEL pairs. This option is ignored if log_config_append is set.

boolean

False

Enables or disables publication of error events.

string

"[instance: %(uuid)s] "

The format for an instance that is passed with the log message.

string

"[instance: %(uuid)s] "

The format for an instance UUID that is passed with the log message.

integer

0

Interval, number of seconds, of log rate limiting.

integer

0

Maximum number of logged messages per rate_limit_interval.

string

CRITICAL

CRITICAL, ERROR, INFO, WARNING, DEBUG, ââ

Log level name used by rate limiting. Logs with level greater or equal to rate_limit_except_level are not filtered. An empty string means that all levels are filtered.

boolean

False

Enables or disables fatal status of deprecations.

integer

64

Size of executor thread pool when executor is threading or eventlet.

Deprecated Variations Â¶ Group Name DEFAULT rpc_thread_pool_size

Group

Name

DEFAULT

rpc_thread_pool_size

integer

60

Seconds to wait for a response from a call.

string

rabbit://

The network address and optional user credentials for connecting to the messaging backend, in URL format. The expected format is:

driver://[user:pass@]host:port[,[userN:passN@]hostN:portN]/virtual_host?query

Example: rabbit://rabbitmq:password@127.0.0.1:5672//

For full details on the fields in the URL see the documentation of oslo_messaging.TransportURL at https://docs.openstack.org/oslo.messaging/latest/reference/transport.html

string

keystone

The default exchange under which topics are scoped. May be overridden by an exchange name specified in the transport_url option.

boolean

False

Add an endpoint to answer to ping calls. Endpoint is named oslo_rpc_server_ping

### api Â¶

string

warn

error, warn, ignore

Configure validation of API responses. warn is the current recommendation for production environments. If you find it necessary to enable the ignore option, please report the issues you are seeing to the Keystone team so we can improve our schemas. error should not be used in a production environment. This is because schema validation happens after the response body has been generated, meaning any side effects will still happen and the call may be non-idempotent despite the user receiving a HTTP 500 error.

Possible values

Raise a HTTP 500 (Server Error) for responses that fail schema validation

Log a warning for responses that fail schema validation

Ignore schema validation failures

### application_credential Â¶

string

sql

Entry point for the application credential backend driver in the keystone.application_credential namespace.  Keystone only provides a sql driver, so there is no reason to change this unless you are providing a custom entry point.

boolean

True

Toggle for application credential caching. This has no effect unless global caching is enabled.

integer

<None>

Time to cache application credential data in seconds. This has no effect unless global caching is enabled.

integer

-1

Maximum number of application credentials a user is permitted to create. A value of -1 means unlimited. If a limit is not set, users are permitted to create application credentials at will, which could lead to bloat in the keystone database or open keystone to a DoS attack.

### assignment Â¶

string

sql

Entry point for the assignment backend driver (where role assignments are stored) in the keystone.assignment namespace. Only a SQL driver is supplied by keystone itself. Unless you are writing proprietary drivers for keystone, you do not need to set this option.

list

['admin']

A list of role names which are prohibited from being an implied role.

### auth Â¶

list

['external', 'password', 'token', 'oauth1', 'mapped', 'application_credential']

Allowed authentication methods. Note: You should disable the external auth method if you are currently using federation. External auth and federation both use the REMOTE_USER variable. Since both the mapped and external plugin are being invoked to validate attributes in the request environment, it can cause conflicts.

string

<None>

Entry point for the password auth plugin module in the keystone.auth.password namespace. You do not need to set this unless you are overriding keystoneâs own password authentication plugin.

string

<None>

Entry point for the token auth plugin module in the keystone.auth.token namespace. You do not need to set this unless you are overriding keystoneâs own token authentication plugin.

string

<None>

Entry point for the external ( REMOTE_USER ) auth plugin module in the keystone.auth.external namespace. Supplied drivers are DefaultDomain and Domain . The default driver is DefaultDomain , which assumes that all users identified by the username specified to keystone in the REMOTE_USER variable exist within the context of the default domain. The Domain option expects an additional environment variable be presented to keystone, REMOTE_DOMAIN , containing the domain name of the REMOTE_USER (if REMOTE_DOMAIN is not set, then the default domain will be used instead). You do not need to set this unless you are taking advantage of âexternal authenticationâ, where the application server (such as Apache) is handling authentication instead of keystone.

string

<None>

Entry point for the OAuth 1.0a auth plugin module in the keystone.auth.oauth1 namespace. You do not need to set this unless you are overriding keystoneâs own oauth1 authentication plugin.

string

<None>

Entry point for the mapped auth plugin module in the keystone.auth.mapped namespace. You do not need to set this unless you are overriding keystoneâs own mapped authentication plugin.

string

<None>

Entry point for the application_credential auth plugin module in the keystone.auth.application_credential namespace. You do not need to set this unless you are overriding keystoneâs own application_credential authentication plugin.

### cache Â¶

string

cache.oslo

Prefix for building the configuration dictionary for the cache region. This should not need to be changed unless there is another dogpile.cache region with the same configuration name.

integer

600

1

Default TTL, in seconds, for any cached item in the dogpile.cache region. This applies to any cached method that doesnât have an explicit cache expiration time defined for it.

integer

<None>

1

Expiration time in cache backend to purge expired records automatically. This should be greater than expiration_time and all cache_time options

string

dogpile.cache.null

oslo_cache.memcache_pool, oslo_cache.dict, oslo_cache.etcd3gw, dogpile.cache.pymemcache, dogpile.cache.memcached, dogpile.cache.pylibmc, dogpile.cache.bmemcached, dogpile.cache.dbm, dogpile.cache.redis, dogpile.cache.redis_sentinel, dogpile.cache.memory, dogpile.cache.memory_pickle, dogpile.cache.null

Cache backend module. For eventlet-based or environments with hundreds of threaded servers, Memcache with pooling (oslo_cache.memcache_pool) is recommended. For environments with less than 100 threaded servers, Memcached (dogpile.cache.memcached) or Redis (dogpile.cache.redis) is recommended. Test environments with a single instance of the server can use the dogpile.cache.memory backend.

multi-valued

''

Arguments supplied to the backend module. Specify this option once per argument to be passed to the dogpile.cache backend. Example format: â<argname>:<value>â.

list

[]

Proxy classes to import that will affect the way the dogpile.cache backend functions. See the dogpile.cache documentation on changing-backend-behavior.

boolean

True

Global toggle for caching.

boolean

False

Extra debugging from the cache backend (cache keys, get/set/delete/etc calls). This is only really useful if you need to see the specific cache-backend get/set/delete calls with the keys/values.  Typically this should be left set to false.

list

['localhost:11211']

Memcache servers in the format of âhost:portâ. This is used by backends dependent on Memcached.If dogpile.cache.memcached or oslo_cache.memcache_pool is used and a given host refer to an IPv6 or a given domain refer to IPv6 then you should prefix the given address with the address family ( inet6 ) (e.g inet6:[::1]:11211 , inet6:[fd12:3456:789a:1::1]:11211 , inet6:[controller-0.internalapi]:11211 ). If the address family is not given then these backends will use the default inet address family which corresponds to IPv4

integer

300

Number of seconds memcached server is considered dead before it is tried again. (dogpile.cache.memcache and oslo_cache.memcache_pool backends only).

integer

10

Max total number of open connections to every memcached server. (oslo_cache.memcache_pool backend only).

integer

60

Number of seconds a connection to memcached is held unused in the pool before it is closed. (oslo_cache.memcache_pool backend only).

integer

10

Number of seconds that an operation will wait to get a memcache client connection.

boolean

False

Global toggle if memcache will be flushed on reconnect. (oslo_cache.memcache_pool backend only).

boolean

False

Enable the SASL(Simple Authentication and SecurityLayer) if the SASL_enable is true, else disable.

string

localhost:6379

Redis server in the format of âhost:portâ

integer

0

0

Database id in Redis server

list

['localhost:26379']

Redis sentinel servers in the format of âhost:portâ

string

mymaster

Service name of the redis sentinel cluster.

string

<None>

the user name for authentication to backend.

Deprecated Variations Â¶ Group Name cache memcache_username cache redis_username

Group

Name

cache

memcache_username

cache

redis_username

string

<None>

the password for authentication to backend.

Deprecated Variations Â¶ Group Name cache memcache_password cache redis_password

Group

Name

cache

memcache_password

cache

redis_password

boolean

False

Global toggle for TLS usage when communicating with the caching servers. Currently supported by dogpile.cache.bmemcache , dogpile.cache.pymemcache , oslo_cache.memcache_pool , dogpile.cache.redis and dogpile.cache.redis_sentinel .

string

<None>

Path to a file of concatenated CA certificates in PEM format necessary to establish the caching serversâ authenticity. If tls_enabled is False, this option is ignored.

string

<None>

Path to a single file in PEM format containing the clientâs certificate as well as any number of CA certificates needed to establish the certificateâs authenticity. This file is only required when client side authentication is necessary. If tls_enabled is False, this option is ignored.

string

<None>

Path to a single file containing the clientâs private key in. Otherwise the private key will be taken from the file specified in tls_certfile. If tls_enabled is False, this option is ignored.

string

<None>

Set the available ciphers for sockets created with the TLS context. It should be a string in the OpenSSL cipher list format. If not specified, all OpenSSL enabled ciphers will be available. Currently supported by dogpile.cache.bmemcache , dogpile.cache.pymemcache and oslo_cache.memcache_pool .

floating point

1.0

Timeout in seconds for every call to a server. Currently supported by dogpile.cache.memcache , oslo_cache.memcache_pool , dogpile.cache.redis and dogpile.cache.redis_sentinel .

Deprecated Variations Â¶ Group Name cache memcache_socket_timeout cache redis_socket_timeout

Group

Name

cache

memcache_socket_timeout

cache

redis_socket_timeout

boolean

False

Global toggle for the socket keepalive of dogpileâs pymemcache backend

integer

1

0

The time (in seconds) the connection needs to remain idle before TCP starts sending keepalive probes. Should be a positive integer most greater than zero.

integer

1

0

The time (in seconds) between individual keepalive probes. Should be a positive integer greater than zero.

integer

1

0

The maximum number of keepalive probes TCP should send before dropping the connection. Should be a positive integer greater than zero.

boolean

False

Enable retry client mechanisms to handle failure. Those mechanisms can be used to wrap all kind of pymemcache clients. The wrapper allows you to define how many attempts to make and how long to wait between attempts.

integer

2

1

Number of times to attempt an action before failing.

floating point

0

Number of seconds to sleep between each attempt.

integer

2

1

Amount of times a client should be tried before it is marked dead and removed from the pool in the HashClientâs internal mechanisms.

floating point

1

Time in seconds that should pass between retry attempts in the HashClientâs internal mechanisms.

Deprecated Variations Â¶ Group Name cache hashclient_retry_delay

Group

Name

cache

hashclient_retry_delay

floating point

60

Time in seconds before attempting to add a node back in the pool in the HashClientâs internal mechanisms.

Deprecated Variations Â¶ Group Name cache dead_timeout

Group

Name

cache

dead_timeout

boolean

False

Global toggle for enforcing the OpenSSL FIPS mode. This feature requires Python support. This is available in Python 3.9 in all environments and may have been backported to older Python versions on select environments. If the Python executable used does not support OpenSSL FIPS mode, an exception will be raised. Currently supported by dogpile.cache.bmemcache , dogpile.cache.pymemcache and oslo_cache.memcache_pool .

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

FIPS_mode_set API was removed in OpenSSL 3.0.0. This option has no effect now.

### catalog Â¶

string

sql

Entry point for the catalog driver in the keystone.catalog namespace. Keystone provides a sql option (which supports basic CRUD operations through SQL) and a endpoint_filter.sql option (which supports arbitrary service catalogs per project).

boolean

True

Toggle for catalog caching. This has no effect unless global caching is enabled. In a typical deployment, there is no reason to disable this.

integer

<None>

Time to cache catalog data (in seconds). This has no effect unless global and catalog caching are both enabled. Catalog data (services, endpoints, etc.) typically does not change frequently, and so a longer duration than the global default may be desirable.

integer

<None>

Maximum number of entities that will be returned in a catalog collection. There is typically no reason to set this, as it would be unusual for a deployment to have enough services or endpoints to exceed a reasonable limit.

### cors Â¶

list

<None>

Indicate whether this resource may be shared with the domain received in the requests âoriginâ header. Format: â<protocol>://<host>[:<port>]â, no trailing slash. Example: https://horizon.example.com

boolean

True

Indicate that the actual request can include user credentials

list

['X-Auth-Token', 'X-Openstack-Request-Id', 'X-Subject-Token', 'Openstack-Auth-Receipt']

Indicate which headers are safe to expose to the API. Defaults to HTTP Simple Headers.

integer

3600

Maximum cache age of CORS preflight requests.

list

['GET', 'PUT', 'POST', 'DELETE', 'PATCH']

Indicate which methods can be used during the actual request.

list

['X-Auth-Token', 'X-Openstack-Request-Id', 'X-Subject-Token', 'X-Project-Id', 'X-Project-Name', 'X-Project-Domain-Id', 'X-Project-Domain-Name', 'X-Domain-Id', 'X-Domain-Name', 'Openstack-Auth-Receipt']

Indicate which header field names may be used during the actual request.

### credential Â¶

string

sql

Entry point for the credential backend driver in the keystone.credential namespace. Keystone only provides a sql driver, so thereâs no reason to change this unless you are providing a custom entry point.

string

fernet

Entry point for credential encryption and decryption operations in the keystone.credential.provider namespace. Keystone only provides a fernet driver, so thereâs no reason to change this unless you are providing a custom entry point to encrypt and decrypt credentials.

string

/etc/keystone/credential-keys/

Directory containing Fernet keys used to encrypt and decrypt credentials stored in the credential backend. Fernet keys used to encrypt credentials have no relationship to Fernet keys used to encrypt Fernet tokens. Both sets of keys should be managed separately and require different rotation policies. Do not share this repository with the repository used to manage keys for Fernet tokens.

boolean

True

Toggle for caching only on retrieval of user credentials. This has no effect unless global caching is enabled.

integer

<None>

Time to cache credential data in seconds. This has no effect unless global caching is enabled.

integer

15

The length of time in minutes for which a signed EC2 or S3 token request is valid from the timestamp contained in the token request.

integer

-1

Maximum number of credentials a user is permitted to create. A value of -1 means unlimited. If a limit is not set, users are permitted to create credentials at will, which could lead to bloat in the keystone database or open keystone to a DoS attack.

### database Â¶

boolean

True

If True, SQLite uses synchronous mode.

string

sqlalchemy

The back end to use for the database.

string

<None>

The SQLAlchemy connection string to use to connect to the database.

string

<None>

The SQLAlchemy connection string to use to connect to the slave database.

string

<None>

The SQLAlchemy asyncio connection string to use to connect to the database.

string

<None>

The SQLAlchemy asyncio connection string to use to connect to the slave database.

boolean

True

Whether or not to assume a reader context needs to guarantee it can read data committed by a writer assuming replication lag is present; defaults to True. When False, a reader context works the same as async_reader and will select the slave database if present. When using a galera cluster, this can be set to False only if you set mysql_wsrep_sync_wait to 1 (this will guarantee that the reader will wait until writesets are committed).Note that this may incur a performance degradation within the galera cluster. Note also that this parameter has no effect if you do not set any slave_connection.

string

TRADITIONAL

The SQL mode to be used for MySQL sessions. This option, including the default, overrides any server-set SQL mode. To use whatever SQL mode is set by the server configuration, set this to no value. Example: mysql_sql_mode=

integer

<None>

For Galera only, configure wsrep_sync_wait causality checks on new connections.  Default is None, meaning donât configure any setting.

integer

3600

Connections which have been present in the connection pool longer than this number of seconds will be replaced with a new one the next time they are checked out from the pool.

integer

5

Maximum number of SQL connections to keep open in a pool. Setting a value of 0 indicates no limit.

integer

10

Maximum number of database connection retries during startup. Set to -1 to specify an infinite retry count.

integer

10

Interval between retries of opening a SQL connection.

integer

50

If set, use this value for max_overflow with SQLAlchemy.

integer

0

0

100

Verbosity of SQL debugging information: 0=None, 100=Everything.

boolean

False

Add Python stack traces to SQL as comment strings.

integer

<None>

If set, use this value for pool_timeout with SQLAlchemy.

boolean

False

Enable the experimental use of database reconnect on connection lost.

integer

1

Seconds between retries of a database transaction.

boolean

True

If True, increases the interval between retries of a database operation up to db_max_retry_interval.

integer

10

If db_inc_retry_interval is set, the maximum seconds between retries of a database operation.

integer

20

Maximum retries in case of connection error or deadlock error before error is raised. Set to -1 to specify an infinite retry count.

string

''

Optional URL parameters to append onto the connection URL at connect time; specify as param1=value1&param2=value2&â¦

### domain_config Â¶

string

sql

Entry point for the domain-specific configuration driver in the keystone.resource.domain_config namespace. Only a sql option is provided by keystone, so there is no reason to set this unless you are providing a custom entry point.

boolean

True

Toggle for caching of the domain-specific configuration backend. This has no effect unless global caching is enabled. There is normally no reason to disable this.

integer

300

Time-to-live (TTL, in seconds) to cache domain-specific configuration data. This has no effect unless [domain_config] caching is enabled.

unknown type

<None>

Additional whitelisted domain-specific options for out-of-tree drivers. This is a dictonary of lists with the key being the group name and value a list of group options.

unknown type

<None>

Additional sensitive domain-specific options for out-of-tree drivers. This is a dictonary of lists with the key being the group name and value a list of group options.

### endpoint_filter Â¶

string

sql

Entry point for the endpoint filter driver in the keystone.endpoint_filter namespace. Only a sql option is provided by keystone, so there is no reason to set this unless you are providing a custom entry point.

boolean

True

This controls keystoneâs behavior if the configured endpoint filters do not result in any endpoints for a user + project pair (and therefore a potentially empty service catalog). If set to true, keystone will return the entire service catalog. If set to false, keystone will return an empty service catalog.

### endpoint_policy Â¶

string

sql

Entry point for the endpoint policy driver in the keystone.endpoint_policy namespace. Only a sql driver is provided by keystone, so there is no reason to set this unless you are providing a custom entry point.

### federation Â¶

string

sql

Entry point for the federation backend driver in the keystone.federation namespace. Keystone only provides a sql driver, so there is no reason to set this option unless you are providing a custom entry point.

string

''

Prefix to use when filtering environment variable names for federated assertions. Matched variables are passed into the federated mapping engine.

string

<None>

Default value for all protocols to be used to obtain the entity ID of the Identity Provider from the environment. For mod_shib , this would be Shib-Identity-Provider . For mod_auth_openidc , this could be HTTP_OIDC_ISS . For mod_auth_mellon , this could be MELLON_IDP . This can be overridden on a per-protocol basis by providing a remote_id_attribute to the federation protocol using the API.

string

Federated

An arbitrary domain name that is reserved to allow federated ephemeral users to have a domain concept. Note that an admin will not be able to create a domain with this name or update an existing domain to this name. You are not advised to change this value unless you really have to.

Warning

This option is deprecated for removal since T.
Its value may be silently ignored 
in the future.

This option has been superseded by ephemeral users existing in the domain of their identity provider.

multi-valued

''

A list of trusted dashboard hosts. Before accepting a Single Sign-On request to return a token, the origin host must be a member of this list. This configuration option may be repeated for multiple values. You must set this in order to use web-based SSO flows. For example: trusted_dashboard=https://acme.example.com/auth/websso trusted_dashboard=https://beta.example.com/auth/websso

string

/etc/keystone/sso_callback_template.html

Absolute path to an HTML file used as a Single Sign-On callback handler. This page is expected to redirect the user from keystone back to a trusted dashboard host, by form encoding a token in a POST request. Keystoneâs default value should be sufficient for most deployments.

boolean

True

Toggle for federation caching. This has no effect unless global caching is enabled. There is typically no reason to disable this.

integer

0

Default time in minutes for the validity of group memberships carried over from a mapping. Default is 0, which means disabled.

string

1.0

The attribute mapping default schema version to be used, if the attribute mapping being registered does not have a schema version. One must bear in mind that changing this value will have no effect on attribute mappings that were previously registered when another default value was applied. Once registered, one needs to update the attribute mapping schema via the update API to be able to change an attribute mapping schema version.

### fernet_receipts Â¶

string

/etc/keystone/fernet-keys/

Directory containing Fernet receipt keys. This directory must exist before using keystone-manage fernet_setup for the first time, must be writable by the user running keystone-manage fernet_setup or keystone-manage fernet_rotate , and of course must be readable by keystoneâs server process. The repository may contain keys in one of three states: a single staged key (always index 0) used for receipt validation, a single primary key (always the highest index) used for receipt creation and validation, and any number of secondary keys (all other index values) used for receipt validation. With multiple keystone nodes, each node must share the same key repository contents, with the exception of the staged key (index 0). It is safe to run keystone-manage fernet_rotate once on any one node to promote a staged key (index 0) to be the new primary (incremented from the previous highest index), and produce a new staged key (a new key with index 0); the resulting repository can then be atomically replicated to other nodes without any risk of race conditions (for example, it is safe to run keystone-manage fernet_rotate on host A, wait any amount of time, create a tarball of the directory on host A, unpack it on host B to a temporary location, and atomically move ( mv ) the directory into place on host B). Running keystone-manage fernet_rotate twice on a key repository without syncing other nodes will result in receipts that can not be validated by all nodes.

integer

3

1

This controls how many keys are held in rotation by keystone-manage fernet_rotate before they are discarded. The default value of 3 means that keystone will maintain one staged key (always index 0), one primary key (the highest numerical index), and one secondary key (every other index). Increasing this value means that additional secondary keys will be kept in the rotation.

### fernet_tokens Â¶

string

/etc/keystone/fernet-keys/

Directory containing Fernet token keys. This directory must exist before using keystone-manage fernet_setup for the first time, must be writable by the user running keystone-manage fernet_setup or keystone-manage fernet_rotate , and of course must be readable by keystoneâs server process. The repository may contain keys in one of three states: a single staged key (always index 0) used for token validation, a single primary key (always the highest index) used for token creation and validation, and any number of secondary keys (all other index values) used for token validation. With multiple keystone nodes, each node must share the same key repository contents, with the exception of the staged key (index 0). It is safe to run keystone-manage fernet_rotate once on any one node to promote a staged key (index 0) to be the new primary (incremented from the previous highest index), and produce a new staged key (a new key with index 0); the resulting repository can then be atomically replicated to other nodes without any risk of race conditions (for example, it is safe to run keystone-manage fernet_rotate on host A, wait any amount of time, create a tarball of the directory on host A, unpack it on host B to a temporary location, and atomically move ( mv ) the directory into place on host B). Running keystone-manage fernet_rotate twice on a key repository without syncing other nodes will result in tokens that can not be validated by all nodes.

integer

3

1

This controls how many keys are held in rotation by keystone-manage fernet_rotate before they are discarded. The default value of 3 means that keystone will maintain one staged key (always index 0), one primary key (the highest numerical index), and one secondary key (every other index). Increasing this value means that additional secondary keys will be kept in the rotation.

### healthcheck Â¶

boolean

False

Show more detailed information as part of the response. Security note: Enabling this option may expose sensitive details about the service being monitored. Be sure to verify that it will not violate your security policies.

list

[]

Additional backends that can perform health checks and report that information back as part of a request.

list

[]

A list of network addresses to limit source ip allowed to access healthcheck information. Any request from ip outside of these network addresses are ignored.

boolean

False

Ignore requests with proxy headers.

string

<None>

Check the presence of a file to determine if an application is running on a port. Used by DisableByFileHealthcheck plugin.

list

[]

Check the presence of a file based on a port to determine if an application is running on a port. Expects a âport:pathâ list of strings. Used by DisableByFilesPortsHealthcheck plugin.

list

[]

Check the presence of files. Used by EnableByFilesHealthcheck plugin.

### identity Â¶

string

default

This references the domain to use for all Identity API v2 requests (which are not aware of domains). A domain with this ID can optionally be created for you by keystone-manage bootstrap . The domain referenced by this ID cannot be deleted on the v3 API, to prevent accidentally breaking the v2 API. There is nothing special about this domain, other than the fact that it must exist to order to maintain support for your v2 clients. There is typically no reason to change this value.

boolean

False

A subset (or all) of domains can have their own identity driver, each with their own partial configuration options, stored in either the resource backend or in a file in a domain configuration directory (depending on the setting of [identity] domain_configurations_from_database ). Only values specific to the domain need to be specified in this manner. This feature is disabled by default, but may be enabled by default in a future release; set to true to enable.

boolean

False

By default, domain-specific configuration data is read from files in the directory identified by [identity] domain_config_dir . Enabling this configuration option allows you to instead manage domain-specific configurations through the API, which are then persisted in the backend (typically, a SQL database), rather than using configuration files on disk.

string

/etc/keystone/domains

Absolute path where keystone should locate domain-specific [identity] configuration files. This option has no effect unless [identity] domain_specific_drivers_enabled is set to true. There is typically no reason to change this value.

string

sql

Entry point for the identity backend driver in the keystone.identity namespace. Keystone provides a sql and ldap driver. This option is also used as the default driver selection (along with the other configuration variables in this section) in the event that [identity] domain_specific_drivers_enabled is enabled, but no applicable domain-specific configuration is defined for the domain in question. Unless your deployment primarily relies on ldap AND is not using domain-specific configuration, you should typically leave this set to sql .

boolean

True

Toggle for identity caching. This has no effect unless global caching is enabled. There is typically no reason to disable this.

integer

600

Time to cache identity data (in seconds). This has no effect unless global and identity caching are enabled.

integer

4096

4096

Maximum allowed length for user passwords. Decrease this value to improve performance. Changing this value does not effect existing passwords. This value can also be overridden by certain hashing algorithms maximum allowed length which takes precedence over the configured value.  The bcrypt max_password_length is 72 bytes.

integer

<None>

Maximum number of entities that will be returned in an identity collection.

string

bcrypt

bcrypt, bcrypt_sha256, scrypt, pbkdf2_sha512

The password hashing algorithm to use for passwords stored within keystone.

integer

<None>

This option represents a trade off between security and performance. Higher values lead to slower performance, but higher security. Changing this option will only affect newly created passwords as existing password hashes already have a fixed number of rounds applied, so it is safe to tune this option in a running cluster.  The default for bcrypt is 12, must be between 4 and 31, inclusive.  The default for scrypt is 16, must be within range(1,32) .  The default for pbkdf_sha512 is 60000, must be within range(1,1<<32) WARNING: If using scrypt, increasing this value increases BOTH time AND memory requirements to hash a password.

integer

<None>

Optional block size to pass to scrypt hash function (the r parameter). Useful for tuning scrypt to optimal performance for your CPU architecture. This option is only used when the password_hash_algorithm option is set to scrypt . Defaults to 8.

integer

<None>

Optional parallelism to pass to scrypt hash function (the p parameter). This option is only used when the password_hash_algorithm option is set to scrypt . Defaults to 1.

integer

<None>

0

96

Number of bytes to use in scrypt and pbkfd2_sha512 hashing salt.  Default for scrypt is 16 bytes. Default for pbkfd2_sha512 is 16 bytes.  Limited to a maximum of 96 bytes due to the size of the column used to store password hashes.

### identity_mapping Â¶

string

sql

Entry point for the identity mapping backend driver in the keystone.identity.id_mapping namespace. Keystone only provides a sql driver, so there is no reason to change this unless you are providing a custom entry point.

string

sha256

Entry point for the public ID generator for user and group entities in the keystone.identity.id_generator namespace. The Keystone identity mapper only supports generators that produce 64 bytes or less. Keystone only provides a sha256 entry point, so there is no reason to change this value unless youâre providing a custom entry point.

boolean

True

The format of user and group IDs changed in Juno for backends that do not generate UUIDs (for example, LDAP), with keystone providing a hash mapping to the underlying attribute in LDAP. By default this mapping is disabled, which ensures that existing IDs will not change. Even when the mapping is enabled by using domain-specific drivers ( [identity] domain_specific_drivers_enabled ), any users and groups from the default domain being handled by LDAP will still not be mapped to ensure their IDs remain backward compatible. Setting this value to false will enable the new mapping for all backends, including the default LDAP driver. It is only guaranteed to be safe to enable this option if you do not already have assignments for users and groups from the default LDAP domain, and you consider it to be acceptable for Keystone to provide the different IDs to clients than it did previously (existing IDs in the API will suddenly change). Typically this means that the only time you can set this value to false is when configuring a fresh installation, although that is the recommended value.

### jwt_tokens Â¶

string

/etc/keystone/jws-keys/public

Directory containing public keys for validating JWS token signatures. This directory must exist in order for keystoneâs server process to start. It must also be readable by keystoneâs server process. It must contain at least one public key that corresponds to a private key in keystone.conf [jwt_tokens] jws_private_key_repository . This option is only applicable in deployments issuing JWS tokens and setting keystone.conf [token] provider = jws .

string

/etc/keystone/jws-keys/private

Directory containing private keys for signing JWS tokens. This directory must exist in order for keystoneâs server process to start. It must also be readable by keystoneâs server process. It must contain at least one private key that corresponds to a public key in keystone.conf [jwt_tokens] jws_public_key_repository . In the event there are multiple private keys in this directory, keystone will use a key named private.pem to sign tokens. In the future, keystone may support the ability to sign tokens with multiple private keys. For now, only a key named private.pem within this directory is required to issue JWS tokens. This option is only applicable in deployments issuing JWS tokens and setting keystone.conf [token] provider = jws .

### ldap Â¶

string

ldap://localhost

URL(s) for connecting to the LDAP server. Multiple LDAP URLs may be specified as a comma separated string. The first URL to successfully bind is used for the connection.

boolean

False

Randomize the order of URLs in each keystone process. This makes the failure behavior more gradual, since if the first server is down, a process/thread will wait for the specified timeout before attempting a connection to a server further down the list. This defaults to False, for backward compatibility.

string

<None>

The user name of the administrator bind DN to use when querying the LDAP server, if your LDAP server requires it.

string

<None>

The password of the administrator bind DN to use when querying the LDAP server, if your LDAP server requires it.

string

cn=example,cn=com

The default LDAP server suffix to use, if a DN is not defined via either [ldap] user_tree_dn or [ldap] group_tree_dn .

string

one

one, sub

The search scope which defines how deep to search within the search base. A value of one (representing oneLevel or singleLevel ) indicates a search of objects immediately below to the base object, but does not include the base object itself. A value of sub (representing subtree or wholeSubtree ) indicates a search of both the base object itself and the entire subtree below it.

integer

0

0

Defines the maximum number of results per page that keystone should request from the LDAP server when listing objects. A value of zero ( 0 ) disables paging.

string

default

never, searching, always, finding, default

The LDAP dereferencing option to use for queries involving aliases. A value of default falls back to using default dereferencing behavior configured by your ldap.conf . A value of never prevents aliases from being dereferenced at all. A value of searching dereferences aliases only after name resolution. A value of finding dereferences aliases only during name resolution. A value of always dereferences aliases in all cases.

integer

<None>

-1

Sets the LDAP debugging level for LDAP calls. A value of 0 means that debugging is not enabled. This value is a bitmask, consult your LDAP documentation for possible values.

boolean

<None>

Sets keystoneâs referral chasing behavior across directory partitions. If left unset, the systemâs default behavior will be used.

string

<None>

The search base to use for users. Defaults to ou=Users with the [ldap] suffix appended to it.

string

<None>

The LDAP search filter to use for users.

string

inetOrgPerson

The LDAP object class to use for users.

string

cn

The LDAP attribute mapped to user IDs in keystone. This must NOT be a multivalued attribute. User IDs are expected to be globally unique across keystone domains and URL-safe.

string

sn

The LDAP attribute mapped to user names in keystone. User names are expected to be unique only within a keystone domain and are not expected to be URL-safe.

string

description

The LDAP attribute mapped to user descriptions in keystone.

string

mail

The LDAP attribute mapped to user emails in keystone.

string

userPassword

The LDAP attribute mapped to user passwords in keystone.

string

enabled

The LDAP attribute mapped to the user enabled attribute in keystone. If setting this option to userAccountControl , then you may be interested in setting [ldap] user_enabled_mask and [ldap] user_enabled_default as well.

boolean

False

Logically negate the boolean value of the enabled attribute obtained from the LDAP server. Some LDAP servers use a boolean lock attribute where âtrueâ means an account is disabled. Setting [ldap] user_enabled_invert = true will allow these lock attributes to be used. This option will have no effect if either the [ldap] user_enabled_mask or [ldap] user_enabled_emulation options are in use.

integer

0

0

Bitmask integer to select which bit indicates the enabled value if the LDAP server represents âenabledâ as a bit on an integer rather than as a discrete boolean. A value of 0 indicates that the mask is not used. If this is not set to 0 the typical value is 2 . This is typically used when [ldap] user_enabled_attribute = userAccountControl . Setting this option causes keystone to ignore the value of [ldap] user_enabled_invert .

string

True

The default value to enable users. This should match an appropriate integer value if the LDAP server uses non-boolean (bitmask) values to indicate if a user is enabled or disabled. If this is not set to True , then the typical value is 512 . This is typically used when [ldap] user_enabled_attribute = userAccountControl .

list

['default_project_id']

List of user attributes to ignore on create and update, or whether a specific user attribute should be filtered for list or show user.

string

<None>

The LDAP attribute mapped to a userâs default_project_id in keystone. This is most commonly used when keystone has write access to LDAP.

boolean

False

If enabled, keystone uses an alternative method to determine if a user is enabled or not by checking if they are a member of the group defined by the [ldap] user_enabled_emulation_dn option. Enabling this option causes keystone to ignore the value of [ldap] user_enabled_invert .

string

<None>

DN of the group entry to hold enabled users when using enabled emulation. Setting this option has no effect unless [ldap] user_enabled_emulation is also enabled.

boolean

False

Use the [ldap] group_member_attribute and [ldap] group_objectclass settings to determine membership in the emulated enabled group. Enabling this option has no effect unless [ldap] user_enabled_emulation is also enabled.

list

[]

A list of LDAP attribute to keystone user attribute pairs used for mapping additional attributes to users in keystone. The expected format is <ldap_attr>:<user_attr> , where ldap_attr is the attribute in the LDAP object and user_attr is the attribute which should appear in the identity API.

string

<None>

The search base to use for groups. Defaults to ou=UserGroups with the [ldap] suffix appended to it.

string

<None>

The LDAP search filter to use for groups.

string

groupOfNames

The LDAP object class to use for groups. If setting this option to posixGroup , you may also be interested in enabling the [ldap] group_members_are_ids option.

string

cn

The LDAP attribute mapped to group IDs in keystone. This must NOT be a multivalued attribute. Group IDs are expected to be globally unique across keystone domains and URL-safe.

string

ou

The LDAP attribute mapped to group names in keystone. Group names are expected to be unique only within a keystone domain and are not expected to be URL-safe.

string

member

The LDAP attribute used to indicate that a user is a member of the group.

boolean

False

Enable this option if the members of the group object class are keystone user IDs rather than LDAP DNs. This is the case when using posixGroup as the group object class in Open Directory.

string

description

The LDAP attribute mapped to group descriptions in keystone.

list

[]

List of group attributes to ignore on create and update. or whether a specific group attribute should be filtered for list or show group.

list

[]

A list of LDAP attribute to keystone group attribute pairs used for mapping additional attributes to groups in keystone. The expected format is <ldap_attr>:<group_attr> , where ldap_attr is the attribute in the LDAP object and group_attr is the attribute which should appear in the identity API.

boolean

False

If enabled, group queries will use Active Directory specific filters for nested groups.

string

<None>

An absolute path to a CA certificate file to use when communicating with LDAP servers. This option will take precedence over [ldap] tls_cacertdir , so there is no reason to set both.

string

<None>

An absolute path to a CA certificate directory to use when communicating with LDAP servers. There is no reason to set this option if youâve also set [ldap] tls_cacertfile .

boolean

False

Enable TLS when communicating with LDAP servers. You should also set the [ldap] tls_cacertfile and [ldap] tls_cacertdir options when using this option. Do not set this option if you are using LDAP over SSL (LDAPS) instead of TLS.

string

demand

demand, never, allow

Specifies which checks to perform against client certificates on incoming TLS sessions. If set to demand , then a certificate will always be requested and required from the LDAP server. If set to allow , then a certificate will always be requested but not required from the LDAP server. If set to never , then a certificate will never be requested.

integer

-1

-1

The connection timeout to use with the LDAP server. A value of -1 means that connections will never timeout.

boolean

True

Enable LDAP connection pooling for queries to the LDAP server. There is typically no reason to disable this.

integer

10

1

The size of the LDAP connection pool. This option has no effect unless [ldap] use_pool is also enabled.

integer

3

1

The maximum number of times to attempt connecting to the LDAP server before aborting. A value of one makes only one connection attempt. This option has no effect unless [ldap] use_pool is also enabled.

floating point

0.1

The number of seconds to wait before attempting to reconnect to the LDAP server. This option has no effect unless [ldap] use_pool is also enabled.

integer

-1

-1

The connection timeout to use when pooling LDAP connections. A value of -1 means that connections will never timeout. This option has no effect unless [ldap] use_pool is also enabled.

integer

600

1

The maximum connection lifetime to the LDAP server in seconds. When this lifetime is exceeded, the connection will be unbound and removed from the connection pool. This option has no effect unless [ldap] use_pool is also enabled.

boolean

True

Enable LDAP connection pooling for end user authentication. There is typically no reason to disable this.

integer

100

1

The size of the connection pool to use for end user authentication. This option has no effect unless [ldap] use_auth_pool is also enabled.

integer

60

1

The maximum end user authentication connection lifetime to the LDAP server in seconds. When this lifetime is exceeded, the connection will be unbound and removed from the connection pool. This option has no effect unless [ldap] use_auth_pool is also enabled.

### oauth1 Â¶

string

sql

Entry point for the OAuth backend driver in the keystone.oauth1 namespace. Typically, there is no reason to set this option unless you are providing a custom entry point.

integer

28800

0

Number of seconds for the OAuth Request Token to remain valid after being created. This is the amount of time the user has to authorize the token. Setting this option to zero means that request tokens will last forever.

integer

86400

0

Number of seconds for the OAuth Access Token to remain valid after being created. This is the amount of time the consumer has to interact with the service provider (which is typically keystone). Setting this option to zero means that access tokens will last forever.

### oauth2 Â¶

list

['tls_client_auth', 'client_secret_basic']

The OAuth2.0 authentication method supported by the system when user obtains an access token through the OAuth2.0 token endpoint. This option can be set to certificate or secret. If the option is not set, the default value is certificate. When the option is set to secret, the OAuth2.0 token endpoint uses client_secret_basic method for authentication, otherwise tls_client_auth method is used for authentication.

string

oauth2_mapping

Used to define the mapping rule id. When not set, the mapping rule id is oauth2_mapping.

### oslo_messaging_kafka Â¶

integer

1048576

Max fetch bytes of Kafka consumer

floating point

1.0

Default timeout(s) for Kafka consumers

string

oslo_messaging_consumer

Group id for Kafka consumer. Consumers in one group will coordinate message consumption

floating point

0.0

Upper bound on the delay for KafkaProducer batching in seconds

integer

16384

Size of batch for the producer async send

string

none

none, gzip, snappy, lz4, zstd

The compression codec for all data generated by the producer. If not set, compression will not be used. Note that the allowed values of this depend on the kafka version

boolean

False

Enable asynchronous consumer commits

integer

500

The maximum number of records returned in a poll call

string

PLAINTEXT

PLAINTEXT, SASL_PLAINTEXT, SSL, SASL_SSL

Protocol used to communicate with brokers

string

PLAIN

Mechanism when security protocol is SASL

string

''

CA certificate PEM file used to verify the server certificate

string

''

Client certificate PEM file used for authentication.

string

''

Client key PEM file used for authentication.

string

''

Client key password file used for authentication.

### oslo_messaging_notifications Â¶

multi-valued

''

The Drivers(s) to handle sending notifications. Possible values are messaging, messagingv2, routing, log, test, noop

string

<None>

A URL representing the messaging driver to use for notifications. If not set, we fall back to the same configuration used for RPC.

list

['notifications']

AMQP topic used for OpenStack notifications.

integer

-1

The maximum number of attempts to re-send a notification message which failed to be delivered due to a recoverable error. 0 - No retry, -1 - indefinite

### oslo_messaging_rabbit Â¶

boolean

False

Use durable queues in AMQP. If rabbit_quorum_queue is enabled, queues will be durable and this value will be ignored.

boolean

False

Auto-delete queues in AMQP.

integer

30

1

Size of RPC connection pool.

integer

2

The pool size limit for connections expiration policy

integer

1200

The time-to-live in sec of idle connections in the pool

boolean

False

Connect over SSL.

string

''

SSL version to use (valid only if SSL enabled). Valid values are TLSv1 and SSLv23. SSLv2, SSLv3, TLSv1_1, and TLSv1_2 may be available on some distributions.

string

''

SSL key file (valid only if SSL enabled).

string

''

SSL cert file (valid only if SSL enabled).

string

''

SSL certification authority file (valid only if SSL enabled).

boolean

False

Global toggle for enforcing the OpenSSL FIPS mode. This feature requires Python support. This is available in Python 3.9 in all environments and may have been backported to older Python versions on select environments. If the Python executable used does not support OpenSSL FIPS mode, an exception will be raised.

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

FIPS_mode_set API was removed in OpenSSL 3.0.0. This option has no effect now.

boolean

False

(DEPRECATED) It is recommend not to use this option anymore. Run the health check heartbeat thread through a native python thread by default. If this option is equal to False then the health check heartbeat will inherit the execution model from the parent process. For example if the parent process has monkey patched the stdlib by using eventlet/greenlet then the heartbeat will be run through a green thread. This option should be set to True only for the wsgi services.

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

The option is related to Eventlet which will be removed. In addition this has never worked as expected with services using eventlet for core service framework.

floating point

1.0

0.0

4.5

How long to wait (in seconds) before reconnecting in response to an AMQP consumer cancel notification.

floating point

0.0

0.0

Random time to wait for when reconnecting in response to an AMQP consumer cancel notification.

string

<None>

EXPERIMENTAL: Possible values are: gzip, bz2. If not set compression will not be used. This option may not be available in future versions.

integer

60

How long to wait a missing client before abandoning to send it its replies. This value should not be longer than rpc_response_timeout.

Deprecated Variations Â¶ Group Name oslo_messaging_rabbit kombu_reconnect_timeout

Group

Name

oslo_messaging_rabbit

kombu_reconnect_timeout

string

round-robin

round-robin, shuffle

Determines how the next RabbitMQ node is chosen in case the one we are currently connected to becomes unavailable. Takes effect only if more than one RabbitMQ node is provided in config.

string

AMQPLAIN

PLAIN, AMQPLAIN, EXTERNAL, RABBIT-CR-DEMO

The RabbitMQ login method.

integer

1

1

How frequently to retry connecting with RabbitMQ.

integer

2

0

How long to backoff for between retries when connecting to RabbitMQ.

integer

30

1

Maximum interval of RabbitMQ connection retries.

boolean

False

Try to use HA queues in RabbitMQ (x-ha-policy: all). If you change this option, you must wipe the RabbitMQ database. In RabbitMQ 3.0, queue mirroring is no longer controlled by the x-ha-policy argument when declaring a queue. If you just want to make sure that all queues (except those with auto-generated names) are mirrored across all nodes, run: ârabbitmqctl set_policy HA â^(?!amq.).*â â{âha-modeâ: âallâ}â â

boolean

False

Use quorum queues in RabbitMQ (x-queue-type: quorum). The quorum queue is a modern queue type for RabbitMQ implementing a durable, replicated FIFO queue based on the Raft consensus algorithm. It is available as of RabbitMQ 3.8.0. If set this option will conflict with the HA queues ( rabbit_ha_queues ) aka mirrored queues, in other words the HA queues should be disabled. Quorum queues are also durable by default so the amqp_durable_queues option is ignored when this option is enabled.

boolean

False

Use quorum queues for transients queues in RabbitMQ. Enabling this option will then make sure those queues are also using quorum kind of rabbit queues, which are HA by default.

integer

0

Each time a message is redelivered to a consumer, a counter is incremented. Once the redelivery count exceeds the delivery limit the message gets dropped or dead-lettered (if a DLX exchange has been configured) Used only when rabbit_quorum_queue is enabled, Default 0 which means dont set a limit.

integer

0

By default all messages are maintained in memory if a quorum queue grows in length it can put memory pressure on a cluster. This option can limit the number of messages in the quorum queue. Used only when rabbit_quorum_queue is enabled, Default 0 which means dont set a limit.

integer

0

By default all messages are maintained in memory if a quorum queue grows in length it can put memory pressure on a cluster. This option can limit the number of memory bytes used by the quorum queue. Used only when rabbit_quorum_queue is enabled, Default 0 which means dont set a limit.

integer

1800

0

Positive integer representing duration in seconds for queue TTL (x-expires). Queues which are unused for the duration of the TTL are automatically deleted. The parameter affects only reply and fanout queues. Setting 0 as value will disable the x-expires. If doing so, make sure you have a rabbitmq policy to delete the queues or you deployment will create an infinite number of queue over time.In case rabbit_stream_fanout is set to True, this option will control data retention policy (x-max-age) for messages in the fanout queue rather then the queue duration itself. So the oldest data in the stream queue will be discarded from it once reaching TTL Setting to 0 will disable x-max-age for stream which make stream grow indefinitely filling up the diskspace

integer

0

Specifies the number of messages to prefetch. Setting to zero allows unlimited messages.

integer

60

Number of seconds after which the Rabbit broker is considered down if heartbeatâs keep-alive fails (0 disables heartbeat).

integer

3

How often times during the heartbeat_timeout_threshold we check the heartbeat.

boolean

True

(DEPRECATED) Enable/Disable the RabbitMQ mandatory flag for direct send. The direct send is used as reply, so the MessageUndeliverable exception is raised in case the client queue does not exist.MessageUndeliverable exception will be used to loop for a timeout to lets a chance to sender to recover.This flag is deprecated and it will not be possible to deactivate this functionality anymore

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

Mandatory flag no longer deactivable.

boolean

False

Enable x-cancel-on-ha-failover flag so that rabbitmq server will cancel and notify consumerswhen queue is down

boolean

False

Should we use consistant queue names or random ones

string

node1.example.com

This option has a sample default set, which means that
its actual default value may vary from the one documented
above.

Hostname used by queue manager. Defaults to the value returned by socket.gethostname().

string

nova-api

This option has a sample default set, which means that
its actual default value may vary from the one documented
above.

Process name used by queue manager

boolean

False

Use stream queues in RabbitMQ (x-queue-type: stream). Streams are a new persistent and replicated data structure (âqueue typeâ) in RabbitMQ which models an append-only log with non-destructive consumer semantics. It is available as of RabbitMQ 3.9.0. If set this option will replace all fanout queues with only one stream queue.

### oslo_middleware Â¶

integer

114688

The maximum body size for each request, in bytes.

boolean

False

Whether the application is behind a proxy or not. This determines if the middleware should parse the headers or not.

string

/etc/htpasswd

HTTP basic auth password file.

### oslo_policy Â¶

boolean

True

This option controls whether or not to enforce scope when evaluating policies. If True , the scope of the token used in the request is compared to the scope_types of the policy being enforced. If the scopes do not match, an InvalidScope exception will be raised. If False , a message will be logged informing operators that policies are being invoked with mismatching scope.

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

This configuration was added temporarily to facilitate a smooth transition to the new RBAC. OpenStack will always enforce scope checks. This configuration option is deprecated and will be removed in the 2025.2 cycle.

boolean

True

This option controls whether or not to use old deprecated defaults when evaluating policies. If True , the old deprecated defaults are not going to be evaluated. This means if any existing token is allowed for old defaults but is disallowed for new defaults, it will be disallowed. It is encouraged to enable this flag along with the enforce_scope flag so that you can get the benefits of new defaults and scope_type together. If False , the deprecated policy check string is logically ORâd with the new policy check string, allowing for a graceful upgrade experience between releases with new policies, which is the default behavior.

string

policy.yaml

The relative or absolute path of a file that maps roles to permissions for a given service. Relative paths must be specified in relation to the configuration file setting this option.

string

default

Default rule. Enforced when a requested rule is not found.

multi-valued

policy.d

Directories where policy configuration files are stored. They can be relative to any directory in the search path defined by the config_dir option, or absolute paths. The file defined by policy_file must exist for these directories to be searched.  Missing or empty directories are ignored.

string

application/x-www-form-urlencoded

application/x-www-form-urlencoded, application/json

Content Type to send and receive data for REST based policy check

boolean

False

server identity verification for REST based policy check

string

<None>

Absolute path to ca cert file for REST based policy check

string

<None>

Absolute path to client cert for REST based policy check

string

<None>

Absolute path client key file REST based policy check

floating point

60

0

Timeout in seconds for REST based policy check

### policy Â¶

string

sql

Entry point for the policy backend driver in the keystone.policy namespace. Supplied drivers are rules (which does not support any CRUD operations for the v3 policy API) and sql . Typically, there is no reason to set this option unless you are providing a custom entry point.

integer

<None>

Maximum number of entities that will be returned in a policy collection.

### profiler Â¶

boolean

False

Enable the profiling for all services on this node.

Default value is False (fully disable the profiling feature).

Possible values:

- True: Enables the feature

True: Enables the feature

- False: Disables the feature. The profiling cannot be started via this project
operations. If the profiling is triggered by another project, this project
part will be empty.

False: Disables the feature. The profiling cannot be started via this project
operations. If the profiling is triggered by another project, this project
part will be empty.

Deprecated Variations Â¶ Group Name profiler profiler_enabled

Group

Name

profiler

profiler_enabled

boolean

False

Enable SQL requests profiling in services.

Default value is False (SQL requests wonât be traced).

Possible values:

- True: Enables SQL requests profiling. Each SQL query will be part of the
trace and can the be analyzed by how much time was spent for that.

True: Enables SQL requests profiling. Each SQL query will be part of the
trace and can the be analyzed by how much time was spent for that.

- False: Disables SQL requests profiling. The spent time is only shown on a
higher level of operations. Single SQL queries cannot be analyzed this way.

False: Disables SQL requests profiling. The spent time is only shown on a
higher level of operations. Single SQL queries cannot be analyzed this way.

boolean

False

Enable python requests package profiling.

Supported drivers: jaeger+otlp

Default value is False.

Possible values:

- True: Enables requests profiling.

True: Enables requests profiling.

- False: Disables requests profiling.

False: Disables requests profiling.

string

SECRET_KEY

Secret key(s) to use for encrypting context data for performance profiling.

This string value should have the following format: <key1>[,<key2>,â¦<keyn>],
where each key is some random string. A user who triggers the profiling via
the REST API has to set one of these keys in the headers of the REST API call
to include profiling results of this node for this particular project.

Both âenabledâ flag and âhmac_keysâ config options should be set to enable
profiling. Also, to generate correct profiling information across all services
at least one key needs to be consistent between OpenStack projects. This
ensures it can be used from client side to generate the trace, containing
information from all possible resources.

string

messaging://

Connection string for a notifier backend.

Default value is messaging:// which sets the notifier to oslo_messaging.

Examples of possible values:

- messaging:// - use oslo_messaging driver for sending spans.

messaging:// - use oslo_messaging driver for sending spans.

- redis://127.0.0.1:6379 - use redis driver for sending spans.

redis://127.0.0.1:6379 - use redis driver for sending spans.

- mongodb://127.0.0.1:27017 - use mongodb driver for sending spans.

mongodb://127.0.0.1:27017 - use mongodb driver for sending spans.

- elasticsearch://127.0.0.1:9200 - use elasticsearch driver for sending
spans.

elasticsearch://127.0.0.1:9200 - use elasticsearch driver for sending
spans.

- jaeger://127.0.0.1:6831 - use jaeger tracing as driver for sending spans.

jaeger://127.0.0.1:6831 - use jaeger tracing as driver for sending spans.

string

notification

Document type for notification indexing in elasticsearch.

string

2m

This parameter is a time value parameter (for example: es_scroll_time=2m),
indicating for how long the nodes that participate in the search will maintain
relevant resources in order to continue and support it.

integer

10000

Elasticsearch splits large requests in batches. This parameter defines
maximum size of each batch (for example: es_scroll_size=10000).

floating point

0.1

Redissentinel provides a timeout option on the connections.
This parameter defines that timeout (for example: socket_timeout=0.1).

string

mymaster

Redissentinel uses a service name to identify a master redis service.
This parameter defines the name (for example: sentinal_service_name=mymaster ).

boolean

False

Enable filter traces that contain error/exception to a separated place.

Default value is set to False.

Possible values:

- True: Enable filter traces that contain error/exception.

True: Enable filter traces that contain error/exception.

- False: Disable the filter.

False: Disable the filter.

### profiler_jaeger Â¶

string

<None>

Set service name prefix to Jaeger service name.

dict

{}

Set process tracer tags.

### profiler_otlp Â¶

string

<None>

Set service name prefix to OTLP exporters.

### receipt Â¶

integer

300

0

86400

The amount of time that a receipt should remain valid (in seconds). This value should always be very short, as it represents how long a user has to reattempt auth with the missing auth methods.

string

fernet

Entry point for the receipt provider in the keystone.receipt.provider namespace. The receipt provider controls the receipt construction and validation operations. Keystone includes just the fernet receipt provider for now. fernet receipts do not need to be persisted at all, but require that you run keystone-manage fernet_setup (also see the keystone-manage fernet_rotate command).

boolean

True

Toggle for caching receipt creation and validation data. This has no effect unless global caching is enabled, or if cache_on_issue is disabled as we only cache receipts on issue.

integer

300

0

The number of seconds to cache receipt creation and validation data. This has no effect unless both global and [receipt] caching are enabled.

boolean

True

Enable storing issued receipt data to receipt validation cache so that first receipt validation doesnât actually cause full validation cycle. This option has no effect unless global caching and receipt caching are enabled.

### resource Â¶

string

sql

Entry point for the resource driver in the keystone.resource namespace. Only a sql driver is supplied by keystone. Unless you are writing proprietary drivers for keystone, you do not need to set this option.

boolean

True

Toggle for resource caching. This has no effect unless global caching is enabled.

Deprecated Variations Â¶ Group Name assignment caching

Group

Name

assignment

caching

integer

<None>

Time to cache resource data in seconds. This has no effect unless global caching is enabled.

Deprecated Variations Â¶ Group Name assignment cache_time

Group

Name

assignment

cache_time

integer

<None>

Maximum number of entities that will be returned in a resource collection.

Deprecated Variations Â¶ Group Name assignment list_limit

Group

Name

assignment

list_limit

string

<None>

Name of the domain that owns the admin_project_name . If left unset, then there is no admin project. [resource] admin_project_name must also be set to use this option.

string

<None>

This is a special project which represents cloud-level administrator privileges across services. Tokens scoped to this project will contain a true is_admin_project attribute to indicate to policy systems that the role assignments on that specific project should apply equally across every project. If left unset, then there is no admin project, and thus no explicit means of cross-project role assignments. [resource] admin_project_domain_name must also be set to use this option.

string

off

off, new, strict

This controls whether the names of projects are restricted from containing URL-reserved characters. If set to new , attempts to create or update a project with a URL-unsafe name will fail. If set to strict , attempts to scope a token with a URL-unsafe project name will fail, thereby forcing all project names to be updated to be URL-safe.

string

off

off, new, strict

This controls whether the names of domains are restricted from containing URL-reserved characters. If set to new , attempts to create or update a domain with a URL-unsafe name will fail. If set to strict , attempts to scope a token with a URL-unsafe domain name will fail, thereby forcing all domain names to be updated to be URL-safe.

### revoke Â¶

string

sql

Entry point for the token revocation backend driver in the keystone.revoke namespace. Keystone only provides a sql driver, so there is no reason to set this option unless you are providing a custom entry point.

integer

1800

0

The number of seconds after a token has expired before a corresponding revocation event may be purged from the backend.

boolean

True

Toggle for revocation event caching. This has no effect unless global caching is enabled.

integer

3600

Time to cache the revocation list and the revocation events (in seconds). This has no effect unless global and [revoke] caching are both enabled.

Deprecated Variations Â¶ Group Name token revocation_cache_time

Group

Name

token

revocation_cache_time

### role Â¶

string

<None>

Entry point for the role backend driver in the keystone.role namespace. Keystone only provides a sql driver, so thereâs no reason to change this unless you are providing a custom entry point.

boolean

True

Toggle for role caching. This has no effect unless global caching is enabled. In a typical deployment, there is no reason to disable this.

integer

<None>

Time to cache role data, in seconds. This has no effect unless both global caching and [role] caching are enabled.

integer

<None>

Maximum number of entities that will be returned in a role collection. This may be useful to tune if you have a large number of discrete roles in your deployment.

### saml Â¶

integer

3600

Determines the lifetime for any SAML assertions generated by keystone, using NotOnOrAfter attributes.

string

xmlsec1

Name of, or absolute path to, the binary to be used for XML signing. Although only the XML Security Library ( xmlsec1 ) is supported, it may have a non-standard name or path on your system. If keystone cannot find the binary itself, you may need to install the appropriate package, use this option to specify an absolute path, or adjust keystoneâs PATH environment variable.

string

/etc/keystone/ssl/certs/signing_cert.pem

Absolute path to the public certificate file to use for SAML signing. The value cannot contain a comma ( , ).

string

/etc/keystone/ssl/private/signing_key.pem

Absolute path to the private key file to use for SAML signing. The value cannot contain a comma ( , ).

URI

<None>

This is the unique entity identifier of the identity provider (keystone) to use when generating SAML assertions. This value is required to generate identity provider metadata and must be a URI (a URL is recommended). For example: https://keystone.example.com/v3/OS-FEDERATION/saml2/idp .

URI

<None>

This is the single sign-on (SSO) service location of the identity provider which accepts HTTP POST requests. A value is required to generate identity provider metadata. For example: https://keystone.example.com/v3/OS-FEDERATION/saml2/sso .

string

en

This is the language used by the identity providerâs organization.

string

SAML Identity Provider

This is the name of the identity providerâs organization.

string

OpenStack SAML Identity Provider

This is the name of the identity providerâs organization to be displayed.

URI

https://example.com/

This is the URL of the identity providerâs organization. The URL referenced here should be useful to humans.

string

Example, Inc.

This is the company name of the identity providerâs contact person.

string

SAML Identity Provider Support

This is the given name of the identity providerâs contact person.

string

Support

This is the surname of the identity providerâs contact person.

string

support@example.com

This is the email address of the identity providerâs contact person.

string

+1 800 555 0100

This is the telephone number of the identity providerâs contact person.

string

other

technical, support, administrative, billing, other

This is the type of contact that best describes the identity providerâs contact person.

string

/etc/keystone/saml2_idp_metadata.xml

Absolute path to the identity provider metadata file. This file should be generated with the keystone-manage saml_idp_metadata command. There is typically no reason to change this value.

string

ss:mem:

The prefix of the RelayState SAML attribute to use when generating enhanced client and proxy (ECP) assertions. In a typical deployment, there is no reason to change this value.

### security_compliance Â¶

integer

<None>

1

The maximum number of days a user can go without authenticating before being considered âinactiveâ and automatically disabled (locked). This feature is disabled by default; set any value to enable it. This feature depends on the sql backend for the [identity] driver . When a user exceeds this threshold and is considered âinactiveâ, the userâs enabled attribute in the HTTP API may not match the value of the userâs enabled column in the user table.

integer

<None>

1

The maximum number of times that a user can fail to authenticate before the user account is locked for the number of seconds specified by [security_compliance] lockout_duration . This feature is disabled by default. If this feature is enabled and [security_compliance] lockout_duration is not set, then users may be locked out indefinitely until the user is explicitly enabled via the API. This feature depends on the sql backend for the [identity] driver .

integer

1800

1

The number of seconds a user account will be locked when the maximum number of failed authentication attempts (as specified by [security_compliance] lockout_failure_attempts ) is exceeded. Setting this option will have no effect unless you also set [security_compliance] lockout_failure_attempts to a non-zero value. This feature depends on the sql backend for the [identity] driver .

integer

<None>

1

The number of days for which a password will be considered valid before requiring it to be changed. This feature is disabled by default. If enabled, new password changes will have an expiration date, however existing passwords would not be impacted. This feature depends on the sql backend for the [identity] driver .

integer

0

0

This controls the number of previous user password iterations to keep in history, in order to enforce that newly created passwords are unique. The total number which includes the new password should not be greater or equal to this value. Setting the value to zero (the default) disables this feature. Thus, to enable this feature, values must be greater than 0. This feature depends on the sql backend for the [identity] driver .

integer

0

0

The number of days that a password must be used before the user can change it. This prevents users from changing their passwords immediately in order to wipe out their password history and reuse an old password. This feature does not prevent administrators from manually resetting passwords. It is disabled by default and allows for immediate password changes. This feature depends on the sql backend for the [identity] driver . Note: If [security_compliance] password_expires_days is set, then the value for this option should be less than the password_expires_days .

string

<None>

The regular expression used to validate password strength requirements. By default, the regular expression will match any password. The following is an example of a pattern which requires at least 1 letter, 1 digit, and have a minimum length of 7 characters: ^(?=.*\d)(?=.*[a-zA-Z]).{7,}$ This feature depends on the sql backend for the [identity] driver .

string

<None>

Describe your password regular expression here in language for humans. If a password fails to match the regular expression, the contents of this configuration variable will be returned to users to explain why their requested password was insufficient.

boolean

False

Enabling this option requires users to change their password when the user is created, or upon administrative reset. Before accessing any services, affected users will have to change their password. To ignore this requirement for specific users, such as service users, set the options attribute ignore_change_password_upon_first_use to True for the desired user via the update user API. This feature is disabled by default. This feature is only applicable with the sql backend for the [identity] driver .

list

event

This option has a sample default set, which means that
its actual default value may vary from the one documented
above.

When configured, enriches the corresponding output channel with hash of invalid password, which could be further used to distinguish bruteforce attacks from e.g. external user automations that did not timely update rotated password by analyzing variability of the hash value. Additional configuration parameters are available using other invalid_password_hash_* configuration entires, that only take effect when this option is activated.

string

<None>

If report_invalid_password_hash is configured, uses provided secret key when generating password hashes to make them unique and distinct from any other Keystone installations out there. Should be some secret static value specific to the current installation (the same value should be used in distributed installations working with the same backend, to make them all generate equal hashes for equal invalid passwords). 16 bytes (128 bits) or more is recommended.

string

sha256

If report_invalid_password_hash is configured, defines the hash function to be used by HMAC. Possible values are names suitable to hashlib.new() - https://docs.python.org/3/library/hashlib.html#hashlib.new .

integer

5

1

This option has a sample default set, which means that
its actual default value may vary from the one documented
above.

If report_invalid_password_hash is configured, defines the number of characters of hash of invalid password to be returned. When not specified, returns full hash. Its length depends on implementation and invalid_password_hash_function configuration, but is typically 16+ characters. Itâs recommended to use the least reasonable value however - itâs the most effective measure to protect the hashes.

boolean

False

INSECURE: When enabled, admin-role delegated tokens (trusts, application credentials, OAuth1 access tokens) are allowed to access credentials outside their project scope. By default (False), delegated tokens can only access credentials whose project_id matches the tokenâs project scope, preventing cross-project lateral movement via a compromised delegation token.  Enable this only if you have automated workflows (e.g. Mistral cron triggers) that use admin-role trusts to access credentials across multiple projects and cannot be migrated to use non-delegated service account credentials. Enabling this option weakens the isolation guarantee provided by the delegation boundary fix for LP#2150089. This option is deprecated and will be removed in a future release.

Warning

This option is deprecated for removal since 2026.1.
Its value may be silently ignored 
in the future.

Migrate automated workflows that use admin-role trusts to access credentials across multiple projects (e.g. Mistral cron triggers) to use non-delegated service account credentials instead, then remove this option.

boolean

False

INSECURE: When enabled, application credential tokens (including restricted ones) are allowed to create, delete, and list trusts. By default (False), application credential tokens are blocked from all trust operations regardless of the unrestricted flag, because allowing an application credential to bootstrap a trust creates a new delegation context. A trust-scoped token produced from that trust can then access authentication material (EC2 credentials, TOTP seeds) and operate entirely outside the delegation chain, breaking the audit trail. The âunrestrictedâ flag governs credential management, not trust management.  Enable this only if you have workflows where application credentials must create trusts (e.g. Heat stacks authenticated via application credentials). Use OIDC federation flows (v3oidcclientcredentials, v3oidcdeviceauthz) as the proper long-term alternative. This option is deprecated and will be removed in a future release.

Warning

This option is deprecated for removal since 2026.1.
Its value may be silently ignored 
in the future.

Migrate workflows where application credentials create trusts to use OIDC federation flows (v3oidcclientcredentials, v3oidcdeviceauthz) instead, then remove this option.

### shadow_users Â¶

string

sql

Entry point for the shadow users backend driver in the keystone.identity.shadow_users namespace. This driver is used for persisting local user references to externally-managed identities (via federation, LDAP, etc). Keystone only provides a sql driver, so there is no reason to change this option unless you are providing a custom entry point.

### token Â¶

integer

3600

0

9223372036854775807

The amount of time that a token should remain valid (in seconds). Drastically reducing this value may break âlong-runningâ operations that involve multiple services to coordinate together, and will force users to authenticate with keystone more frequently. Drastically increasing this value will increase the number of tokens that will be simultaneously valid. Keystone tokens are also bearer tokens, so a shorter duration will also reduce the potential security impact of a compromised token.

string

fernet

Entry point for the token provider in the keystone.token.provider namespace. The token provider controls the token construction, validation, and revocation operations. Supported upstream providers are fernet and jws . Neither fernet or jws tokens require persistence and both require additional setup. If using fernet , youâre required to run keystone-manage fernet_setup , which creates symmetric keys used to encrypt tokens. If using jws , youâre required to generate an ECDSA keypair using a SHA-256 hash algorithm for signing and validating token, which can be done with keystone-manage create_jws_keypair . Note that fernet tokens are encrypted and jws tokens are only signed. Please be sure to consider this if your deployment has security requirements regarding payload contents used to generate token IDs.

boolean

True

Toggle for caching token creation and validation data. This has no effect unless global caching is enabled.

integer

<None>

0

9223372036854775807

The number of seconds to cache token creation and validation data. This has no effect unless both global and [token] caching are enabled.

boolean

True

This toggles support for revoking individual tokens by the token identifier and thus various token enumeration operations (such as listing all tokens issued to a specific user). These operations are used to determine the list of tokens to consider revoked. Do not disable this option if youâre using the kvs [revoke] driver .

boolean

True

This toggles whether scoped tokens may be re-scoped to a new project or domain, thereby preventing users from exchanging a scoped token (including those with a default project scope) for any other token. This forces users to either authenticate for unscoped tokens (and later exchange that unscoped token for tokens with a more specific scope) or to provide their credentials in every request for a scoped token to avoid re-scoping altogether.

boolean

True

Enable storing issued token data to token validation cache so that first token validation doesnât actually cause full validation cycle. This option has no effect unless global caching is enabled and will still cache tokens even if [token] caching = False .

Warning

This option is deprecated for removal since S.
Its value may be silently ignored 
in the future.

Keystone already exposes a configuration option for caching tokens. Having a separate configuration option to cache tokens when they are issued is redundant, unnecessarily complicated, and is misleading if token caching is disabled because tokens will still be pre-cached by default when they are issued. The ability to pre-cache tokens when they are issued is going to rely exclusively on the keystone.conf [token] caching option in the future.

integer

172800

This controls the number of seconds that a token can be retrieved for beyond the built-in expiry time. This allows long running operations to succeed. Defaults to two days.

### tokenless_auth Â¶

multi-valued

''

The list of distinguished names which identify trusted issuers of client certificates allowed to use X.509 tokenless authorization. If the option is absent then no certificates will be allowed. The format for the values of a distinguished name (DN) must be separated by a comma and contain no spaces. Furthermore, because an individual DN may contain commas, this configuration option may be repeated multiple times to represent multiple values. For example, keystone.conf would include two consecutive lines in order to trust two different DNs, such as trusted_issuer = CN=john,OU=keystone,O=openstack and trusted_issuer = CN=mary,OU=eng,O=abc .

string

x509

The federated protocol ID used to represent X.509 tokenless authorization. This is used in combination with the value of [tokenless_auth] issuer_attribute to find a corresponding federated mapping. In a typical deployment, there is no reason to change this value.

string

SSL_CLIENT_I_DN

The name of the WSGI environment variable used to pass the issuer of the client certificate to keystone. This attribute is used as an identity provider ID for the X.509 tokenless authorization along with the protocol to look up its corresponding mapping. In a typical deployment, there is no reason to change this value.

### totp Â¶

integer

1

0

10

The number of previous windows to check when processing TOTP passcodes.

### trust Â¶

boolean

False

Allows authorization to be redelegated from one user to another, effectively chaining trusts together. When disabled, the remaining_uses attribute of a trust is constrained to be zero.

integer

3

Maximum number of times that authorization can be redelegated from one user to another in a chain of trusts. This number may be reduced further for a specific trust.

string

sql

Entry point for the trust backend driver in the keystone.trust namespace. Keystone only provides a sql driver, so there is no reason to change this unless you are providing a custom entry point.

### unified_limit Â¶

string

sql

Entry point for the unified limit backend driver in the keystone.unified_limit namespace. Keystone only provides a sql driver, so thereâs no reason to change this unless you are providing a custom entry point.

boolean

True

Toggle for unified limit caching. This has no effect unless global caching is enabled. In a typical deployment, there is no reason to disable this.

integer

<None>

Time to cache unified limit data, in seconds. This has no effect unless both global caching and [unified_limit] caching are enabled.

integer

<None>

Maximum number of entities that will be returned in a unified limit collection. This may be useful to tune if you have a large number of unified limits in your deployment.

string

flat

flat, strict_two_level

The enforcement model to use when validating limits associated to projects. Enforcement models will behave differently depending on the existing limits, which may result in backwards incompatible changes if a model is switched in a running deployment.

### wsgi Â¶

boolean

False

If set to true, this enables the oslo debug middleware in Keystone. This Middleware prints a lot of information about the request and the response. It is useful for getting information about the data on the wire (decoded) and passed to the WSGI application pipeline. This middleware has no effect on the âdebugâ setting in the [DEFAULT] section of the config file or setting Keystoneâs log-level to âDEBUGâ; it is specific to debugging the WSGI data as it enters and leaves Keystone (specific request-related data). This option is used for introspection on the request and response data between the web server (apache, nginx, etc) and Keystone.  This middleware is inserted as the first element in the middleware chain and will show the data closest to the wire.  WARNING: NOT INTENDED FOR USE IN PRODUCTION. THIS MIDDLEWARE CAN AND WILL EMIT SENSITIVE/PRIVILEGED DATA.

## Domain-specific Identity drivers Â¶

The Identity service supports domain-specific Identity drivers
installed on an SQL or LDAP back end, and supports domain-specific
Identity configuration options, which are stored in domain-specific
configuration files. See Domain-specific configuration for more information.
