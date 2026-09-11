# Cells (v2) Â¶

Added in version 16.0.0: (Pike)

This document describes the layout of a deployment with cells v2, including
deployment considerations for security and scale and recommended practices and
tips for running and maintaining cells v2 for admins and operators. It is
focused on code present in Pike and later, and while it is geared towards
people who want to have multiple cells for whatever reason, the nature of the
cells v2 support in Nova means that it applies in some way to all deployments.

Before reading any further, there is a nice overview presentation that Andrew
Laski gave at the Austin (Newton) summit which may be worth watching.

Note

Cells v2 is different to the cells feature found in earlier versions of
nova, also known as Cells v1. Cells v1 was deprecated in 16.0.0 (Pike) and
removed entirely in Train (20.0.0).

## Overview Â¶

The purpose of the cells functionality in nova is to allow larger deployments
to shard their many compute nodes into cells. All nova deployments are by
definition cells deployments, even if most will only ever have a single cell.
This means a multi-cell deployment will not be radically different from a
âstandardâ nova deployment.

Consider such a deployment. It will consists of the following components:

- The Compute API which provides the external REST API to users.

The Compute API which provides the external REST API to users.

- The nova-scheduler and placement services which are
responsible for tracking resources and deciding which compute node instances
should be on.

The nova-scheduler and placement services which are
responsible for tracking resources and deciding which compute node instances
should be on.

- An âAPI databaseâ that is used primarily by the Compute API and nova-scheduler (called API-level services below) to track
location information about instances, as well as a temporary location for
instances being built but not yet scheduled.

An âAPI databaseâ that is used primarily by the Compute API and nova-scheduler (called API-level services below) to track
location information about instances, as well as a temporary location for
instances being built but not yet scheduled.

- The nova-conductor service which offloads long-running tasks for
the API-level services and insulates compute nodes from direct database access

The nova-conductor service which offloads long-running tasks for
the API-level services and insulates compute nodes from direct database access

- The nova-compute service which manages the virt driver and
hypervisor host.

The nova-compute service which manages the virt driver and
hypervisor host.

- A âcell databaseâ which is used by API, conductor and compute
services, and which houses the majority of the information about
instances.

A âcell databaseâ which is used by API, conductor and compute
services, and which houses the majority of the information about
instances.

- A âcell0 databaseâ which is just like the cell database, but
contains only instances that failed to be scheduled. This database mimics a
regular cell, but has no compute nodes and is used only as a place to put
instances that fail to land on a real compute node (and thus a real cell).

A âcell0 databaseâ which is just like the cell database, but
contains only instances that failed to be scheduled. This database mimics a
regular cell, but has no compute nodes and is used only as a place to put
instances that fail to land on a real compute node (and thus a real cell).

- A message queue which allows the services to communicate with each
other via RPC.

A message queue which allows the services to communicate with each
other via RPC.

In smaller deployments, there will typically be a single message queue that all
services share and a single database server which hosts the API database, a
single cell database, as well as the required cell0 database. Because we only
have one ârealâ cell, we consider this a âsingle-cell deploymentâ.

In larger deployments, we can opt to shard the deployment using multiple cells.
In this configuration there will still only be one global API database but
there will be a cell database (where the bulk of the instance information
lives) for each cell, each containing a portion of the instances for the entire
deployment within, as well as per-cell message queues and per-cell nova-conductor instances. There will also be an additional nova-conductor instance, known as a super conductor , to handle
API-level operations.

In these larger deployments, each of the nova services will use a cell-specific
configuration file, all of which will at a minimum specify a message queue
endpoint (i.e. transport_url ). Most of the services will
also contain database connection configuration information (i.e. database.connection ), while API-level services that need
access to the global routing and placement information will also be configured
to reach the API database (i.e. api_database.connection ).

Note

The pair of transport_url and database.connection configured for a service defines
what cell a service lives in.

API-level services need to be able to contact other services in all of
the cells. Since they only have one configured transport_url and database.connection , they look up the information for the
other cells in the API database, with records called cell mappings .

Note

The API database must have cell mapping records that match
the transport_url and database.connection configuration options of the
lower-level services. See the nova-manage Cells v2 Commands commands for more information about how to create and examine these records.

The following section goes into more detail about the difference between
single-cell and multi-cell deployments.

## Service layout Â¶

The services generally have a well-defined communication pattern that
dictates their layout in a deployment. In a small/simple scenario, the
rules do not have much of an impact as all the services can
communicate with each other on a single message bus and in a single
cell database. However, as the deployment grows, scaling and security
concerns may drive separation and isolation of the services.

### Single cell Â¶

This is a diagram of the basic services that a simple (single-cell) deployment
would have, as well as the relationships (i.e. communication paths) between
them:

All of the services are configured to talk to each other over the same
message bus, and there is only one cell database where live instance
data resides. The cell0 database is present (and required) but as no
compute nodes are connected to it, this is still a âsingle cellâ
deployment.

### Multiple cells Â¶

In order to shard the services into multiple cells, a number of things
must happen. First, the message bus must be split into pieces along
the same lines as the cell database. Second, a dedicated conductor
must be run for the API-level services, with access to the API
database and a dedicated message queue. We call this super conductor to distinguish its place and purpose from the per-cell conductor nodes.

It is important to note that services in the lower cell boxes only
have the ability to call back to the placement API but cannot access
any other API-layer services via RPC, nor do they have access to the
API database for global visibility of resources across the cloud.
This is intentional and provides security and failure domain
isolation benefits, but also has impacts on some things that would
otherwise require this any-to-any communication style. Check Operations requiring upcalls below for the most up-to-date information about any caveats that may be present
due to this limitation.

