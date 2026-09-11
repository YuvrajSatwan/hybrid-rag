# Storage Policies Â¶

Storage Policies allow for some level of segmenting the cluster for various
purposes through the creation of multiple object rings. The Storage Policies
feature is implemented throughout the entire code base so it is an important
concept in understanding Swift architecture.

As described in The Rings , Swift uses modified hashing rings to
determine where data should reside in the cluster. There is a separate ring for
account databases, container databases, and there is also one object ring per
storage policy.  Each object ring behaves exactly the same way and is maintained
in the same manner, but with policies, different devices can belong to different
rings. By supporting multiple object rings, Swift allows the application and/or
deployer to essentially segregate the object storage within a single cluster.
There are many reasons why this might be desirable:

- Different levels of durability:  If a provider wants to offer, for example,
2x replication and 3x replication but doesnât want to maintain 2 separate
clusters, they would setup a 2x and a 3x replication policy and assign the
nodes to their respective rings. Furthermore, if a provider wanted to offer a
cold storage tier, they could create an erasure coded policy.

Different levels of durability:  If a provider wants to offer, for example,
2x replication and 3x replication but doesnât want to maintain 2 separate
clusters, they would setup a 2x and a 3x replication policy and assign the
nodes to their respective rings. Furthermore, if a provider wanted to offer a
cold storage tier, they could create an erasure coded policy.

- Performance:  Just as SSDs can be used as the exclusive members of an account
or database ring, an SSD-only object ring can be created as well and used to
implement a low-latency/high performance policy.

Performance:  Just as SSDs can be used as the exclusive members of an account
or database ring, an SSD-only object ring can be created as well and used to
implement a low-latency/high performance policy.

- Collecting nodes into group:  Different object rings may have different
physical servers so that objects in specific storage policies are always
placed in a particular data center or geography.

Collecting nodes into group:  Different object rings may have different
physical servers so that objects in specific storage policies are always
placed in a particular data center or geography.

- Different Storage implementations:  Another example would be to collect
together a set of nodes that use a different Diskfile (e.g., Kinetic,
GlusterFS) and use a policy to direct traffic just to those nodes.

Different Storage implementations:  Another example would be to collect
together a set of nodes that use a different Diskfile (e.g., Kinetic,
GlusterFS) and use a policy to direct traffic just to those nodes.

- Different read and write affinity settings: proxy-servers can be configured
to use different read and write affinity options for each policy. See Per policy configuration for more details.

Different read and write affinity settings: proxy-servers can be configured
to use different read and write affinity options for each policy. See Per policy configuration for more details.

Note

Today, Swift supports two different policy types: Replication and Erasure
Code. See Erasure Code Support for details.

Also note that Diskfile refers to backend object storage plug-in
architecture. See Pluggable On-Disk Back-end APIs for details.

## Containers and Policies Â¶

Policies are implemented at the container level.  There are many advantages to
this approach, not the least of which is how easy it makes life on
applications that want to take advantage of them.  It also ensures that
Storage Policies remain a core feature of Swift independent of the auth
implementation.  Policies were not implemented at the account/auth layer
because it would require changes to all auth systems in use by Swift
deployers.  Each container has a new special immutable metadata element called
the storage policy index.  Note that internally, Swift relies on policy
indexes and not policy names.  Policy names exist for human readability and
translation is managed in the proxy.  When a container is created, one new
optional header is supported to specify the policy name. If no name is
specified, the default policy is used (and if no other policies defined,
Policy-0 is considered the default).  We will be covering the difference
between default and Policy-0 in the next section.

Policies are assigned when a container is created.  Once a container has been
assigned a policy, it cannot be changed (unless it is deleted/recreated).  The
implications on data placement/movement for large datasets would make this a
task best left for applications to perform. Therefore, if a container has an
existing policy of, for example 3x replication, and one wanted to migrate that
data to an Erasure Code policy, the application would create another container
specifying the other policy parameters and then simply move the data from one
container to the other.  Policies apply on a per container basis allowing for
minimal application awareness; once a container has been created with a specific
policy, all objects stored in it will be done so in accordance with that policy.
If a container with a specific name is deleted (requires the container be empty)
a new container may be created with the same name without any restriction on
storage policy enforced by the deleted container which previously shared the
same name.

