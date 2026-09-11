# Configuration Â¶

- Active-active L3 Gateway with Multihoming Why Prerequisites How Use cases Example

- Why

- Prerequisites

- How

- Use cases

- Example

- Address Scopes Accessing address scopes Backwards compatibility Create shared address scopes as an administrative user Routing with address scopes for non-privileged users

- Accessing address scopes

- Backwards compatibility

- Create shared address scopes as an administrative user

- Routing with address scopes for non-privileged users

- Automatic allocation of network topologies Enabling the deployment for auto-allocation Get Me A Network Validating the requirements for auto-allocation Project resources created by auto-allocation Compatibility notes

- Enabling the deployment for auto-allocation

- Get Me A Network

- Validating the requirements for auto-allocation

- Project resources created by auto-allocation

- Compatibility notes

- Availability Zones Use case Required extensions Network scheduler Router scheduler L3 high availability DHCP high availability

- Use case

- Required extensions

- Network scheduler

- Router scheduler

- L3 high availability

- DHCP high availability

- BGP Dynamic Routing Example configuration Prefix advertisement Operation with Distributed Virtual Routers (DVR) IPv6 High availability

- Example configuration

- Prefix advertisement

- Operation with Distributed Virtual Routers (DVR)

- IPv6

- High availability

- BGP Floating IPs over L2 Segmented Networks Configuring the Neutron API side The BGP agent Setting-up BGP peering with the switches Setting-up physical network names Setting-up the provider network Setting-up the 2nd segment Setting-up the provider subnets for the BGP next HOP routing Adding a subnet for VM floating IPs and router gateways Setting-up BGP advertizing Per project operation Cumulus switch configuration Verification

- Configuring the Neutron API side

- The BGP agent

- Setting-up BGP peering with the switches

- Setting-up physical network names

- Setting-up the provider network

- Setting-up the 2nd segment

- Setting-up the provider subnets for the BGP next HOP routing

- Adding a subnet for VM floating IPs and router gateways

- Setting-up BGP advertizing

- Per project operation

- Cumulus switch configuration

- Verification

- Agents and Services Configuration options L2 agents Metadata agent DHCP agent L3 agent External processes run by agents

- Configuration options

- L2 agents

- Metadata agent

- DHCP agent

- L3 agent

- External processes run by agents

- DNS Integration The Networking service internal DNS resolution

- The Networking service internal DNS resolution

- DNS Integration with an External Service Configuring OpenStack Networking for integration with an external DNS service Use case 1: Floating IPs are published with associated port DNS attributes Use case 2: Floating IPs are published in the external DNS service Use case 3: Ports are published directly in the external DNS service Performance considerations Configuration of the externally accessible network for use cases 3b and 3c The portâs dns_assignment attribute with use case 3

- Configuring OpenStack Networking for integration with an external DNS service

- Use case 1: Floating IPs are published with associated port DNS attributes

- Use case 2: Floating IPs are published in the external DNS service

- Use case 3: Ports are published directly in the external DNS service

- Performance considerations

- Configuration of the externally accessible network for use cases 3b and 3c

- The portâs dns_assignment attribute with use case 3

- DNS Resolution for Instances Case 1: Each virtual network uses unique DNS resolver(s) Case 2: DHCP agents forward DNS queries from instances

- Case 1: Each virtual network uses unique DNS resolver(s)

- Case 2: DHCP agents forward DNS queries from instances

- Distributed Virtual Routing with VRRP Configuration example Known limitations

- Configuration example

- Known limitations

- Experimental Features Framework

- Floating IP Port Forwarding Configuring floating IP port forwarding

- Configuring floating IP port forwarding

- IPAM Configuration The basics Known limitations

- The basics

- Known limitations

- IPv6 Neutron subnets and the IPv6 API attributes Project network considerations Router support Advanced services Security considerations OpenStack control & management network considerations Prefix delegation

- Neutron subnets and the IPv6 API attributes

- Project network considerations

- Router support

- Advanced services

- Security considerations

- OpenStack control & management network considerations

- Prefix delegation

- Macvtap Mechanism Driver Prerequisites Architecture Example configuration Network traffic flow

- Prerequisites

- Architecture

- Example configuration

- Network traffic flow

- Metadata Service Caching

- Metadata Service Query Rate-limiting

- ML2 Plug-in Architecture Configuration Reference implementations

- Architecture

- Configuration

- Reference implementations

- MTU Considerations Jumbo frames Instance network interfaces (VIFs) Networks with enabled vlan transparency

- Jumbo frames

- Instance network interfaces (VIFs)

- Networks with enabled vlan transparency

- NDP Proxy Configuration of NDP proxy User workflow Known limitations

- Configuration of NDP proxy

- User workflow

- Known limitations

- Network Segment Ranges Why you need it How it works Default network segment ranges Example configuration Workflow Known limitations

