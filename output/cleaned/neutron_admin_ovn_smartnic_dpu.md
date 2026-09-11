# Off-path SmartNIC DPUs with OVN Â¶

The purpose of this page is to describe how off-path SmartNIC DPU hardware
can be integrated with Neutron when OVN mechanism driver is used. For an
in-depth discussion of underlying mechanisms it is recommended to get
familiar with the following specifications

- Neutron Off-path SmartNIC DPU Port Binding with OVN specification ;

Neutron Off-path SmartNIC DPU Port Binding with OVN specification ;

- Nova Integration With Off-path Network Backends specification .

Nova Integration With Off-path Network Backends specification .

## Overview Â¶

A class of devices collectively referred to as off-path SmartNIC DPUs
introduces an important change to earlier architectures where compute and
networking agents used to coexist at the hypervisor host: networking control
plane components are now moved to the SmartNIC DPUâs CPU side which includes ovs-vswitchd and ovn-controller . The following diagram provides an
overview of the components involved:

ââââââââââââââââââââââââââââââââââââââ
                       â  Hypervisor                        â    LoM Ports
                       â  âââââââââââââ       âââââââââââââ â   (on-board,
                       â  â Instance  â       â  Nova     â ââââ optional)
                       â  â(e.g. QEMU)â       â Compute   â â  âââââââââââ
                       â  â           â       â           â ââââ         â
                       â  âââââââââââââ       âââââââââââââ â            â
                       â                                    â            â
                       ââââââââââââââââââ¬ââ¬ââââââââ¬ââ¬âââ¬âââââ            â
                                        â â       â â  â                 â
                                        â â       â â  â Control Traffic â
                           Instance VF  â â       â â  â PF associated   â
                                        â â       â â  â with an uplink  â
                                        â â       â â  â port or a VF.   â
                                        â â       â â  â (used to replaceâ
                                        â â       â â  â  LoM)           â
   ââââââââââââââââââââââââââââââââââââââ¼ââ¼ââââââââ¼ââ¼âââ¼ââ               â
   â   SmartNIC DPU Board               â â       â â  â â               â
   â                                    â â       â â  â â               â
   â  ââââââââââââââââ Control traffic  â â       â â  â â               â
   â  â   App. CPU   â via PFs or VFs  ââ´ââ´ââââââââ´ââ´â â â               â
   â  ââââââââââââââââ¤  (DC Fabric)    â             â â â               â
   â  âovn-controllerâââââââââââââââââââ¼ââ           â â â               â
   â  ââââââââââââââââ¤                 â â           â â â               â
   â  âovs-vswitchd  â                 â âNIC Switch â â â               â
   â  ââââââââââââââââ¤                 â âASIC/FPGA  â â â               â
   â  â Neutron OVN  â                 â â           â â â               â
   â  âmetadata agentâ                 â â           â â â               â
   â  ââââââââââââââââ¤Port representorsâ â           â â â               â
   â  â    br-int    âââââââââââââââââââ¤ â           â â â               â
   â  ââââââââââââââââ                 âââ¼ââââ¬ââ¬ââââââ â â               â
 â â´â â â âOptional port for             â   â â       â â               â
ââ¤OOB Port initial NIC switch config     â   â âuplink â â               â
 â â¬â â â â                              â   â â       â â               â
   â                                     â   â â       â â               â
   âââââââââââââââââââââââââââââââââââââââ¼ââââ¼ââ¼ââââââââ¼ââ               â
                                         â   â â       â                 â
                                      ââââ¼ââââ´ââ´ââââââââ¼âââââââââ        â
                                      â  â             â        â        â
                                      â  â   DC Fabric ââââââââââ¼âââââââââ
                                      â  â             â        â
                                      ââââ¼ââââââââââââââ¼âââââââââ
                                         â             â
                                         â         âââââ´âââââââ
                                         â         â          â
                                     âââââ¼âââ  âââââ¼ââââ ââââââ¼âââââ
                                     âOVN SBâ  âNeutronâ âPlacementâ
                                     ââââââââ  âServer â â         â
                                               âââââââââ âââââââââââ

## Prerequisites Â¶

- OpenStack Yoga or newer;

OpenStack Yoga or newer;

- Open vSwitch >= 2.17;

Open vSwitch >= 2.17;

- Open Virtual Network >= 21.12.0;

Open Virtual Network >= 21.12.0;

- OVN VIF >= 21.12.0;

