# Quality of Service (QoS): Guaranteed Minimum Packet Rate Â¶

Similarly to how bandwidth can be a limiting factor of a network interface,
packet processing capacity tend to be a limiting factor of the soft switching
solutions like OVS. At the same time certain applications are dependent on not
just guaranteed bandwidth, but also on guaranteed packet rate to function
properly. OpenStack already supports bandwidth guarantees via the
minimum bandwidth QoS policy rules, which is described in detail in Quality of Service (QoS): Guaranteed Minimum Bandwidth . Itâs recommended to read Guaranteed Minimum Bandwidth
guide first, but itâs not strictly required.

Just like Quality of Service (QoS): Guaranteed Minimum Bandwidth guide, this chapter does not aim to replace Nova or
Placement documentation in any way, but gives a brief overview of the feature
and explains how it can be configured.

In a similar way to guaranteed bandwidth, we can distinguish two levels of
enforcement for guaranteeing packet processing capacity constraint:

- placement: Avoiding over-subscription when placing (scheduling) VMs and their
ports.

placement: Avoiding over-subscription when placing (scheduling) VMs and their
ports.

- data plane: Enforcing the guarantee on the soft switch

data plane: Enforcing the guarantee on the soft switch

Note

At the time of writing this guide, only placement enforcement is supported.
For detailed list of supported enforcement types and backends, please refer
to QoS configuration chapter of the Networking Guide .

The solution needs to differentiate between two different deployment scenarios:

- The packet processing functionality is implemented on the compute host CPUs
and therefore packets processed from both ingress and egress directions are
handled by the same set of CPU cores. This is the case in the
non-hardware-offloaded OVS deployments. In this scenario OVS represents a
single packet processing resource pool, which is represented with a
single resource class called NET_PACKET_RATE_KILOPACKET_PER_SEC .

The packet processing functionality is implemented on the compute host CPUs
and therefore packets processed from both ingress and egress directions are
handled by the same set of CPU cores. This is the case in the
non-hardware-offloaded OVS deployments. In this scenario OVS represents a
single packet processing resource pool, which is represented with a
single resource class called NET_PACKET_RATE_KILOPACKET_PER_SEC .

- The packet processing functionality is implemented in a specialized hardware
where the incoming and outgoing packets are handled by independent
hardware resources. This is the case for hardware-offloaded OVS. In this
scenario a single OVS has two independent resource pools one for the
incoming packets and one for the outgoing packets. Therefore these needs to
be represented with two different resource classes NET_PACKET_RATE_EGR_KILOPACKET_PER_SEC and NET_PACKET_RATE_IGR_KILOPACKET_PER_SEC .

The packet processing functionality is implemented in a specialized hardware
where the incoming and outgoing packets are handled by independent
hardware resources. This is the case for hardware-offloaded OVS. In this
scenario a single OVS has two independent resource pools one for the
incoming packets and one for the outgoing packets. Therefore these needs to
be represented with two different resource classes NET_PACKET_RATE_EGR_KILOPACKET_PER_SEC and NET_PACKET_RATE_IGR_KILOPACKET_PER_SEC .

## Limitations Â¶

Since Guaranteed Minimum Packet Rate and Guaranteed Minimum Bandwidth features
have a lot in common, they also share certain limitations.

- A pre-created port with a minimum-packet-rate rule must be passed
when booting a server ( openstack server create ). Passing a network
with a minimum-packet-rate rule at boot is not supported because of
technical reasons (in this case the port is created too late for
Neutron to affect scheduling).

A pre-created port with a minimum-packet-rate rule must be passed
when booting a server ( openstack server create ). Passing a network
with a minimum-packet-rate rule at boot is not supported because of
technical reasons (in this case the port is created too late for
Neutron to affect scheduling).

- Changing the guarantee of a QoS policy (adding/deleting a minimum_packet_rate rule, or changing the min_kpps field of a minimum_packet_rate rule) is only possible while the policy is not in
effect. That is ports of the QoS policy are not yet bound by Nova. Requests
to change guarantees of in-use policies are rejected.

