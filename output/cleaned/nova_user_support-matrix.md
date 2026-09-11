# Feature Support Matrix Â¶

When considering which capabilities should be marked as mandatory the
following general guiding principles were applied

- Inclusivity - people have shown ability to make effective
use of a wide range of virtualization technologies with broadly
varying feature sets. Aiming to keep the requirements as inclusive
as possible, avoids second-guessing what a user may wish to use
the cloud compute service for.

Inclusivity - people have shown ability to make effective
use of a wide range of virtualization technologies with broadly
varying feature sets. Aiming to keep the requirements as inclusive
as possible, avoids second-guessing what a user may wish to use
the cloud compute service for.

- Bootstrapping - a practical use case test is to consider that
starting point for the compute deploy is an empty data center
with new machines and network connectivity. The look at what
are the minimum features required of a compute service, in order
to get user instances running and processing work over the
network.

Bootstrapping - a practical use case test is to consider that
starting point for the compute deploy is an empty data center
with new machines and network connectivity. The look at what
are the minimum features required of a compute service, in order
to get user instances running and processing work over the
network.

- Competition - an early leader in the cloud compute service space
was Amazon EC2. A sanity check for whether a feature should be
mandatory is to consider whether it was available in the first
public release of EC2. This had quite a narrow feature set, but
none the less found very high usage in many use cases. So it
serves to illustrate that many features need not be considered
mandatory in order to get useful work done.

Competition - an early leader in the cloud compute service space
was Amazon EC2. A sanity check for whether a feature should be
mandatory is to consider whether it was available in the first
public release of EC2. This had quite a narrow feature set, but
none the less found very high usage in many use cases. So it
serves to illustrate that many features need not be considered
mandatory in order to get useful work done.

- Reality - there are many virt drivers currently shipped with
Nova, each with their own supported feature set. Any feature which is
missing in at least one virt driver that is already in-tree, must
by inference be considered optional until all in-tree drivers
support it. This does not rule out the possibility of a currently
optional feature becoming mandatory at a later date, based on other
principles above.

Reality - there are many virt drivers currently shipped with
Nova, each with their own supported feature set. Any feature which is
missing in at least one virt driver that is already in-tree, must
by inference be considered optional until all in-tree drivers
support it. This does not rule out the possibility of a currently
optional feature becoming mandatory at a later date, based on other
principles above.

Summary

Feature Status Ironic Libvirt KVM (aarch64) Libvirt KVM (ppc64) Libvirt KVM (s390x) Libvirt KVM (x86) Libvirt LXC Libvirt QEMU (x86) Libvirt Virtuozzo CT Libvirt Virtuozzo VM VMware vCenter zVM Attach block volume to instance optional â â â â â â â â â â â Attach tagged block device to instance optional â â â â â â â â â â â Detach block volume from instance optional â â â â â â â â â â â Extend block volume attached to instance optional â â ? ? â â â â ? â â Attach virtual network interface to instance optional â â â â â â â â â â â Attach tagged virtual network interface to instance optional â ? â â â â â â â â â Detach virtual network interface from instance optional â â â â â â â â â â â Set the host in a maintenance mode optional â â â â â â â â â â â Evacuate instances from a host optional ? â ? â â ? ? â â ? ? Rebuild instance optional â â â â â â â â â â ? Rebuild volume backed instance optional â â â â â ? â â â â â Guest instance status mandatory â â â â â â â â â â â Guest host uptime optional â â â â â â â â â â â Guest host ip optional â â â â â â â â â â â Live migrate instance across hosts optional â â â â â â â â â â â Force live migration to complete optional â â â â â â â â â â â Abort an in-progress or queued live migration optional â â â â â â â ? ? â â Launch instance mandatory â â â â â â â â â â â Stop instance CPUs (pause) optional â â â â â â â â â â â Reboot instance optional â â â â â â â â â â â Rescue instance optional â ? â â â â â â â â â Resize instance optional â â â â â â â â â â â Restore instance optional â â â â â â â â â â â Set instance admin password optional â ? â â â â â â â â â Save snapshot of instance disk optional â â â â â â â â â â â Suspend instance optional â â â â â â â â â â â Swap block volumes optional â ? â â â â â â â â â Shutdown instance mandatory â â â â â â â â â â â Trigger crash dump optional â ? â â â â â â â â â Resume instance CPUs (unpause) optional â â â â â â â â â â â uefi boot optional â â â â â â â â â â â Device tags optional â â â â â ? â ? â â â quiesce optional â ? â â â â â â â â â unquiesce optional â ? â â â â â â â â â Attach block volume to multiple instances optional â ? â â â â â â â â â Attach encrypted block volume to server optional â ? ? ? â â â â ? â â Validate image with trusted certificates optional â â â â â â â â â â â File backed memory optional â ? ? ? â â â â â â â Report CPU traits optional â ? â â â â â â â â â SR-IOV ports with resource request optional â â â â â â â â â â â Boot instance with secure encrypted memory optional â â â â â â â â â â â Cache base images for faster instance boot optional â â â â â ? â â â â â Boot instance with an emulated trusted platform module (TPM) optional â â â â â â â â â â â Boot instance with stateless firmware optional â â â â â â â â â â â

Details