OVN VIF >= 21.12.0;

- A SmartNIC DPU with the following characteristics: A NIC that exposes a card serial number via a PCIe VPD capability on its
physical or virtual function PCIe endpoints to both the hypervisor host
and the DPU host; Exposes the information about representor ports to applications running on
the SmartNIC DPUâs CPU in a manner supported by one of the OVN VIF Plug
Providers .

A SmartNIC DPU with the following characteristics:

- A NIC that exposes a card serial number via a PCIe VPD capability on its
physical or virtual function PCIe endpoints to both the hypervisor host
and the DPU host;

A NIC that exposes a card serial number via a PCIe VPD capability on its
physical or virtual function PCIe endpoints to both the hypervisor host
and the DPU host;

- Exposes the information about representor ports to applications running on
the SmartNIC DPUâs CPU in a manner supported by one of the OVN VIF Plug
Providers .

Exposes the information about representor ports to applications running on
the SmartNIC DPUâs CPU in a manner supported by one of the OVN VIF Plug
Providers .

## Nova configuration Â¶

Hypervisor hosts need to be configured to enable:

- Nova PCI passthrough for Nova Compute; Important For more information on other version requirements and limitations check
the SR-IOV section of the Nova networking guide .

Nova PCI passthrough for Nova Compute;

Important

For more information on other version requirements and limitations check
the SR-IOV section of the Nova networking guide .

- SR-IOV virtual functions on selected physical functions provided by DPUs
to the hypervisor hosts.

SR-IOV virtual functions on selected physical functions provided by DPUs
to the hypervisor hosts.

In addition to the regular PCI device allow list configuration, the PCI device
specification must include the remote_managed tag as in the following
examples:

- Virtual networks without physical segments; [pci] passthrough_whitelist = {"vendor_id" : "15b3" , "product_id" : "101e" , "physical_network": null, "remote_managed" : "true" }

Virtual networks without physical segments;

[pci] passthrough_whitelist = {"vendor_id" : "15b3" , "product_id" : "101e" , "physical_network": null, "remote_managed" : "true" }

- Physical networks (flat, VLAN) with a label: [pci] passthrough_whitelist = {"vendor_id" : "15b3" , "product_id" : "101e" , "physical_network" : "dcfabric" , "remote_managed" : "true" } Note âdcfabricâ is an arbitrary physnet name. In order for this to work it must
be specified consistenly in Nova config, during OVN configuraton when
specifying external_ids:ovn-bridge-mappings and during Neutron provider
network segment creation.

Physical networks (flat, VLAN) with a label:

[pci] passthrough_whitelist = {"vendor_id" : "15b3" , "product_id" : "101e" , "physical_network" : "dcfabric" , "remote_managed" : "true" }

Note

âdcfabricâ is an arbitrary physnet name. In order for this to work it must
be specified consistenly in Nova config, during OVN configuraton when
specifying external_ids:ovn-bridge-mappings and during Neutron provider
network segment creation.

## Auto-Discovery Â¶

When an instance with a remote-managed port is scheduled to a compute host
with a free remote-managed device, it claims it and supplies additional
information from that device about the NIC to Neutron so that it knows which
OVN chassis needs to handle an representor interface plugging and flow
programming. For PCI VFs this additional information includes:

- A card serial number from the NICâs VPD;

A card serial number from the NICâs VPD;

- PF mac address;

PF mac address;

- VF logical number.

VF logical number.

Neutron uses the card serial number to look up a chassis host name which is
needed for port binding to succeed and the rest is used by ovn-vif to set
up the matching representor port.

As a result, no direct communication or configuration is required between the
SmartNIC DPU host and the compute host in order to handle matching of compute
hosts to SmartNIC DPUs.

Note

Multiple DPUs per hypervisor host are possible to use, however, at the time
of writing, there is no way to indicate to Nova which VFs to choose via
Neutron port object attributes.

Having the OVN controller expose the SmartNIC DPU serial number is accomplished
by providing the serial number via the ovn-cms-options entry in external_ids column of the SmartNIC DPU local Open_vSwitch table:

$ ovs-vsctl set Open_vSwitch . external-ids:ovn-cms-options = "card-serial-number=AB0123XX0042"

## Launch an instance with remote managed port Â¶

$ openstack port create \ --network network \ --vnic-type remote-managed \ port1

$ openstack server create \ --flavor 1 \ --nic port-id = port1
