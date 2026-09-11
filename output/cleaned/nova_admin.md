# Admin Documentation Â¶

The OpenStack Compute service allows you to control an
Infrastructure-as-a-Service (IaaS) cloud computing platform.  It gives you
control over instances and networks, and allows you to manage access to the
cloud through users and projects.

Compute does not include virtualization software. Instead, it defines drivers
that interact with underlying virtualization mechanisms that run on your host
operating system, and exposes functionality over a web-based API.

## Overview Â¶

To effectively administer compute, you must understand how the different
installed nodes interact with each other. Compute can be installed in many
different ways using multiple servers, but generally multiple compute nodes
control the virtual servers and a cloud controller node contains the remaining
Compute services.

The Compute cloud works using a series of daemon processes named nova-* that exist persistently on the host machine. These binaries can all run on the
same machine or be spread out on multiple boxes in a large deployment. The
responsibilities of services and drivers are:

Services

A WSGI application that serves the Nova OpenStack Compute API.

A WSGI application that serves the Nova Metadata API.

Manages virtual machines. Loads a Service object, and exposes the public
methods on ComputeManager through a Remote Procedure Call (RPC).

Provides database-access support for compute nodes (thereby reducing security
risks).

Dispatches requests for new virtual machines to the correct node.

Provides a VNC proxy for browsers, allowing VNC consoles to access virtual
machines.

Provides a SPICE proxy for browsers, allowing SPICE consoles to access
virtual machines.

Provides a serial console proxy, allowing users to access a virtual machineâs
serial console.

The architecture is covered in much greater detail in Nova System Architecture .

- Nova System Architecture Components Hypervisors Projects, users, and roles Block storage Building blocks Nova service architecture

- Components

- Hypervisors

- Projects, users, and roles

- Block storage

- Building blocks

- Nova service architecture

Note

Some services have drivers that change how the service implements its core
functionality. For example, the nova-compute service supports drivers
that let you choose which hypervisor type it can use.

## Deployment Considerations Â¶

There is information you might want to consider before doing your deployment,
especially if it is going to be a larger deployment. For smaller deployments
the defaults from the install guide will be sufficient.

- Compute Driver Features Supported : While the majority of nova deployments use
libvirt/kvm, you can use nova with other compute drivers. Nova attempts to
provide a unified feature set across these, however, not all features are
implemented on all backends, and not all features are equally well tested. Feature Support by Use Case : A view of
what features each driver supports based on whatâs important to some large
use cases (General Purpose Cloud, NFV Cloud, HPC Cloud). Feature Support full list : A detailed dive through
features in each compute driver backend.

Compute Driver Features Supported : While the majority of nova deployments use
libvirt/kvm, you can use nova with other compute drivers. Nova attempts to
provide a unified feature set across these, however, not all features are
implemented on all backends, and not all features are equally well tested.

- Feature Support by Use Case : A view of
what features each driver supports based on whatâs important to some large
use cases (General Purpose Cloud, NFV Cloud, HPC Cloud).

Feature Support by Use Case : A view of
what features each driver supports based on whatâs important to some large
use cases (General Purpose Cloud, NFV Cloud, HPC Cloud).

- Feature Support full list : A detailed dive through
features in each compute driver backend.

Feature Support full list : A detailed dive through
features in each compute driver backend.

- Cells v2 configuration : For large deployments, cells v2
cells allow sharding of your compute environment. Upfront planning is key to
a successful cells v2 layout.

Cells v2 configuration : For large deployments, cells v2
cells allow sharding of your compute environment. Upfront planning is key to
a successful cells v2 layout.

- Availability Zones : Availability Zones are
an end-user visible logical abstraction for partitioning a cloud without
knowing the physical infrastructure.

Availability Zones : Availability Zones are
an end-user visible logical abstraction for partitioning a cloud without
knowing the physical infrastructure.

- Placement service : Overview of the placement
service, including how it fits in with the rest of nova.

Placement service : Overview of the placement
service, including how it fits in with the rest of nova.

- Running nova-api on wsgi : Considerations for deploying
the APIs.