- Attach block volume to instance Status: optional. CLI commands: nova volume-attach <server> <volume> Notes: The attach volume operation provides a means to hotplug
additional block storage to a running instance. This allows
storage capabilities to be expanded without interruption of
service. In a cloud model it would be more typical to just
spin up a new instance with large storage, so the ability to
hotplug extra storage is for those cases where the instance
is considered to be more of a pet than cattle. Therefore
this operation is not considered to be mandatory to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova volume-attach <server> <volume>

- nova volume-attach <server> <volume>

Notes: The attach volume operation provides a means to hotplug
additional block storage to a running instance. This allows
storage capabilities to be expanded without interruption of
service. In a cloud model it would be more typical to just
spin up a new instance with large storage, so the ability to
hotplug extra storage is for those cases where the instance
is considered to be more of a pet than cattle. Therefore
this operation is not considered to be mandatory to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Attach tagged block device to instance Status: optional. CLI commands: nova volume-attach <server> <volume> [--tag <tag>] Notes: Attach a block device with a tag to an existing server instance. See
âDevice tagsâ for more information. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova volume-attach <server> <volume> [--tag <tag>]

- nova volume-attach <server> <volume> [--tag <tag>]

Notes: Attach a block device with a tag to an existing server instance. See
âDevice tagsâ for more information.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- Detach block volume from instance Status: optional. CLI commands: nova volume-detach <server> <volume> Notes: See notes for attach volume operation. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova volume-detach <server> <volume>

- nova volume-detach <server> <volume>

Notes: See notes for attach volume operation.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Extend block volume attached to instance Status: optional. CLI commands: cinder extend <volume> <new_size> Notes: The extend volume operation provides a means to extend
the size of an attached volume. This allows volume size
to be expanded without interruption of service.
In a cloud model it would be more typical to just
spin up a new instance with large storage, so the ability to
extend the size of an attached volume is for those cases
where the instance is considered to be more of a pet than cattle.
Therefore this operation is not considered to be mandatory to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: cinder extend <volume> <new_size>

- cinder extend <volume> <new_size>

Notes: The extend volume operation provides a means to extend
the size of an attached volume. This allows volume size
to be expanded without interruption of service.
In a cloud model it would be more typical to just
spin up a new instance with large storage, so the ability to
extend the size of an attached volume is for those cases
where the instance is considered to be more of a pet than cattle.
Therefore this operation is not considered to be mandatory to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): unknown

- Libvirt KVM (s390x): unknown

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: unknown

- VMware vCenter: missing

- zVM: missing

- Attach virtual network interface to instance Status: optional. CLI commands: nova interface-attach <server> Notes: The attach interface operation provides a means to hotplug
additional interfaces to a running instance. Hotplug support
varies between guest OSes and some guests require a reboot for
new interfaces to be detected. This operation allows interface
capabilities to be expanded without interruption of service.
In a cloud model it would be more typical to just spin up a
new instance with more interfaces. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova interface-attach <server>

- nova interface-attach <server>

Notes: The attach interface operation provides a means to hotplug
additional interfaces to a running instance. Hotplug support
varies between guest OSes and some guests require a reboot for
new interfaces to be detected. This operation allows interface
capabilities to be expanded without interruption of service.
In a cloud model it would be more typical to just spin up a
new instance with more interfaces.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Attach tagged virtual network interface to instance Status: optional. CLI commands: nova interface-attach <server> [--tag <tag>] Notes: Attach a virtual network interface with a tag to an existing
server instance. See âDevice tagsâ for more information. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova interface-attach <server> [--tag <tag>]

- nova interface-attach <server> [--tag <tag>]

Notes: Attach a virtual network interface with a tag to an existing
server instance. See âDevice tagsâ for more information.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- Detach virtual network interface from instance Status: optional. CLI commands: nova interface-detach <server> <port_id> Notes: See notes for attach-interface operation. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova interface-detach <server> <port_id>

- nova interface-detach <server> <port_id>

Notes: See notes for attach-interface operation.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Set the host in a maintenance mode Status: optional. CLI commands: nova host-update <host> Notes: This operation allows a host to be placed into maintenance
mode, automatically triggering migration of any running
instances to an alternative host and preventing new
instances from being launched. This is not considered
to be a mandatory operation to support.
The driver methods to implement are âhost_maintenance_modeâ and
âset_host_enabledâ. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): missing Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova host-update <host>

- nova host-update <host>

Notes: This operation allows a host to be placed into maintenance
mode, automatically triggering migration of any running
instances to an alternative host and preventing new
instances from being launched. This is not considered
to be a mandatory operation to support.
The driver methods to implement are âhost_maintenance_modeâ and
âset_host_enabledâ.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): missing Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): missing

- Libvirt LXC: missing

- Libvirt QEMU (x86): missing

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Evacuate instances from a host Status: optional. CLI commands: nova evacuate <server> nova host-evacuate <host> Notes: A possible failure scenario in a cloud environment is the outage
of one of the compute nodes. In such a case the instances of the down
host can be evacuated to another host. It is assumed that the old host
is unlikely ever to be powered back on, otherwise the evacuation
attempt will be rejected. When the instances get moved to the new
host, their volumes get re-attached and the locally stored data is
dropped. That happens in the same way as a rebuild.
This is not considered to be a mandatory operation to support. Driver Support: Ironic: unknown Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): unknown Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: unknown zVM: unknown

Status: optional.

CLI commands: nova evacuate <server> nova host-evacuate <host>

