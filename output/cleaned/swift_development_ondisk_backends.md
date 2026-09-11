# Pluggable On-Disk Back-end APIs Â¶

The internal REST API used between the proxy server and the account, container
and object server is almost identical to public Swift REST API, but with a few
internal extensions (for example, update an account with a new container).

The pluggable back-end APIs for the three REST API servers (account,
container, object) abstracts the needs for servicing the various REST APIs
from the details of how data is laid out and stored on-disk.

The APIs are documented in the reference implementations for all three
servers. For historical reasons, the object server backend reference
implementation module is named diskfile , while the account and container
server backend reference implementation modules are named appropriately.

This API is still under development and not yet finalized.

## Back-end API for Account Server REST APIs Â¶

Pluggable Back-end for Account Server

Encapsulates working with an account database.

Create account_stat table which is specific to the account DB.
Not a part of Pluggable Back-ends, internal to the baseline code.

- conn â DB connection object

conn â DB connection object

- put_timestamp â put timestamp

put_timestamp â put timestamp

Create container table which is specific to the account DB.

conn â DB connection object

Create policy_stat table which is specific to the account DB.
Not a part of Pluggable Back-ends, internal to the baseline code.

conn â DB connection object

Check if the account DB is empty.

True if the database has no active containers.

Get global data for the account.

dict with keys: account, created_at, put_timestamp,
delete_timestamp, status_changed_at, container_count,
object_count, bytes_used, hash, id

Get global policy stats for the account.

do_migrations â boolean, if True the policy stat dicts will
always include the âcontainer_countâ key;
otherwise it may be omitted on legacy databases
until they are migrated.

dict of policy stats where the key is the policy index and
the value is a dictionary like {âobject_countâ: M,
âbytes_usedâ: N, âcontainer_countâ: L}

Only returns true if the status field is set to DELETED.

Get a list of containers sorted by name starting at marker onward, up
to limit entries. Entries will begin with the prefix and will not have
the delimiter after the prefix.

- limit â maximum number of entries to get

limit â maximum number of entries to get

- marker â marker query

marker â marker query

- end_marker â end marker query

end_marker â end marker query

- prefix â prefix query

prefix â prefix query

- delimiter â delimiter for query

delimiter â delimiter for query

- reverse â reverse the result order.

reverse â reverse the result order.

- allow_reserved â exclude names with reserved-byte by default

allow_reserved â exclude names with reserved-byte by default

list of tuples of (name, object_count, bytes_used,
put_timestamp, storage_policy_index, is_subdir)

Turn this db record dict into the format this service uses for
pending pickles.

Merge items into the container table.

- item_list â list of dictionaries of {ânameâ, âput_timestampâ,
âdelete_timestampâ, âobject_countâ, âbytes_usedâ,
âdeletedâ, âstorage_policy_indexâ}

item_list â list of dictionaries of {ânameâ, âput_timestampâ,
âdelete_timestampâ, âobject_countâ, âbytes_usedâ,
âdeletedâ, âstorage_policy_indexâ}

- source â if defined, update incoming_sync with the source

source â if defined, update incoming_sync with the source

Logical namespace path used for logging.

For AccountBroker we return just â<account>â.

Create a container with the given attributes.

- name â name of the container to create (a native string)

name â name of the container to create (a native string)

- put_timestamp â put_timestamp of the container to create

put_timestamp â put_timestamp of the container to create

- delete_timestamp â delete_timestamp of the container to create

delete_timestamp â delete_timestamp of the container to create

- object_count â number of objects in the container

object_count â number of objects in the container

- bytes_used â number of bytes used by the container

bytes_used â number of bytes used by the container

- storage_policy_index â the storage policy for this container

storage_policy_index â the storage policy for this container

## Back-end API for Container Server REST APIs Â¶

Pluggable Back-ends for Container Server

Encapsulates working with a container database.

Note that this may involve multiple on-disk DB files if the container
becomes sharded:

- _db_file is the path to the legacy container DB name, i.e. <hash>.db . This file should exist for an initialised broker that
has never been sharded, but will not exist once a container has been
sharded.

_db_file is the path to the legacy container DB name, i.e. <hash>.db . This file should exist for an initialised broker that
has never been sharded, but will not exist once a container has been
sharded.

- db_files is a list of existing db files for the broker. This
list should have at least one entry for an initialised broker, and
should have two entries while a broker is in SHARDING state.

db_files is a list of existing db files for the broker. This
list should have at least one entry for an initialised broker, and
should have two entries while a broker is in SHARDING state.

- db_file is the path to whichever db is currently authoritative
for the container. Depending on the containerâs state, this may not be
the same as the db_file argument given to __init__() , unless force_db_file is True in which case db_file is always equal
to the db_file argument given to __init__() .

db_file is the path to whichever db is currently authoritative
for the container. Depending on the containerâs state, this may not be
the same as the db_file argument given to __init__() , unless force_db_file is True in which case db_file is always equal
to the db_file argument given to __init__() .

- pending_file is always equal to _db_file extended with .pending , i.e. <hash>.db.pending .

pending_file is always equal to _db_file extended with .pending , i.e. <hash>.db.pending .

Create a ContainerBroker instance. If the db doesnât exist, initialize
the db file.

- device_path â device path

device_path â device path

- part â partition number

part â partition number

- account â account name string

account â account name string

- container â container name string

container â container name string

- logger â a logger instance

logger â a logger instance

- epoch â a timestamp to include in the db filename

epoch â a timestamp to include in the db filename

- put_timestamp â initial timestamp if broker needs to be
initialized

put_timestamp â initial timestamp if broker needs to be
initialized

- storage_policy_index â the storage policy index

storage_policy_index â the storage policy index

a tuple of ( broker , initialized ) where broker is
an instance of swift.container.backend.ContainerBroker and initialized is True if the db file was initialized, False
otherwise.

Create the container_info table which is specific to the container DB.
Not a part of Pluggable Back-ends, internal to the baseline code.
Also creates the container_stat view.

- conn â DB connection object

conn â DB connection object

- put_timestamp â put timestamp

put_timestamp â put timestamp

- storage_policy_index â storage policy index

storage_policy_index â storage policy index

Create the object table which is specific to the container DB.
Not a part of Pluggable Back-ends, internal to the baseline code.

conn â DB connection object

Create policy_stat table.

- conn â DB connection object

conn â DB connection object

- storage_policy_index â the policy_index the container is
being created with

storage_policy_index â the policy_index the container is
being created with

Create the shard_range table which is specific to the container DB.

conn â DB connection object

Get the path to the primary db file for this broker. This is typically
the db file for the most recent sharding epoch. However, if no db files
exist on disk, or if force_db_file was True when the broker was
constructed, then the primary db file is the file passed to the broker
constructor.

A path to a db file; the file does not necessarily exist.