Running nova-api on wsgi : Considerations for deploying
the APIs.

- Nova service concurrency : Considerations on how
to use and tune Nova services in threading mode.

Nova service concurrency : Considerations on how
to use and tune Nova services in threading mode.

- Cells (v2) Overview Service layout Database layout Usage Design Comparison with cells v1 Caveats Handling cell failures FAQs References

- Overview

- Service layout

- Database layout

- Usage

- Design

- Comparison with cells v1

- Caveats

- Handling cell failures

- FAQs

- References

- Host aggregates Configure scheduler to support host aggregates Aggregates in Placement Tenant Isolation with Placement Usage Configuration Image Caching References

- Configure scheduler to support host aggregates

- Aggregates in Placement

- Tenant Isolation with Placement

- Usage

- Configuration

- Image Caching

- References

- Compute service node firewall requirements

- Availability Zones Availability Zones with Placement Implications for moving servers Using availability zones to select hosts Usage Configuration

- Availability Zones with Placement

- Implications for moving servers

- Using availability zones to select hosts

- Usage

- Configuration

- Configuration Service User Tokens Compute API configuration Resize Cross-cell resize Configuring Fibre Channel Support Configuring iSCSI interface and offload support Hypervisors Compute log files Compute service sample configuration files

- Service User Tokens

- Compute API configuration

- Resize

- Cross-cell resize

- Configuring Fibre Channel Support

- Configuring iSCSI interface and offload support

- Hypervisors

- Compute log files

- Compute service sample configuration files

- Nova service concurrency Selecting concurrency mode for a service Tunables for the native threading mode Upgrading to nova 33.0.0 (2026.1. Gazpacho) or newer

- Selecting concurrency mode for a service

- Tunables for the native threading mode

- Upgrading to nova 33.0.0 (2026.1. Gazpacho) or newer

## Basic configuration Â¶

Once you have an OpenStack deployment up and running, you will want to manage
it. The below guides cover everything from creating initial flavor and image to
log management and live migration of instances.

- Quotas : Managing project quotas in nova.

Quotas : Managing project quotas in nova.

- Scheduling : How the scheduler is
configured, and how that will impact where compute instances land in your
environment. If you are seeing unexpected distribution of compute instances
in your hosts, youâll want to dive into this configuration.

Scheduling : How the scheduler is
configured, and how that will impact where compute instances land in your
environment. If you are seeing unexpected distribution of compute instances
in your hosts, youâll want to dive into this configuration.

- Exposing custom metadata to compute instances : How
and when you might want to extend the basic metadata exposed to compute
instances (either via metadata server or config drive) for your specific
purposes.

Exposing custom metadata to compute instances : How
and when you might want to extend the basic metadata exposed to compute
instances (either via metadata server or config drive) for your specific
purposes.

- Manage the cloud Show usage statistics for hosts and instances

- Show usage statistics for hosts and instances

- Manage Compute services

- Graceful Shutdown How graceful shutdown works for nova-compute service The additional RabbitMQ queue for compute service Operations handled during shutdown Configuration Upgrade considerations

- How graceful shutdown works for nova-compute service

- The additional RabbitMQ queue for compute service

- Operations handled during shutdown

- Configuration

- Upgrade considerations

- Configure Compute service groups Database ServiceGroup driver Memcache ServiceGroup driver

- Database ServiceGroup driver

- Memcache ServiceGroup driver

- Logging Logging module Syslog Rsyslog Serial console

- Logging module

- Syslog

- Rsyslog

- Serial console

- Secure with rootwrap Configure rootwrap Configure the rootwrap daemon

- Configure rootwrap

- Configure the rootwrap daemon

- Configure SSH between compute nodes

- Configure live migrations Libvirt VMware

- Libvirt

- VMware

- Live-migrate instances Manual selection of the destination host Automatic selection of the destination host Monitoring the migration What to do when the migration times out

- Manual selection of the destination host

- Automatic selection of the destination host

- Monitoring the migration

- What to do when the migration times out