Containers have a many-to-one relationship with policies meaning that any number
of containers can share one policy.  There is no limit to how many containers
can use a specific policy.

The notion of associating a ring with a container introduces an interesting
scenario: What would happen if 2 containers of the same name were created with
different Storage Policies on either side of a network outage at the same time?
Furthermore, what would happen if objects were placed in those containers, a
whole bunch of them, and then later the network outage was restored?  Well,
without special care it would be a big problem as an application could end up
using the wrong ring to try and find an object.  Luckily there is a solution for
this problem, a daemon known as the Container Reconciler works tirelessly to
identify and rectify this potential scenario.

## Container Reconciler Â¶

Because atomicity of container creation cannot be enforced in a
distributed eventually consistent system, object writes into the wrong
storage policy must be eventually merged into the correct storage policy
by an asynchronous daemon.  Recovery from object writes during a network
partition which resulted in a split brain container created with
different storage policies are handled by the swift-container-reconciler daemon.

The container reconciler works off a queue similar to the
object-expirer.  The queue is populated during container-replication.
It is never considered incorrect to enqueue an object to be evaluated by
the container-reconciler because if there is nothing wrong with the location
of the object the reconciler will simply dequeue it.  The
container-reconciler queue is an indexed log for the real location of an
object for which a discrepancy in the storage policy of the container was
discovered.

To determine the correct storage policy of a container, it is necessary
to update the status_changed_at field in the container_stat table when a
container changes status from deleted to re-created.  This transaction
log allows the container-replicator to update the correct storage policy
both when replicating a container and handling REPLICATE requests.

Because each object write is a separate distributed transaction it is
not possible to determine the correctness of the storage policy for each
object write with respect to the entire transaction log at a given
container database.  As such, container databases will always record the
object write regardless of the storage policy on a per object row basis.
Object byte and count stats are tracked per storage policy in each
container and reconciled using normal object row merge semantics.

The object rows are ensured to be fully durable during replication using
the normal container replication.  After the container
replicator pushes its object rows to available primary nodes any
misplaced object rows are bulk loaded into containers based off the
object timestamp under the .misplaced_objects system account.  The
rows are initially written to a handoff container on the local node, and
at the end of the replication pass the .misplaced_objects containers are
replicated to the correct primary nodes.

The container-reconciler processes the .misplaced_objects containers in
descending order and reaps its containers as the objects represented by
the rows are successfully reconciled.  The container-reconciler will
always validate the correct storage policy for enqueued objects using
direct container HEAD requests which are accelerated via caching.

Because failure of individual storage nodes in aggregate is assumed to
be common at scale, the container-reconciler will make forward progress
with a simple quorum majority.  During a combination of failures and
rebalances it is possible that a quorum could provide an incomplete
record of the correct storage policy - so an object write may have to be
applied more than once.  Because storage nodes and container databases
will not process writes with an X-Timestamp less than or equal to
their existing record when objects writes are re-applied their timestamp
is slightly incremented.  In order for this increment to be applied
transparently to the client a second vector of time has been added to
Swift for internal use.  See Timestamp .

As the reconciler applies object writes to the correct storage policy it
cleans up writes which no longer apply to the incorrect storage policy
and removes the rows from the .misplaced_objects containers.  After all
rows have been successfully processed it sleeps and will periodically
check for newly enqueued rows to be discovered during container
replication.

## Default versus âPolicy-0â Â¶