Gets the cached list of valid db files that exist on disk for this
broker.

reload_db_files() .

A list of paths to db files ordered by ascending epoch;
the list may be empty.

Mark an object deleted.

- name â object name to be deleted

name â object name to be deleted

- timestamp â string representation of the timestamp when the
object was marked as deleted

timestamp â string representation of the timestamp when the
object was marked as deleted

- storage_policy_index â the storage policy index for the object

storage_policy_index â the storage policy index for the object

Check if container DB is empty.

This method uses more stringent checks on object count than is_deleted() : this method checks that there are no objects in any
policy; if the container is in the process of sharding then both fresh
and retiring databases are checked to be empty; if a root container has
shard ranges then they are checked to be empty.

True if the database has no active objects, False otherwise

Updates this brokerâs own shard range with the given epoch, sets its
state to SHARDING and persists it in the DB.

epoch â a Timestamp

the brokerâs updated own shard range.

Scans the container db for shard ranges. Scanning will start at the
upper bound of the any existing_ranges that are given, otherwise
at ShardRange.MIN . Scanning will stop when limit shard ranges
have been found or when no more shard ranges can be found. In the
latter case, the upper bound of the final shard range will be equal to
the upper bound of the container namespace.

This method does not modify the state of the db; callers are
responsible for persisting any shard range data in the db.

- shard_size â the size of each shard range

shard_size â the size of each shard range

- limit â the maximum number of shard points to be found; a
negative value (default) implies no limit.

limit â the maximum number of shard points to be found; a
negative value (default) implies no limit.

- existing_ranges â an optional list of existing ShardRanges; if
given, this list should be sorted in order of upper bounds; the
scan for new shard ranges will start at the upper bound of the last
existing ShardRange.

existing_ranges â an optional list of existing ShardRanges; if
given, this list should be sorted in order of upper bounds; the
scan for new shard ranges will start at the upper bound of the last
existing ShardRange.

- minimum_shard_size â Minimum size of the final shard range. If
this is greater than one then the final shard range may be extended
to more than shard_size in order to avoid a further shard range
with less minimum_shard_size rows.

minimum_shard_size â Minimum size of the final shard range. If
this is greater than one then the final shard range may be extended
to more than shard_size in order to avoid a further shard range
with less minimum_shard_size rows.

a tuple; the first value in the tuple is a list of
dicts each having keys {âindexâ, âlowerâ, âupperâ, âobject_countâ}
in order of ascending âupperâ; the second value in the tuple is a
boolean which is True if the last shard range has been found, False
otherwise.

Returns a list of all shard range data, including own shard range and
deleted shard ranges.

A list of dict representations of a ShardRange.

Return a list of brokers for component dbs. The list has two entries
while the db state is sharding: the first entry is a broker for the
retiring db with skip_commits set to True ; the second entry is
a broker for the fresh db  with skip_commits set to False . For
any other db state the list has one entry.

a list of ContainerBroker

Returns the current state of on disk db files.

Get global data for the container.

dict with keys: account, container, created_at,
put_timestamp, delete_timestamp, status, status_changed_at,
object_count, bytes_used, reported_put_timestamp,
reported_delete_timestamp, reported_object_count,
reported_bytes_used, hash, id, x_container_sync_point1,
x_container_sync_point2, and storage_policy_index,
db_state.

Get the is_deleted status and info for the container.

a tuple, in the form (info, is_deleted) info is a dict as
returned by get_info and is_deleted is a boolean.

Get a list of objects which are in a storage policy different
from the containerâs storage policy.

- start â last reconciler sync point

start â last reconciler sync point

- count â maximum number of entries to get

count â maximum number of entries to get

list of dicts with keys: name, created_at, size,
content_type, etag, storage_policy_index

Returns a list of persisted namespaces per input parameters.

- marker â restricts the returned list to shard ranges whose
namespace includes or is greater than the marker value. If reverse=True then marker is treated as end_marker . marker is ignored if includes is specified.

marker â restricts the returned list to shard ranges whose
namespace includes or is greater than the marker value. If reverse=True then marker is treated as end_marker . marker is ignored if includes is specified.

- end_marker â restricts the returned list to shard ranges whose
namespace includes or is less than the end_marker value. If reverse=True then end_marker is treated as marker . end_marker is ignored if includes is specified.

end_marker â restricts the returned list to shard ranges whose
namespace includes or is less than the end_marker value. If reverse=True then end_marker is treated as marker . end_marker is ignored if includes is specified.

- includes â restricts the returned list to the shard range that
includes the given value; if includes is specified then fill_gaps , marker and end_marker are ignored.

includes â restricts the returned list to the shard range that
includes the given value; if includes is specified then fill_gaps , marker and end_marker are ignored.

- reverse â reverse the result order.

reverse â reverse the result order.

- states â if specified, restricts the returned list to namespaces
that have one of the given states; should be a list of ints.

states â if specified, restricts the returned list to namespaces
that have one of the given states; should be a list of ints.

- fill_gaps â if True, insert a modified copy of own shard range to
fill any gap between the end of any found shard ranges and the
upper bound of own shard range. Gaps enclosed within the found
shard ranges are not filled.

fill_gaps â if True, insert a modified copy of own shard range to
fill any gap between the end of any found shard ranges and the
upper bound of own shard range. Gaps enclosed within the found
shard ranges are not filled.

a list of Namespace objects.

Returns a list of objects, including deleted objects, in all policies.
Each object in the list is described by a dict with keys {ânameâ,
âcreated_atâ, âsizeâ, âcontent_typeâ, âetagâ, âdeletedâ,
âstorage_policy_indexâ}.

- limit â maximum number of entries to get

limit â maximum number of entries to get

- marker â if set, objects with names less than or equal to this
value will not be included in the list.

marker â if set, objects with names less than or equal to this
value will not be included in the list.

- end_marker â if set, objects with names greater than or equal to
this value will not be included in the list.

end_marker â if set, objects with names greater than or equal to
this value will not be included in the list.

- include_deleted â if True, include only deleted objects; if
False, include only undeleted objects; otherwise (default), include
both deleted and undeleted objects.

include_deleted â if True, include only deleted objects; if
False, include only undeleted objects; otherwise (default), include
both deleted and undeleted objects.

- since_row â include only items whose ROWID is greater than
the given row id; by default all rows are included.

since_row â include only items whose ROWID is greater than
the given row id; by default all rows are included.

a list of dicts, each describing an object.

Returns a shard range representing this brokerâs own shard range. If no
such range has been persisted in the brokerâs shard ranges table then a
default shard range representing the entire namespace will be returned.

The object_count and bytes_used of the returned shard range are
not guaranteed to be up-to-date with the current object stats for this
broker. Callers that require up-to-date stats should use the get_info method.

no_default â if True and the brokerâs own shard range is not
found in the shard ranges table then None is returned, otherwise a
default shard range is returned.