- Secure live migration with QEMU-native TLS Context Prerequisites Validating your TLS environment on compute nodes Other TLS environment related checks on compute nodes Performing the migration Related information

- Context

- Prerequisites

- Validating your TLS environment on compute nodes

- Other TLS environment related checks on compute nodes

- Performing the migration

- Related information

- Manage volumes Volume multi-attach Managing volume attachments

- Volume multi-attach

- Managing volume attachments

- Manage shares Overview Use Cases Prerequisites Configure instance shared memory Limitations Known bugs Managing shares

- Overview

- Use Cases

- Prerequisites

- Configure instance shared memory

- Limitations

- Known bugs

- Managing shares

- Manage Flavors Create a flavor Modify a flavor Delete a flavor Default Flavors

- Create a flavor

- Modify a flavor

- Delete a flavor

- Default Flavors

- Injecting the administrator password

- Configure remote console access Overview Consoleauth configuration: Supported consoles: noVNC-based VNC console SPICE console Serial console MKS console About nova-consoleauth Frequently Asked Questions References

- Overview

- Consoleauth configuration:

- Supported consoles:

- noVNC-based VNC console

- SPICE console

- Serial console

- MKS console

- About nova-consoleauth

- Frequently Asked Questions

- References

- Compute schedulers Prefilters The Filter Scheduler Filters ComputeFilter DifferentHostFilter Weights Utilization-aware scheduling Allocation ratios Cells considerations Compute capabilities as traits Writing Your Own Filter Writing your own weigher

- Prefilters

- The Filter Scheduler

- Filters

- ComputeFilter

- DifferentHostFilter

- Weights

- Utilization-aware scheduling

- Allocation ratios

- Cells considerations

- Compute capabilities as traits

- Writing Your Own Filter

- Writing your own weigher

- Config drives Requirements and guidelines Configuration

- Requirements and guidelines

- Configuration

- Image Caching What is Image Caching? Image Caching Resource Accounting Image pre-caching

- What is Image Caching?

- Image Caching Resource Accounting

- Image pre-caching

- Metadata service Configuration Config drives Vendordata User data

- Configuration

- Config drives

- Vendordata

- User data

- Manage Unified Limits Quotas Quotas Unified limits Configuration Setting quota limits on resources Quota enforcement Quota usage from Placement Migration to unified limits quotas

- Quotas

- Unified limits

- Configuration

- Setting quota limits on resources

- Quota enforcement

- Quota usage from Placement

- Migration to unified limits quotas

- Networking with neutron SR-IOV NUMA Affinity virtio-net Multiqueue

- SR-IOV

- NUMA Affinity

- virtio-net Multiqueue

- Security hardening Encrypt Compute metadata traffic Securing live migration streams with QEMU-native TLS Mitigation for MDS (Microarchitectural Data Sampling) security flaws

- Encrypt Compute metadata traffic

- Securing live migration streams with QEMU-native TLS

- Mitigation for MDS (Microarchitectural Data Sampling) security flaws

- Vendordata StaticJSON DynamicJSON References

- StaticJSON

- DynamicJSON

- References

- Notifications Legacy (unversioned) notifications Versioned notifications Configuration Reference

- Legacy (unversioned) notifications

- Versioned notifications

- Configuration

- Reference

## Advanced configuration Â¶

OpenStack clouds run on platforms that differ greatly in the capabilities that
they provide. By default, the Compute service seeks to abstract the underlying
hardware that it runs on, rather than exposing specifics about the underlying
host platforms. This abstraction manifests itself in many ways. For example,
rather than exposing the types and topologies of CPUs running on hosts, the
service exposes a number of generic CPUs (virtual CPUs, or vCPUs) and allows
for overcommitting of these. In a similar manner, rather than exposing the
individual types of network devices available on hosts, generic
software-powered network ports are provided. These features are designed to
allow high resource utilization and allows the service to provide a generic
cost-effective and highly scalable cloud upon which to build applications.

