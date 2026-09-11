# barbican.conf Â¶

## DEFAULT Â¶

string

<None>

Enable eventlet backdoor.  Acceptable values are 0, <port>, and <start>:<end>, where 0 results in listening on a random tcp port number; <port> results in listening on the specified port number (and not enabling backdoor if that port is in use); and <start>:<end> results in listening on the smallest unused port number within the specified range of port numbers. The chosen port is displayed in the serviceâs log file.

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

The âbackdoor_portâ option is deprecated and will be removed in a future release.

string

<None>

Enable eventlet backdoor, using the provided path as a unix socket that can receive connections. This option is mutually exclusive with âbackdoor_portâ in that only one should be provided. If both are provided then the existence of this option overrides the usage of that option. Inside the path {pid} will be replaced with the PID of the current process.

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

The âbackdoor_socketâ option is deprecated and will be removed in a future release.

boolean

True

Enables or disables logging values of all registered options when starting a service (at DEBUG level).

integer

60

Specify a timeout after which a gracefully shutdown server will exit. Zero value means endless wait.

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

openstack

The default exchange under which topics are scoped. May be overridden by an exchange name specified in the transport_url option.

boolean

False

Add an endpoint to answer to ping calls. Endpoint is named oslo_rpc_server_ping

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

['amqp=WARN', 'boto=WARN', 'sqlalchemy=WARN', 'suds=INFO', 'oslo.messaging=INFO', 'oslo_messaging=INFO', 'iso8601=WARN', 'requests.packages.urllib3.connectionpool=WARN', 'urllib3.connectionpool=WARN', 'websocket=WARN', 'requests.packages.urllib3.util.retry=WARN', 'urllib3.util.retry=WARN', 'keystonemiddleware=WARN', 'routes.middleware=WARN', 'stevedore=WARN', 'taskflow=WARN', 'keystoneauth=WARN', 'oslo.cache=INFO', 'oslo_policy=INFO', 'dogpile.core.dogpile=INFO']

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

string

admin

Role used to identify an authenticated user as administrator.

boolean

False

Allow unauthenticated users to access the API with read-only privileges. This only applies when using ContextMiddleware.

integer

25000

Maximum allowed http request size against the barbican-api.

integer

20000

Maximum allowed secret size in bytes.

string

http://localhost:9311

Host name, for use in HATEOAS-style references Note: Typically this would be the load balanced endpoint that clients would use to communicate back with this service. If a deployment wants to derive host from wsgi request instead then make this blank. Blank is needed to override default config value which is â http://localhost:9311 â

boolean

False

Create the Barbican database on service startup.

integer

100

Maximum page size for the âlimitâ paging URL parameter.

integer

10

Default page size for the âlimitâ paging URL parameter.

string

QueuePool

Accepts a class imported from the sqlalchemy.pool module, and handles the details of building the pool for you. If commented out, SQLAlchemy will select based on the database dialect. Other options are QueuePool (for SQLAlchemy-managed connections) and NullPool (to disabled SQLAlchemy management of connections). See http://docs.sqlalchemy.org/en/latest/core/pooling.html for more details

Warning

This option is deprecated for removal.
Its value may be silently ignored 
in the future.

This option has been ineffective

boolean

False

Show SQLAlchemy pool-related debugging output in logs (sets DEBUG log level output) if specified.

## audit_middleware_notifications Â¶

boolean

True

Indicate whether to use oslo_messaging as the notifier. If set to False, the local logger will be used as the notifier. If set to True, the oslo_messaging package must also be present. Otherwise, the local will be used instead.

string

<None>

The Driver to handle sending notifications. Possible values are messaging, messagingv2, routing, log, test, noop. If not specified, then value from oslo_messaging_notifications conf section is used.

list

<None>

List of AMQP topics used for OpenStack notifications. If not specified, then value from  oslo_messaging_notifications conf section is used.

string

<None>

A URL representing messaging driver to use for notification. If not specified, we fall back to the same configuration used for RPC.

## cors Â¶

list

<None>

Indicate whether this resource may be shared with the domain received in the requests âoriginâ header. Format: â<protocol>://<host>[:<port>]â, no trailing slash. Example: https://horizon.example.com

boolean

True

Indicate that the actual request can include user credentials

list

['X-Auth-Token', 'X-Openstack-Request-Id', 'X-Project-Id', 'X-Identity-Status', 'X-User-Id', 'X-Storage-Token', 'X-Domain-Id', 'X-User-Domain-Id', 'X-Project-Domain-Id', 'X-Roles']

