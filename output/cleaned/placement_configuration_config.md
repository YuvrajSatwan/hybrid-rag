# Configuration Options Â¶

The following is an overview of all available configuration options in
Placement.  For a sample configuration file, refer to Sample Configuration File .

## DEFAULT Â¶

string

<None>

Explicitly specify the temporary working directory.

string

<Path>

This option has a sample default set, which means that
its actual default value may vary from the one documented
above.

The directory where the Placement python modules are installed.

This is the default path for other config options which need to persist
Placement internal data. It is very unlikely that you need to
change this option from its default value.

Possible values:

- The full path to a directory.

The full path to a directory.

Related options:

- state_path

state_path

string

$pybasedir

The top-level directory for maintaining state used in Placement.

This directory is used to store Placementâs internal state. It is used by some
tests that have behaviors carried over from Nova.

Possible values:

- The full path to a directory. Defaults to value provided in pybasedir .

The full path to a directory. Defaults to value provided in pybasedir .

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

## api Â¶

Options under this group are used to define Placement API.

string

keystone

keystone, noauth2

This determines the strategy to use for authentication: keystone or noauth2.
ânoauth2â is designed for testing only, as it does no actual credential
checking. ânoauth2â provides administrative credentials only if âadminâ is
specified as the username.

Deprecated Variations Â¶ Group Name DEFAULT auth_strategy

Group

Name

DEFAULT

auth_strategy

## cors Â¶

list

<None>

Indicate whether this resource may be shared with the domain received in the requests âoriginâ header. Format: â<protocol>://<host>[:<port>]â, no trailing slash. Example: https://horizon.example.com

boolean

True

Indicate that the actual request can include user credentials

list

[]

Indicate which headers are safe to expose to the API. Defaults to HTTP Simple Headers.

integer

3600

Maximum cache age of CORS preflight requests.

list

