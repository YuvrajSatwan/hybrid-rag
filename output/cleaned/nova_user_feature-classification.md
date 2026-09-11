# Feature Classification Â¶

This document presents a matrix that describes which features are ready to be
used and which features are works in progress. It includes links to relevant
documentation and functional tests.

Warning

Please note: this is a work in progress!

## Aims Â¶

Users want reliable, long-term solutions for their use cases.
The feature classification matrix identifies which features are
complete and ready to use, and which should be used with caution.

The matrix also benefits developers by providing a list of features that
require further work to be considered complete.

Below is a matrix for a selection of important verticals:

- General Purpose Cloud Features

General Purpose Cloud Features

- NFV Cloud Features

NFV Cloud Features

- HPC Cloud Features

HPC Cloud Features

For more details on the concepts in each matrix,
please see Notes on Concepts .

## General Purpose Cloud Features Â¶

This is a summary of the key features dev/test clouds, and other similar
general purpose clouds need, and it describes their current state.

Below there are sections on NFV and HPC specific features. These look at
specific features and scenarios that are important to those more specific
sets of use cases.

Summary

Feature Maturity Ironic CI libvirt+kvm (x86 & ppc64) libvirt+kvm (s390x) libvirt+virtuozzo CT libvirt+virtuozzo VM VMware CI IBM zVM CI Create Server and Delete Server complete ? â ? â â â â Snapshot Server complete ? â ? â â ? â Server power ops complete ? â ? â â â â Rebuild Server complete ? â ? â â â â Resize Server complete ? â ? â â â â Volume Operations complete â â ? â â â â Custom disk configurations on boot complete â â ? â â â â Custom neutron configurations on boot complete â â ? ? ? â â Pause a Server complete â â ? â â â â Suspend a Server complete â â ? â â â â Server console output complete â â ? ? ? â â Server Rescue complete â â ? â â â â Server Config Drive complete â â ? â â â â Server Change Password experimental â â ? â â â â Server Shelve and Unshelve complete â â ? â â â â

Details

- Create Server and Delete Server This includes creating a server, and deleting a server.
Specifically this is about booting a server from a glance image
using the default disk and network configuration. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#servers-servers Admin Docs: https://docs.openstack.org/nova/latest/user/launch-instances.html Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: complete

This includes creating a server, and deleting a server.
Specifically this is about booting a server from a glance image
using the default disk and network configuration.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#servers-servers Admin Docs: https://docs.openstack.org/nova/latest/user/launch-instances.html Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#servers-servers

- Admin Docs: https://docs.openstack.org/nova/latest/user/launch-instances.html

- Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: unknown

- IBM zVM CI: complete

- Snapshot Server This is creating a glance image from the currently running server. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: https://docs.openstack.org/glance/latest/admin/troubleshooting.html Tempest tests: aaacd1d0-55a2-4ce8-818a-b5439df8adc9 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: unknown Ironic CI: unknown IBM zVM CI: complete

This is creating a glance image from the currently running server.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: https://docs.openstack.org/glance/latest/admin/troubleshooting.html Tempest tests: aaacd1d0-55a2-4ce8-818a-b5439df8adc9

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action

- Admin Docs: https://docs.openstack.org/glance/latest/admin/troubleshooting.html

- Tempest tests: aaacd1d0-55a2-4ce8-818a-b5439df8adc9

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: unknown Ironic CI: unknown IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: unknown

- Ironic CI: unknown

- IBM zVM CI: complete

- Server power ops This includes reboot, shutdown and start. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: 2cb1baf6-ac8d-4429-bf0d-ba8a0ba53e32 , af8eafd4-38a7-4a4b-bdbc-75145a580560 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: complete

This includes reboot, shutdown and start.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: 2cb1baf6-ac8d-4429-bf0d-ba8a0ba53e32 , af8eafd4-38a7-4a4b-bdbc-75145a580560

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action

- Admin Docs:

- Tempest tests: 2cb1baf6-ac8d-4429-bf0d-ba8a0ba53e32 , af8eafd4-38a7-4a4b-bdbc-75145a580560

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: unknown

- IBM zVM CI: complete

- Rebuild Server You can rebuild a server, optionally specifying the glance image to use. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: aaa6cdf3-55a7-461a-add9-1c8596b9a07c drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: missing

You can rebuild a server, optionally specifying the glance image to use.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: aaa6cdf3-55a7-461a-add9-1c8596b9a07c

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action

- Admin Docs:

- Tempest tests: aaa6cdf3-55a7-461a-add9-1c8596b9a07c

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: unknown

- IBM zVM CI: missing