Changing the guarantee of a QoS policy (adding/deleting a minimum_packet_rate rule, or changing the min_kpps field of a minimum_packet_rate rule) is only possible while the policy is not in
effect. That is ports of the QoS policy are not yet bound by Nova. Requests
to change guarantees of in-use policies are rejected.

- Changing the QoS policy of the port with new minimum_packet_rate rules
changes placement allocations from Yoga release.
If the VM was booted with port without QoS policy and minimum_packet_rate rules the port update succeeds but placement allocations will not change.
The same is true if the port had no allocation record in Placement before
QoS policy update. But if the VM was booted with a port with QoS policy and minimum_packet_rate rules the update is possible and the allocations are
changed in placement as well.

Changing the QoS policy of the port with new minimum_packet_rate rules
changes placement allocations from Yoga release.
If the VM was booted with port without QoS policy and minimum_packet_rate rules the port update succeeds but placement allocations will not change.
The same is true if the port had no allocation record in Placement before
QoS policy update. But if the VM was booted with a port with QoS policy and minimum_packet_rate rules the update is possible and the allocations are
changed in placement as well.

Note

As it is possible to update a port to remove the QoS policy, updating it
back to have QoS policy with minimum_packet_rate rule will not result in placement allocation record. In this case only dataplane enforcement will
happen.

Note

Updating the minimum_packet_rate rule of a QoS policy that is attached
to a port which is bound to a VM is still not possible.

- When QoS is used with a trunk, Placement enforcement is applied only to the
trunkâs parent port. Subports are not going to have Placement allocation.
As a workaround, parent port QoS policy should take into account subports
needs and request enough minimum packet rate resources to accommodate every
port in the trunk.

When QoS is used with a trunk, Placement enforcement is applied only to the
trunkâs parent port. Subports are not going to have Placement allocation.
As a workaround, parent port QoS policy should take into account subports
needs and request enough minimum packet rate resources to accommodate every
port in the trunk.

## Placement pre-requisites Â¶

Placement must support microversion 1.36 .
This was first released in Train.

## Nova pre-requisites Â¶

Nova must support top of microversion 2.72 ,
additionally the Nova Xena release is needed to support the new port-resource-request-groups Neutron API extension.

Not all Nova virt drivers are supported, please refer to the Virt Driver Support section of the Nova Admin Guide .

## Neutron pre-requisites Â¶

Neutron must support the following API extensions:

- qos-pps-minimum

qos-pps-minimum

- port-resource-request-groups

port-resource-request-groups

These were all first released in Yoga.

### Neutron DB sanitization Â¶

The resource_request field of the Neutron port is used to express the
resource needs of the port. The information in this field is calculated from
the QoS policy rules attached to the port. Initially, only the minimum
bandwidth rule was used as a source of requested resources. The format of resource_request looked like this:

{ "required": [<CUSTOM_PHYSNET_ traits>, <CUSTOM_VNIC_TYPE traits>], "resources": { <NET_BW_[E|I]GR_KILOBIT_PER_SEC resource class name>: <requested bandwidth amount from the QoS policy> } },

This structure allowed to describe only one group of resources and traits,
which was sufficient at the time. However, with the introduction of QoS minimum
packet rate rule, ports can now have multiple sources of requested resources
and traits. Because of that, the format of resource_request field was
incapable of expressing such request and it had to be changed.

To solve this issue, port-resource-request-groups extension was
added in Neutron Yoga release. It provides support for the new format of resource_request field, that allows to request multiple groups of
resources and traits from the same RP subtree. The new format looks like this:

{ "request_groups": [ { "id": <min-pps-group-uuid> "required": [<CUSTOM_VNIC_TYPE traits>], "resources": { NET_PACKET_RATE_[E|I]GR_KILOPACKET_PER_SEC: <amount requested via the QoS policy> } }, { "id": <min-bw-group-uuid> "required": [<CUSTOM_PHYSNET_ traits>, <CUSTOM_VNIC_TYPE traits>], "resources": { <NET_BW_[E|I]GR_KILOBIT_PER_SEC resource class name>: <requested bandwidth amount from the QoS policy> } } ], "same_subtree": [ <min-pps-group-uuid>, <min-bw-group-uuid> ] }