## Database layout Â¶

As mentioned previously, there is a split between global data and data that is
local to a cell. These databases schema are referred to as the API and main database schemas, respectively.

### API database Â¶

The API database is the database used for API-level services, such as the
Compute API and, in a multi-cell deployment, the superconductor.
The models and migrations related to this database can be found in nova.db.api , and the database can be managed using the nova-manage api_db commands.

### Main (cell-level) database Â¶

The main database is the database used for cell-level nova-conductor instances. The models and migrations related to this database can be found in nova.db.main , and the database can be managed using the nova-manage db commands.

## Usage Â¶

As noted previously, all deployments are in effect now cells v2 deployments. As
a result, setup of any nova deployment - even those that intend to only have
one cell - will involve some level of cells configuration. These changes are
configuration-related, both in the main nova configuration file as well as some
extra records in the databases.

All nova deployments must now have the following databases available
and configured:

- The âAPIâ database

The âAPIâ database

- One special âcellâ database called âcell0â

One special âcellâ database called âcell0â

- One (or eventually more) âcellâ databases

One (or eventually more) âcellâ databases

Thus, a small nova deployment will have an API database, a cell0, and
what we will call here a âcell1â database. High-level tracking
information is kept in the API database. Instances that are never
scheduled are relegated to the cell0 database, which is effectively a
graveyard of instances that failed to start. All successful/running
instances are stored in âcell1â.

Note

Since Nova services make use of both configuration file and some
databases records, starting or restarting those services with an
incomplete configuration could lead to an incorrect deployment.
Only restart the services once you are done with the described
steps below.

Note

The following examples show the full expanded command line usage of
the setup commands. This is to make it easier to visualize which of
the various URLs are used by each of the commands. However, you should be
able to put all of that in the config file and nova-manage will
use those values. If need be, you can create separate config files and pass
them as nova-manage --config-file foo.conf to control the behavior
without specifying things on the command lines.

### Configuring a new deployment Â¶

If you are installing Nova for the first time and have no compute hosts in the
database yet then it will be necessary to configure cell0 and at least one
additional ârealâ cell. To begin, ensure your API database schema has been
populated using the nova-manage api_db sync command. Ensure the
connection information for this database is stored in the nova.conf file
using the api_database.connection config option:

[api_database] connection = mysql+pymysql://root:secretmysql@dbserver/nova_api?charset=utf8

Since there may be multiple âcellâ databases (and in fact everyone
will have cell0 and cell1 at a minimum), connection info for these is
stored in the API database. Thus, the API database must exist and must provide
information on how to connect to it before continuing to the steps below, so
that nova-manage can find your other databases.

Next, we will create the necessary records for the cell0 database. To
do that we will first use nova-manage cell_v2 map_cell0 to create
and map cell0. For example:

$ nova-manage cell_v2 map_cell0 \ --database_connection mysql+pymysql://root:secretmysql@dbserver/nova_cell0?charset = utf8

Note

If you donât specify --database_connection then the commands will use
the database.connection value from your config file
and mangle the database name to have a _cell0 suffix

Warning

If your databases are on separate hosts then you should specify --database_connection or make certain that the nova.conf being used has the database.connection value pointing
to the same user/password/host that will work for the cell0 database.
If the cell0 mapping was created incorrectly, it can be deleted
using the nova-manage cell_v2 delete_cell command before running nova-manage cell_v2 map_cell0 again with the proper database
connection value.

We will then use nova-manage db sync to apply the database schema to
this new database. For example:

$ nova-manage db sync \ --database_connection mysql+pymysql://root:secretmysql@dbserver/nova_cell0?charset = utf8

Since no hosts are ever in cell0, nothing further is required for its setup.
Note that all deployments only ever have one cell0, as it is special, so once
you have done this step you never need to do it again, even if you add more
regular cells.

Now, we must create another cell which will be our first âregularâ
cell, which has actual compute hosts in it, and to which instances can
actually be scheduled. First, we create the cell record using nova-manage cell_v2 create_cell . For example:

$ nova-manage cell_v2 create_cell \ --name cell1 \ --database_connection mysql+pymysql://root:secretmysql@127.0.0.1/nova?charset = utf8 \ --transport-url rabbit://stackrabbit:secretrabbit@mqserver:5672/

Note

If you donât specify the database and transport urls then nova-manage will use the transport_url and database.connection values from the config file.

Note

It is a good idea to specify a name for the new cell you create so you can
easily look up cell UUIDs with the nova-manage cell_v2 list_cells command later if needed.

Note

The nova-manage cell_v2 create_cell command will print the UUID
of the newly-created cell if --verbose is passed, which is useful if you
need to run commands like nova-manage cell_v2 discover_hosts targeted at a specific cell.

At this point, the API database can now find the cell database, and further
commands will attempt to look inside. If this is a completely fresh database
(such as if youâre adding a cell, or if this is a new deployment), then you
will need to run nova-manage db sync on it to initialize the
schema.

Now we have a cell, but no hosts are in it which means the scheduler will never
actually place instances there. The next step is to scan the database for
compute node records and add them into the cell we just created. For this step,
you must have had a compute node started such that it registers itself as a
running service. You can identify this using the openstack compute
service list command:

$ openstack compute service list --service nova-compute