Indicate which headers are safe to expose to the API. Defaults to HTTP Simple Headers.

integer

3600

Maximum cache age of CORS preflight requests.

list

['GET', 'PUT', 'POST', 'DELETE', 'PATCH']

Indicate which methods can be used during the actual request.

list

['X-Auth-Token', 'X-Openstack-Request-Id', 'X-Project-Id', 'X-Identity-Status', 'X-User-Id', 'X-Storage-Token', 'X-Domain-Id', 'X-User-Domain-Id', 'X-Project-Domain-Id', 'X-Roles']

Indicate which header field names may be used during the actual request.

## crypto Â¶

string

barbican.crypto.plugin

Extension namespace to search for plugins.

multi-valued

simple_crypto

List of crypto plugins to load.

## database Â¶

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

## dogtag_plugin Â¶

string

/etc/barbican/kra_admin_cert.pem

Path to PEM file for authentication

string

localhost

Hostname for the Dogtag instance

port number

8443

0

65535

Port for the Dogtag instance

string

/etc/barbican/alias

Path to the NSS certificate database

string

<None>

Password for the NSS certificate databases

string

Dogtag KRA

User friendly plugin name

integer

3

Retries when storing or generating secrets

## healthcheck Â¶

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

## keystone_authtoken Â¶

string

<None>

Complete âpublicâ Identity API endpoint. This endpoint should not be an âadminâ endpoint, as it should be accessible by all end users. Unauthenticated clients are redirected to this endpoint to authenticate. Although this endpoint should ideally be unversioned, client support in the wild varies. If youâre using a versioned v2 endpoint here, then this should not be the same endpoint the service user utilizes for validating tokens, because normal end users may not be able to reach that endpoint.

Deprecated Variations Â¶ Group Name keystone_authtoken auth_uri

Group

Name

keystone_authtoken

auth_uri

string

<None>

Complete âpublicâ Identity API endpoint. This endpoint should not be an âadminâ endpoint, as it should be accessible by all end users. Unauthenticated clients are redirected to this endpoint to authenticate. Although this endpoint should ideally be unversioned, client support in the wild varies. If youâre using a versioned v2 endpoint here, then this should not be the same endpoint the service user utilizes for validating tokens, because normal end users may not be able to reach that endpoint. This option is deprecated in favor of www_authenticate_uri and will be removed in the S release.

Warning

This option is deprecated for removal since Queens.
Its value may be silently ignored 
in the future.

The auth_uri option is deprecated in favor of www_authenticate_uri and will be removed in the S  release.

string

<None>

API version of the Identity API endpoint.

string

internal

Interface to use for the Identity API endpoint. Valid values are âpublicâ, âinternalâ (default) or âadminâ.

boolean

False

Do not handle authorization requests within the middleware, but delegate the authorization decision to downstream WSGI components.

integer

<None>

Request timeout value for communicating with Identity API server.

integer

3

How many times are we trying to reconnect when communicating with Identity API Server.

string

<None>

Request environment key where the Swift cache object is stored. When auth_token middleware is deployed with a Swift cache, use this option to have the middleware share a caching backend with swift. Otherwise, use the memcached_servers option instead.

string

<None>

Required if identity server requires client certificate

string

<None>

Required if identity server requires client certificate

string

<None>

A PEM encoded Certificate Authority to use when verifying HTTPs connections. Defaults to system CAs.

boolean

False

Verify HTTPS connections.

string

<None>

The region in which the identity server can be found.

list

<None>

Optionally specify a list of memcached server(s) to use for caching. If left undefined, tokens will instead be cached in-process.

Deprecated Variations Â¶ Group Name keystone_authtoken memcache_servers

Group

Name

keystone_authtoken

memcache_servers

integer

300

In order to prevent excessive effort spent validating tokens, the middleware caches previously-seen tokens for a configurable duration (in seconds). Set to -1 to disable caching completely.

string

None

None, MAC, ENCRYPT

(Optional) If defined, indicate whether token data should be authenticated or authenticated and encrypted. If MAC, token data is authenticated (with HMAC) in the cache. If ENCRYPT, token data is encrypted and authenticated in the cache. If the value is not one of these options or empty, auth_token will raise an exception on initialization.

string

<None>

(Optional, mandatory if memcache_security_strategy is defined) This string is used for key derivation.

boolean

False

(Optional) Global toggle for TLS usage when comunicating with the caching servers.

string

<None>

