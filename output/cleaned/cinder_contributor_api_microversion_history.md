# REST API Version History Â¶

This documents the changes made to the REST API with every
microversion change. The description for each version should be a
verbose one which has enough information to be suitable for use in
user documentation.

## 3.0 (Maximum in Mitaka) Â¶

The 3.0 Cinder API includes all v2 core APIs existing prior to
the introduction of microversions.  The /v3 URL is used to call
3.0 APIs.
This is the initial version of the Cinder API which supports
microversions.

A user can specify a header in the API request:

OpenStack - API - Version : volume < version >

where <version> is any valid api version for this API.

If no version is specified then the API will behave as if version 3.0
was requested.

The only API change in version 3.0 is versions, i.e.
GET http://localhost:8786/ , which now returns information about
3.0 and later versions and their respective /v3 endpoints.

All other 3.0 APIs are functionally identical to version 2.0.

## 3.1 Â¶

Added the parameters protected and visibility to
_volume_upload_image requests.

## 3.2 Â¶

Change in return value of âGET API requestâ for fetching cinder volume
list on the basis of âbootableâ status of volume as filter.

Before V3.2, âGET API requestâ to fetch volume list returns non-bootable
volumes if bootable filter value is any of the false or False.
For any other value provided to this filter, it always returns
bootable volume list.

But in V3.2, this behavior is updated.
In V3.2, bootable volume list will be returned for any of the
âT/True/1/trueâ bootable filter values only.
Non-bootable volume list will be returned for any of âF/False/0/falseâ
bootable filter values.
But for any other values passed for bootable filter, it will return
âInvalid input received: bootable={filter value}â error.

## 3.3 Â¶

Added /messages API.

## 3.4 Â¶

Added the filter parameters glance_metadata to
list/detail volumes requests.

## 3.5 Â¶

Added pagination support to /messages API

## 3.6 Â¶

Allowed to set empty description and empty name for consistency
group in consisgroup-update operation.

## 3.7 Â¶

Added cluster_name field to service list/detail.

Added /clusters endpoint to list/show/update clusters.

Show endpoint requires the cluster name and optionally the binary as a URL
parameter (default is âcinder-volumeâ).  Returns:

{ "cluster" : { "created_at" : "" , "disabled_reason" : null , "last_heartbeat" : "" , "name" : "cluster_name" , "num_down_hosts" : 4 , "num_hosts" : 2 , "state" : "up" , "status" : "enabled" , "updated_at" : "" } }

Update endpoint allows enabling and disabling a cluster in a similar way to
serviceâs update endpoint, but in the body we must specify the name and
optionally the binary (âcinder-volumeâ is the default) and the disabled
reason. Returns:

{ "cluster" : { "name" : "cluster_name" , "state" : "up" , "status" : "enabled" , "disabled_reason" : null } }

Index and detail accept filtering by name , binary , disabled , num_hosts , num_down_hosts , and up/down status ( is_up ) as URL
parameters.

Index endpoint returns:

{ "clusters" : [ { "name" : "cluster_name" , "state" : "up" , "status" : "enabled" } ] }

Detail endpoint returns:

{ "clusters" : [ { "created_at" : "" , "disabled_reason" : null , "last_heartbeat" : "" , "name" : "cluster_name" , "num_down_hosts" : 4 , "num_hosts" : 2 , "state" : "up" , "status" : "enabled" , "updated_at" : "" } ] }

## 3.8 Â¶

Adds the following resources that were previously in extensions:

- os-volume-manage => /v3/<project_id>/manageable_volumes

os-volume-manage => /v3/<project_id>/manageable_volumes

- os-snapshot-manage => /v3/<project_id>/manageable_snapshots

os-snapshot-manage => /v3/<project_id>/manageable_snapshots

## 3.9 Â¶

Added backup update interface to change name and description.
Returns:

{ "backup" : { "id" : "backup_id" , "name" : "backup_name" , "links" : "backup_link" } }