- nova evacuate <server>

- nova host-evacuate <host>

Notes: A possible failure scenario in a cloud environment is the outage
of one of the compute nodes. In such a case the instances of the down
host can be evacuated to another host. It is assumed that the old host
is unlikely ever to be powered back on, otherwise the evacuation
attempt will be rejected. When the instances get moved to the new
host, their volumes get re-attached and the locally stored data is
dropped. That happens in the same way as a rebuild.
This is not considered to be a mandatory operation to support.

Driver Support: Ironic: unknown Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): unknown Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: unknown zVM: unknown

- Ironic: unknown

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): unknown

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: unknown

- Libvirt QEMU (x86): unknown

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: unknown

- zVM: unknown

- Rebuild instance Status: optional. CLI commands: nova rebuild <server> <image> Notes: A possible use case is additional attributes need to be set
to the instance, nova will purge all existing data from the system
and remakes the VM with given information such as âmetadataâ and
âpersonalitiesâ. Though this is not considered to be a mandatory
operation to support. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: unknown

Status: optional.

CLI commands: nova rebuild <server> <image>

- nova rebuild <server> <image>

Notes: A possible use case is additional attributes need to be set
to the instance, nova will purge all existing data from the system
and remakes the VM with given information such as âmetadataâ and
âpersonalitiesâ. Though this is not considered to be a mandatory
operation to support.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: unknown

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: unknown

- Rebuild volume backed instance Status: optional. CLI commands: openstack server rebuild --reimage-boot-volume --image <image> <server> Notes: This will wipe out all existing data in the root volume
of a volume backed instance. This is available from microversion
2.93 and onwards. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: openstack server rebuild --reimage-boot-volume --image <image> <server>

- openstack server rebuild --reimage-boot-volume --image <image> <server>

Notes: This will wipe out all existing data in the root volume
of a volume backed instance. This is available from microversion
2.93 and onwards.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: unknown

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Guest instance status Status: mandatory. Notes: Provides realtime information about the power state of the guest
instance. Since the power state is used by the compute manager for
tracking changes in guests, this operation is considered mandatory to
support. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: mandatory.

Notes: Provides realtime information about the power state of the guest
instance. Since the power state is used by the compute manager for
tracking changes in guests, this operation is considered mandatory to
support.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Guest host uptime Status: optional. Notes: Returns the result of host uptime since power on,
itâs used to report hypervisor status. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

Status: optional.

Notes: Returns the result of host uptime since power on,
itâs used to report hypervisor status.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: complete

- Guest host ip Status: optional. Notes: Returns the ip of this host, itâs used when doing
resize and migration. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: optional.

Notes: Returns the ip of this host, itâs used when doing
resize and migration.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Live migrate instance across hosts Status: optional. CLI commands: nova live-migration <server> nova host-evacuate-live <host> Notes: Live migration provides a way to move an instance off one
compute host, to another compute host. Administrators may use
this to evacuate instances from a host that needs to undergo
maintenance tasks, though of course this may not help if the
host is already suffering a failure. In general instances are
considered cattle rather than pets, so it is expected that an
instance is liable to be killed if host maintenance is required.
It is technically challenging for some hypervisors to provide
support for the live migration operation, particularly those
built on the container based virtualization. Therefore this
operation is not considered mandatory to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova live-migration <server> nova host-evacuate-live <host>

- nova live-migration <server>

- nova host-evacuate-live <host>