(Optional) Path to a file of concatenated CA certificates in PEM format necessary to establish the caching serverâs authenticity. If tls_enabled is False, this option is ignored.

string

<None>

(Optional) Path to a single file in PEM format containing the clientâs certificate as well as any number of CA certificates needed to establish the certificateâs authenticity. This file is only required when client side authentication is necessary. If tls_enabled is False, this option is ignored.

string

<None>

(Optional) Path to a single file containing the clientâs private key in. Otherwhise the private key will be taken from the file specified in tls_certfile. If tls_enabled is False, this option is ignored.

string

<None>

(Optional) Set the available ciphers for sockets created with the TLS context. It should be a string in the OpenSSL cipher list format. If not specified, all OpenSSL enabled ciphers will be available.

integer

300

(Optional) Number of seconds memcached server is considered dead before it is tried again.

integer

10

(Optional) Maximum total number of open connections to every memcached server.

integer

3

(Optional) Socket timeout in seconds for communicating with a memcached server.

integer

60

(Optional) Number of seconds a connection to memcached is held unused in the pool before it is closed.

integer

10

(Optional) Number of seconds that an operation will wait to get a memcached client connection from the pool.

boolean

True

(Optional) Use the advanced (eventlet safe) memcached client pool.

boolean

True

(Optional) Indicate whether to set the X-Service-Catalog header. If False, middleware will not ask for service catalog on token validation and will not set the X-Service-Catalog header.

string

permissive

Used to control the use and type of token binding. Can be set to: âdisabledâ to not check token binding. âpermissiveâ (default) to validate binding information if the bind type is of a form known to the server and ignore it if not. âstrictâ like âpermissiveâ but if the bind type is unknown the token will be rejected. ârequiredâ any form of token binding is needed to be allowed. Finally the name of a binding method that must be present in tokens.

list

['service']

A choice of roles that must be present in a service token. Service tokens are allowed to request that an expired token can be used and so this check should tightly control that only actual services should be sending this token. Roles here are applied as an ANY check so any role in this list must be present. For backwards compatibility reasons this currently only affects the allow_expired check.

boolean

False

For backwards compatibility reasons we must let valid service tokens pass that donât pass the service_token_roles check as valid. Setting this true will become the default in a future release and should be enabled if possible.

string

<None>

The name or type of the service as it appears in the service catalog. This is used to validate tokens that have restricted access rules.

boolean

False

Enable the SASL(Simple Authentication and Security Layer) if the SASL_enable is true, else disable.

string

''

the user name for the SASL

string

''

the username password for SASL

unknown type

<None>

Authentication type to load

Deprecated Variations Â¶ Group Name keystone_authtoken auth_plugin

Group

Name

keystone_authtoken

auth_plugin

unknown type

<None>

Config Section from which to load plugin specific options

## keystone_notifications Â¶

boolean

False

True enables keystone notification listener  functionality.

string

keystone

The default exchange under which topics are scoped. May be overridden by an exchange name specified in the transport_url option.

string

notifications

Keystone notification queue topic name. This name needs to match one of values mentioned in Keystone deploymentâs ânotification_topicsâ configuration e.g.    notification_topics=notifications,     barbican_notificationsMultiple servers may listen on a topic and messages will be dispatched to one of the servers in a round-robin fashion. Thatâs why Barbican service should have its own dedicated notification queue so that it receives all of Keystone notifications. Alternatively if the chosen oslo.messaging backend supports listener pooling (for example rabbitmq), setting a non-default âpool_nameâ option should be preferred.

string

<None>

Pool name for notifications listener. Setting this to a distinctive value will allow barbican notifications listener to receive its own copy of all messages from the topic without without interfering with other services listening on the same topic. This feature is supported only by some oslo.messaging backends (in particilar by rabbitmq) and for those it is preferrable to use it instead of separate notification topic for barbican.

boolean

False

True enables requeue feature in case of notification processing error. Enable this only when underlying transport supports this feature.

string

1.0

Version of tasks invoked via notifications

integer

10

Define the number of max threads to be used for notification server processing functionality.

## kmip_plugin Â¶

string

<None>

Username for authenticating with KMIP server

string

<None>

Password for authenticating with KMIP server

string

localhost

Address of the KMIP server

port number

5696

0

65535

Port for the KMIP server

string

PROTOCOL_TLSv1_2

SSL version, maps to the module sslâs constants

string

<None>

File path to concatenated âcertification authorityâ certificates

string

<None>

File path to local client certificate