Once that has happened, you can scan and add it to the cell using the nova-manage cell_v2 discover_hosts command:

$ nova-manage cell_v2 discover_hosts

This command will connect to any databases for which you have created cells (as
above), look for hosts that have registered themselves there, and map those
hosts in the API database so that they are visible to the scheduler as
available targets for instances. Any time you add more compute hosts to a cell,
you need to re-run this command to map them from the top-level so they can be
utilized. You can also configure a periodic task to have Nova discover new
hosts automatically by setting the scheduler.discover_hosts_in_cells_interval to a time
interval in seconds. The periodic task is run by the nova-scheduler service, so you must be sure to configure it on all of your nova-scheduler hosts.

Note

In the future, whenever you add new compute hosts, you will need to run the nova-manage cell_v2 discover_hosts command after starting them to
map them to the cell if you did not configure automatic host discovery using scheduler.discover_hosts_in_cells_interval .

### Adding a new cell to an existing deployment Â¶

You can add additional cells to your deployment using the same steps used above
to create your first cell. We can create a new cell record using nova-manage cell_v2 create_cell . For example:

$ nova-manage cell_v2 create_cell \ --name cell2 \ --database_connection mysql+pymysql://root:secretmysql@127.0.0.1/nova?charset = utf8 \ --transport-url rabbit://stackrabbit:secretrabbit@mqserver:5672/

Note

If you donât specify the database and transport urls then nova-manage will use the transport_url and database.connection values from the config file.

Note

It is a good idea to specify a name for the new cell you create so you can
easily look up cell UUIDs with the nova-manage cell_v2 list_cells command later if needed.

Note

The nova-manage cell_v2 create_cell command will print the UUID
of the newly-created cell if --verbose is passed, which is useful if you
need to run commands like nova-manage cell_v2 discover_hosts targeted at a specific cell.

You can repeat this step for each cell you wish to add to your deployment. Your
existing cell database will be reused - this simply informs the top-level API
database about your existing cell databases.

Once youâve created your new cell, use nova-manage cell_v2
discover_hosts to map compute hosts to cells. This is only necessary if you
havenât enabled automatic discovery using the scheduler.discover_hosts_in_cells_interval option. For
example:

$ nova-manage cell_v2 discover_hosts

Note

This command will search for compute hosts in each cell database and map
them to the corresponding cell. This can be slow, particularly for larger
deployments. You may wish to specify the --cell_uuid option, which will
limit the search to a specific cell. You can use the nova-manage
cell_v2 list_cells command to look up cell UUIDs if you are going to
specify --cell_uuid .

Finally, run the nova-manage cell_v2 map_instances command to map
existing instances to the new cell(s). For example:

$ nova-manage cell_v2 map_instances

Note

This command will search for instances in each cell database and map them to
the correct cell. This can be slow, particularly for larger deployments. You
may wish to specify the --cell_uuid option, which will limit the search
to a specific cell. You can use the nova-manage cell_v2
list_cells command to look up cell UUIDs if you are going to specify --cell_uuid .

Note

The --max-count option can be specified if you would like to limit the
number of instances to map in a single run. If --max-count is not
specified, all instances will be mapped. Repeated runs of the command will
start from where the last run finished so it is not necessary to increase --max-count to finish. An exit code of 0 indicates that all instances
have been mapped. An exit code of 1 indicates that there are remaining
instances that need to be mapped.

### Template URLs in Cell Mappings Â¶