- Resize Server You resize a server to a new flavor, then confirm or revert that
operation. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: 1499262a-9328-4eda-9068-db1ac57498d2 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: complete libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: missing

You resize a server to a new flavor, then confirm or revert that
operation.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action Admin Docs: Tempest tests: 1499262a-9328-4eda-9068-db1ac57498d2

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=#servers-run-an-action-servers-action

- Admin Docs:

- Tempest tests: 1499262a-9328-4eda-9068-db1ac57498d2

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: complete libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: unknown IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: complete

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: unknown

- IBM zVM CI: missing

- Volume Operations This is about attaching volumes, detaching volumes. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#servers-with-volume-attachments-servers-os-volume-attachments Admin Docs: https://docs.openstack.org/cinder/latest/admin/blockstorage-manage-volumes.html Tempest tests: fff42874-7db5-4487-a8e1-ddda5fb5288d drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: complete libvirt+virtuozzo VM: complete VMware CI: complete Ironic CI: missing IBM zVM CI: missing

This is about attaching volumes, detaching volumes.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#servers-with-volume-attachments-servers-os-volume-attachments Admin Docs: https://docs.openstack.org/cinder/latest/admin/blockstorage-manage-volumes.html Tempest tests: fff42874-7db5-4487-a8e1-ddda5fb5288d

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#servers-with-volume-attachments-servers-os-volume-attachments

- Admin Docs: https://docs.openstack.org/cinder/latest/admin/blockstorage-manage-volumes.html

- Tempest tests: fff42874-7db5-4487-a8e1-ddda5fb5288d

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: complete libvirt+virtuozzo VM: complete VMware CI: complete Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: complete

- libvirt+virtuozzo VM: complete

- VMware CI: complete

- Ironic CI: missing

- IBM zVM CI: missing

- Custom disk configurations on boot This is about supporting all the features of BDMv2.
This includes booting from a volume, in various ways, and
specifying a custom set of ephemeral disks. Note some drivers
only supports part of what the API allows. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=create-image-createimage-action-detail#create-server Admin Docs: https://docs.openstack.org/nova/latest/user/block-device-mapping.html Tempest tests: 557cd2c2-4eb8-4dce-98be-f86765ff311b, 36c34c67-7b54-4b59-b188-02a2f458a63b drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: complete VMware CI: partial Ironic CI: missing IBM zVM CI: missing

This is about supporting all the features of BDMv2.
This includes booting from a volume, in various ways, and
specifying a custom set of ephemeral disks. Note some drivers
only supports part of what the API allows.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=create-image-createimage-action-detail#create-server Admin Docs: https://docs.openstack.org/nova/latest/user/block-device-mapping.html Tempest tests: 557cd2c2-4eb8-4dce-98be-f86765ff311b, 36c34c67-7b54-4b59-b188-02a2f458a63b

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=create-image-createimage-action-detail#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/user/block-device-mapping.html

- Tempest tests: 557cd2c2-4eb8-4dce-98be-f86765ff311b, 36c34c67-7b54-4b59-b188-02a2f458a63b

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: complete VMware CI: partial Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: missing

- libvirt+virtuozzo VM: complete

- VMware CI: partial

- Ironic CI: missing

- IBM zVM CI: missing

- Custom neutron configurations on boot This is about supporting booting from one or more neutron ports,
or all the related short cuts such as booting a specified network.
This does not include SR-IOV or similar, just simple neutron ports. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?&expanded=create-server-detail Admin Docs: Tempest tests: 2f3a0127-95c7-4977-92d2-bc5aec602fb4 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: partial Ironic CI: missing IBM zVM CI: partial

This is about supporting booting from one or more neutron ports,
or all the related short cuts such as booting a specified network.
This does not include SR-IOV or similar, just simple neutron ports.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?&expanded=create-server-detail Admin Docs: Tempest tests: 2f3a0127-95c7-4977-92d2-bc5aec602fb4

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?&expanded=create-server-detail

- Admin Docs:

- Tempest tests: 2f3a0127-95c7-4977-92d2-bc5aec602fb4

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: partial Ironic CI: missing IBM zVM CI: partial

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: unknown

- libvirt+virtuozzo VM: unknown

- VMware CI: partial

- Ironic CI: missing

- IBM zVM CI: partial

- Pause a Server This is pause and unpause a server, where the state is held in memory. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?#pause-server-pause-action Admin Docs: Tempest tests: bd61a9fd-062f-4670-972b-2d6c3e3b9e73 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: partial VMware CI: partial Ironic CI: missing IBM zVM CI: complete