string

<None>

File path to local client certificate keyfile

boolean

False

Only support PKCS#1 encoding of asymmetric keys

string

KMIP HSM

User friendly plugin name

## oslo_messaging_kafka Â¶

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

## oslo_messaging_notifications Â¶

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

## oslo_messaging_rabbit Â¶

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

## oslo_middleware Â¶

boolean

False

Whether the application is behind a proxy or not. This determines if the middleware should parse the headers or not.

## oslo_policy Â¶

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

## oslo_versionedobjects Â¶

boolean

False

Make exception message format errors fatal

## p11_crypto_plugin Â¶

string

<None>

Path to vendor PKCS11 library

string

<None>

Token serial number used to identify the token to be used.

list

[]

List of labels for one or more tokens to be used. Typically this is a single label, but some HSM devices may require more than one label for Load Balancing or High Availability configurations.

string

<None>

Password (PIN) to login to PKCS11 session

string

<None>

Master KEK label (as stored in the HSM)

integer

32

1

Master KEK length in bytes.

string

<None>

Master HMAC Key label (as stored in the HSM)

integer

1

(Optional) HSM Slot ID that contains the token device to be used.

boolean

True

Flag for Read/Write Sessions

integer

32

Project KEK length in bytes.

integer

900

Project KEK Cache Time To Live, in seconds

integer

100

Project KEK Cache Item Limit

string

CKM_AES_CBC

Secret encryption mechanism

string

CKK_AES

HMAC Key Type

string

CKM_AES_KEY_GEN

HMAC Key Generation Algorithm used to create the master HMAC Key.

string

CKM_SHA256_HMAC

HMAC algorithm used to sign encrypted data.

Deprecated Variations Â¶ Group Name p11_crypto_plugin hmac_keywrap_mechanism

Group

Name

p11_crypto_plugin

hmac_keywrap_mechanism

string

CKM_AES_CBC_PAD

Key Wrapping algorithm used to wrap Project KEKs.

boolean

True

Generate IVs for Key Wrapping mechanism.

string

''

File to pull entropy for seeding RNG

integer

32

Amount of data to read from file for seed

string

PKCS11 HSM

User friendly plugin name

boolean

True

Generate IVs for CKM_AES_GCM mechanism.

Deprecated Variations Â¶ Group Name p11_crypto_plugin generate_iv

Group

Name

p11_crypto_plugin

generate_iv

boolean

True

Always set CKA_SENSITIVE=CK_TRUE including CKA_EXTRACTABLE=CK_TRUE keys.

boolean

False

Enable CKF_OS_LOCKING_OK flag when initializing the PKCS#11 client library.

## queue Â¶

boolean

False

True enables queuing, False invokes workers synchronously

string

barbican

Queue namespace

string

barbican.workers

Queue topic name

string

1.1

Version of tasks invoked via queue

string

barbican.queue

Server name for RPC task processing server

integer

1

Number of asynchronous worker processes

## quotas Â¶

integer

-1

Number of secrets allowed per project

integer

-1

Number of orders allowed per project

integer

-1

Number of containers allowed per project

integer

-1

Number of consumers allowed per project

integer

-1

Number of CAs allowed per project

## retry_scheduler Â¶

floating point

10.0

Seconds (float) to wait before starting retry scheduler

floating point

10.0

Seconds (float) to wait between periodic schedule events

## secretstore Â¶

string

barbican.secretstore.plugin

Extension namespace to search for plugins.

multi-valued

store_crypto

List of secret store plugins to load.

boolean

False

Flag to enable multiple secret store plugin backend support. Default is False

list

<None>

List of suffix to use for looking up plugins which are supported with multiple backend support.

## simple_crypto_plugin Â¶

multi-valued

''

Fernet Key-Encryption Key (KEK) to be used by SimpleCrypto Plugin to encrypt Project-specific KEKs.

string

Software Only Crypto

User friendly plugin name

## vault_plugin Â¶

string

<None>

root token for vault

string

<None>

AppRole role_id for authentication with vault

string

<None>

AppRole secret_id for authentication with vault

string

secret

Mountpoint of KV store in Vault to use, for example: secret

string

http://127.0.0.1:8200

Use this endpoint to connect to Vault, for example: â http://127.0.0.1:8200 â

string

<None>

Absolute path to ca cert file

boolean

False

SSL Enabled/Disabled

string

<None>

Vault Namespace to use for all requests. Namespaces is a feature available in HasiCorp Vault Enterprise only.