Storage Policies is a versatile feature intended to support both new and
pre-existing clusters with the same level of flexibility.  For that reason, we
introduce the Policy-0 concept which is not the same as the âdefaultâ
policy.  As you will see when we begin to configure policies, each policy has
a single name and an arbitrary number of aliases (human friendly,
configurable) as well as an index (or simply policy number). Swift reserves
index 0 to map to the object ring thatâs present in all installations
(e.g., /etc/swift/object.ring.gz ). You can name this policy anything you
like, and if no policies are defined it will report itself as Policy-0 ,
however you cannot change the index as there must always be a policy with
index 0.

Another important concept is the default policy which can be any policy
in the cluster.  The default policy is the policy that is automatically
chosen when a container creation request is sent without a storage
policy being specified. Configuring Policies describes how to set the
default policy.  The difference from Policy-0 is subtle but
extremely important. Policy-0 is what is used by Swift when
accessing pre-storage-policy containers which wonât have a policy - in
this case we would not use the default as it might not have the same
policy as legacy containers.  When no other policies are defined, Swift
will always choose Policy-0 as the default.

In other words, default means âcreate using this policy if nothing else is
specifiedâ and Policy-0 means âuse the legacy policy if a container doesnât
have oneâ which really means use object.ring.gz for lookups.

Note

With the Storage Policy based code, itâs not possible to create a
container that doesnât have a policy.  If nothing is provided, Swift will
still select the default and assign it to the container.  For containers
created before Storage Policies were introduced, the legacy Policy-0 will
be used.

## Deprecating Policies Â¶

There will be times when a policy is no longer desired; however simply
deleting the policy and associated rings would be problematic for existing
data.  In order to ensure that resources are not orphaned in the cluster (left
on disk but no longer accessible) and to provide proper messaging to
applications when a policy needs to be retired, the notion of deprecation is
used. Configuring Policies describes how to deprecate a policy.

Swiftâs behavior with deprecated policies is as follows:

- The deprecated policy will not appear in /info

The deprecated policy will not appear in /info

- PUT/GET/DELETE/POST/HEAD are still allowed on the pre-existing containers
created with a deprecated policy

PUT/GET/DELETE/POST/HEAD are still allowed on the pre-existing containers
created with a deprecated policy

- Clients will get an ââ400 Bad Requestââ error when trying to create a new
container using the deprecated policy

Clients will get an ââ400 Bad Requestââ error when trying to create a new
container using the deprecated policy

- Clients still have access to policy statistics via HEAD on pre-existing
containers

Clients still have access to policy statistics via HEAD on pre-existing
containers

Note

A policy cannot be both the default and deprecated.  If you deprecate the
default policy, you must specify a new default.

You can also use the deprecated feature to rollout new policies.  If you
want to test a new storage policy before making it generally available
you could deprecate the policy when you initially roll it the new
configuration and rings to all nodes.  Being deprecated will render it
innate and unable to be used.  To test it you will need to create a
container with that storage policy; which will require a single proxy
instance (or a set of proxy-servers which are only internally
accessible) that has been one-off configured with the new policy NOT
marked deprecated.  Once the container has been created with the new
storage policy any client authorized to use that container will be able
to add and access data stored in that container in the new storage
policy.  When satisfied you can roll out a new swift.conf which does
not mark the policy as deprecated to all nodes.

## Configuring Policies Â¶

Note

See Adding Storage Policies to an Existing SAIO for a step by step guide on adding a policy to the
SAIO setup.

It is important that the deployer have a solid understanding of the semantics
for configuring policies.  Configuring a policy is a three-step process:

- Edit your /etc/swift/swift.conf file to define your new policy.

Edit your /etc/swift/swift.conf file to define your new policy.

- Create the corresponding policy object ring file.

Create the corresponding policy object ring file.

- (Optional) Create policy-specific proxy-server configuration settings.

(Optional) Create policy-specific proxy-server configuration settings.

### Defining a policy Â¶

Each policy is defined by a section in the /etc/swift/swift.conf file. The
section name must be of the form [storage-policy:<N>] where <N> is the
policy index. Thereâs no reason other than readability that policy indexes be
sequential but the following rules are enforced:

- If a policy with index 0 is not declared and no other policies are
defined, Swift will create a default policy with index 0 .

If a policy with index 0 is not declared and no other policies are
defined, Swift will create a default policy with index 0 .

- The policy index must be a non-negative integer.

The policy index must be a non-negative integer.

- Policy indexes must be unique.

Policy indexes must be unique.

Warning

The index of a policy should never be changed once a policy has been
created and used. Changing a policy index may cause loss of access to data.

Each policy section contains the following options:

- name = <policy_name> (required) The primary name of the policy. Policy names are case insensitive. Policy names must contain only letters, digits or a dash. Policy names must be unique. Policy names can be changed. The name Policy-0 can only be used for the policy with
index 0 . To avoid confusion with policy indexes it is strongly recommended that
policy names are not numbers (e.g. â1â). However, for backwards
compatibility, names that are numbers are supported.

- The primary name of the policy.

The primary name of the policy.

- Policy names are case insensitive.

Policy names are case insensitive.

- Policy names must contain only letters, digits or a dash.

Policy names must contain only letters, digits or a dash.

- Policy names must be unique.

Policy names must be unique.

- Policy names can be changed.

Policy names can be changed.

- The name Policy-0 can only be used for the policy with
index 0 .

The name Policy-0 can only be used for the policy with
index 0 .

- To avoid confusion with policy indexes it is strongly recommended that
policy names are not numbers (e.g. â1â). However, for backwards
compatibility, names that are numbers are supported.

To avoid confusion with policy indexes it is strongly recommended that
policy names are not numbers (e.g. â1â). However, for backwards
compatibility, names that are numbers are supported.

- aliases = <policy_name>[, <policy_name>, ...] (optional) A comma-separated list of alternative names for the policy. The default value is an empty list (i.e. no aliases). All alias names must follow the rules for the name option. Aliases can be added to and removed from the list. Aliases can be useful to retain support for old primary names if the
primary name is changed.

- A comma-separated list of alternative names for the policy.

A comma-separated list of alternative names for the policy.

- The default value is an empty list (i.e. no aliases).

The default value is an empty list (i.e. no aliases).

- All alias names must follow the rules for the name option.

All alias names must follow the rules for the name option.

- Aliases can be added to and removed from the list.

Aliases can be added to and removed from the list.

- Aliases can be useful to retain support for old primary names if the
primary name is changed.

Aliases can be useful to retain support for old primary names if the
primary name is changed.

- default = [true|false] (optional) If true then this policy will be used when the client does not
specify a policy. The default value is false . The default policy can be changed at any time, by setting default = true in the desired policy section. If no policy is declared as the default and no other policies are
defined, the policy with index 0 is set as the default; Otherwise, exactly one policy must be declared default. Deprecated policies cannot be declared the default. See Default versus âPolicy-0â for more information.

- If true then this policy will be used when the client does not
specify a policy.

If true then this policy will be used when the client does not
specify a policy.

- The default value is false .

The default value is false .

- The default policy can be changed at any time, by setting default = true in the desired policy section.

The default policy can be changed at any time, by setting default = true in the desired policy section.

- If no policy is declared as the default and no other policies are
defined, the policy with index 0 is set as the default;

If no policy is declared as the default and no other policies are
defined, the policy with index 0 is set as the default;

- Otherwise, exactly one policy must be declared default.

Otherwise, exactly one policy must be declared default.

- Deprecated policies cannot be declared the default.

Deprecated policies cannot be declared the default.

- See Default versus âPolicy-0â for more information.

See Default versus âPolicy-0â for more information.

- deprecated = [true|false] (optional) If true then new containers cannot be created using this policy. The default value is false . Any policy may be deprecated by adding the deprecated option to
the desired policy section. However, a deprecated policy may not also
be declared the default. Therefore, since there must always be a
default policy, there must also always be at least one policy which
is not deprecated. See Deprecating Policies for more information.