The main drawback about the new structure of resource_request field is lack
of backwards compatibility. This can cause issues if ml2_port_bindings table in Neutron DB contains port bindings that were created before the
introduction of port-resource-request-groups extension. Because port-resource-request-groups extension is enabled by default in Yoga
release, itâs necessary to perform DB sanitization before upgrading Neutron to
Yoga.

DB sanitization will ensure that every row of ml2_port_bindings table
uses the new format. Upgrade check can be run before DB sanitization, to see
if there are any rows in the DB that require sanitization.

$ neutron-status upgrade check # If 'Port Binding profile sanity check' fails, DB sanitization is needed $ neutron-sanitize-port-binding-profile-allocation --config-file /etc/neutron/neutron.conf

### Supported drivers and agents Â¶

In release Yoga the following agent-based ML2 mechanism drivers are
supported:

- Open vSwitch ( openvswitch ) vnic_types: normal , direct

Open vSwitch ( openvswitch ) vnic_types: normal , direct

### neutron-server config Â¶

QoS minimum packet rate rule requires exactly the same configuration in the neutron-server as QoS minimum bandwidth rule. Please refer to neutron-server config section of Quality of Service (QoS): Guaranteed Minimum Bandwidth guide for more details.

### neutron-openvswitch-agent config Â¶

Set the agent configuration as the authentic source of the resources available.
Depending on OVS deployment type, packet processing capacity can be configured
with:

- ovs.resource_provider_packet_processing_without_direction Format for this option is <hypervisor>:<packet_rate> . This option should
be used for non-hardware-offloaded OVS deployments.

ovs.resource_provider_packet_processing_without_direction Format for this option is <hypervisor>:<packet_rate> . This option should
be used for non-hardware-offloaded OVS deployments.

- ovs.resource_provider_packet_processing_with_direction Format for this option is <hypervisor>:<egress_packet_rate>:<ingress_packet_rate> . You may set only
one direction and omit the other. This option should be used for
hardware-offloaded OVS deployments.

ovs.resource_provider_packet_processing_with_direction

Format for this option is <hypervisor>:<egress_packet_rate>:<ingress_packet_rate> . You may set only
one direction and omit the other. This option should be used for
hardware-offloaded OVS deployments.

Regardless if direction-less or direction-oriented packet processing mode is
used, configuration is always applied to the whole OVS instance.

Note

egress / ingress is meant from the VM point of view.
That is egress = cloud server upload, ingress = download.

Egress and ingress available packet rate values are in kilo packet/sec (kpps) .

Direction-less and direction-oriented modes are mutually exclusive options.
Only one can be used at a time.

The hypervisor name is optional, and needs to be set only in the rare case
cases. For more information, please refer to Neutron agent documentation.

If desired, resource provider inventory fields can be tweaked on a
per-agent basis by setting ovs.resource_provider_packet_processing_inventory_defaults .
Valid values are all the optional parameters of the update resource provider inventory call .

/etc/neutron/plugins/ml2/ovs_agent.ini (on compute and network nodes):

[ovs] resource_provider_packet_processing_with_direction = :10000000:10000000,... #resource_provider_packet_processing_inventory_defaults = step_size:1000,...

## Propagation of resource information Â¶

Propagation of resource information is explained in detail in Quality of Service (QoS): Guaranteed Minimum Bandwidth guide .

## Sample usage Â¶

Network and QoS policies (together with their rules) are usually pre-created
by a cloud admin:

# as admin $ openstack network create net0 $ openstack subnet create subnet0 \ --network net0 \ --subnet-range 10 .0.4.0/24 $ openstack network qos policy create policy0 $ openstack network qos rule create policy0 \ --type minimum-packet-rate \ --min-kpps 1000000 \ --egress $ openstack network qos rule create policy0 \ --type minimum-packet-rate \ --min-kpps 1000000 \ --ingress

Then a normal user can use the pre-created policy to create ports and boot
servers with those ports:

# as an unprivileged user # an ordinary soft-switched port: `` --vnic-type normal `` is the default $ openstack port create port-normal-qos \ --network net0 \ --qos-policy policy0 $ openstack server create server0 \ --os-compute-api-version 2 .72 \ --flavor cirros256 \ --image cirros-0.5.2-x86_64-disk \ --port port-normal-qos