This is pause and unpause a server, where the state is held in memory.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?#pause-server-pause-action Admin Docs: Tempest tests: bd61a9fd-062f-4670-972b-2d6c3e3b9e73

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?#pause-server-pause-action

- Admin Docs:

- Tempest tests: bd61a9fd-062f-4670-972b-2d6c3e3b9e73

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: partial VMware CI: partial Ironic CI: missing IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: missing

- libvirt+virtuozzo VM: partial

- VMware CI: partial

- Ironic CI: missing

- IBM zVM CI: complete

- Suspend a Server This suspend and resume a server, where the state is held on disk. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=suspend-server-suspend-action-detail Admin Docs: Tempest tests: 0d8ee21e-b749-462d-83da-b85b41c86c7f drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: missing IBM zVM CI: missing

This suspend and resume a server, where the state is held on disk.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/?expanded=suspend-server-suspend-action-detail Admin Docs: Tempest tests: 0d8ee21e-b749-462d-83da-b85b41c86c7f

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/?expanded=suspend-server-suspend-action-detail

- Admin Docs:

- Tempest tests: 0d8ee21e-b749-462d-83da-b85b41c86c7f

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: missing

- IBM zVM CI: missing

- Server console output This gets the current server console output. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#show-console-output-os-getconsoleoutput-action Admin Docs: Tempest tests: 4b8867e6-fffa-4d54-b1d1-6fdda57be2f3 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: partial Ironic CI: missing IBM zVM CI: complete

This gets the current server console output.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#show-console-output-os-getconsoleoutput-action Admin Docs: Tempest tests: 4b8867e6-fffa-4d54-b1d1-6fdda57be2f3

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#show-console-output-os-getconsoleoutput-action

- Admin Docs:

- Tempest tests: 4b8867e6-fffa-4d54-b1d1-6fdda57be2f3

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: partial Ironic CI: missing IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: unknown

- libvirt+virtuozzo VM: unknown

- VMware CI: partial

- Ironic CI: missing

- IBM zVM CI: complete

- Server Rescue This boots a server with a new root disk from the specified glance image
to allow a user to fix a boot partition configuration, or similar. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#rescue-server-rescue-action Admin Docs: Tempest tests: fd032140-714c-42e4-a8fd-adcd8df06be6 , 70cdb8a1-89f8-437d-9448-8844fd82bf46 drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: complete VMware CI: complete Ironic CI: missing IBM zVM CI: missing

This boots a server with a new root disk from the specified glance image
to allow a user to fix a boot partition configuration, or similar.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#rescue-server-rescue-action Admin Docs: Tempest tests: fd032140-714c-42e4-a8fd-adcd8df06be6 , 70cdb8a1-89f8-437d-9448-8844fd82bf46

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#rescue-server-rescue-action

- Admin Docs:

- Tempest tests: fd032140-714c-42e4-a8fd-adcd8df06be6 , 70cdb8a1-89f8-437d-9448-8844fd82bf46

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: complete VMware CI: complete Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: complete

- VMware CI: complete

- Ironic CI: missing

- IBM zVM CI: missing

- Server Config Drive This ensures the user data provided by the user when booting
a server is available in one of the expected config drive locations. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/config-drive.html Tempest tests: 7fff3fb3-91d8-4fd0-bd7d-0204f1f180ba drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: partial IBM zVM CI: complete

This ensures the user data provided by the user when booting
a server is available in one of the expected config drive locations.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/config-drive.html Tempest tests: 7fff3fb3-91d8-4fd0-bd7d-0204f1f180ba

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/config-drive.html

- Tempest tests: 7fff3fb3-91d8-4fd0-bd7d-0204f1f180ba

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: partial VMware CI: complete Ironic CI: partial IBM zVM CI: complete

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: missing

- libvirt+virtuozzo VM: partial

- VMware CI: complete

- Ironic CI: partial

- IBM zVM CI: complete

- Server Change Password The ability to reset the password of a user within the server. info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#change-administrative-password-changepassword-action Admin Docs: Tempest tests: 6158df09-4b82-4ab3-af6d-29cf36af858d drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: missing VMware CI: missing Ironic CI: missing IBM zVM CI: missing

The ability to reset the password of a user within the server.

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#change-administrative-password-changepassword-action Admin Docs: Tempest tests: 6158df09-4b82-4ab3-af6d-29cf36af858d

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#change-administrative-password-changepassword-action

- Admin Docs:

- Tempest tests: 6158df09-4b82-4ab3-af6d-29cf36af858d

drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: missing VMware CI: missing Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): partial

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: missing

- libvirt+virtuozzo VM: missing

- VMware CI: missing

- Ironic CI: missing

- IBM zVM CI: missing