- If true then new containers cannot be created using this policy.

If true then new containers cannot be created using this policy.

- The default value is false .

The default value is false .

- Any policy may be deprecated by adding the deprecated option to
the desired policy section. However, a deprecated policy may not also
be declared the default. Therefore, since there must always be a
default policy, there must also always be at least one policy which
is not deprecated.

Any policy may be deprecated by adding the deprecated option to
the desired policy section. However, a deprecated policy may not also
be declared the default. Therefore, since there must always be a
default policy, there must also always be at least one policy which
is not deprecated.

- See Deprecating Policies for more information.

See Deprecating Policies for more information.

- policy_type = [replication|erasure_coding] (optional) The option policy_type is used to distinguish between different
policy types. The default value is replication . When defining an EC policy use the value erasure_coding .

- The option policy_type is used to distinguish between different
policy types.

The option policy_type is used to distinguish between different
policy types.

- The default value is replication .

The default value is replication .

- When defining an EC policy use the value erasure_coding .

When defining an EC policy use the value erasure_coding .

- diskfile_module = <entry point> (optional) The option diskfile_module is used to load an alternate backend
object storage plug-in architecture. The default value is egg:swift#replication.fs or egg:swift#erasure_coding.fs depending on the policy type. The scheme
and package name are optionals and default to egg and swift .

- The option diskfile_module is used to load an alternate backend
object storage plug-in architecture.

The option diskfile_module is used to load an alternate backend
object storage plug-in architecture.

- The default value is egg:swift#replication.fs or egg:swift#erasure_coding.fs depending on the policy type. The scheme
and package name are optionals and default to egg and swift .

The default value is egg:swift#replication.fs or egg:swift#erasure_coding.fs depending on the policy type. The scheme
and package name are optionals and default to egg and swift .

The EC policy type has additional required options. See Using an Erasure Code Policy for details.

The following is an example of a properly configured swift.conf file. See Adding Storage Policies to an Existing SAIO for full instructions on setting up an all-in-one with
this example configuration.:

[ swift - hash ] # random unique strings that can never change (DO NOT LOSE) # Use only printable chars (python -c "import string; print(string.printable)") swift_hash_path_prefix = changeme swift_hash_path_suffix = changeme [ storage - policy : 0 ] name = gold aliases = yellow , orange policy_type = replication default = yes [ storage - policy : 1 ] name = silver policy_type = replication diskfile_module = replication . fs deprecated = yes

### Creating a ring Â¶

Once swift.conf is configured for a new policy, a new ring must be created.
The ring tools are not policy name aware so itâs critical that the correct
policy index be used when creating the new policyâs ring file. Additional
object rings are created using swift-ring-builder in the same manner as the
legacy ring except that -N is appended after the word object in the
builder file name, where N matches the policy index used in swift.conf .
So, to create the ring for policy index 1 :

swift - ring - builder object - 1. builder create 10 3 1

Continue to use the same naming convention when using swift-ring-builder to
add devices, rebalance etc. This naming convention is also used in the pattern
for per-policy storage node data directories.

Note

The same drives can indeed be used for multiple policies and the details
of how thatâs managed on disk will be covered in a later section, itâs
important to understand the implications of such a configuration before
setting one up.  Make sure itâs really what you want to do, in many cases
it will be, but in others maybe not.

### Proxy server configuration (optional) Â¶

The Proxy Server configuration options related to read and write
affinity may optionally be overridden for individual storage policies. See Per policy configuration for more details.

## Using Policies Â¶

Using policies is very simple - a policy is only specified when a container is
initially created.  There are no other API changes.  Creating a container can
be done without any special policy information:

curl - v - X PUT - H 'X-Auth-Token: <your auth token>' \ http : // 127.0.0.1 : 8080 / v1 / AUTH_test / myCont0