an instance of ShardRange

Get information about the DB required for replication.

dict containing keys from get_info plus max_row and metadata

âcountâ and metadata is the raw string.

Returns a list of persisted shard ranges.

- marker â restricts the returned list to shard ranges whose
namespace includes or is greater than the marker value. If reverse=True then marker is treated as end_marker . marker is ignored if includes is specified.

marker â restricts the returned list to shard ranges whose
namespace includes or is greater than the marker value. If reverse=True then marker is treated as end_marker . marker is ignored if includes is specified.

- end_marker â restricts the returned list to shard ranges whose
namespace includes or is less than the end_marker value. If reverse=True then end_marker is treated as marker . end_marker is ignored if includes is specified.

end_marker â restricts the returned list to shard ranges whose
namespace includes or is less than the end_marker value. If reverse=True then end_marker is treated as marker . end_marker is ignored if includes is specified.

- includes â restricts the returned list to the shard range that
includes the given value; if includes is specified then fill_gaps , marker and end_marker are ignored, but other
constraints are applied (e.g. exclude_others and include_deleted ).

includes â restricts the returned list to the shard range that
includes the given value; if includes is specified then fill_gaps , marker and end_marker are ignored, but other
constraints are applied (e.g. exclude_others and include_deleted ).

- reverse â reverse the result order.

reverse â reverse the result order.

- include_deleted â include items that have the delete marker set.

include_deleted â include items that have the delete marker set.

- states â if specified, restricts the returned list to shard
ranges that have one of the given states; should be a list of ints.

states â if specified, restricts the returned list to shard
ranges that have one of the given states; should be a list of ints.

- include_own â boolean that governs whether the row whose name
matches the brokerâs path is included in the returned list. If
True, that row is included unless it is excluded by other
constraints (e.g. marker , end_marker , includes ). If
False, that row is not included. Default is False.

include_own â boolean that governs whether the row whose name
matches the brokerâs path is included in the returned list. If
True, that row is included unless it is excluded by other
constraints (e.g. marker , end_marker , includes ). If
False, that row is not included. Default is False.

- exclude_others â boolean that governs whether the rows whose
names do not match the brokerâs path are included in the returned
list. If True, those rows are not included, otherwise they are
included. Default is False.

exclude_others â boolean that governs whether the rows whose
names do not match the brokerâs path are included in the returned
list. If True, those rows are not included, otherwise they are
included. Default is False.

- fill_gaps â if True, insert a modified copy of own shard range to
fill any gap between the end of any found shard ranges and the
upper bound of own shard range. Gaps enclosed within the found
shard ranges are not filled. fill_gaps is ignored if includes is specified.

fill_gaps â if True, insert a modified copy of own shard range to
fill any gap between the end of any found shard ranges and the
upper bound of own shard range. Gaps enclosed within the found
shard ranges are not filled. fill_gaps is ignored if includes is specified.

a list of instances of swift.common.utils.ShardRange .

Get the aggregate object stats for all shard ranges in states ACTIVE,
SHARDING or SHRINKING.

a dict with keys {bytes_used, object_count}

Returns sharding specific info from the brokerâs metadata.

key â if given the value stored under key in the sharding
info will be returned.

either a dict of sharding info or the value stored under key in that dict.

Returns sharding specific info from the brokerâs metadata with
timestamps.

key â if given the value stored under key in the sharding
info will be returned.

a dict of sharding info with their timestamps.

This function tells if there is any shard range other than the
brokerâs own shard range, that is not marked as deleted.

A boolean value as described above.

Check if the broker abstraction is empty, and has been marked deleted
for at least a reclaim age.

Returns True if this container is a root container, False otherwise.

A root container is a container that is not a shard of another
container.

Get a list of objects sorted by name starting at marker onward, up
to limit entries.  Entries will begin with the prefix and will not
have the delimiter after the prefix.

- limit â maximum number of entries to get

limit â maximum number of entries to get

- marker â marker query

marker â marker query

- end_marker â end marker query

end_marker â end marker query

- prefix â prefix query

prefix â prefix query

- delimiter â delimiter for query

delimiter â delimiter for query

- path â if defined, will set the prefix and delimiter based on
the path

path â if defined, will set the prefix and delimiter based on
the path

- storage_policy_index â storage policy index for query

storage_policy_index â storage policy index for query

- reverse â reverse the result order.

reverse â reverse the result order.

- include_deleted â if True, include only deleted objects; if
False (default), include only undeleted objects; otherwise, include
both deleted and undeleted objects.

include_deleted â if True, include only deleted objects; if
False (default), include only undeleted objects; otherwise, include
both deleted and undeleted objects.

- since_row â include only items whose ROWID is greater than
the given row id; by default all rows are included.

since_row â include only items whose ROWID is greater than
the given row id; by default all rows are included.

- transform_func â an optional function that if given will be
called for each object to get a transformed version of the object
to include in the listing; should have same signature as _transform_record() ; defaults to _transform_record() .

transform_func â an optional function that if given will be
called for each object to get a transformed version of the object
to include in the listing; should have same signature as _transform_record() ; defaults to _transform_record() .

- all_policies â if True, include objects for all storage policies
ignoring any value given for storage_policy_index

all_policies â if True, include objects for all storage policies
ignoring any value given for storage_policy_index

- allow_reserved â exclude names with reserved-byte by default

allow_reserved â exclude names with reserved-byte by default

list of tuples of (name, created_at, size, content_type,
etag, deleted)

Turn this db record dict into the format this service uses for
pending pickles.

Merge items into the object table.

- item_list â list of dictionaries of {ânameâ, âcreated_atâ,
âsizeâ, âcontent_typeâ, âetagâ, âdeletedâ,
âstorage_policy_indexâ, âctype_timestampâ,
âmeta_timestampâ}

item_list â list of dictionaries of {ânameâ, âcreated_atâ,
âsizeâ, âcontent_typeâ, âetagâ, âdeletedâ,
âstorage_policy_indexâ, âctype_timestampâ,
âmeta_timestampâ}

- source â if defined, update incoming_sync with the source

source â if defined, update incoming_sync with the source

Merge shard ranges into the shard range table.

shard_ranges â a shard range or a list of shard ranges; each
shard range should be an instance of ShardRange or a dict representation of
a shard range having SHARD_RANGE_KEYS .

Creates an object in the DB with its metadata.

- name â object name to be created

name â object name to be created

- timestamp â string representation of the timestamp when the
object was created

timestamp â string representation of the timestamp when the
object was created

- size â object size

size â object size

- content_type â object content-type

content_type â object content-type

- etag â object etag

etag â object etag

- deleted â if True, marks the object as deleted and sets the
deleted_at timestamp to timestamp

deleted â if True, marks the object as deleted and sets the
deleted_at timestamp to timestamp