- Server Shelve and Unshelve The ability to keep a server logically alive, but not using any
cloud resources. For local disk based instances, this involves taking
a snapshot, called offloading. info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#shelve-server-shelve-action Admin Docs: Tempest tests: 1164e700-0af0-4a4c-8792-35909a88743c,c1b6318c-b9da-490b-9c67-9339b627271f drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: complete VMware CI: missing Ironic CI: missing IBM zVM CI: missing

The ability to keep a server logically alive, but not using any
cloud resources. For local disk based instances, this involves taking
a snapshot, called offloading.

info: Maturity: complete API Docs: https://docs.openstack.org/api-ref/compute/#shelve-server-shelve-action Admin Docs: Tempest tests: 1164e700-0af0-4a4c-8792-35909a88743c,c1b6318c-b9da-490b-9c67-9339b627271f

- Maturity: complete

- API Docs: https://docs.openstack.org/api-ref/compute/#shelve-server-shelve-action

- Admin Docs:

- Tempest tests: 1164e700-0af0-4a4c-8792-35909a88743c,c1b6318c-b9da-490b-9c67-9339b627271f

drivers: libvirt+kvm (x86 & ppc64): complete libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: missing libvirt+virtuozzo VM: complete VMware CI: missing Ironic CI: missing IBM zVM CI: missing

- libvirt+kvm (x86 & ppc64): complete

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: missing

- libvirt+virtuozzo VM: complete

- VMware CI: missing

- Ironic CI: missing

- IBM zVM CI: missing

## NFV Cloud Features Â¶

Network Function Virtualization (NFV) is about virtualizing network node
functions into building blocks that may connect, or chain together to
create a particular service. It is common for this workloads needing
bare metal like performance, i.e. low latency and close to line speed
performance.

Important

In deployments older than Train, or in mixed Stein/Train deployments with a
rolling upgrade in progress, unless specifically enabled , live migration is not
possible for instances with a NUMA topology when using the libvirt
driver. A NUMA topology may be specified explicitly or can be added
implicitly due to the use of CPU pinning or huge pages. Refer to bug
#1289064 for more information. As of Train, live migration of instances
with a NUMA topology when using the libvirt driver is fully supported.

Summary

Feature Maturity libvirt+kvm (x86 & ppc64) libvirt+kvm (s390x) NUMA Placement experimental â ? CPU Pinning Policy experimental â ? CPU Pinning Thread Policy experimental â ?

Details

- NUMA Placement Configure placement of instance vCPUs and memory across host NUMA nodes info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997 drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

Configure placement of instance vCPUs and memory across host NUMA nodes

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies

- Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

- libvirt+kvm (x86 & ppc64): partial

- libvirt+kvm (s390x): unknown

- CPU Pinning Policy Enable/disable binding of instance vCPUs to host CPUs info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests: drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

Enable/disable binding of instance vCPUs to host CPUs

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests:

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies

- Tempest tests:

drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

- libvirt+kvm (x86 & ppc64): partial

- libvirt+kvm (s390x): unknown

- CPU Pinning Thread Policy Configure usage of host hardware threads when pinning is used info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests: drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

Configure usage of host hardware threads when pinning is used

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies Tempest tests:

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/cpu-topologies.html#customizing-instance-cpu-pinning-policies

- Tempest tests:

drivers: libvirt+kvm (x86 & ppc64): partial libvirt+kvm (s390x): unknown

- libvirt+kvm (x86 & ppc64): partial

- libvirt+kvm (s390x): unknown

## HPC Cloud Features Â¶

High Performance Compute (HPC) cloud have some specific needs that are covered
in this set of features.

Summary

Feature Maturity Ironic libvirt+kvm (x86 & ppc64) libvirt+kvm (s390x) libvirt+virtuozzo CT libvirt+virtuozzo VM VMware CI GPU Passthrough experimental ? â l ? â â â Virtual GPUs experimental â â queens ? ? ? â

Details

- GPU Passthrough The PCI passthrough feature in OpenStack allows full access and direct
control of a physical PCI device in guests. This mechanism is generic
for any devices that can be attached to a PCI bus. Correct driver
installation is the only requirement for the guest to properly use the
devices. info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/pci-passthrough.html Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997 drivers: libvirt+kvm (x86 & ppc64): complete (updated in âLâ release) libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: missing Ironic: unknown

The PCI passthrough feature in OpenStack allows full access and direct
control of a physical PCI device in guests. This mechanism is generic
for any devices that can be attached to a PCI bus. Correct driver
installation is the only requirement for the guest to properly use the
devices.

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/pci-passthrough.html Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/pci-passthrough.html