Which will result in a container created that is associated with the
policy name âgoldâ assuming weâre using the swift.conf example from
above.  It would use âgoldâ because it was specified as the default.
Now, when we put an object into this container, it will get placed on
nodes that are part of the ring we created for policy âgoldâ.

If we wanted to explicitly state that we wanted policy âgoldâ the command
would simply need to include a new header as shown below:

curl - v - X PUT - H 'X-Auth-Token: <your auth token>' \ - H 'X-Storage-Policy: gold' http : // 127.0.0.1 : 8080 / v1 / AUTH_test / myCont0

And thatâs it!  The application does not need to specify the policy name ever
again.  There are some illegal operations however:

- If an invalid (typo, non-existent) policy is specified: 400 Bad Request

If an invalid (typo, non-existent) policy is specified: 400 Bad Request

- if you try to change the policy either via PUT or POST: 409 Conflict

if you try to change the policy either via PUT or POST: 409 Conflict

If youâd like to see how the storage in the cluster is being used, simply HEAD
the account and youâll see not only the cumulative numbers, as before, but
per policy statistics as well.  In the example below thereâs 3 objects total
with two of them in policy âgoldâ and one in policy âsilverâ:

curl - i - X HEAD - H 'X-Auth-Token: <your auth token>' \ http : // 127.0.0.1 : 8080 / v1 / AUTH_test

and your results will include (some output removed for readability):

X - Account - Container - Count : 3 X - Account - Object - Count : 3 X - Account - Bytes - Used : 21 X - Storage - Policy - Gold - Object - Count : 2 X - Storage - Policy - Gold - Bytes - Used : 14 X - Storage - Policy - Silver - Object - Count : 1 X - Storage - Policy - Silver - Bytes - Used : 7

## Under the Hood Â¶

Now that weâve explained a little about what Policies are and how to
configure/use them, letâs explore how Storage Policies fit in at the
nuts-n-bolts level.

### Parsing and Configuring Â¶

The module, Storage Policy , is responsible for parsing the swift.conf file, validating the input, and creating a global collection of
configured policies via class StoragePolicyCollection .  This
collection is made up of policies of class StoragePolicy . The
collection class includes handy functions for getting to a policy either by
name or by index , getting info about the policies, etc. Thereâs also one
very important function, get_object_ring() .
Object rings are members of the StoragePolicy class and are
actually not instantiated until the load_ring() method is called.  Any caller anywhere in the code base that needs to access
an object ring must use the POLICIES global singleton to access the get_object_ring() function and provide the
policy index which will call load_ring() if
needed; however, when starting request handling services such as the Proxy Server rings are proactively loaded to provide moderate
protection against a mis-configuration resulting in a run time error.  The
global is instantiated when Swift starts and provides a mechanism to patch
policies for the test code.

### Middleware Â¶

Middleware can take advantage of policies through the POLICIES global
and by importing get_container_info() to gain access to the policy index
associated with the container in question.  From the index it can then use the POLICIES singleton to grab the right ring.  For example, List Endpoints is policy aware using the means just described. Another
example is Recon which will report the md5 sums for all of the rings.

### Proxy Server Â¶

The Proxy Server moduleâs role in Storage Policies is essentially to make
sure the correct ring is used as its member element.  Before policies, the one
object ring would be instantiated when the Application class was
instantiated and could be overridden by test code via init parameter.  With
policies, however, there is no init parameter and the Application class instead depends on the POLICIES global singleton to retrieve the
ring which is instantiated the first time itâs needed.  So, instead of an object
ring member of the Application class, there is an accessor function, get_object_ring() , that gets the ring from POLICIES .

In general, when any module running on the proxy requires an object ring, it
does so via first getting the policy index from the cached container info.  The
exception is during container creation where it uses the policy name from the
request header to look up policy index from the POLICIES global.  Once
the proxy has determined the policy index, it can use the get_object_ring() method described earlier to gain access to
the correct ring.  It then has the responsibility of passing the index
information, not the policy name, on to the back-end servers via the header X -Backend-Storage-Policy-Index . Going the other way, the proxy also strips the
index out of headers that go back to clients, and makes sure they only see the
friendly policy names.