Starting in the 18.0.0 (Rocky) release, the URLs provided in the cell mappings
for --database_connection and --transport-url can contain
variables which are evaluated each time they are loaded from the
database, and the values of which are taken from the corresponding
base options in the hostâs configuration file.  The base URL is parsed
and the following elements may be substituted into the cell mapping
URL (using rabbit://bob:s3kret@myhost:123/nova?sync=true#extra ):

Cell Mapping URL Variables Â¶ Variable Meaning Part of example URL scheme The part before the :// rabbit username The username part of the credentials bob password The password part of the credentials s3kret hostname The hostname or address myhost port The port number (must be specified) 123 path The âpathâ part of the URL (without leading slash) nova query The full query string arguments (without leading question mark) sync=true fragment Everything after the first hash mark extra

Variable

Meaning

Part of example URL

scheme

The part before the ://

rabbit

username

The username part of the credentials

bob

password

The password part of the credentials

s3kret

hostname

The hostname or address

myhost

port

The port number (must be specified)

123

path

The âpathâ part of the URL (without leading slash)

nova

query

The full query string arguments (without leading question mark)

sync=true

fragment

Everything after the first hash mark

extra

Variables are provided in curly brackets, like {username} . A simple template
of rabbit://{username}:{password}@otherhost/{path} will generate a full URL
of rabbit://bob:s3kret@otherhost/nova when used with the above example.

Note

The database.connection and transport_url values are not reloaded from the
configuration file during a SIGHUP, which means that a full service restart
will be required to notice changes in a cell mapping record if variables are
changed.

Note

The transport_url option can contain an
extended syntax for the ânetlocâ part of the URL
(i.e. userA:passwordA@hostA:portA,userB:passwordB@hostB:portB ). In this
case, substitutions of the form username1 , username2 , etc will be
honored and can be used in the template URL.

The templating of these URLs may be helpful in order to provide each service host
with its own credentials for, say, the database. Without templating, all hosts
will use the same URL (and thus credentials) for accessing services like the
database and message queue. By using a URL with a template that results in the
credentials being taken from the host-local configuration file, each host will
use different values for those connections.

Assuming you have two service hosts that are normally configured with the cell0
database as their primary connection, their (abbreviated) configurations would
look like this:

[database] connection = mysql+pymysql://service1:foo@myapidbhost/nova_cell0

and:

[database] connection = mysql+pymysql://service2:bar@myapidbhost/nova_cell0

Without cell mapping template URLs, they would still use the same credentials
(as stored in the mapping) to connect to the cell databases. However, consider
template URLs like the following:

mysql + pymysql : // { username }:{ password } @mycell1dbhost / nova

and:

mysql + pymysql : // { username }:{ password } @mycell2dbhost / nova

Using the first service and cell1 mapping, the calculated URL that will actually
be used for connecting to that database will be:

mysql + pymysql : // service1 : foo @mycell1dbhost / nova

## Design Â¶

Prior to the introduction of cells v2, when a request hit the Nova API for a
particular instance, the instance information was fetched from the database.
The information contained the hostname of the compute node on which the
instance was currently located. If the request needed to take action on the
instance (which it generally would), the hostname was used to calculate the
name of a queue and a message was written there which would eventually find its
way to the proper compute node.

The meat of the cells v2 feature was to split this hostname lookup into two parts
that yielded three pieces of information instead of one. Basically, instead of
merely looking up the name of the compute node on which an instance was
located, we also started obtaining database and queue connection information.
Thus, when asked to take action on instance $foo, we now:

- Lookup the three-tuple of (database, queue, hostname) for that instance

Lookup the three-tuple of (database, queue, hostname) for that instance

- Connect to that database and fetch the instance record

Connect to that database and fetch the instance record

- Connect to the queue and send the message to the proper hostname queue

Connect to the queue and send the message to the proper hostname queue

The above differs from the previous organization in two ways. First, we now
need to do two database lookups before we know where the instance lives.
Second, we need to demand-connect to the appropriate database and queue. Both
of these changes had performance implications, but it was possible to mitigate
them through the use of things like a memcache of instance mapping information
and pooling of connections to database and queue systems. The number of cells
will always be much smaller than the number of instances.

There were also availability implications with the new feature since something like a
instance list which might query multiple cells could end up with a partial result
if there is a database failure in a cell. These issues can be mitigated, as
discussed in Handling cell failures . A database failure within a cell
would cause larger issues than a partial list result so the expectation is that
it would be addressed quickly and cells v2 will handle it by indicating in the
response that the data may not be complete.

## Comparison with cells v1 Â¶

Prior to the introduction of cells v2, nova had a very similar feature, also
called cells or referred to as cells v1 for disambiguation. Cells v2 was an
effort to address many of the perceived shortcomings of the cell v1 feature.
Benefits of the cells v2 feature over the previous cells v1 feature include:

- Native sharding of the database and queue as a first-class-feature in nova.
All of the code paths will go through the lookup procedure and thus we wonât
have the same feature parity issues as we do with current cells.

Native sharding of the database and queue as a first-class-feature in nova.
All of the code paths will go through the lookup procedure and thus we wonât
have the same feature parity issues as we do with current cells.

- No high-level replication of all the cell databases at the top. The API will
need a database of its own for things like the instance index, but it will
not need to replicate all the data at the top level.

No high-level replication of all the cell databases at the top. The API will
need a database of its own for things like the instance index, but it will
not need to replicate all the data at the top level.

- It draws a clear line between global and local data elements. Things like
flavors and keypairs are clearly global concepts that need only live at the
top level. Providing this separation allows compute nodes to become even more
stateless and insulated from things like deleted/changed global data.

It draws a clear line between global and local data elements. Things like
flavors and keypairs are clearly global concepts that need only live at the
top level. Providing this separation allows compute nodes to become even more
stateless and insulated from things like deleted/changed global data.

- Existing non-cells users will suddenly gain the ability to spawn a new âcellâ
from their existing deployment without changing their architecture. Simply
adding information about the new database and queue systems to the new index
will allow them to consume those resources.

Existing non-cells users will suddenly gain the ability to spawn a new âcellâ
from their existing deployment without changing their architecture. Simply
adding information about the new database and queue systems to the new index
will allow them to consume those resources.

- Existing cells users will need to fill out the cells mapping index, shutdown
their existing cells synchronization service, and ultimately clean up their
top level database. However, since the high-level organization is not
substantially different, they will not have to re-architect their systems to
move to cells v2.

Existing cells users will need to fill out the cells mapping index, shutdown
their existing cells synchronization service, and ultimately clean up their
top level database. However, since the high-level organization is not
substantially different, they will not have to re-architect their systems to
move to cells v2.

- Adding new sets of hosts as a new âcellâ allows them to be plugged into a
deployment and tested before allowing builds to be scheduled to them.

Adding new sets of hosts as a new âcellâ allows them to be plugged into a
deployment and tested before allowing builds to be scheduled to them.

## Caveats Â¶

Note

Many of these caveats have been addressed since the introduction of cells v2
in the 16.0.0 (Pike) release. These are called out below.

### Cross-cell move operations Â¶

Support for cross-cell cold migration and resize was introduced in the 21.0.0
(Ussuri) release. This is documented in Cross-cell resize . Prior to this release, it was
not possible to cold migrate or resize an instance from a host in one cell to a
host in another cell.

It is not currently possible to live migrate, evacuate or unshelve an instance
from a host in one cell to a host in another cell.

### Quota-related quirks Â¶

Quotas are now calculated live at the point at which an operation
would consume more resource, instead of being kept statically in the
database. This means that a multi-cell environment may incorrectly
calculate the usage of a tenant if one of the cells is unreachable, as
those resources cannot be counted. In this case, the tenant may be
able to consume more resource from one of the available cells, putting
them far over quota when the unreachable cell returns.

Note

Starting in the Train (20.0.0) release, it is possible to configure
counting of quota usage from the placement service and API database
to make quota usage calculations resilient to down or poor-performing
cells in a multi-cell environment. See the quotas documentation for more details.

Starting in the 2023.2 Bobcat (28.0.0) release, it is possible to configure
unified limits quotas, which stores quota limits as Keystone unified limits
and counts quota usage from the placement service and API database. See the unified limits documentation for more
details.

### Performance of listing instances Â¶

Prior to the 17.0.0 (Queens) release, the instance list operation may not sort
and paginate results properly when crossing multiple cell boundaries. Further,
the performance of a sorted list operation across multiple cells was
considerably slower than with a single cell. This was resolved as part of the efficient-multi-cell-instance-list-and-sort spec.

### Notifications Â¶

With a multi-cell environment with multiple message queues, it is
likely that operators will want to configure a separate connection to
a unified queue for notifications. This can be done in the configuration file
of all nodes. Refer to the oslo.messaging configuration
documentation for more
details.

### Nova Metadata API service Â¶

Starting from the 19.0.0 (Stein) release, the nova metadata API service can be run either globally or per cell using the api.local_metadata_per_cell configuration option.

Global

If you have networks that span cells, you might need to run Nova metadata API
globally by setting api.local_metadata_per_cell to false . When running globally, it should be configured as an API-level
service with access to the api_database.connection information.

Local per cell

Running Nova metadata API per cell can have better performance and data
isolation in a multi-cell deployment. If your networks are segmented along
cell boundaries, then you can run Nova metadata API service per cell by setting api.local_metadata_per_cell to true . If you choose to
run it per cell, you should also configure each neutron-metadata-agent service to
point to the hostname/IP address of the corresponding Compute Metadata API.

### Console proxies Â¶

Starting from the 18.0.0 (Rocky) release, console proxies must be run per cell
because console token authorizations are stored in cell databases. This means
that each console proxy server must have access to the database.connection information for the cell database
containing the instances for which it is proxying console access. This
functionality was added as part of the convert-consoles-to-objects spec.

### Operations requiring upcalls Â¶

If you deploy multiple cells with a superconductor as described above,
computes and cell-based conductors will not have the ability to speak
to the scheduler as they are not connected to the same MQ. This is by
design for isolation, but currently the processes are not in place to
implement some features without such connectivity. Thus, anything that
requires a so-called âupcallâ will not function. This impacts the
following:

- Instance reschedules during boot and resize (part 1) Note This has been resolved in the Queens release .

Instance reschedules during boot and resize (part 1)

Note

This has been resolved in the Queens release .

- Instance affinity reporting from the compute nodes to scheduler

Instance affinity reporting from the compute nodes to scheduler

- The late anti-affinity check during server create and evacuate

The late anti-affinity check during server create and evacuate

- Querying host aggregates from the cell Note This has been resolved in the Rocky release .

Querying host aggregates from the cell

Note

This has been resolved in the Rocky release .

- Attaching a volume and [cinder] cross_az_attach = False

Attaching a volume and [cinder] cross_az_attach = False

- Instance reschedules during boot and resize (part 2) Note This has been resolved in the Ussuri release .

Instance reschedules during boot and resize (part 2)

Note

This has been resolved in the Ussuri release .

The first is simple: if you boot an instance, it gets scheduled to a
compute node, fails, it would normally be re-scheduled to another
node. That requires scheduler intervention and thus it will not work
in Pike with a multi-cell layout. If you do not rely on reschedules
for covering up transient compute-node failures, then this will not
affect you. To ensure you do not make futile attempts at rescheduling,
you should set scheduler.max_attempts to 1 in nova.conf .

The second two are related. The summary is that some of the facilities
that Nova has for ensuring that affinity/anti-affinity is preserved
between instances does not function in Pike with a multi-cell
layout. If you donât use affinity operations, then this will not
affect you. To make sure you donât make futile attempts at the
affinity check, you should set workarounds.disable_group_policy_check_upcall to True and filter_scheduler.track_instance_changes to False in nova.conf .

The fourth was previously only a problem when performing live migrations using
the since-removed XenAPI driver and not specifying --block-migrate . The
driver would attempt to figure out if block migration should be performed based
on source and destination hosts being in the same aggregate. Since aggregates
data had migrated to the API database, the cell conductor would not be able to
access the aggregate information and would fail.

The fifth is a problem because when a volume is attached to an instance
in the nova-compute service, and [cinder]/cross_az_attach=False in
nova.conf, we attempt to look up the availability zone that the instance is
in which includes getting any host aggregates that the instance.host is in.
Since the aggregates are in the API database and the cell conductor cannot
access that information, so this will fail. In the future this check could be
moved to the nova-api service such that the availability zone between the
instance and the volume is checked before we reach the cell, except in the
case of boot from volume where the nova-compute service itself creates the volume and must tell Cinder in which availability
zone to create the volume. Long-term, volume creation during boot from volume
should be moved to the top-level superconductor which would eliminate this AZ
up-call check problem.

The sixth is detailed in bug 1781286 and is similar to the first issue.
The issue is that servers created without a specific availability zone
will have their AZ calculated during a reschedule based on the alternate host
selected. Determining the AZ for the alternate host requires an âup callâ to
the API DB.

## Handling cell failures Â¶

For an explanation on how nova-api handles cell failures please see the Handling Down Cells section of the Compute API guide. Below, you can find
some recommended practices and considerations for effectively tolerating cell
failure situations.

### Configuration considerations Â¶

Since a cell being reachable or not is determined through timeouts, it is suggested
to provide suitable values for the following settings based on your requirements.

- database.max_retries is 10 by default meaning every time
a cell becomes unreachable, it would retry 10 times before nova can declare the
cell as a âdownâ cell.

database.max_retries is 10 by default meaning every time
a cell becomes unreachable, it would retry 10 times before nova can declare the
cell as a âdownâ cell.

- database.retry_interval is 10 seconds and oslo_messaging_rabbit.rabbit_retry_interval is 1 second by
default meaning every time a cell becomes unreachable it would retry every 10
seconds or 1 second depending on if itâs a database or a message queue problem.

database.retry_interval is 10 seconds and oslo_messaging_rabbit.rabbit_retry_interval is 1 second by
default meaning every time a cell becomes unreachable it would retry every 10
seconds or 1 second depending on if itâs a database or a message queue problem.

- Nova also has a timeout value called CELL_TIMEOUT which is hardcoded to 60
seconds and that is the total time the nova-api would wait before returning
partial results for the âdownâ cells.

Nova also has a timeout value called CELL_TIMEOUT which is hardcoded to 60
seconds and that is the total time the nova-api would wait before returning
partial results for the âdownâ cells.

The values of the above settings will affect the time required for nova to decide
if a cell is unreachable and then take the necessary actions like returning
partial results.

The operator can also control the results of certain actions like listing
servers and services depending on the value of the api.list_records_by_skipping_down_cells config option.
If this is true, the results from the unreachable cells will be skipped
and if it is false, the request will just fail with an API error in situations where
partial constructs cannot be computed.

### Disabling down cells Â¶

While the temporary outage in the infrastructure is being fixed, the affected
cells can be disabled so that they are removed from being scheduling candidates.
To enable or disable a cell, use nova-manage cell_v2 update_cell
--cell_uuid <cell_uuid> --disable . See the Cells v2 Commands man page
for details on command usage.

### Known issues Â¶

- Services and Performance: In case a cell is down during the startup of nova
services, there is the chance that the services hang because of not being able
to connect to all the cell databases that might be required for certain calculations
and initializations. An example scenario of this situation is if upgrade_levels.compute is set to auto then the nova-api service hangs on startup if there is at least one unreachable
cell. This is because it needs to connect to all the cells to gather
information on each of the compute serviceâs version to determine the compute
version cap to use. The current workaround is to pin the upgrade_levels.compute to a particular version like
ârockyâ and get the service up under such situations. See bug 1815697 for more details. Also note
that in general during situations where cells are not reachable certain
âslownessâ may be experienced in operations requiring hitting all the cells
because of the aforementioned configurable timeout/retry values.

Services and Performance: In case a cell is down during the startup of nova
services, there is the chance that the services hang because of not being able
to connect to all the cell databases that might be required for certain calculations
and initializations. An example scenario of this situation is if upgrade_levels.compute is set to auto then the nova-api service hangs on startup if there is at least one unreachable
cell. This is because it needs to connect to all the cells to gather
information on each of the compute serviceâs version to determine the compute
version cap to use. The current workaround is to pin the upgrade_levels.compute to a particular version like
ârockyâ and get the service up under such situations. See bug 1815697 for more details. Also note
that in general during situations where cells are not reachable certain
âslownessâ may be experienced in operations requiring hitting all the cells
because of the aforementioned configurable timeout/retry values.

- Counting Quotas: Another known issue is in the current approach of counting
quotas where we query each cell database to get the used resources and aggregate
them which makes it sensitive to temporary cell outages. While the cell is
unavailable, we cannot count resource usage residing in that cell database and
things would behave as though more quota is available than should be. That is,
if a tenant has used all of their quota and part of it is in cell A and cell A
goes offline temporarily, that tenant will suddenly be able to allocate more
resources than their limit (assuming cell A returns, the tenant will have more
resources allocated than their allowed quota). Note Starting in the Train (20.0.0) release, it is possible to
configure counting of quota usage from the placement service and
API database to make quota usage calculations resilient to down or
poor-performing cells in a multi-cell environment. See the quotas documentation for more details.

Counting Quotas: Another known issue is in the current approach of counting
quotas where we query each cell database to get the used resources and aggregate
them which makes it sensitive to temporary cell outages. While the cell is
unavailable, we cannot count resource usage residing in that cell database and
things would behave as though more quota is available than should be. That is,
if a tenant has used all of their quota and part of it is in cell A and cell A
goes offline temporarily, that tenant will suddenly be able to allocate more
resources than their limit (assuming cell A returns, the tenant will have more
resources allocated than their allowed quota).

Note

Starting in the Train (20.0.0) release, it is possible to
configure counting of quota usage from the placement service and
API database to make quota usage calculations resilient to down or
poor-performing cells in a multi-cell environment. See the quotas documentation for more details.

## FAQs Â¶

- How do I find out which hosts are bound to which cell? There are a couple of ways to do this. Run nova-manage cell_v2 discover_hosts --verbose . This does not produce a report but if you are trying to determine if a
host is in a cell you can run this and it will report any hosts that are
not yet mapped to a cell and map them. This command is idempotent. Run nova-manage cell_v2 list_hosts . This will list hosts in all cells. If you want to list hosts in a
specific cell, you can use the --cell_uuid option.

How do I find out which hosts are bound to which cell?

There are a couple of ways to do this.

- Run nova-manage cell_v2 discover_hosts --verbose . This does not produce a report but if you are trying to determine if a
host is in a cell you can run this and it will report any hosts that are
not yet mapped to a cell and map them. This command is idempotent.

Run nova-manage cell_v2 discover_hosts --verbose .

This does not produce a report but if you are trying to determine if a
host is in a cell you can run this and it will report any hosts that are
not yet mapped to a cell and map them. This command is idempotent.

- Run nova-manage cell_v2 list_hosts . This will list hosts in all cells. If you want to list hosts in a
specific cell, you can use the --cell_uuid option.

Run nova-manage cell_v2 list_hosts .

This will list hosts in all cells. If you want to list hosts in a
specific cell, you can use the --cell_uuid option.

- I updated the database_connection and/or transport_url in a cell
using the nova-manage cell_v2 update_cell command but the API is still
trying to use the old settings. The cell mappings are cached in the compute API service worker so you
will need to restart the worker process to rebuild the cache. Note that there
is another global cache tied to request contexts, which is used in the
nova-conductor and nova-scheduler services, so you might need to do the same
if you are having the same issue in those services. As of the 16.0.0 (Pike)
release there is no timer on the cache or hook to refresh the cache using a
SIGHUP to the service.

I updated the database_connection and/or transport_url in a cell
using the nova-manage cell_v2 update_cell command but the API is still
trying to use the old settings.

The cell mappings are cached in the compute API service worker so you
will need to restart the worker process to rebuild the cache. Note that there
is another global cache tied to request contexts, which is used in the
nova-conductor and nova-scheduler services, so you might need to do the same
if you are having the same issue in those services. As of the 16.0.0 (Pike)
release there is no timer on the cache or hook to refresh the cache using a
SIGHUP to the service.

- I have upgraded from Newton to Ocata and I can list instances but I get a
HTTP 404 (NotFound) error when I try to get details on a specific instance. Instances need to be mapped to cells so the API knows which cell an instance
lives in. When upgrading, the nova-manage cell_v2 simple_cell_setup command will automatically map the instances to the single cell which is
backed by the existing nova database. If you have already upgraded and did
not use the nova-manage cell_v2 simple_cell_setup command, you can run the nova-manage cell_v2 map_instances command with the --cell_uuid option to map all instances in the given cell. See the Cells v2 Commands man page for details on command usage.

I have upgraded from Newton to Ocata and I can list instances but I get a
HTTP 404 (NotFound) error when I try to get details on a specific instance.

Instances need to be mapped to cells so the API knows which cell an instance
lives in. When upgrading, the nova-manage cell_v2 simple_cell_setup command will automatically map the instances to the single cell which is
backed by the existing nova database. If you have already upgraded and did
not use the nova-manage cell_v2 simple_cell_setup command, you can run the nova-manage cell_v2 map_instances command with the --cell_uuid option to map all instances in the given cell. See the Cells v2 Commands man page for details on command usage.

- Can I create a cell but have it disabled from scheduling? Yes. It is possible to create a pre-disabled cell such that it does not
become a candidate for scheduling new VMs. This can be done by running the nova-manage cell_v2 create_cell command with the --disabled option.

Can I create a cell but have it disabled from scheduling?

Yes. It is possible to create a pre-disabled cell such that it does not
become a candidate for scheduling new VMs. This can be done by running the nova-manage cell_v2 create_cell command with the --disabled option.

- How can I disable a cell so that the new server create requests do not go to
it while I perform maintenance? Existing cells can be disabled by running nova-manage cell_v2
update_cell with the --disable option and can be re-enabled once the
maintenance period is over by running this command with the --enable option.

How can I disable a cell so that the new server create requests do not go to
it while I perform maintenance?

Existing cells can be disabled by running nova-manage cell_v2
update_cell with the --disable option and can be re-enabled once the
maintenance period is over by running this command with the --enable option.

- I disabled (or enabled) a cell using the nova-manage cell_v2
update_cell or I created a new (pre-disabled) cell(mapping) using the nova-manage cell_v2 create_cell command but the scheduler is still
using the old settings. The cell mappings are cached in the scheduler worker so you will either need
to restart the scheduler process to refresh the cache, or send a SIGHUP
signal to the scheduler by which it will automatically refresh the cells
cache and the changes will take effect.

I disabled (or enabled) a cell using the nova-manage cell_v2
update_cell or I created a new (pre-disabled) cell(mapping) using the nova-manage cell_v2 create_cell command but the scheduler is still
using the old settings.

The cell mappings are cached in the scheduler worker so you will either need
to restart the scheduler process to refresh the cache, or send a SIGHUP
signal to the scheduler by which it will automatically refresh the cells
cache and the changes will take effect.

- Why was the cells REST API not implemented for cells v2? Why are there no
CRUD operations for cells in the API? One of the deployment challenges that cells v1 had was the requirement for
the API and control services to be up before a new cell could be deployed.
This was not a problem for large-scale public clouds that never shut down,
but is not a reasonable requirement for smaller clouds that do offline
upgrades and/or clouds which could be taken completely offline by something
like a power outage. Initial devstack and gate testing for cells v1 was
delayed by the need to engineer a solution for bringing the services
partially online in order to deploy the rest, and this continues to be a gap
for other deployment tools. Consider also the FFU case where the control
plane needs to be down for a multi-release upgrade window where changes to
cell records have to be made. This would be quite a bit harder if the way
those changes are made is via the API, which must remain down during the
process. Further, there is a long-term goal to move cell configuration (i.e.
cell_mappings and the associated URLs and credentials) into config and get
away from the need to store and provision those things in the database.
Obviously a CRUD interface in the API would prevent us from making that move.

Why was the cells REST API not implemented for cells v2? Why are there no
CRUD operations for cells in the API?

One of the deployment challenges that cells v1 had was the requirement for
the API and control services to be up before a new cell could be deployed.
This was not a problem for large-scale public clouds that never shut down,
but is not a reasonable requirement for smaller clouds that do offline
upgrades and/or clouds which could be taken completely offline by something
like a power outage. Initial devstack and gate testing for cells v1 was
delayed by the need to engineer a solution for bringing the services
partially online in order to deploy the rest, and this continues to be a gap
for other deployment tools. Consider also the FFU case where the control
plane needs to be down for a multi-release upgrade window where changes to
cell records have to be made. This would be quite a bit harder if the way
those changes are made is via the API, which must remain down during the
process.

Further, there is a long-term goal to move cell configuration (i.e.
cell_mappings and the associated URLs and credentials) into config and get
away from the need to store and provision those things in the database.
Obviously a CRUD interface in the API would prevent us from making that move.

- Why are cells not exposed as a grouping mechanism in the API for listing
services, instances, and other resources? Early in the design of cells v2 we set a goal to not let the cell concept
leak out of the API, even for operators. Aggregates are the way nova supports
grouping of hosts for a variety of reasons, and aggregates can cut across
cells, and/or be aligned with them if desired. If we were to support cells as
another grouping mechanism, we would likely end up having to implement many
of the same features for them as aggregates, such as scheduler features,
metadata, and other searching/filtering operations. Since aggregates are how
Nova supports grouping, we expect operators to use aggregates any time they
need to refer to a cell as a group of hosts from the API, and leave actual
cells as a purely architectural detail. The need to filter instances by cell in the API can and should be solved by
adding a generic by-aggregate filter, which would allow listing instances on
hosts contained within any aggregate, including one that matches the cell
boundaries if so desired.

Why are cells not exposed as a grouping mechanism in the API for listing
services, instances, and other resources?

Early in the design of cells v2 we set a goal to not let the cell concept
leak out of the API, even for operators. Aggregates are the way nova supports
grouping of hosts for a variety of reasons, and aggregates can cut across
cells, and/or be aligned with them if desired. If we were to support cells as
another grouping mechanism, we would likely end up having to implement many
of the same features for them as aggregates, such as scheduler features,
metadata, and other searching/filtering operations. Since aggregates are how
Nova supports grouping, we expect operators to use aggregates any time they
need to refer to a cell as a group of hosts from the API, and leave actual
cells as a purely architectural detail.

The need to filter instances by cell in the API can and should be solved by
adding a generic by-aggregate filter, which would allow listing instances on
hosts contained within any aggregate, including one that matches the cell
boundaries if so desired.

- Why are the API responses for GET /servers , GET /servers/detail , GET /servers/{server_id} and GET /os-services missing some
information for certain cells at certain times? Why do I see the status as
âUNKNOWNâ for the servers in those cells at those times when I run openstack server list or openstack server show ? Starting from microversion 2.69 the API responses of GET /servers , GET /servers/detail , GET /servers/{server_id} and GET /os-services may
contain missing keys during down cell situations. See the Handling Down
Cells section of the Compute API guide for more information on the partial
constructs. For administrative considerations, see Handling cell failures .

Why are the API responses for GET /servers , GET /servers/detail , GET /servers/{server_id} and GET /os-services missing some
information for certain cells at certain times? Why do I see the status as
âUNKNOWNâ for the servers in those cells at those times when I run openstack server list or openstack server show ?

Starting from microversion 2.69 the API responses of GET /servers , GET /servers/detail , GET /servers/{server_id} and GET /os-services may
contain missing keys during down cell situations. See the Handling Down
Cells section of the Compute API guide for more information on the partial
constructs.

For administrative considerations, see Handling cell failures .

## References Â¶

A large number of cells v2-related presentations have been given at various
OpenStack and OpenInfra Summits over the years. These provide an excellent
reference on the history and development of the feature along with details from
real-world users of the feature.

- Newton Summit Video - Nova Cells V2: Whatâs Going On?

Newton Summit Video - Nova Cells V2: Whatâs Going On?

- Pike Summit Video - Scaling Nova: How CellsV2 Affects Your Deployment

Pike Summit Video - Scaling Nova: How CellsV2 Affects Your Deployment

- Queens Summit Video - Add Cellsv2 to your existing Nova deployment

Queens Summit Video - Add Cellsv2 to your existing Nova deployment

- Rocky Summit Video - Moving from CellsV1 to CellsV2 at CERN

Rocky Summit Video - Moving from CellsV1 to CellsV2 at CERN

- Stein Summit Video - Scaling Nova with CellsV2: The Nova Developer and the
CERN Operator perspective

Stein Summit Video - Scaling Nova with CellsV2: The Nova Developer and the
CERN Operator perspective

- Train Summit Video - Whatâs new in Nova Cellsv2?

Train Summit Video - Whatâs new in Nova Cellsv2?