Notes: Live migration provides a way to move an instance off one
compute host, to another compute host. Administrators may use
this to evacuate instances from a host that needs to undergo
maintenance tasks, though of course this may not help if the
host is already suffering a failure. In general instances are
considered cattle rather than pets, so it is expected that an
instance is liable to be killed if host maintenance is required.
It is technically challenging for some hypervisors to provide
support for the live migration operation, particularly those
built on the container based virtualization. Therefore this
operation is not considered mandatory to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Force live migration to complete Status: optional. CLI commands: nova live-migration-force-complete <server> <migration> Notes: Live migration provides a way to move a running instance to another
compute host. But it can sometimes fail to complete if an instance has
a high rate of memory or disk page access.
This operation provides the user with an option to assist the progress
of the live migration. The mechanism used to complete the live
migration depends on the underlying virtualization subsystem
capabilities. If libvirt/qemu is used and the post-copy feature is
available and enabled then the force complete operation will cause
a switch to post-copy mode. Otherwise the instance will be suspended
until the migration is completed or aborted. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt KVM (s390x): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt KVM (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova live-migration-force-complete <server> <migration>

- nova live-migration-force-complete <server> <migration>

Notes: Live migration provides a way to move a running instance to another
compute host. But it can sometimes fail to complete if an instance has
a high rate of memory or disk page access.
This operation provides the user with an option to assist the progress
of the live migration. The mechanism used to complete the live
migration depends on the underlying virtualization subsystem
capabilities. If libvirt/qemu is used and the post-copy feature is
available and enabled then the force complete operation will cause
a switch to post-copy mode. Otherwise the instance will be suspended
until the migration is completed or aborted.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt KVM (s390x): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt KVM (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0 Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

- Libvirt KVM (s390x): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

- Libvirt KVM (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

Notes: Requires libvirt>=1.3.3, qemu>=2.5.0

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Abort an in-progress or queued live migration Status: optional. CLI commands: nova live-migration-abort <server> <migration> Notes: Live migration provides a way to move a running instance to another
compute host. But it can sometimes need a large amount of time to complete
if an instance has a high rate of memory or disk page access or is stuck in
queued status if there are too many in-progress live migration jobs in the
queue.
This operation provides the user with an option to abort in-progress live
migrations.
When the live migration job is still in âqueuedâ or âpreparingâ status,
it can be aborted regardless of the type of underneath hypervisor, but once
the job status changes to ârunningâ, only some of the hypervisors support
this feature. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: unknown Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova live-migration-abort <server> <migration>

- nova live-migration-abort <server> <migration>

Notes: Live migration provides a way to move a running instance to another
compute host. But it can sometimes need a large amount of time to complete
if an instance has a high rate of memory or disk page access or is stuck in
queued status if there are too many in-progress live migration jobs in the
queue.
This operation provides the user with an option to abort in-progress live
migrations.
When the live migration job is still in âqueuedâ or âpreparingâ status,
it can be aborted regardless of the type of underneath hypervisor, but once
the job status changes to ârunningâ, only some of the hypervisors support
this feature.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: unknown Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: unknown

- Libvirt Virtuozzo VM: unknown

- VMware vCenter: missing

- zVM: missing

- Launch instance Status: mandatory. Notes: Importing pre-existing running virtual machines on a host is
considered out of scope of the cloud paradigm. Therefore this
operation is mandatory to support in drivers. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: mandatory.

Notes: Importing pre-existing running virtual machines on a host is
considered out of scope of the cloud paradigm. Therefore this
operation is mandatory to support in drivers.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Stop instance CPUs (pause) Status: optional. CLI commands: nova pause <server> Notes: Stopping an instances CPUs can be thought of as roughly
equivalent to suspend-to-RAM. The instance is still present
in memory, but execution has stopped. The problem, however,
is that there is no mechanism to inform the guest OS that
this takes place, so upon unpausing, its clocks will no
longer report correct time. For this reason hypervisor vendors
generally discourage use of this feature and some do not even
implement it. Therefore this operation is considered optional
to support in drivers. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

Status: optional.

CLI commands: nova pause <server>

- nova pause <server>

Notes: Stopping an instances CPUs can be thought of as roughly
equivalent to suspend-to-RAM. The instance is still present
in memory, but execution has stopped. The problem, however,
is that there is no mechanism to inform the guest OS that
this takes place, so upon unpausing, its clocks will no
longer report correct time. For this reason hypervisor vendors
generally discourage use of this feature and some do not even
implement it. Therefore this operation is considered optional
to support in drivers.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: complete

- Reboot instance Status: optional. CLI commands: nova reboot <server> Notes: It is reasonable for a guest OS administrator to trigger a
graceful reboot from inside the instance. A host initiated
graceful reboot requires guest co-operation and a non-graceful
reboot can be achieved by a combination of stop+start. Therefore
this operation is considered optional. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: optional.

CLI commands: nova reboot <server>

- nova reboot <server>

Notes: It is reasonable for a guest OS administrator to trigger a
graceful reboot from inside the instance. A host initiated
graceful reboot requires guest co-operation and a non-graceful
reboot can be achieved by a combination of stop+start. Therefore
this operation is considered optional.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Rescue instance Status: optional. CLI commands: nova rescue <server> Notes: The rescue operation starts an instance in a special
configuration whereby it is booted from an special root
disk image. The goal is to allow an administrator to
recover the state of a broken virtual machine. In general
the cloud model considers instances to be cattle, so if
an instance breaks the general expectation is that it be
thrown away and a new instance created. Therefore this
operation is considered optional to support in drivers. Driver Support: Ironic: complete Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova rescue <server>

- nova rescue <server>

Notes: The rescue operation starts an instance in a special
configuration whereby it is booted from an special root
disk image. The goal is to allow an administrator to
recover the state of a broken virtual machine. In general
the cloud model considers instances to be cattle, so if
an instance breaks the general expectation is that it be
thrown away and a new instance created. Therefore this
operation is considered optional to support in drivers.

Driver Support: Ironic: complete Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: complete

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Resize instance Status: optional. CLI commands: nova resize <server> <flavor> Notes: The resize operation allows the user to change a running
instance to match the size of a different flavor from the one
it was initially launched with. There are many different
flavor attributes that potentially need to be updated. In
general it is technically challenging for a hypervisor to
support the alteration of all relevant config settings for a
running instance. Therefore this operation is considered
optional to support in drivers. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova resize <server> <flavor>

- nova resize <server> <flavor>

Notes: The resize operation allows the user to change a running
instance to match the size of a different flavor from the one
it was initially launched with. There are many different
flavor attributes that potentially need to be updated. In
general it is technically challenging for a hypervisor to
support the alteration of all relevant config settings for a
running instance. Therefore this operation is considered
optional to support in drivers.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Restore instance Status: optional. CLI commands: nova resume <server> Notes: See notes for the suspend operation Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova resume <server>

- nova resume <server>

Notes: See notes for the suspend operation

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Set instance admin password Status: optional. CLI commands: nova set-password <server> Notes: Provides a mechanism to (re)set the password of the administrator
account inside the instance operating system. This requires that the
hypervisor has a way to communicate with the running guest operating
system. Given the wide range of operating systems in existence it is
unreasonable to expect this to be practical in the general case. The
configdrive and metadata service both provide a mechanism for setting
the administrator password at initial boot time. In the case where this
operation were not available, the administrator would simply have to
login to the guest and change the password in the normal manner, so
this is just a convenient optimization. Therefore this operation is
not considered mandatory for drivers to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent. Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent. Libvirt Virtuozzo CT: complete Notes: Requires libvirt>=2.0.0 Libvirt Virtuozzo VM: complete Notes: Requires libvirt>=2.0.0 VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova set-password <server>

- nova set-password <server>

Notes: Provides a mechanism to (re)set the password of the administrator
account inside the instance operating system. This requires that the
hypervisor has a way to communicate with the running guest operating
system. Given the wide range of operating systems in existence it is
unreasonable to expect this to be practical in the general case. The
configdrive and metadata service both provide a mechanism for setting
the administrator password at initial boot time. In the case where this
operation were not available, the administrator would simply have to
login to the guest and change the password in the normal manner, so
this is just a convenient optimization. Therefore this operation is
not considered mandatory for drivers to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent. Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent. Libvirt Virtuozzo CT: complete Notes: Requires libvirt>=2.0.0 Libvirt Virtuozzo VM: complete Notes: Requires libvirt>=2.0.0 VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent.

Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent.

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent.

Notes: Requires libvirt>=1.2.16 and hw_qemu_guest_agent.

- Libvirt Virtuozzo CT: complete Notes: Requires libvirt>=2.0.0

Notes: Requires libvirt>=2.0.0

- Libvirt Virtuozzo VM: complete Notes: Requires libvirt>=2.0.0

Notes: Requires libvirt>=2.0.0

- VMware vCenter: missing

- zVM: missing

- Save snapshot of instance disk Status: optional. CLI commands: nova image-create <server> <name> Notes: The snapshot operation allows the current state of the
instance root disk to be saved and uploaded back into the
glance image repository. The instance can later be booted
again using this saved image. This is in effect making
the ephemeral instance root disk into a semi-persistent
storage, in so much as it is preserved even though the guest
is no longer running. In general though, the expectation is
that the root disks are ephemeral so the ability to take a
snapshot cannot be assumed. Therefore this operation is not
considered mandatory to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: optional.

CLI commands: nova image-create <server> <name>

- nova image-create <server> <name>

Notes: The snapshot operation allows the current state of the
instance root disk to be saved and uploaded back into the
glance image repository. The instance can later be booted
again using this saved image. This is in effect making
the ephemeral instance root disk into a semi-persistent
storage, in so much as it is preserved even though the guest
is no longer running. In general though, the expectation is
that the root disks are ephemeral so the ability to take a
snapshot cannot be assumed. Therefore this operation is not
considered mandatory to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Suspend instance Status: optional. CLI commands: nova suspend <server> Notes: Suspending an instance can be thought of as roughly
equivalent to suspend-to-disk. The instance no longer
consumes any RAM or CPUs, with its live running state
having been preserved in a file on disk. It can later
be restored, at which point it should continue execution
where it left off. As with stopping instance CPUs, it suffers from the fact
that the guest OS will typically be left with a clock that
is no longer telling correct time. For container based
virtualization solutions, this operation is particularly
technically challenging to implement and is an area of
active research. This operation tends to make more sense
when thinking of instances as pets, rather than cattle,
since with cattle it would be simpler to just terminate
the instance instead of suspending. Therefore this operation
is considered optional to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

Status: optional.

CLI commands: nova suspend <server>

- nova suspend <server>

Notes: Suspending an instance can be thought of as roughly
equivalent to suspend-to-disk. The instance no longer
consumes any RAM or CPUs, with its live running state
having been preserved in a file on disk. It can later
be restored, at which point it should continue execution
where it left off. As with stopping instance CPUs, it suffers from the fact
that the guest OS will typically be left with a clock that
is no longer telling correct time. For container based
virtualization solutions, this operation is particularly
technically challenging to implement and is an area of
active research. This operation tends to make more sense
when thinking of instances as pets, rather than cattle,
since with cattle it would be simpler to just terminate
the instance instead of suspending. Therefore this operation
is considered optional to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: missing

- Swap block volumes Status: optional. CLI commands: nova volume-update <server> <attachment> <volume> Notes: The swap volume operation is a mechanism for changing a running
instance so that its attached volume(s) are backed by different
storage in the host. An alternative to this would be to simply
terminate the existing instance and spawn a new instance with the
new storage. In other words this operation is primarily targeted towards
the pet use case rather than cattle, however, it is required for volume
migration to work in the volume service. This is considered optional to
support. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova volume-update <server> <attachment> <volume>

- nova volume-update <server> <attachment> <volume>

Notes: The swap volume operation is a mechanism for changing a running
instance so that its attached volume(s) are backed by different
storage in the host. An alternative to this would be to simply
terminate the existing instance and spawn a new instance with the
new storage. In other words this operation is primarily targeted towards
the pet use case rather than cattle, however, it is required for volume
migration to work in the volume service. This is considered optional to
support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- Shutdown instance Status: mandatory. CLI commands: nova delete <server> Notes: The ability to terminate a virtual machine is required in
order for a cloud user to stop utilizing resources and thus
avoid indefinitely ongoing billing. Therefore this operation
is mandatory to support in drivers. Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Notes: Fails in latest Ubuntu Trusty kernel
from security repository (3.13.0-76-generic), but works in upstream
3.13.x kernels as well as default Ubuntu Trusty latest kernel
(3.13.0-58-generic). Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

Status: mandatory.

CLI commands: nova delete <server>

- nova delete <server>

Notes: The ability to terminate a virtual machine is required in
order for a cloud user to stop utilizing resources and thus
avoid indefinitely ongoing billing. Therefore this operation
is mandatory to support in drivers.

Driver Support: Ironic: complete Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Notes: Fails in latest Ubuntu Trusty kernel
from security repository (3.13.0-76-generic), but works in upstream
3.13.x kernels as well as default Ubuntu Trusty latest kernel
(3.13.0-58-generic). Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: complete zVM: complete

- Ironic: complete

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete Notes: Fails in latest Ubuntu Trusty kernel
from security repository (3.13.0-76-generic), but works in upstream
3.13.x kernels as well as default Ubuntu Trusty latest kernel
(3.13.0-58-generic).

Notes: Fails in latest Ubuntu Trusty kernel
from security repository (3.13.0-76-generic), but works in upstream
3.13.x kernels as well as default Ubuntu Trusty latest kernel
(3.13.0-58-generic).

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: complete

- zVM: complete

- Trigger crash dump Status: optional. CLI commands: nova trigger-crash-dump <server> Notes: The trigger crash dump operation is a mechanism for triggering
a crash dump in an instance. The feature is typically implemented by
injecting an NMI (Non-maskable Interrupt) into the instance. It provides
a means to dump the production memory image as a dump file which is useful
for users. Therefore this operation is considered optional to support. Driver Support: Ironic: complete Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova trigger-crash-dump <server>

- nova trigger-crash-dump <server>

Notes: The trigger crash dump operation is a mechanism for triggering
a crash dump in an instance. The feature is typically implemented by
injecting an NMI (Non-maskable Interrupt) into the instance. It provides
a means to dump the production memory image as a dump file which is useful
for users. Therefore this operation is considered optional to support.

Driver Support: Ironic: complete Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: complete

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Resume instance CPUs (unpause) Status: optional. CLI commands: nova unpause <server> Notes: See notes for the âStop instance CPUsâ operation Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

Status: optional.

CLI commands: nova unpause <server>

- nova unpause <server>

Notes: See notes for the âStop instance CPUsâ operation

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: complete

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: complete

- uefi boot Status: optional. Notes: This allows users to boot a guest with uefi firmware. Driver Support: Ironic: partial Notes: depends on hardware support Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: complete zVM: missing

Status: optional.

Notes: This allows users to boot a guest with uefi firmware.

Driver Support: Ironic: partial Notes: depends on hardware support Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: complete zVM: missing

- Ironic: partial Notes: depends on hardware support

Notes: depends on hardware support

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: complete

- zVM: missing

- Device tags Status: optional. CLI commands: nova boot Notes: This allows users to set tags on virtual devices when creating a
server instance. Device tags are used to identify virtual device
metadata, as exposed in the metadata API and on the config drive.
For example, a network interface tagged with ânic1â will appear in
the metadata along with its bus (ex: PCI), bus address
(ex: 0000:00:02.0), MAC address, and tag (nic1). If multiple networks
are defined, the order in which they appear in the guest operating
system will not necessarily reflect the order in which they are given
in the server boot request. Guests should therefore not depend on
device order to deduce any information about their network devices.
Instead, device role tags should be used. Device tags can be
applied to virtual network interfaces and block devices. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: unknown Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova boot

- nova boot

Notes: This allows users to set tags on virtual devices when creating a
server instance. Device tags are used to identify virtual device
metadata, as exposed in the metadata API and on the config drive.
For example, a network interface tagged with ânic1â will appear in
the metadata along with its bus (ex: PCI), bus address
(ex: 0000:00:02.0), MAC address, and tag (nic1). If multiple networks
are defined, the order in which they appear in the guest operating
system will not necessarily reflect the order in which they are given
in the server boot request. Guests should therefore not depend on
device order to deduce any information about their network devices.
Instead, device role tags should be used. Device tags can be
applied to virtual network interfaces and block devices.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: unknown Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: unknown

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: unknown

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- quiesce Status: optional. Notes: Quiesce the specified instance to prepare for snapshots.
For libvirt, guest filesystems will be frozen through qemu
agent. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

Notes: Quiesce the specified instance to prepare for snapshots.
For libvirt, guest filesystems will be frozen through qemu
agent.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- unquiesce Status: optional. Notes: See notes for the quiesce operation Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

Notes: See notes for the quiesce operation

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Attach block volume to multiple instances Status: optional. CLI commands: nova volume-attach <server> <volume> Notes: The multiattach volume operation is an extension to
the attach volume operation. It allows to attach a
single volume to multiple instances. This operation is
not considered to be mandatory to support.
Note that for the libvirt driver, this is only supported
if qemu<2.10 or libvirt>=3.10. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova volume-attach <server> <volume>

- nova volume-attach <server> <volume>

Notes: The multiattach volume operation is an extension to
the attach volume operation. It allows to attach a
single volume to multiple instances. This operation is
not considered to be mandatory to support.
Note that for the libvirt driver, this is only supported
if qemu<2.10 or libvirt>=3.10.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- Attach encrypted block volume to server Status: optional. CLI commands: nova volume-attach <server> <volume> Notes: This is the same as the attach volume operation
except with an encrypted block device. Encrypted
volumes are controlled via admin-configured volume
types in the block storage service. Since attach
volume is optional this feature is also optional for
compute drivers to support. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Notes: For native QEMU decryption of the
encrypted volume (and rbd support), QEMU>=2.6.0 and libvirt>=2.2.0
are required and only the âluksâ type provider is supported. Otherwise
both âluksâ and âcryptsetupâ types are supported but not natively, i.e.
not all volume types are supported. Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: The same restrictions apply as KVM x86. Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova volume-attach <server> <volume>

- nova volume-attach <server> <volume>

Notes: This is the same as the attach volume operation
except with an encrypted block device. Encrypted
volumes are controlled via admin-configured volume
types in the block storage service. Since attach
volume is optional this feature is also optional for
compute drivers to support.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Notes: For native QEMU decryption of the
encrypted volume (and rbd support), QEMU>=2.6.0 and libvirt>=2.2.0
are required and only the âluksâ type provider is supported. Otherwise
both âluksâ and âcryptsetupâ types are supported but not natively, i.e.
not all volume types are supported. Libvirt LXC: missing Libvirt QEMU (x86): complete Notes: The same restrictions apply as KVM x86. Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: unknown VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): unknown

- Libvirt KVM (s390x): unknown

- Libvirt KVM (x86): complete Notes: For native QEMU decryption of the
encrypted volume (and rbd support), QEMU>=2.6.0 and libvirt>=2.2.0
are required and only the âluksâ type provider is supported. Otherwise
both âluksâ and âcryptsetupâ types are supported but not natively, i.e.
not all volume types are supported.

Notes: For native QEMU decryption of the
encrypted volume (and rbd support), QEMU>=2.6.0 and libvirt>=2.2.0
are required and only the âluksâ type provider is supported. Otherwise
both âluksâ and âcryptsetupâ types are supported but not natively, i.e.
not all volume types are supported.

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete Notes: The same restrictions apply as KVM x86.

Notes: The same restrictions apply as KVM x86.

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: unknown

- VMware vCenter: missing

- zVM: missing

- Validate image with trusted certificates Status: optional. CLI commands: nova boot --trusted-image-certificate-id ... Notes: Since trusted image certification validation is configurable
by the cloud deployer it is considered optional. However, it is
a virt-agnostic feature so there is no good reason that all virt
drivers cannot support the feature since it is mostly just plumbing
user requests through the virt driver when downloading images. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova boot --trusted-image-certificate-id ...

- nova boot --trusted-image-certificate-id ...

Notes: Since trusted image certification validation is configurable
by the cloud deployer it is considered optional. However, it is
a virt-agnostic feature so there is no good reason that all virt
drivers cannot support the feature since it is mostly just plumbing
user requests through the virt driver when downloading images.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: complete Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: complete

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: missing

- zVM: missing

- File backed memory Status: optional. Notes: The file backed memory feature in Openstack allows a Nova node to serve
guest memory from a file backing store. This mechanism uses the libvirt
file memory source, causing guest instance memory to be allocated as files
within the libvirt memory backing directory. This is only supported if
qemu>2.6 and libvirt>4.0.0 Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

Notes: The file backed memory feature in Openstack allows a Nova node to serve
guest memory from a file backing store. This mechanism uses the libvirt
file memory source, causing guest instance memory to be allocated as files
within the libvirt memory backing directory. This is only supported if
qemu>2.6 and libvirt>4.0.0

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): unknown Libvirt KVM (s390x): unknown Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): unknown