- storage_policy_index â the storage policy index for the object

storage_policy_index â the storage policy index for the object

- ctype_timestamp â string representation of the timestamp when
content_type was last updated, or None

ctype_timestamp â string representation of the timestamp when
content_type was last updated, or None

- meta_timestamp â string representation of the timestamp when
metadata was last updated, or None

meta_timestamp â string representation of the timestamp when
metadata was last updated, or None

Reloads the cached list of valid on disk db files for this broker.

Removes object records in the given namespace range from the object
table.

Note that objects are removed regardless of their storage_policy_index.

- lower â defines the lower bound of object names that will be
removed; names greater than this value will be removed; names less
than or equal to this value will not be removed.

lower â defines the lower bound of object names that will be
removed; names greater than this value will be removed; names less
than or equal to this value will not be removed.

- upper â defines the upper bound of object names that will be
removed; names less than or equal to this value will be removed;
names greater than this value will not be removed. The empty string
is interpreted as there being no upper bound.

upper â defines the upper bound of object names that will be
removed; names less than or equal to this value will be removed;
names greater than this value will not be removed. The empty string
is interpreted as there being no upper bound.

- max_row â if specified only rows less than or equal to max_row
will be removed

max_row â if specified only rows less than or equal to max_row
will be removed

Update reported stats, available with containerâs get_info .

- put_timestamp â put_timestamp to update

put_timestamp â put_timestamp to update

- delete_timestamp â delete_timestamp to update

delete_timestamp â delete_timestamp to update

- object_count â object_count to update

object_count â object_count to update

- bytes_used â bytes_used to update

bytes_used â bytes_used to update

Given a list of values each of which may be the name of a state, the
number of a state, or an alias, return the set of state numbers
described by the list.

The following alias values are supported: âlistingâ maps to all states
that are considered valid when listing objects; âupdatingâ maps to all
states that are considered valid for redirecting an object update;
âauditingâ maps to all states that are considered valid for a shard
container that is updating its own shard range table from a root (this
currently maps to all states except FOUND).

states â a list of values each of which may be the name of a
state, the number of a state, or an alias

a set of integer state numbers, or None if no states are given

ValueError â if any value in the given list is neither a valid
state nor a valid alias

Unlinkâs the brokerâs retiring DB file.

True if the retiring DB was successfully unlinked, False
otherwise.

Creates and initializes a fresh DB file in preparation for sharding a
retiring DB. The brokerâs own shard range must have an epoch timestamp
for this method to succeed.

True if the fresh DB was successfully created, False
otherwise.

Updates the brokerâs metadata stored under the given key
prefixed with a sharding specific namespace.

- key â metadata key in the sharding metadata namespace.

key â metadata key in the sharding metadata namespace.

- value â metadata value

value â metadata value

Update the container_stat policy_index and status_changed_at.

Returns True if a broker has shard range state that would be necessary
for sharding to have been initiated, False otherwise.

Returns True if a broker has shard range state that would be necessary
for sharding to have been initiated but has not yet completed sharding,
False otherwise.

Compares shard_data with existing and updates shard_data with
any items of existing that take precedence over the corresponding item
in shard_data .

- shard_data â a dict representation of shard range that may be
modified by this method.

shard_data â a dict representation of shard range that may be
modified by this method.

- existing â a dict representation of shard range.

existing â a dict representation of shard range.

True if shard data has any item(s) that are considered to
take precedence over the corresponding item in existing

Compares new and existing shard ranges, updating the new shard ranges with
any more recent state from the existing, and returns shard ranges sorted
into those that need adding because they contain new or updated state and
those that need deleting because their state has been superseded.

- new_shard_ranges â a list of dicts, each of which represents a shard
range.

new_shard_ranges â a list of dicts, each of which represents a shard
range.

- existing_shard_ranges â a dict mapping shard range names to dicts
representing a shard range.

existing_shard_ranges â a dict mapping shard range names to dicts
representing a shard range.

a tuple (to_add, to_delete); to_add is a list of dicts, each of
which represents a shard range that is to be added to the existing
shard ranges; to_delete is a set of shard range names that are to be
deleted.

Compare the data and meta related timestamps of a new object item with
the timestamps of an existing object record, and update the new item
with data and/or meta related attributes from the existing record if
their timestamps are newer.

The multiple timestamps are encoded into a single string for storing
in the âcreated_atâ column of the objects db table.

- new_item â A dict of object update attributes

new_item â A dict of object update attributes

- existing â A dict of existing object attributes

existing â A dict of existing object attributes

True if any attributes of the new item dict were found to be
newer than the existing and therefore not updated, otherwise
False implying that the updated item is equal to the existing.

## Back-end API for Object Server REST APIs Â¶

Disk File Interface for the Swift Object Server

The DiskFile , DiskFileWriter and DiskFileReader classes combined define
the on-disk abstraction layer for supporting the object server REST API
interfaces (excluding REPLICATE ). Other implementations wishing to provide
an alternative backend for the object server must implement the three
classes. An example alternative implementation can be found in the mem_server.py and mem_diskfile.py modules along size this one.

The DiskFileManager is a reference implemenation specific class and is not
part of the backend API.

The remaining methods in this module are considered implementation specific and
are also not considered part of the backend API.

Represents an object location to be audited.

Other than being a bucket of data, the only useful thing this does is
stringify to a filesystem path so the auditorâs logs look okay.

Manage object files.

This specific implementation manages object files on a disk formatted with
a POSIX-compliant file system that supports extended attributes as
metadata on a file or directory.

Note

The arguments to the constructor are considered implementation
specific. The API does not define the constructor arguments.

The following path format is used for data file locations:
<devices_path/<device_dir>/<datadir>/<partdir>/<suffixdir>/<hashdir>/
<datafile>.<ext>

- mgr â associated DiskFileManager instance

mgr â associated DiskFileManager instance

- device_path â path to the target device or drive

device_path â path to the target device or drive

- partition â partition on the device in which the object lives

partition â partition on the device in which the object lives

- account â account name for the object

account â account name for the object

- container â container name for the object

container â container name for the object

- obj â object name for the object

obj â object name for the object

- _datadir â override the full datadir otherwise constructed here

_datadir â override the full datadir otherwise constructed here

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

- use_splice â if true, use zero-copy splice() to send data

use_splice â if true, use zero-copy splice() to send data

- pipe_size â size of pipe buffer used in zero-copy operations

pipe_size â size of pipe buffer used in zero-copy operations

- open_expired â if True, open() will not raise a DiskFileExpired if
object is expired

open_expired â if True, open() will not raise a DiskFileExpired if
object is expired

- next_part_power â the next partition power to be used

next_part_power â the next partition power to be used

Context manager to create a file. We create a temporary file first, and
then return a DiskFileWriter object to encapsulate the state.

Note