### On Disk Storage Â¶

Policies each have their own directories on the back-end servers and are
identified by their storage policy indexes.  Organizing the back-end directory
structures by policy index helps keep track of things and also allows for
sharing of disks between policies which may or may not make sense depending on
the needs of the provider.  More on this later, but for now be aware of the
following directory naming convention:

- /objects maps to objects associated with Policy-0

/objects maps to objects associated with Policy-0

- /objects-N maps to storage policy index #N

/objects-N maps to storage policy index #N

- /async_pending maps to async pending update for Policy-0

/async_pending maps to async pending update for Policy-0

- /async_pending-N maps to async pending update for storage policy index #N

/async_pending-N maps to async pending update for storage policy index #N

- /tmp maps to the DiskFile temporary directory for Policy-0

/tmp maps to the DiskFile temporary directory for Policy-0

- /tmp-N maps to the DiskFile temporary directory for policy index #N

/tmp-N maps to the DiskFile temporary directory for policy index #N

- /quarantined/objects maps to the quarantine directory for Policy-0

/quarantined/objects maps to the quarantine directory for Policy-0

- /quarantined/objects-N maps to the quarantine directory for policy index #N

/quarantined/objects-N maps to the quarantine directory for policy index #N

Note that these directory names are actually owned by the specific Diskfile
implementation, the names shown above are used by the default Diskfile.

### Object Server Â¶

The Object Server is not involved with selecting the storage policy
placement directly.  However, because of how back-end directory structures are
setup for policies, as described earlier, the object server modules do play a
role.  When the object server gets a Diskfile , it passes in the
policy index and leaves the actual directory naming/structure mechanisms to Diskfile .  By passing in the index, the instance of Diskfile being used will assure that data is properly located in the
tree based on its policy.

For the same reason, the Object Updater also is policy aware.  As
previously described, different policies use different async pending directories
so the updater needs to know how to scan them appropriately.

The Object Replicator is policy aware in that, depending on the policy,
it may have to do drastically different things, or maybe not.  For example, the
difference in handling a replication job for 2x versus 3x is trivial; however,
the difference in handling replication between 3x and erasure code is most
definitely not.  In fact, the term âreplicationâ really isnât appropriate for
some policies like erasure code; however, the majority of the framework for
collecting and processing jobs is common.  Thus, those functions in the
replicator are leveraged for all policies and then there is policy specific code
required for each policy, added when the policy is defined if needed.

The ssync functionality is policy aware for the same reason. Some of the
other modules may not obviously be affected, but the back-end directory
structure owned by Diskfile requires the policy index
parameter.  Therefore ssync being policy aware really means passing the
policy index along.  See ssync_sender and ssync_receiver for more information on ssync.

For Diskfile itself, being policy aware is all about managing the
back-end structure using the provided policy index.  In other words, callers who
get a Diskfile instance provide a policy index and Diskfile âs job is to keep data separated via this index (however it
chooses) such that policies can share the same media/nodes if desired.  The
included implementation of Diskfile lays out the directory structure
described earlier but thatâs owned within Diskfile ; external modules
have no visibility into that detail.  A common function is provided to map
various directory names and/or strings based on their policy index. For example Diskfile defines get_data_dir() which builds
off of a generic get_policy_string() to consistently build policy aware
strings for various usage.

### Container Server Â¶

The Container Server plays a very important role in Storage Policies, it
is responsible for handling the assignment of a policy to a container and the
prevention of bad things like changing policies or picking the wrong policy to
use when nothing is specified (recall earlier discussion on Policy-0 versus
default).

The Container Updater is policy aware, however its job is very simple, to
pass the policy index along to the Account Server via a request header.