## 3.10 Â¶

Added the filter parameters group_id to
list/detail volumes requests.

## 3.11 Â¶

Added group types and group specs APIs.

## 3.12 Â¶

Added volumes/summary API.

## 3.13 Â¶

Added create/delete/update/list/show APIs for generic volume groups.

## 3.14 Â¶

Added group snapshots and create group from src APIs.

## 3.15 (Maximum in Newton) Â¶

Added injecting the responseâs Etag header to avoid the lost update
problem with volume metadata.

## 3.16 Â¶

os-migrate_volume now accepts cluster parameter when we want to migrate a
volume to a cluster.  If we pass the host parameter for a volume that is
in a cluster, the request will be sent to the cluster as if we had requested
that specific cluster.  Only host or cluster can be provided.

Creating a managed volume also supports the cluster parameter.

## 3.17 Â¶

os-snapshot-manage and os-volume-manage now support cluster parameter on
listings (summary and detailed).  Both location parameters, cluster and host are exclusive and only one should be provided.

## 3.18 Â¶

Added backup project attribute.

## 3.19 Â¶

Added reset status actions âreset_statusâ to group snapshot.

## 3.20 Â¶

Added reset status actions âreset_statusâ to generic volume group.

## 3.21 Â¶

Show provider_id in detailed view of a volume for admin.

## 3.22 Â¶

Added support to filter snapshot list based on metadata of snapshot.

## 3.23 Â¶

Allow passing force parameter to volume delete.

## 3.24 Â¶

New API endpoint /workers/cleanup allows triggering cleanup for cinder-volume
services.  Meant for cleaning ongoing operations from failed nodes.

The cleanup will be performed by other services belonging to the same
cluster, so at least one of them must be up to be able to do the cleanup.

Cleanup cannot be triggered during a cloud upgrade.

If no arguments are provided cleanup will try to issue a clean message for
all nodes that are down, but we can restrict which nodes we want to be
cleaned using parameters service_id , cluster_name , host , binary , and disabled .

Cleaning specific resources is also possible using resource_type and resource_id parameters.

We can even force cleanup on nodes that are up with is_up , but thatâs
not recommended and should only used if you know what you are doing.  For
example if you know a specific cinder-volume is down even though itâs still
not being reported as down when listing the services and you know the cluster
has at least another service to do the cleanup.

API will return a dictionary with 2 lists, one with services that have been
issued a cleanup request ( cleaning key) and the other with services
that cannot be cleaned right now because there is no alternative service to
do the cleanup in that cluster ( unavailable key).

Data returned for each service element in these two lists consist of the id , host , binary , and cluster_name .  These are not the
services that will be performing the cleanup, but the services that will be
cleaned up or couldnât be cleaned up.

## 3.25 Â¶

Add volumes field to group list/detail and group show.

## 3.26 Â¶

- New failover action equivalent to failover_host , but accepting cluster parameter as well as the host cluster that failover_host accepts.

New failover action equivalent to failover_host , but accepting cluster parameter as well as the host cluster that failover_host accepts.

- freeze and thaw actions accept cluster parameter.

freeze and thaw actions accept cluster parameter.

- Cluster listing accepts replication_status , frozen and active_backend_id as filters, and returns additional fields for each
cluster: replication_status , frozen , active_backend_id .

Cluster listing accepts replication_status , frozen and active_backend_id as filters, and returns additional fields for each
cluster: replication_status , frozen , active_backend_id .

## 3.27 (Maximum in Ocata) Â¶

Added new attachment APIs. See the API reference for details.

## 3.28 Â¶

Add filters support to get_pools

## 3.29 Â¶

Add filter, sorter and pagination support in group snapshot.

## 3.30 Â¶

Support sort snapshots with ânameâ.

## 3.31 Â¶

Add support for configure resource query filters.

## 3.32 Â¶