An implementation is not required to perform on-disk
preallocations even if the parameter is specified. But if it does
and it fails, it must raise a DiskFileNoSpace exception.

- size â optional initial size of file to explicitly allocate on
disk

size â optional initial size of file to explicitly allocate on
disk

- extension â file extension to use for the newly-created file;
defaults to .data for the sake of tests

extension â file extension to use for the newly-created file;
defaults to .data for the sake of tests

DiskFileNoSpace â if a size is specified and allocation fails

Delete the object.

This implementation creates a tombstone file using the given
timestamp, and removes any older versions of the object file. Any
file that has an older timestamp than timestamp will be deleted.

Note

An implementation is free to use or ignore the timestamp
parameter.

timestamp â timestamp to compare with each file

DiskFileError â this implementation will raise the same
errors as the create() method.

Provides the timestamp of the newest data file found in the object
directory.

A Timestamp instance, or None if no data file was found.

DiskFileNotOpen â if the open() method has not been previously
called on this instance.

Provide the datafile metadata for a previously opened object as a
dictionary. This is metadata that was included when the object was
first PUT, and does not include metadata set by any subsequent POST.

objectâs datafile metadata dictionary

DiskFileNotOpen â if the swift.obj.diskfile.DiskFile.open() method was not previously
invoked

Provide the metadata for a previously opened object as a dictionary.

objectâs metadata dictionary

DiskFileNotOpen â if the swift.obj.diskfile.DiskFile.open() method was not previously
invoked

Provide the metafile metadata for a previously opened object as a
dictionary. This is metadata that was written by a POST and does not
include any persistent metadata that was set by the original PUT.

objectâs .meta file metadata dictionary, or None if there is
no .meta file

DiskFileNotOpen â if the swift.obj.diskfile.DiskFile.open() method was not previously
invoked

Open the object.

This implementation opens the data file representing the object, reads
the associated metadata in the extended attributes, additionally
combining metadata from fast-POST .meta files.

- modernize â if set, update this diskfile to the latest format.
Currently, this means adding metadata checksums if none are
present.

modernize â if set, update this diskfile to the latest format.
Currently, this means adding metadata checksums if none are
present.

- current_time â Unix time used in checking expiration. If not
present, the current time will be used.

current_time â Unix time used in checking expiration. If not
present, the current time will be used.

Note

An implementation is allowed to raise any of the following
exceptions, but is only required to raise DiskFileNotExist when
the object representation does not exist.

- DiskFileCollision â on name mis-match with metadata

DiskFileCollision â on name mis-match with metadata

- DiskFileNotExist â if the object does not exist

DiskFileNotExist â if the object does not exist

- DiskFileDeleted â if the object was previously deleted

DiskFileDeleted â if the object was previously deleted

- DiskFileQuarantined â if while reading metadata of the file
some data did pass cross checks

DiskFileQuarantined â if while reading metadata of the file
some data did pass cross checks

itself for use as a context manager

Return the metadata for an object without requiring the caller to open
the object first.

current_time â Unix time used in checking expiration. If not
present, the current time will be used.

metadata dictionary for an object

DiskFileError â this implementation will raise the same
errors as the open() method.

Return a swift.common.swob.Response class compatible
â app_iter â object as defined by swift.obj.diskfile.DiskFileReader .

For this implementation, the responsibility of closing the open file
is passed to the swift.obj.diskfile.DiskFileReader object.

- keep_cache â callerâs preference for keeping data read in the
OS buffer cache

keep_cache â callerâs preference for keeping data read in the
OS buffer cache

- cooperative_period â the period parameter for cooperative
yielding during file read

cooperative_period â the period parameter for cooperative
yielding during file read

- etag_validate_frac â the probability that we should perform etag
validation during a complete file read

etag_validate_frac â the probability that we should perform etag
validation during a complete file read

- _quarantine_hook â 1-arg callable called when obj quarantined;
the arg is the reason for quarantine.
Default is to ignore it.
Not needed by the REST layer.

_quarantine_hook â 1-arg callable called when obj quarantined;
the arg is the reason for quarantine.
Default is to ignore it.
Not needed by the REST layer.

a swift.obj.diskfile.DiskFileReader object

Write a block of metadata to an object without requiring the caller to
create the object first. Supports fast-POST behavior semantics.

metadata â dictionary of metadata to be associated with the
object

DiskFileError â this implementation will raise the same
errors as the create() method.

Management class for devices, providing common place for shared parameters
and methods not provided by the DiskFile class (which primarily services
the object server REST API layer).

The get_diskfile() method is how this implementation creates a DiskFile object.

Note

This class is reference implementation specific and not part of the
pluggable on-disk backend API.

Note

TODO(portante): Not sure what the right name to recommend here, as
âmanagerâ seemed generic enough, though suggestions are welcome.

- conf â caller provided configuration object

conf â caller provided configuration object

- logger â caller provided logger

logger â caller provided logger

Clean up on-disk files that are obsolete and gather the set of valid
on-disk files for an object.

- hsh_path â object hash path

hsh_path â object hash path

- frag_index â if set, search for a specific fragment index .data
file, otherwise accept the first valid .data file

frag_index â if set, search for a specific fragment index .data
file, otherwise accept the first valid .data file

a dict that may contain: valid on disk files keyed by their
filename extension; a list of obsolete files stored under the
key âobsoleteâ; a list of files remaining in the directory,
reverse sorted, stored under the key âfilesâ.

Take whatâs in hashes.pkl and hashes.invalid, combine them, write the
result back to hashes.pkl, and clear out hashes.invalid.

partition_dir â absolute path to partition dir containing hashes.pkl
and hashes.invalid

a dict, the suffix hashes (if any), the key âvalidâ will be False
if hashes.pkl is corrupt, cannot be read or does not exist

Construct the path to a device without checking if it is mounted.

device â name of target device

full path to the device

Return the path to a device, first checking to see if either it
is a proper mount point, or at least a directory depending on
the mount_check configuration option.

- device â name of target device

device â name of target device

- mount_check â whether or not to check mountedness of device.
Defaults to bool(self.mount_check).

mount_check â whether or not to check mountedness of device.
Defaults to bool(self.mount_check).

full path to the device, None if the path to the device is
not a proper mount point or directory.

Returns a BaseDiskFile instance for an object based on the objectâs
partition, path parts and policy.

- device â name of target device

device â name of target device

- partition â partition on device in which the object lives

partition â partition on device in which the object lives

- account â account name for the object

account â account name for the object

- container â container name for the object

container â container name for the object

- obj â object name for the object

obj â object name for the object

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

Returns a tuple of (a DiskFile instance for an object at the given
object_hash, the basenames of the files in the objectâs hash dir).
Just in case someone thinks of refactoring, be sure DiskFileDeleted is not raised, but the DiskFile instance representing the tombstoned
object is returned instead.