The Container Backend is responsible for both altering existing DB
schema as well as assuring new DBs are created with a schema that supports
storage policies.  The âon-demandâ migration of container schemas allows Swift
to upgrade without downtime (sqliteâs alter statements are fast regardless of
row count).  To support rolling upgrades (and downgrades) the incompatible
schema changes to the container_stat table are made to a container_info table, and the container_stat table is replaced with a
view that includes an INSTEAD OF UPDATE trigger which makes it behave like
the old table.

The policy index is stored here for use in reporting information
about the container as well as managing split-brain scenario induced
discrepancies between containers and their storage policies.  Furthermore,
during split-brain, containers must be prepared to track object updates from
multiple policies so the object table also includes a storage_policy_index column.  Per-policy object counts and bytes are
updated in the policy_stat table using INSERT and DELETE triggers
similar to the pre-policy triggers that updated container_stat directly.

The Container Replicator daemon will pro-actively migrate legacy
schemas as part of its normal consistency checking process when it updates the reconciler_sync_point entry in the container_info table.  This ensures
that read heavy containers which do not encounter any writes will still get
migrated to be fully compatible with the post-storage-policy queries without
having to fall back and retry queries with the legacy schema to service
container read requests.

The Container Sync functionality only needs to be policy aware in
that it accesses the object rings.  Therefore, it needs to pull the policy index
out of the container information and use it to select the appropriate object
ring from the POLICIES global.

### Account Server Â¶

The Account Server âs role in Storage Policies is really limited to
reporting. When a HEAD request is made on an account (see example provided
earlier), the account server is provided with the storage policy index and
builds the object_count and byte_count information for the client on a
per policy basis.

The account servers are able to report per-storage-policy object and byte
counts because of some policy specific DB schema changes.  A policy specific
table, policy_stat , maintains information on a per policy basis (one row
per policy) in the same manner in which the account_stat table does.  The account_stat table still serves the same purpose and is not replaced by policy_stat , it holds the total account stats whereas policy_stat just
has the break downs.  The backend is also responsible for migrating
pre-storage-policy accounts by altering the DB schema and populating the policy_stat table for Policy-0 with current account_stat data at that
point in time.

The per-storage-policy object and byte counts are not updated with each object
PUT and DELETE request, instead container updates to the account server are
performed asynchronously by the swift-container-updater .

### Upgrading and Confirming Functionality Â¶

Upgrading to a version of Swift that has Storage Policy support is not
difficult, in fact, the cluster administrator isnât required to make any special
configuration changes to get going.  Swift will automatically begin using the
existing object ring as both the default ring and the Policy-0 ring.  Adding the
declaration of policy 0 is totally optional and in its absence, the name given
to the implicit policy 0 will be âPolicy-0â.  Letâs say for testing purposes
that you wanted to take an existing cluster that already has lots of data on it
and upgrade to Swift with Storage Policies. From there you want to go ahead and
create a policy and test a few things out.  All you need to do is:

- Upgrade all of your Swift nodes to a policy-aware version of Swift

Upgrade all of your Swift nodes to a policy-aware version of Swift

- Define your policies in /etc/swift/swift.conf

Define your policies in /etc/swift/swift.conf

- Create the corresponding object rings

Create the corresponding object rings

- Create containers and objects and confirm their placement is as expected

Create containers and objects and confirm their placement is as expected

For a specific example that takes you through these steps, please see Adding Storage Policies to an Existing SAIO

Note

If you downgrade from a Storage Policy enabled version of Swift to an
older version that doesnât support policies, you will not be able to
access any data stored in policies other than the policy with index 0 but
those objects WILL appear in container listings (possibly as duplicates if
there was a network partition and un-reconciled objects).  It is EXTREMELY
important that you perform any necessary integration testing on the
upgraded deployment before enabling an additional storage policy to ensure
a consistent API experience for your clients.  DO NOT downgrade to a
version of Swift that does not support storage policies once you expose
multiple storage policies.