- Libvirt KVM (s390x): unknown

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Report CPU traits Status: optional. Notes: The report CPU traits feature in OpenStack allows a Nova node to report
its CPU traits according to CPU mode configuration. This gives users the ability
to boot instances based on desired CPU traits. Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

Notes: The report CPU traits feature in OpenStack allows a Nova node to report
its CPU traits according to CPU mode configuration. This gives users the ability
to boot instances based on desired CPU traits.

Driver Support: Ironic: missing Libvirt KVM (aarch64): unknown Libvirt KVM (ppc64): complete Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): unknown

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- SR-IOV ports with resource request Status: optional. CLI commands: nova boot --nic port-id <neutron port with resource request> ... Notes: To support neutron SR-IOV ports (vnic_type=direct or vnic_type=macvtap)
with resource request the virt driver needs to include the âparent_ifnameâ
key in each subdict which represents a VF under the âpci_passthrough_devicesâ
key in the dict returned from the ComputeDriver.get_available_resource()
call. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: nova boot --nic port-id <neutron port with resource request> ...

- nova boot --nic port-id <neutron port with resource request> ...

Notes: To support neutron SR-IOV ports (vnic_type=direct or vnic_type=macvtap)
with resource request the virt driver needs to include the âparent_ifnameâ
key in each subdict which represents a VF under the âpci_passthrough_devicesâ
key in the dict returned from the ComputeDriver.get_available_resource()
call.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): complete Libvirt LXC: missing Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): complete