- device â name of target device

device â name of target device

- partition â partition on the device in which the object lives

partition â partition on the device in which the object lives

- object_hash â the hash of an object path

object_hash â the hash of an object path

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

DiskFileNotExist â if the object does not exist

a tuple comprising (an instance of BaseDiskFile, a list of
file basenames)

Returns a BaseDiskFile instance for an object at the given
AuditLocation.

audit_location â object location to be audited

Returns a DiskFile instance for an object at the given object_hash.
Just in case someone thinks of refactoring, be sure DiskFileDeleted is not raised, but the DiskFile instance representing the tombstoned
object is returned instead.

- device â name of target device

device â name of target device

- partition â partition on the device in which the object lives

partition â partition on the device in which the object lives

- object_hash â the hash of an object path

object_hash â the hash of an object path

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

DiskFileNotExist â if the object does not exist

an instance of BaseDiskFile

- device â name of target device

device â name of target device

- partition â partition name

partition â partition name

- suffixes â a list of suffix directories to be recalculated

suffixes â a list of suffix directories to be recalculated

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

- skip_rehash â just mark the suffixes dirty; return None

skip_rehash â just mark the suffixes dirty; return None

a dictionary that maps suffix directories

Given a simple list of files names, determine the files that constitute
a valid fileset i.e. a set of files that defines the state of an
object, and determine the files that are obsolete and could be deleted.
Note that some files may fall into neither category.

If a file is considered part of a valid fileset then its info dict will
be added to the results dict, keyed by <extension>_info. Any files that
are no longer required will have their info dicts added to a list
stored under the key âobsoleteâ.

The results dict will always contain entries with keys âts_fileâ,
âdata_fileâ and âmeta_fileâ. Their values will be the fully qualified
path to a file of the corresponding type if there is such a file in the
valid fileset, or None.

- files â a list of file names.

files â a list of file names.

- datadir â directory name files are from; this is used to
construct file paths in the results, but the datadir is
not modified by this method.

datadir â directory name files are from; this is used to
construct file paths in the results, but the datadir is
not modified by this method.

- verify â if True verify that the ondisk file contract has not
been violated, otherwise do not verify.

verify â if True verify that the ondisk file contract has not
been violated, otherwise do not verify.

- policy â storage policy used to store the files. Used to
validate fragment indexes for EC policies.

policy â storage policy used to store the files. Used to
validate fragment indexes for EC policies.

a dict that will contain keys: ts_file   -> path to a .ts file or None
data_file -> path to a .data file or None
meta_file -> path to a .meta file or None
ctype_file -> path to a .meta file or None and may contain keys: ts_info   -> a file info dict for a .ts file
data_info -> a file info dict for a .data file
meta_info -> a file info dict for a .meta file
ctype_info -> a file info dict for a .meta file which
contains the content-type value
unexpected -> a list of file paths for unexpected
files
possible_reclaim -> a list of file info dicts for possible
reclaimable files
obsolete  -> a list of file info dicts for obsolete files

ts_file   -> path to a .ts file or None
data_file -> path to a .data file or None
meta_file -> path to a .meta file or None
ctype_file -> path to a .meta file or None

ts_info   -> a file info dict for a .ts file
data_info -> a file info dict for a .data file
meta_info -> a file info dict for a .meta file
ctype_info -> a file info dict for a .meta file which
contains the content-type value
unexpected -> a list of file paths for unexpected
files
possible_reclaim -> a list of file info dicts for possible
reclaimable files
obsolete  -> a list of file info dicts for obsolete files

Invalidates the hash for a suffix_dir in the partitionâs hashes file.

suffix_dir â absolute path to suffix dir whose hash needs
invalidating

Returns filename for given timestamp.

- timestamp â the object timestamp, an instance of Timestamp

timestamp â the object timestamp, an instance of Timestamp

- ext â an optional string representing a file extension to be
appended to the returned file name

ext â an optional string representing a file extension to be
appended to the returned file name

- ctype_timestamp â an optional content-type timestamp, an instance
of Timestamp

ctype_timestamp â an optional content-type timestamp, an instance
of Timestamp

a file name

Yield an AuditLocation for all objects stored under device_dirs.

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

- device_dirs â directory of target device

device_dirs â directory of target device

- auditor_type â either ALL or ZBF

auditor_type â either ALL or ZBF

Parse an on disk file name.

- filename â the file name including extension

filename â the file name including extension

- policy â storage policy used to store the file

policy â storage policy used to store the file

a dict, with keys for timestamp, ext and ctype_timestamp: timestamp is a Timestamp ctype_timestamp is a Timestamp or
None for .meta files, otherwise None ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension. Subclasses may override this method to add further keys to the
returned dict.

a dict, with keys for timestamp, ext and ctype_timestamp:

- timestamp is a Timestamp

timestamp is a Timestamp

- ctype_timestamp is a Timestamp or
None for .meta files, otherwise None

ctype_timestamp is a Timestamp or
None for .meta files, otherwise None

- ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension.

ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension.

Subclasses may override this method to add further keys to the
returned dict.

DiskFileError â if any part of the filename is not able to be
validated.

A context manager that will lock on the partition given.

- device â device targeted by the lock request

device â device targeted by the lock request

- policy â policy targeted by the lock request

policy â policy targeted by the lock request

- partition â partition targeted by the lock request

partition â partition targeted by the lock request

PartitionLockTimeout â If the lock on the partition
cannot be granted within the configured timeout.

Write data describing a container update notification to a pickle file
in the async_pending directory.

- device â name of target device

device â name of target device

- account â account name for the object

account â account name for the object

- container â container name for the object

container â container name for the object

- obj â object name for the object

obj â object name for the object

- data â update data to be written to pickle file

data â update data to be written to pickle file

- timestamp â a Timestamp

timestamp â a Timestamp

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

In the case that a file is corrupted, move it to a quarantined
area to allow replication to fix it.

The path to the device the corrupted file is on.

The path to the file you want quarantined.

path (str) of directory the file was moved to

OSError â re-raises non errno.EEXIST / errno.ENOTEMPTY
exceptions from rename

A context manager that will lock on the partition and, if configured
to do so, on the device given.

- device â name of target device

device â name of target device

- policy â policy targeted by the replication request

policy â policy targeted by the replication request

- partition â partition targeted by the replication request

partition â partition targeted by the replication request

ReplicationLockTimeout â If the lock on the device
cannot be granted within the configured timeout.

Yields tuples of (hash_only, timestamps) for object
information stored for the given device, partition, and
(optionally) suffixes. If suffixes is None, all stored
suffixes will be searched for object hashes. Note that if
suffixes is not None but empty, such as [], then nothing will
be yielded.

timestamps is a dict which may contain items mapping:

- ts_data -> timestamp of data or tombstone file,