## On Healing of Allocations Â¶

Since Placement carries a global view of a cloud deploymentâs resources
(what is available, what is used) it may in some conditions get out of sync
with reality.

One important case stems from OpenStack not having distributed transactions to
allocate resources provided by multiple OpenStack components (here Nova and
Neutron). There are known race conditions in which Placementâs view may get
out of sync with reality. The design knowingly minimizes the race condition
windows, but there are known problems:

- If a QoS policy is modified after Nova read a portâs resource_request but before the port is bound its state before the modification will be
applied.

If a QoS policy is modified after Nova read a portâs resource_request but before the port is bound its state before the modification will be
applied.

- If a bound port with a resource allocation is deleted. The portâs allocation
is leaked. https://bugs.launchpad.net/nova/+bug/1820588

If a bound port with a resource allocation is deleted. The portâs allocation
is leaked. https://bugs.launchpad.net/nova/+bug/1820588

Note

Deleting a bound port has no known use case. Please consider detaching
the interface first by openstack server remove port instead.

Incorrect allocations may be fixed by:

- Moving the server, which will delete the wrong allocation and create the
correct allocation. Moving servers fixes local overallocations.

Moving the server, which will delete the wrong allocation and create the
correct allocation. Moving servers fixes local overallocations.

- With placement heal_allocations tool.

With placement heal_allocations tool.

- Manually, by using openstack resource provider allocation set / delete .

Manually, by using openstack resource provider allocation set / delete .

## Debugging Â¶

- Is Nova running at least Xena release and Neutron at least the Yoga release?

Is Nova running at least Xena release and Neutron at least the Yoga release?

- Are qos-pps-minimum and port-resource-request-groups extensions
available?

Are qos-pps-minimum and port-resource-request-groups extensions
available?

$ openstack extension show qos-pps-minimum $ openstack extension show port-resource-request-groups

- Is the placement service plugin enabled in neutron-server?

Is the placement service plugin enabled in neutron-server?

- Is resource_provider_packet_processing_with_direction or resource_provider_packet_processing_without_direction configured for the
relevant neutron agent?

Is resource_provider_packet_processing_with_direction or resource_provider_packet_processing_without_direction configured for the
relevant neutron agent?

- Was the agent restarted since changing the configuration file?

Was the agent restarted since changing the configuration file?

- Is resource_provider_packet_processing_with_direction or resource_provider_packet_processing_without_direction reaching
neutron-server?

Is resource_provider_packet_processing_with_direction or resource_provider_packet_processing_without_direction reaching
neutron-server?

# as admin $ openstack network agent show ... -c configuration -f json

Please find an example in section Propagation of resource information .

- Did neutron-server successfully sync to Placement?

Did neutron-server successfully sync to Placement?

# as admin $ openstack network agent show ... | grep resources_synced

Please find an example in section Propagation of resource information .

- Is the resource provider tree correct? Is the root a compute host? One level
below the agents?

Is the resource provider tree correct? Is the root a compute host? One level
below the agents?

$ openstack --os-placement-api-version 1 .17 resource provider list +--------------------------------------+------------------------------------------+------------+--------------------------------------+--------------------------------------+ | uuid                                 | name                                     | generation | root_provider_uuid                   | parent_provider_uuid                 | +--------------------------------------+------------------------------------------+------------+--------------------------------------+--------------------------------------+ | 3b36d91e-bf60-460f-b1f8-3322dee5cdfd | devstack0                                |          2 | 3b36d91e-bf60-460f-b1f8-3322dee5cdfd | None                                 | | 89ca1421-5117-5348-acab-6d0e2054239c | devstack0:Open vSwitch agent             |          0 | 3b36d91e-bf60-460f-b1f8-3322dee5cdfd | 3b36d91e-bf60-460f-b1f8-3322dee5cdfd | +--------------------------------------+------------------------------------------+------------+--------------------------------------+--------------------------------------+

- Does Placement have the expected traits?

Does Placement have the expected traits?

# as admin $ openstack --os-placement-api-version 1 .17 trait list | awk '/CUSTOM_/ { print $2 }' | sort CUSTOM_VNIC_TYPE_NORMAL CUSTOM_VNIC_TYPE_SMART_NIC CUSTOM_VNIC_TYPE_VDPA