- Libvirt LXC: missing

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Boot instance with secure encrypted memory Status: optional. CLI commands: openstack server create <usual server create parameters> Notes: The feature allows VMs to be booted with their memory
hardware-encrypted with a key specific to the VM, to help
protect the data residing in the VM against access from anyone
other than the user of the VM. The Configuration and Security
Guides specify usage of this feature. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: This feature is currently only
available with hosts which support the SEV (Secure Encrypted
Virtualization) technology from AMD. Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: openstack server create <usual server create parameters>

- openstack server create <usual server create parameters>

Notes: The feature allows VMs to be booted with their memory
hardware-encrypted with a key specific to the VM, to help
protect the data residing in the VM against access from anyone
other than the user of the VM. The Configuration and Security
Guides specify usage of this feature.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: This feature is currently only
available with hosts which support the SEV (Secure Encrypted
Virtualization) technology from AMD. Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): partial Notes: This feature is currently only
available with hosts which support the SEV (Secure Encrypted
Virtualization) technology from AMD.

Notes: This feature is currently only
available with hosts which support the SEV (Secure Encrypted
Virtualization) technology from AMD.

- Libvirt LXC: missing

- Libvirt QEMU (x86): missing

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Cache base images for faster instance boot Status: optional. CLI commands: openstack server create <usual server create parameters> Notes: Drivers supporting this feature cache base images on the compute host so
that subsequent boots need not incur the expense of downloading them. Partial
support entails caching an image after the first boot that uses it. Complete
support allows priming the cache so that the first boot also benefits. Image
caching support is tunable via config options in the [image_cache] group. Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: partial zVM: missing