ts_data -> timestamp of data or tombstone file,

- ts_meta -> timestamp of meta file, if one exists

ts_meta -> timestamp of meta file, if one exists

- ts_ctype -> timestamp of meta file containing most recent content-type value, if one exists

content-type value, if one exists

- durable -> True if data file at ts_data is durable, False otherwise

durable -> True if data file at ts_data is durable, False otherwise

where timestamps are instances of Timestamp

- device â name of target device

device â name of target device

- partition â partition name

partition â partition name

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

- suffixes â optional list of suffix directories to be searched

suffixes â optional list of suffix directories to be searched

Yields tuples of (full_path, suffix_only) for suffixes stored
on the given device and partition.

- device â name of target device

device â name of target device

- partition â partition name

partition â partition name

- policy â the StoragePolicy instance

policy â the StoragePolicy instance

Encapsulation of the WSGI read context for servicing GET REST API
requests. Serves as the context manager object for the swift.obj.diskfile.DiskFile classâs swift.obj.diskfile.DiskFile.reader() method.

Note

The quarantining behavior of this method is considered implementation
specific, and is not required of the API.

Note

The arguments to the constructor are considered implementation
specific. The API does not define the constructor arguments.

- fp â open file object pointer reference

fp â open file object pointer reference

- data_file â on-disk data file name for the object

data_file â on-disk data file name for the object

- obj_size â verified on-disk size of the object

obj_size â verified on-disk size of the object

- etag â expected metadata etag value for entire file

etag â expected metadata etag value for entire file

- disk_chunk_size â size of reads from disk in bytes

disk_chunk_size â size of reads from disk in bytes

- keep_cache_size â maximum object size that will be kept in cache

keep_cache_size â maximum object size that will be kept in cache

- device_path â on-disk device path, used when quarantining an obj

device_path â on-disk device path, used when quarantining an obj

- logger â logger caller wants this object to use

logger â logger caller wants this object to use

- quarantine_hook â 1-arg callable called w/reason when quarantined

quarantine_hook â 1-arg callable called w/reason when quarantined

- use_splice â if true, use zero-copy splice() to send data

use_splice â if true, use zero-copy splice() to send data

- pipe_size â size of pipe buffer used in zero-copy operations

pipe_size â size of pipe buffer used in zero-copy operations

- diskfile â the diskfile creating this DiskFileReader instance

diskfile â the diskfile creating this DiskFileReader instance

- keep_cache â should resulting reads be kept in the buffer cache

keep_cache â should resulting reads be kept in the buffer cache

- cooperative_period â the period parameter when does cooperative
yielding during file read

cooperative_period â the period parameter when does cooperative
yielding during file read

- etag_validate_frac â the probability that we should perform etag
validation during a complete file read

etag_validate_frac â the probability that we should perform etag
validation during a complete file read

Returns an iterator over the data file for range (start, stop)

Returns an iterator over the data file for a set of ranges

Close the open file handle if present.

For this specific implementation, this method will handle quarantining
the file if necessary.

Does some magic with splice() and tee() to move stuff from disk to
network without ever touching userspace.

wsockfd â file descriptor (integer) of the socket out which to
send data

Encapsulation of the write context for servicing PUT REST API
requests. Serves as the context manager object for the swift.obj.diskfile.DiskFile classâs swift.obj.diskfile.DiskFile.create() method.

Note

It is the responsibility of the swift.obj.diskfile.DiskFile.create() method context manager to
close the open file descriptor.

Note

The arguments to the constructor are considered implementation
specific. The API does not define the constructor arguments.

- name â name of object from REST API

name â name of object from REST API

- datadir â on-disk directory object will end up in on swift.obj.diskfile.DiskFileWriter.put()

datadir â on-disk directory object will end up in on swift.obj.diskfile.DiskFileWriter.put()

- fd â open file descriptor of temporary file to receive data

fd â open file descriptor of temporary file to receive data

- tmppath â full path name of the opened file descriptor

tmppath â full path name of the opened file descriptor

- bytes_per_sync â number bytes written between sync calls

bytes_per_sync â number bytes written between sync calls

- diskfile â the diskfile creating this DiskFileWriter instance

diskfile â the diskfile creating this DiskFileWriter instance

- next_part_power â the next partition power to be used

next_part_power â the next partition power to be used

- extension â the file extension to be used; may be used internally
to distinguish between PUT/POST/DELETE operations

extension â the file extension to be used; may be used internally
to distinguish between PUT/POST/DELETE operations

Expose internal stats about written chunks.

a tuple, (upload_size, etag)

Perform any operations necessary to mark the object as durable. For
replication policy type this is a no-op.

timestamp â object put timestamp, an instance of Timestamp

Finalize writing the file on disk.

metadata â dictionary of metadata to be associated with the
object

Write a chunk of data to disk. All invocations of this method must
come before invoking the :func:

For this implementation, the data is written into a temporary file.

chunk â the chunk of data to write as a string object

alias of DiskFileReader

alias of DiskFileWriter

alias of DiskFile

Finalize writing the file on disk.

metadata â dictionary of metadata to be associated with the
object

Provides the timestamp of the newest durable file found in the object
directory.

A Timestamp instance, or None if no durable file was found.

DiskFileNotOpen â if the open() method has not been previously
called on this instance.

Provides information about all fragments that were found in the object
directory, including fragments without a matching durable file, and
including any fragment chosen to construct the opened diskfile.

A dict mapping <Timestamp instance> -> <list of frag indexes>,
or None if the diskfile has not been opened or no fragments
were found.

Remove a tombstone file matching the specified timestamp or
datafile matching the specified timestamp and fragment index
from the object directory.

This provides the EC reconstructor/ssync process with a way to
remove a tombstone or fragment from a handoff node after
reverting it to its primary node.

The hash will be invalidated, and if empty the hsh_path will
be removed immediately.

- timestamp â the object timestamp, an instance of Timestamp

timestamp â the object timestamp, an instance of Timestamp

- frag_index â fragment archive index, must be
a whole number or None.

frag_index â fragment archive index, must be
a whole number or None.

- nondurable_purge_delay â only remove a non-durable data file if
itâs been on disk longer than this many seconds.

nondurable_purge_delay â only remove a non-durable data file if
itâs been on disk longer than this many seconds.

- meta_timestamp â if not None then remove any meta file with this
timestamp

meta_timestamp â if not None then remove any meta file with this
timestamp

alias of ECDiskFileReader

alias of ECDiskFileWriter

alias of ECDiskFile

Returns the EC specific filename for given timestamp.

- timestamp â the object timestamp, an instance of Timestamp

timestamp â the object timestamp, an instance of Timestamp

- ext â an optional string representing a file extension to be
appended to the returned file name

ext â an optional string representing a file extension to be
appended to the returned file name

- frag_index â a fragment archive index, used with .data extension
only, must be a whole number.