This abstraction is beneficial for most workloads. However, there are some
workloads where determinism and per-instance performance are important, if not
vital. In these cases, instances can be expected to deliver near-native
performance. The Compute service provides features to improve individual
instance for these kind of workloads.

Important

In deployments older than Train, or in mixed Stein/Train deployments with a
rolling upgrade in progress, unless specifically enabled , live migration is not
possible for instances with a NUMA topology when using the libvirt
driver. A NUMA topology may be specified explicitly or can be added
implicitly due to the use of CPU pinning or huge pages. Refer to bug
#1289064 for more information. As of Train, live migration of instances
with a NUMA topology when using the libvirt driver is fully supported.

- Attaching physical PCI devices to guests Enabling PCI passthrough Configuring a flavor or image PCI-NUMA affinity policies PCI tracking in Placement Support for multiple types of VFs Configuring Live Migration for PCI devices Virtual IOMMU support Known Issues One-Time-Use Devices

- Enabling PCI passthrough

- Configuring a flavor or image

- PCI-NUMA affinity policies

- PCI tracking in Placement

- Support for multiple types of VFs

- Configuring Live Migration for PCI devices

- Virtual IOMMU support

- Known Issues

- One-Time-Use Devices

- CPU topologies SMP, NUMA, and SMT PCPU and VCPU Customizing instance NUMA placement policies Customizing instance CPU pinning policies Customizing instance CPU topologies Configuring libvirt compute nodes for CPU pinning Configuring CPU power management for dedicated cores

- SMP, NUMA, and SMT

- PCPU and VCPU

- Customizing instance NUMA placement policies

- Customizing instance CPU pinning policies

- Customizing instance CPU topologies

- Configuring libvirt compute nodes for CPU pinning

- Configuring CPU power management for dedicated cores

- Real Time Enabling Real-Time Configuring a flavor or image References

- Enabling Real-Time

- Configuring a flavor or image

- References

- Huge pages Pages, the TLB and huge pages Enabling huge pages on the host Customizing instance huge pages allocations

- Pages, the TLB and huge pages

- Enabling huge pages on the host

- Customizing instance huge pages allocations

- Attaching virtual GPU devices to guests Enable GPU types (Compute) Configure a flavor (Controller) Create instances with virtual GPU devices Ask for more than one vGPU per instance by the flavor How to discover a GPU type Checking allocations and inventories for virtual GPUs (Optional) Provide custom traits for multiple GPU types Caveats

- Enable GPU types (Compute)

- Configure a flavor (Controller)

- Create instances with virtual GPU devices

- Ask for more than one vGPU per instance by the flavor

- How to discover a GPU type

- Checking allocations and inventories for virtual GPUs

- (Optional) Provide custom traits for multiple GPU types

- Caveats

- File-backed memory Prerequisites and Limitations Configure the backing store Configure Nova Compute for file-backed memory

- Prerequisites and Limitations

- Configure the backing store

- Configure Nova Compute for file-backed memory

- Using ports with resource request Resource allocation Resource Group policy Virt driver support Extended resource request

- Resource allocation

- Resource Group policy

- Virt driver support

- Extended resource request

- Using ports vnic_type=âvdpaâ vDPA device tracking Virt driver support vDPA lifecycle operations vDPA live migration

- vDPA device tracking

- Virt driver support

- vDPA lifecycle operations

- vDPA live migration

- Attaching virtual persistent memory to guests Dependencies Configure PMEM namespaces (Compute) Configure a flavor Verify inventories and allocations

- Dependencies

- Configure PMEM namespaces (Compute)

- Configure a flavor

- Verify inventories and allocations

- Emulated Trusted Platform Module (vTPM) Enabling vTPM Security Configuring a flavor or image Legacy servers and live migration Limitations References

- Enabling vTPM

- Security

- Configuring a flavor or image

- Legacy servers and live migration

- Limitations

- References

- UEFI Enabling UEFI Configuring a flavor or image References

- Enabling UEFI

- Configuring a flavor or image

- References

- Secure Boot Enabling Secure Boot Configuring a flavor or image References

- Enabling Secure Boot

- Configuring a flavor or image

- References