- Why you need it

- How it works

- Default network segment ranges

- Example configuration

- Workflow

- Known limitations

- Open vSwitch with DPDK Datapath The basics Using vhost-user interfaces Using vhost-user multiqueue Known limitations

- The basics

- Using vhost-user interfaces

- Using vhost-user multiqueue

- Known limitations

- Open vSwitch Hardware Offloading The basics Using Open vSwitch hardware offloading

- The basics

- Using Open vSwitch hardware offloading

- Open vSwitch Native Firewall Driver Configuring heterogeneous firewall drivers Prerequisites Enable the native OVS firewall driver Using GRE tunnels inside VMs with OVS firewall driver Differences between OVS and iptables firewall drivers Open Flow rules processing considerations Permitted ethertypes References

- Configuring heterogeneous firewall drivers

- Prerequisites

- Enable the native OVS firewall driver

- Using GRE tunnels inside VMs with OVS firewall driver

- Differences between OVS and iptables firewall drivers

- Open Flow rules processing considerations

- Permitted ethertypes

- References

- Packet Logging Framework ML2/OVN Driver ML2/OVS Driver

- ML2/OVN Driver

- ML2/OVS Driver

- Quality of Service (QoS) Supported QoS rule types L3 QoS support Configuration User workflow

- Supported QoS rule types

- L3 QoS support

- Configuration

- User workflow

- Quality of Service (QoS): Guaranteed Minimum Bandwidth Limitations Placement pre-requisites Nova pre-requisites Neutron pre-requisites Propagation of resource information Sample usage On Healing of Allocations Debugging Links

- Limitations

- Placement pre-requisites

- Nova pre-requisites

- Neutron pre-requisites

- Propagation of resource information

- Sample usage

- On Healing of Allocations

- Debugging

- Links

- Quality of Service (QoS): Guaranteed Minimum Packet Rate Limitations Placement pre-requisites Nova pre-requisites Neutron pre-requisites Propagation of resource information Sample usage On Healing of Allocations Debugging Links

- Limitations

- Placement pre-requisites

- Nova pre-requisites

- Neutron pre-requisites

- Propagation of resource information

- Sample usage

- On Healing of Allocations

- Debugging

- Links

- Role-Based Access Control (RBAC) Supported objects for sharing with specific projects Sharing an object with specific projects Sharing a network with specific projects Sharing a QoS policy with specific projects Sharing a security group with specific projects Sharing an address scope with specific projects Sharing a subnet pool with specific projects Sharing an address group with specific projects How the âsharedâ flag relates to these entries Allowing a network to be used as an external network Preventing regular users from sharing objects with each other Improve database RBAC query operations

- Supported objects for sharing with specific projects

- Sharing an object with specific projects

- Sharing a network with specific projects

- Sharing a QoS policy with specific projects

- Sharing a security group with specific projects

- Sharing an address scope with specific projects

- Sharing a subnet pool with specific projects

- Sharing an address group with specific projects

- How the âsharedâ flag relates to these entries

- Allowing a network to be used as an external network

- Preventing regular users from sharing objects with each other

- Improve database RBAC query operations

- Routed provider networks Prerequisites Example configuration Create a routed provider network Migrating non-routed networks to routed Routed provider networks as external networks for tenant routed networks Multiple routed provider segments per host

- Prerequisites

- Example configuration

- Create a routed provider network

- Migrating non-routed networks to routed

- Routed provider networks as external networks for tenant routed networks

- Multiple routed provider segments per host

- Router flavors with the L3 OVN service plugin

- SR-IOV The basics Using SR-IOV interfaces SR-IOV with ConnectX-3/ConnectX-3 Pro Dual Port Ethernet SR-IOV with InfiniBand Known limitations

- The basics

- Using SR-IOV interfaces

- SR-IOV with ConnectX-3/ConnectX-3 Pro Dual Port Ethernet

- SR-IOV with InfiniBand

- Known limitations

- Service Function Chaining Architecture Resources Operations

- Architecture

- Resources

- Operations

- Service Subnets Operation Usage

- Operation

- Usage

- Subnet Onboarding How it works

- How it works

- Subnet Pools Why you need them How they work Quotas Default subnet pools

- Why you need them

- How they work

- Quotas

- Default subnet pools

- Trunking Operation Example configuration Using trunks and subports inside an instance Trunk states Limitations and issues

- Operation

- Example configuration

- Using trunks and subports inside an instance

- Trunk states

- Limitations and issues

- WSGI Usage with the Neutron API WSGI Application Neutron API behind uwsgi Start Neutron RPC server Neutron Worker Processes

- WSGI Application

- Neutron API behind uwsgi

- Start Neutron RPC server

- Neutron Worker Processes

Note

For general configuration, see the Configuration Reference .