frag_index â a fragment archive index, used with .data extension
only, must be a whole number.

- ctype_timestamp â an optional content-type timestamp, an instance
of Timestamp

ctype_timestamp â an optional content-type timestamp, an instance
of Timestamp

- durable â if True then include a durable marker in data filename.

durable â if True then include a durable marker in data filename.

a file name

DiskFileError â if ext==â.dataâ and the kwarg frag_index is not
a whole number

Returns timestamp(s) and other info extracted from a policy specific
file name. For EC policy the data file name includes a fragment index
and possibly a durable marker, both of which must be stripped off
to retrieve the timestamp.

filename â the file name including extension

a dict, with keys for timestamp, frag_index, durable, ext and ctype_timestamp: timestamp is a Timestamp frag_index is an int or None ctype_timestamp is a Timestamp or
None for .meta files, otherwise None ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension durable is a boolean that is True if the filename is a data file
that includes a durable marker

ctype_timestamp:

- timestamp is a Timestamp

timestamp is a Timestamp

- frag_index is an int or None

frag_index is an int or None

- ctype_timestamp is a Timestamp or
None for .meta files, otherwise None

ctype_timestamp is a Timestamp or
None for .meta files, otherwise None

- ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension

ext is a string, the file extension including the leading dot or
the empty string if the filename has no extension

- durable is a boolean that is True if the filename is a data file
that includes a durable marker

durable is a boolean that is True if the filename is a data file
that includes a durable marker

DiskFileError â if any part of the filename is not able to be
validated.

Return int representation of frag_index, or raise a DiskFileError if
frag_index is not a whole number.

- frag_index â a fragment archive index

frag_index â a fragment archive index

- policy â storage policy used to validate the index against

policy â storage policy used to validate the index against

Finalize put by renaming the object data file to include a durable
marker. We do this for EC policy because it requires a 2-phase put
commit confirmation.

timestamp â object put timestamp, an instance of Timestamp

DiskFileError â if the diskfile frag_index has not been set
(either during initialisation or a call to put())

The only difference between this method and the replication policy
DiskFileWriter method is adding the frag index to the metadata.

metadata â dictionary of metadata to be associated with object

Take whatâs in hashes.pkl and hashes.invalid, combine them, write the
result back to hashes.pkl, and clear out hashes.invalid.

partition_dir â absolute path to partition dir containing hashes.pkl
and hashes.invalid

a dict, the suffix hashes (if any), the key âvalidâ will be False
if hashes.pkl is corrupt, cannot be read or does not exist

Extracts the policy for an object (based on the name of the objects
directory) given the device-relative path to the object. Returns None in
the event that the path is malformed in some way.

The device-relative path is everything after the mount point; for example:

485dc017205a81df3af616d917c90179/1401811134.873649.data

would have device-relative path:

objects-5/30/179/485dc017205a81df3af616d917c90179/1401811134.873649.data

obj_path â device-relative path of an object, or the full path

a BaseStoragePolicy or None

Get the async dir for the given policy.

policy_or_index â StoragePolicy instance, or an index (string or
int); if None, the legacy Policy-0 is assumed.

async_pending or async_pending-<N> as appropriate

Get the data dir for the given policy.

policy_or_index â StoragePolicy instance, or an index (string or
int); if None, the legacy Policy-0 is assumed.

objects or objects-<N> as appropriate

Given the device path, policy, and partition, returns the full
path to the partition

Get the temp dir for the given policy.

policy_or_index â StoragePolicy instance, or an index (string or
int); if None, the legacy Policy-0 is assumed.

tmp or tmp-<N> as appropriate

Invalidates the hash for a suffix_dir in the partitionâs hashes file.

suffix_dir â absolute path to suffix dir whose hash needs
invalidating

Given a devices path (e.g. â/srv/nodeâ), yield an AuditLocation for all
objects stored under that directory for the given datadir (policy),
if device_dirs isnât set.  If device_dirs is set, only yield AuditLocation
for the objects under the entries in device_dirs. The AuditLocation only
knows the path to the hash directory, not to the .data file therein
(if any). This is to avoid a double listdir(hash_dir); the DiskFile object
will always do one, so we donât.

- devices â parent directory of the devices to be audited

devices â parent directory of the devices to be audited

- datadir â objects directory

datadir â objects directory

- mount_check â flag to check if a mount check should be performed
on devices

mount_check â flag to check if a mount check should be performed
on devices

- logger â a logger object

logger â a logger object

- device_dirs â a list of directories under devices to traverse

device_dirs â a list of directories under devices to traverse

- auditor_type â either ALL or ZBF

auditor_type â either ALL or ZBF

In the case that a file is corrupted, move it to a quarantined
area to allow replication to fix it.

The path to the device the corrupted file is on.

The path to the file you want quarantined.

path (str) of directory the file was moved to

OSError â re-raises non errno.EEXIST / errno.ENOTEMPTY
exceptions from rename

Read the existing hashes.pkl

a dict, the suffix hashes (if any), the key âvalidâ will be False
if hashes.pkl is corrupt, cannot be read or does not exist

Helper function to read the pickled metadata from an object data file.

The only difference from _read_file_metadata is that this function
raises DiskFileNotExist when the file cannot be read.

- fd â file descriptor or filename to load the metadata from

fd â file descriptor or filename to load the metadata from

- add_missing_checksum â if set and checksum is missing, add it

add_missing_checksum â if set and checksum is missing, add it

dictionary of metadata

- DiskFileXattrNotSupported â if the filesystem does not support xattr

DiskFileXattrNotSupported â if the filesystem does not support xattr

- DiskFileNotExist â if the file metadata could not be read

DiskFileNotExist â if the file metadata could not be read

- DiskFileBadMetadataChecksum â if the checksum of the read metadata
does not match the stored checksum

DiskFileBadMetadataChecksum â if the checksum of the read metadata
does not match the stored checksum

Hard-links a file located in target_path using the second path new_target_path . Creates intermediate directories if required.

- target_path â current absolute filename

target_path â current absolute filename

- new_target_path â new absolute filename for the hardlink

new_target_path â new absolute filename for the hardlink

- ignore_missing â if True then no exception is raised if the link
could not be made because target_path did not exist, otherwise an
OSError will be raised.

ignore_missing â if True then no exception is raised if the link
could not be made because target_path did not exist, otherwise an
OSError will be raised.

OSError if the hard link could not be created, unless the intended
hard link already exists or the target_path does not exist and must_exist if False.

True if the link was created by the call to this method, False
otherwise.

Write hashes to hashes.pkl

The updated key is added to hashes before it is written.

Helper function to write pickled metadata for an object file.

- fd â file descriptor or filename to write the metadata

fd â file descriptor or filename to write the metadata

- metadata â metadata to write

metadata â metadata to write