Added set-log and get-log service actions.

## 3.33 Â¶

Add resource_filters API to retrieve configured resource filters.

## 3.34 Â¶

Add like filter support in volume , backup , snapshot , message , attachment , group and group-snapshot list APIs.

## 3.35 Â¶

Add volume-type filter to Get-Pools API.

## 3.36 Â¶

Add metadata to volumes/summary response body.

## 3.37 Â¶

Support sort backup by ânameâ.

## 3.38 Â¶

Added enable_replication/disable_replication/failover_replication/
list_replication_targets for replication groups (Tiramisu).

## 3.39 Â¶

Add project_id admin filters support to limits.

## 3.40 Â¶

Add volume revert to its latest snapshot support.

## 3.41 Â¶

Add user_id field to snapshot list/detail and snapshot show.

## 3.42 Â¶

Add ability to extend âin-useâ volume. User should be aware of the
whole environment before using this feature because itâs dependent
on several external factors below:

- nova-compute version - needs to be the latest for Pike.

nova-compute version - needs to be the latest for Pike.

- only the libvirt compute driver supports this currently.

only the libvirt compute driver supports this currently.

- only iscsi and fibre channel volume types are supported on the
nova side currently.

only iscsi and fibre channel volume types are supported on the
nova side currently.

Administrator can disable this ability by updating the volume:extend_attached_volume policy rule.  Extend of a reserved
Volume is NOT allowed.

## 3.43 (Maximum in Pike) Â¶

Support backup CRUD with metadata.

## 3.44 Â¶

Support attachment completion. See the API reference for details.

## 3.45 Â¶

Add count field to volume, backup and snapshot list and detail APIs.

## 3.46 Â¶

Modify the behavior of the volume-create ( POST /v3/volumes ) call when
passing an imageRef in the request body.  Prior to this microversion,
the image was simply downloaded and written to the volume.  However, when
a volume is attached to a server, it is possible to use the Compute API
server createImage action to create an instance snapshot of the volume.
This is a zero-byte image in the Image Service that has a block_device_mapping image property whose value contains snapshot as the source_type and a snapshot_id reference to a volume snapshot
in the Block Storage service.  From microversion 3.46 and later, when a
volume-create request is made referring to such an image, instead of using
the image to create a volume, the snapshot it references will be used.

Note

Due to changes to cinder to handle image-related CVEs, making a
volume-create call with an imageRef referring to a nova instance
snapshot specifying a microversion less than 3.46 may create a volume
in error status.  This occurs when the disk_format property
of the image is something other than raw , because for non-raw
formats, even an image containing no data will consist of more than
zero bytes, and thus the image is rejected as being of a different
format than is claimed.

## 3.47 Â¶

Support create volume from backup.

## 3.48 Â¶

Add shared_targets and service_uuid fields to volume.

## 3.49 Â¶

Support report backend storage state in service list.

## 3.50 (Maximum in Queens) Â¶

Services supporting this microversion are capable of volume multiattach.
This version does not need to be requested when creating the volume, but can
be used as a way to query if the capability exists in the Cinder service.

## 3.51 Â¶

Add support for cross AZ backups.

## 3.52 Â¶

RESKEY:availability_zones is a reserved spec key for AZ volume type,
and filter volume type by extra_specs is supported now.

## 3.53 Â¶

Schema validation support has been added using jsonschema for V2/V3
volume APIs.

- Create volume API Before 3.53, create volume API used to accept any invalid parameters in the
request body like the ones below were passed by python-cinderclient. user_id project_id status attach_status But in 3.53, this behavior is updated. If user passes any invalid
parameters to the API which are not documented in api-ref, then
it will raise badRequest error.

Before 3.53, create volume API used to accept any invalid parameters in the
request body like the ones below were passed by python-cinderclient.

- user_id

user_id

- project_id

project_id

- status

status

- attach_status

attach_status