Status: optional.

CLI commands: openstack server create <usual server create parameters>

- openstack server create <usual server create parameters>

Notes: Drivers supporting this feature cache base images on the compute host so
that subsequent boots need not incur the expense of downloading them. Partial
support entails caching an image after the first boot that uses it. Complete
support allows priming the cache so that the first boot also benefits. Image
caching support is tunable via config options in the [image_cache] group.

Driver Support: Ironic: missing Libvirt KVM (aarch64): complete Libvirt KVM (ppc64): complete Libvirt KVM (s390x): complete Libvirt KVM (x86): complete Libvirt LXC: unknown Libvirt QEMU (x86): complete Libvirt Virtuozzo CT: complete Libvirt Virtuozzo VM: complete VMware vCenter: partial zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): complete

- Libvirt KVM (ppc64): complete

- Libvirt KVM (s390x): complete

- Libvirt KVM (x86): complete

- Libvirt LXC: unknown

- Libvirt QEMU (x86): complete

- Libvirt Virtuozzo CT: complete

- Libvirt Virtuozzo VM: complete

- VMware vCenter: partial

- zVM: missing

- Boot instance with an emulated trusted platform module (TPM) Status: optional. CLI commands: openstack server create <usual server create parameters> Notes: Allows VMs to be booted with an emulated trusted platform module (TPM)
device. Only lifecycle operations performed by the VM owner are supported, as
the userâs credentials are required to unlock the virtual device files on the
host. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: Move operations are not yet supported. Libvirt LXC: missing Libvirt QEMU (x86): partial Notes: Move operations are not yet supported. Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: openstack server create <usual server create parameters>