- AMD SEV (Secure Encrypted Virtualization) Enabling SEV Configuring a flavor or image Limitations References

- Enabling SEV

- Configuring a flavor or image

- Limitations

- References

- Managing Resource Providers Using Config Files Placing Files Examples Schema Example

- Placing Files

- Examples

- Schema Example

- Compute Node Identification Self-provisioning of the node identity Deployment provisioning of the node identity Upgrading from pre-2023.1

- Self-provisioning of the node identity

- Deployment provisioning of the node identity

- Upgrading from pre-2023.1

- Resource Limits Configuring resource limits

- Configuring resource limits

- CPU models CPU modes CPU models CPU feature flags Mitigation for MDS (âMicroarchitectural Data Samplingâ) Security Flaws

- CPU modes

- CPU models

- CPU feature flags

- Mitigation for MDS (âMicroarchitectural Data Samplingâ) Security Flaws

- Other libvirt features Guest agent support Watchdog behavior Random number generator Performance Monitoring Unit (vPMU) Hiding hypervisor signature Locked memory allocation

- Guest agent support

- Watchdog behavior

- Random number generator

- Performance Monitoring Unit (vPMU)

- Hiding hypervisor signature

- Locked memory allocation

## Maintenance Â¶

Once you are running nova, the following information is extremely useful.

- Upgrades : How nova is designed to be upgraded for minimal
service impact, and the order you should do them in.

Upgrades : How nova is designed to be upgraded for minimal
service impact, and the order you should do them in.

- Troubleshoot Compute Orphaned resource allocations Rebuild placement DB Affinity policy violated with parallel requests Compute service logging Guru Meditation reports Common errors and fixes for Compute Credential errors, 401, and 403 forbidden errors Live migration permission issues Instance errors Empty log output for Linux instances Reset the state of an instance Injection problems Cannot find suitable emulator for x86_64 Failed to attach volume after detaching Failed to attach volume, systool is not installed Failed to connect volume in FC SAN Multipath call failed exit Failed to Attach Volume, Missing sg_scan Requested microversions are ignored

- Orphaned resource allocations

- Rebuild placement DB

- Affinity policy violated with parallel requests

- Compute service logging

- Guru Meditation reports

- Common errors and fixes for Compute

- Credential errors, 401, and 403 forbidden errors

- Live migration permission issues

- Instance errors

- Empty log output for Linux instances

- Reset the state of an instance

- Injection problems

- Cannot find suitable emulator for x86_64

- Failed to attach volume after detaching

- Failed to attach volume, systool is not installed

- Failed to connect volume in FC SAN

- Multipath call failed exit

- Failed to Attach Volume, Missing sg_scan

- Requested microversions are ignored

- Evacuate instances Evacuate a single instance Evacuate all instances

- Evacuate a single instance

- Evacuate all instances

- Migrate instances Example

- Example

- Use snapshots to migrate instances Create a snapshot of the instance Download the snapshot as an image Import the snapshot to the new environment Boot a new instance from the snapshot

- Create a snapshot of the instance

- Download the snapshot as an image

- Import the snapshot to the new environment

- Boot a new instance from the snapshot

- Upgrades Minimal Downtime Upgrade Process Current Database Upgrade Types Concepts Testing

- Minimal Downtime Upgrade Process

- Current Database Upgrade Types

- Concepts

- Testing

- Recover from a failed compute node Evacuate instances Manual recovery Recover from a UID/GID mismatch Recover cloud after disaster

- Evacuate instances

- Manual recovery

- Recover from a UID/GID mismatch

- Recover cloud after disaster

- hw_machine_type - Configuring and updating QEMU instance machine types Introduction Configure Update Device bus and model image properties

- Introduction

- Configure

- Update

- Device bus and model image properties

- hw_emulation_architecture - Configuring QEMU instance emulation architecture Introduction Configure

- Introduction

- Configure

- Soft Delete and Shadow Tables Soft delete instances that can be restored Soft delete database rows to shadow tables

- Soft delete instances that can be restored

- Soft delete database rows to shadow tables