- Tempest tests: 9a438d88-10c6-4bcd-8b5b-5b6e25e1346f , 585e934c-448e-43c4-acbf-d06a9b899997

drivers: libvirt+kvm (x86 & ppc64): complete (updated in âLâ release) libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: partial libvirt+virtuozzo VM: partial VMware CI: missing Ironic: unknown

- libvirt+kvm (x86 & ppc64): complete (updated in âLâ release)

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: partial

- libvirt+virtuozzo VM: partial

- VMware CI: missing

- Ironic: unknown

- Virtual GPUs Attach a virtual GPU to an instance at server creation time info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/virtual-gpu.html Tempest tests: drivers: libvirt+kvm (x86 & ppc64): partial (updated in âQUEENSâ release) libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: missing Ironic: missing

Attach a virtual GPU to an instance at server creation time

info: Maturity: experimental API Docs: https://docs.openstack.org/api-ref/compute/#create-server Admin Docs: https://docs.openstack.org/nova/latest/admin/virtual-gpu.html Tempest tests:

- Maturity: experimental

- API Docs: https://docs.openstack.org/api-ref/compute/#create-server

- Admin Docs: https://docs.openstack.org/nova/latest/admin/virtual-gpu.html

- Tempest tests:

drivers: libvirt+kvm (x86 & ppc64): partial (updated in âQUEENSâ release) libvirt+kvm (s390x): unknown libvirt+virtuozzo CT: unknown libvirt+virtuozzo VM: unknown VMware CI: missing Ironic: missing

- libvirt+kvm (x86 & ppc64): partial (updated in âQUEENSâ release)

- libvirt+kvm (s390x): unknown

- libvirt+virtuozzo CT: unknown

- libvirt+virtuozzo VM: unknown

- VMware CI: missing

- Ironic: missing

## Notes on Concepts Â¶

This document uses the following terminology.

### Users Â¶

These are the users we talk about in this document:

creates and deletes servers, directly or indirectly using an API

creates images and apps that run on the cloud

administers the cloud

runs and uses the cloud

Note

This is not an exhaustive list of personas, but rather an indicative set of
users.

### Feature Group Â¶

To reduce the size of the matrix, we organize the features into groups.
Each group maps to a set of user stories that can be validated by a set
of scenarios and tests. Typically, this means a set of tempest tests.

This list focuses on API concepts like attach and detach volumes, rather than
deployment specific concepts like attach an iSCSI volume to a KVM based VM.

### Deployment Â¶

A deployment maps to a specific test environment. We provide a full description
of the environment, so it is possible to reproduce the reported test results
for each of the Feature Groups.

This description includes all aspects of the deployment, for example
the hypervisor, number of nova-compute services, storage, network driver,
and types of images being tested.

### Feature Group Maturity Â¶

The Feature Group Maturity rating is specific to the API concepts, rather than
specific to a particular deployment. That detail is covered in the deployment
rating for each feature group.

Note

Although having some similarities, this list is not directly related
to the Interop effort.

Feature Group ratings:

Incomplete features are those that do not have enough functionality to
satisfy real world use cases.

Experimental features should be used with extreme caution. They are likely
to have little or no upstream testing, and are therefore likely to
contain bugs.

For a feature to be considered complete, it must have:

- complete API docs (concept and REST call definition)

complete API docs (concept and REST call definition)

- complete Administrator docs

complete Administrator docs

- tempest tests that define if the feature works correctly

tempest tests that define if the feature works correctly

- sufficient functionality and reliability to be useful in real world
scenarios

sufficient functionality and reliability to be useful in real world
scenarios

- a reasonable expectation that the feature will be supported long-term

a reasonable expectation that the feature will be supported long-term

There are various reasons why a complete feature may be required, but
generally it is when all drivers support that feature. New
drivers need to prove they support all required features before they are
allowed in upstream Nova.

Required features are those that any new technology must support before
being allowed into tree. The larger the list, the more features are
available on all Nova based clouds.

Deprecated features are those that are scheduled to be removed in a future
major release of Nova. If a feature is marked as complete, it should
never be deprecated.

If a feature is incomplete or experimental for several releases,
it runs the risk of being deprecated and later removed from the code base.

### Deployment Rating for a Feature Group Â¶

The deployment rating refers to the state of the tests for each
Feature Group on a particular deployment.

Deployment ratings:

No data is available.

No tests exist.

Self declared that the tempest tests pass.

Tested by third party CI.

Tested as part of the check or gate queue.

The eventual goal is to automate this list from a third party CI reporting
system, but currently we document manual inspections in an ini file.
Ideally, we will review the list at every milestone.