- openstack server create <usual server create parameters>

Notes: Allows VMs to be booted with an emulated trusted platform module (TPM)
device. Only lifecycle operations performed by the VM owner are supported, as
the userâs credentials are required to unlock the virtual device files on the
host.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: Move operations are not yet supported. Libvirt LXC: missing Libvirt QEMU (x86): partial Notes: Move operations are not yet supported. Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): partial Notes: Move operations are not yet supported.

Notes: Move operations are not yet supported.

- Libvirt LXC: missing

- Libvirt QEMU (x86): partial Notes: Move operations are not yet supported.

Notes: Move operations are not yet supported.

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

- Boot instance with stateless firmware Status: optional. CLI commands: openstack server create <usual server create parameters> Notes: The feature allows VMs to be booted with read-only firmware image without
NVRAM file. This feature is especially useful for confidential computing use
case because it allows more complete measurement of elements involved in
the boot chain and disables the potential attack serface from hypervisors. Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: This feature is supported only with UEFI firmware Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

Status: optional.

CLI commands: openstack server create <usual server create parameters>

- openstack server create <usual server create parameters>

Notes: The feature allows VMs to be booted with read-only firmware image without
NVRAM file. This feature is especially useful for confidential computing use
case because it allows more complete measurement of elements involved in
the boot chain and disables the potential attack serface from hypervisors.

Driver Support: Ironic: missing Libvirt KVM (aarch64): missing Libvirt KVM (ppc64): missing Libvirt KVM (s390x): missing Libvirt KVM (x86): partial Notes: This feature is supported only with UEFI firmware Libvirt LXC: missing Libvirt QEMU (x86): missing Libvirt Virtuozzo CT: missing Libvirt Virtuozzo VM: missing VMware vCenter: missing zVM: missing

- Ironic: missing

- Libvirt KVM (aarch64): missing

- Libvirt KVM (ppc64): missing

- Libvirt KVM (s390x): missing

- Libvirt KVM (x86): partial Notes: This feature is supported only with UEFI firmware

Notes: This feature is supported only with UEFI firmware

- Libvirt LXC: missing

- Libvirt QEMU (x86): missing

- Libvirt Virtuozzo CT: missing

- Libvirt Virtuozzo VM: missing

- VMware vCenter: missing

- zVM: missing

Notes:

- This document is a continuous work in progress