['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'PATCH']

Indicate which methods can be used during the actual request.

list

[]

Indicate which header field names may be used during the actual request.

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

## placement Â¶

boolean

False

If True, when limiting allocation candidate results, the results will be
a random sampling of the full result set. The
[placement]max_allocation_candidates config might limit the size of the full
set used as the input of the sampling.

If False, allocation candidates are returned in a deterministic but undefined
order. That is, all things being equal, two requests for allocation candidates
will return the same results in the same order; but no guarantees are made as
to how that order is determined.

string

00000000-0000-0000-0000-000000000000

Early API microversions (<1.8) allowed creating allocations and not specifying
a project or user identifier for the consumer. In cleaning up the data
modeling, we no longer allow missing project and user information. If an older
client makes an allocation, weâll use this in place of the information it
doesnât provide.

string

00000000-0000-0000-0000-000000000000

Early API microversions (<1.8) allowed creating allocations and not specifying
a project or user identifier for the consumer. In cleaning up the data
modeling, we no longer allow missing project and user information. If an older
client makes an allocation, weâll use this in place of the information it
doesnât provide.

integer

10

The number of times to retry, server-side, writing allocations when there is
a resource provider generation conflict. Raising this value may be useful
when many concurrent allocations to the same resource provider are expected.

integer

-1

The maximum number of allocation candidates placement generates for a single
request. This is a global limit to avoid excessive memory use and query
runtime. If set to -1 it means that the number of generated candidates are
only limited by the number and structure of the resource providers and the
content of the allocation_candidates query.

Note that the limit param of the allocation_candidates query is applied after
all the viable candidates are generated so that limit alone is not enough to
restrict the runtime or memory consumption of the query.

In a deployment with thousands of resource providers or if the deployment has
wide and symmetric provider trees, i.e. there are multiple children providers
under the same root having inventory from the same resource class
(e.g. in case of novaâs mdev GPU or PCI in Placement features) we recommend
to tune this config option based on the memory available for the
placement service and the client timeout setting on the client side. A good
initial value could be around 100000.

In a deployment with wide and symmetric provider trees we also recommend to
change the [placement]allocation_candidates_generation_strategy to
breadth-first.

string

depth-first

depth-first, breadth-first

Defines the order placement visits viable root providers during allocation
candidate generation:

- depth-first, generates all candidates from the first viable root provider
before moving to the next.

depth-first, generates all candidates from the first viable root provider
before moving to the next.

- breadth-first, generates candidates from viable roots in a round-robin
fashion, creating one candidate from each viable root before creating the
second candidate from the first root.

breadth-first, generates candidates from viable roots in a round-robin
fashion, creating one candidate from each viable root before creating the
second candidate from the first root.

If the deployment has wide and symmetric provider trees, i.e. there are
multiple children providers under the same root having inventory from the same
resource class (e.g. in case of novaâs mdev GPU or PCI in Placement features)
then the depth-first strategy with a max_allocation_candidates
limit might produce candidates from a limited set of root providers. On the
other hand breadth-first strategy will ensure that the candidates are returned
from all viable roots in a balanced way.

Both strategies produce the candidates in the API response in an undefined but
deterministic order. That is, all things being equal, two requests for
allocation candidates will return the same results in the same order; but no
guarantees are made as to how that order is determined.

## placement_database Â¶

The Placement API Database is a the database used with the placement
service. If the connection option is not set, the placement service will
not start.

string

<None>

The SQLAlchemy connection string to use to connect to the database.

string

''

Optional URL parameters to append onto the connection URL at connect time; specify as param1=value1&param2=value2&â¦

boolean

True

If True, SQLite uses synchronous mode.

string

<None>

The SQLAlchemy connection string to use to connect to the slave database.

string

TRADITIONAL

The SQL mode to be used for MySQL sessions. This option, including the default, overrides any server-set SQL mode. To use whatever SQL mode is set by the server configuration, set this to no value. Example: mysql_sql_mode=

integer

3600

Connections which have been present in the connection pool longer than this number of seconds will be replaced with a new one the next time they are checked out from the pool.

integer

<None>

Maximum number of SQL connections to keep open in a pool. Setting a value of 0 indicates no limit.

integer

10

Maximum number of database connection retries during startup. Set to -1 to specify an infinite retry count.

integer

10

Interval between retries of opening a SQL connection.

integer

<None>

If set, use this value for max_overflow with SQLAlchemy.

integer

0

Verbosity of SQL debugging information: 0=None, 100=Everything.

boolean

False

Add Python stack traces to SQL as comment strings.

integer

<None>

If set, use this value for pool_timeout with SQLAlchemy.

boolean

False

If True, database schema migrations will be attempted when the web service starts.

## profiler Â¶

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

## profiler_jaeger Â¶

string

<None>

Set service name prefix to Jaeger service name.

dict

{}

Set process tracer tags.

## profiler_otlp Â¶

string

<None>

Set service name prefix to OTLP exporters.

## workarounds Â¶

A collection of workarounds used to mitigate bugs or issues found under
certain conditions. These should only be enabled in exceptional circumstances.
All options are linked against bug IDs, where more information on the issue can
be found.

boolean

False

Enable optimization of allocation candidate generation for wide provider trees.

As reported in bug #2126751 in the situation where many similar child
provider is defined under the same root provider, placementâs allocation
candidate generation algorithm scales poorly. This config option enables
certain optimizations that help decrease the time it takes to generate the
GET /allocation_candidates response for queries requesting multiple resources
from those child providers.

For example if a compute has 8 or more child resource providers providing one
resource each (e.g. 8 individual PGPU) and a VM requests 8 or more such
resources each in independent request groups then without this optimization
enabled the GET /allocation_candidates query takes too long to compute and
the scheduling will fail.

Setting the [placement]max_allocation_candidates config option to a small number (e.g. 100) can help to a certain degree but
alone cannot solve the problem when the number of devices available or the
number of requested devices increases.

When to enable: If you have at least 8 child resource providers within a
tree providing inventory of the same resource class. And you are trying
to support VMs with more than 4 such resources.
E.g.:

- Novaâs PCI in Placement feature is enabled and you have at least 8 PCI
devices with the same product_id in a single compute and you are using
flavors requesting more than 4 such devices.

Novaâs PCI in Placement feature is enabled and you have at least 8 PCI
devices with the same product_id in a single compute and you are using
flavors requesting more than 4 such devices.

- Novaâs GPU support is enabled and you have at least 8 GPUs per compute node
while requesting more than 4 per VM.

Novaâs GPU support is enabled and you have at least 8 GPUs per compute node
while requesting more than 4 per VM.

When not to enable: If you have a flat resource provider tree, i.e. all
resources reported on the root provider. Or if your flavors are not requesting
more than 4 PCI or GPU resources of the same type.

Related options:

- [placement]max_allocation_candidates : If you need to enable the
this optimization then you are also in a situation where you want to set max_allocation_candidates to a number not more than 1000.

[placement]max_allocation_candidates : If you need to enable the
this optimization then you are also in a situation where you want to set max_allocation_candidates to a number not more than 1000.

- [placement]allocation_candidates_generation_strategy : If you use max_allocation_candidates then it is suggested to configure allocation_candidates_generation_strategy to breadth-first which will
return candidates balanced across available compute nodes.

[placement]allocation_candidates_generation_strategy : If you use max_allocation_candidates then it is suggested to configure allocation_candidates_generation_strategy to breadth-first which will
return candidates balanced across available compute nodes.