- Do the OVS agent resource provider have the proper trait associations and
inventories?

Do the OVS agent resource provider have the proper trait associations and
inventories?

# as admin $ openstack --os-placement-api-version 1 .17 resource provider trait list <RP-UUID> $ openstack --os-placement-api-version 1 .17 resource provider inventory list <RP-UUID>

- Does the QoS policy have a minimum-packet-rate rule?

Does the QoS policy have a minimum-packet-rate rule?

- Does the port have the proper policy?

Does the port have the proper policy?

- Does the port have a resource_request ?

Does the port have a resource_request ?

# as admin $ openstack port show port-normal-qos | grep resource_request

- Was the server booted with a port (as opposed to a network)?

Was the server booted with a port (as opposed to a network)?

- Did nova allocate resources for the server in Placement?

Did nova allocate resources for the server in Placement?

# as admin $ openstack --os-placement-api-version 1 .17 resource provider allocation show <SERVER-UUID>

- Does the allocation have a part on the expected OVS agent resource provider?

Does the allocation have a part on the expected OVS agent resource provider?

# as admin $ openstack --os-placement-api-version 1 .17 resource provider show --allocations <RP-UUID>

- Did placement manage to produce an allocation candidate list to nova during
scheduling?

Did placement manage to produce an allocation candidate list to nova during
scheduling?

- Did nova manage to schedule the server?

Did nova manage to schedule the server?

- Did nova tell neutron which OVS agent resource provider was allocated to
satisfy the packet rate request?

Did nova tell neutron which OVS agent resource provider was allocated to
satisfy the packet rate request?

# as admin $ openstack port show port-normal-qos | grep binding.profile.*allocation

- Did neutron manage to bind the port?

Did neutron manage to bind the port?

## Links Â¶

- Nova documentation on using a port with resource_request API Guide Admin Guide

Nova documentation on using a port with resource_request

- API Guide

API Guide

- Admin Guide

Admin Guide

- Neutron spec: QoS minimum guaranteed packet rate on specs.openstack.org on review.opendev.org

Neutron spec: QoS minimum guaranteed packet rate

- on specs.openstack.org

on specs.openstack.org

- on review.opendev.org

on review.opendev.org

- Nova spec: QoS minimum guaranteed packet rate on specs.openstack.org on review.opendev.org

Nova spec: QoS minimum guaranteed packet rate

- on specs.openstack.org

on specs.openstack.org

- on review.opendev.org

on review.opendev.org

- Relevant OpenStack Networking API references https://docs.openstack.org/api-ref/network/v2/#agent-resources-synced-extension https://docs.openstack.org/api-ref/network/v2/#port-resource-request https://docs.openstack.org/api-ref/network/v2/#port-resource-request-groups https://docs.openstack.org/api-ref/network/v2/#qos-minimum-packet-rate-rules

Relevant OpenStack Networking API references

- https://docs.openstack.org/api-ref/network/v2/#agent-resources-synced-extension

https://docs.openstack.org/api-ref/network/v2/#agent-resources-synced-extension

- https://docs.openstack.org/api-ref/network/v2/#port-resource-request

https://docs.openstack.org/api-ref/network/v2/#port-resource-request

- https://docs.openstack.org/api-ref/network/v2/#port-resource-request-groups

https://docs.openstack.org/api-ref/network/v2/#port-resource-request-groups

- https://docs.openstack.org/api-ref/network/v2/#qos-minimum-packet-rate-rules

https://docs.openstack.org/api-ref/network/v2/#qos-minimum-packet-rate-rules

- Microversion histories Compute 2.72 Placement 1.36

Microversion histories

- Compute 2.72

Compute 2.72

- Placement 1.36

Placement 1.36

- Implementation on review.opendev.org

Implementation

- on review.opendev.org

on review.opendev.org

- Known Bugs Bandwidth resource is leaked this issue also affects
packet rate resources.

Known Bugs

- Bandwidth resource is leaked this issue also affects
packet rate resources.

Bandwidth resource is leaked this issue also affects
packet rate resources.