But in 3.53, this behavior is updated. If user passes any invalid
parameters to the API which are not documented in api-ref, then
it will raise badRequest error.

- Update volume API Before 3.53, even if user doesnât pass any valid parameters in the request
body, the volume was updated.
But in 3.53, user will need to pass at least one valid parameter in the
request body otherwise it will return 400 error.

Before 3.53, even if user doesnât pass any valid parameters in the request
body, the volume was updated.
But in 3.53, user will need to pass at least one valid parameter in the
request body otherwise it will return 400 error.

## 3.54 Â¶

Add mode argument to attachment-create.

## 3.55 (Maximum in Rocky) Â¶

Support ability to transfer snapshots along with their parent volume.

## 3.56 Â¶

Add user_id attribute to response body of list backup with detail and show
backup detail APIs.

## 3.57 Â¶

Expanded volume transfer record details by adding source_project_id , destination_project_id and accepted fields to transfer table and
related api (create/show/list detail transfer APIs) responses.

## 3.58 Â¶

Add project_id attribute to response body of list groups with detail,
list group snapshots with detail, show group detail and show group snapshot
detail APIs.

## 3.59 (Maximum in Stein and Train) Â¶

Support volume transfer pagination.

## 3.60 (Maximum in Ussuri) Â¶

Users may apply time comparison filters to the volume summary list and volume
detail list requests by using the created_at or updated_at fields.
Time must be expressed in ISO 8601 format.

## 3.61 Â¶

Add cluster_name attribute to response body of volume details for admin in
Active/Active HA mode.

## 3.62 (Maximum in Victoria) Â¶

Add support for set, get, and unset a default volume type for a specific
project. Setting this default overrides the configured default_volume_type
value.

## 3.63 Â¶

Includes volume type ID in the volume-show and volume-detail-list JSON
responses. Before this microversion, Cinder returns only the volume type name
in the volume details.

## 3.64 (Maximum in Wallaby) Â¶

Include the encryption_key_id in volume and backup details when the
associated volume is encrypted.

## 3.65 Â¶

Include a consumes_quota field in volume and snapshot details to indicate
whether the resource is consuming quota or not.  Also, accept a consumes_quota filter, which takes a boolean value, in the volume and
snapshot list requests.  (The default listing behavior is not to use this
filter.)

## 3.66 (Maximum in Xena) Â¶

Volume snapshots of in-use volumes can be created without the âforceâ flag.
Although the âforceâ flag is now considered invalid when passed in a volume
snapshot request, for backward compatibility, the âforceâ flag with a value
evaluating to True is silently ignored.

## 3.67 Â¶

API URLs no longer need a âproject_idâ argument in them. For example, the API
route: https://$(controller)s/volume/v3/$(project_id)s/volumes is
equivalent to https://$(controller)s/volume/v3/volumes . When interacting
with the cinder service as system or domain scoped users, a project_id should
not be specified in the API path.

## 3.68 (Maximum in Yoga) Â¶

Support ability to re-image a volume with a specific image. Specify the os-reimage action in the request body.

## 3.69 Â¶

Volume field shared_targets is a tristate boolean value now, with the
following meanings:

- true : Do os-brick locking when host iSCSI initiator doesnât support
manual scans.

true : Do os-brick locking when host iSCSI initiator doesnât support
manual scans.

- false : Never do locking.

false : Never do locking.

- null : Forced locking regardless of the iSCSI initiator.

null : Forced locking regardless of the iSCSI initiator.

## 3.70 (Maximum in Zed, 2023.1 and 2023.2) Â¶

Add the ability to transfer encrypted volumes and their snapshots. The feature
removes a prior restriction on transferring encrypted volumes. Otherwise, the
API request and response schema are unchanged.

## 3.71 (Maximum in 2024.1 and 2024.2) Â¶

Add the os-extend_volume_completion volume action, which Nova can use
to notify Cinder of success and error when handling a volume-extended external server event.
