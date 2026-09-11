# OpenStack Compute (nova) Â¶

## What is nova? Â¶

Nova is the OpenStack project that provides a way to provision compute
instances (aka virtual servers). Nova supports creating virtual machines,
baremetal servers (through the use of ironic), and has limited support for
system containers. Nova runs as a set of daemons on top of existing Linux
servers to provide that service.

It requires the following additional OpenStack services for basic function:

- Keystone : This provides identity and authentication for
all OpenStack services.

Keystone : This provides identity and authentication for
all OpenStack services.

- Glance : This provides the compute image repository. All
compute instances launch from glance images.

Glance : This provides the compute image repository. All
compute instances launch from glance images.

- Neutron : This is responsible for provisioning the virtual
or physical networks that compute instances connect to on boot.

Neutron : This is responsible for provisioning the virtual
or physical networks that compute instances connect to on boot.

- Placement : This is responsible for tracking inventory of
resources available in a cloud and assisting in choosing which provider of
those resources will be used when creating a virtual machine.

Placement : This is responsible for tracking inventory of
resources available in a cloud and assisting in choosing which provider of
those resources will be used when creating a virtual machine.

It can also integrate with other services to include: persistent block
storage, encrypted disks, and baremetal compute instances.

## For End Users Â¶

As an end user of nova, youâll use nova to create and manage servers with
either tools or the API directly.

### Tools for using Nova Â¶

- Horizon : The official web UI for
the OpenStack Project.

Horizon : The official web UI for
the OpenStack Project.

- OpenStack Client : The official CLI for
OpenStack Projects. You should use this as your CLI for most things, it
includes not just nova commands but also commands for most of the projects in
OpenStack.

OpenStack Client : The official CLI for
OpenStack Projects. You should use this as your CLI for most things, it
includes not just nova commands but also commands for most of the projects in
OpenStack.

- Nova Client : For some very
advanced features (or administrative commands) of nova you may need to use
nova client. It is still supported, but the openstack cli is recommended.

Nova Client : For some very
advanced features (or administrative commands) of nova you may need to use
nova client. It is still supported, but the openstack cli is recommended.

### Writing to the API Â¶

All end user (and some administrative) features of nova are exposed via a REST
API, which can be used to build more complicated logic or automation with
nova. This can be consumed directly, or via various SDKs. The following
resources will help you get started with consuming the API directly.

- Compute API Guide : The
concept guide for the API. This helps lay out the concepts behind the API to
make consuming the API reference easier.

Compute API Guide : The
concept guide for the API. This helps lay out the concepts behind the API to
make consuming the API reference easier.

- Compute API Reference :
The complete reference for the compute API, including all methods and
request / response parameters and their meaning.

Compute API Reference :
The complete reference for the compute API, including all methods and
request / response parameters and their meaning.

- Compute API Microversion History :
The compute API evolves over time through Microversions . This
provides the history of all those changes. Consider it a âwhatâs newâ in the
compute API.

Compute API Microversion History :
The compute API evolves over time through Microversions . This
provides the history of all those changes. Consider it a âwhatâs newâ in the
compute API.

- Block Device Mapping : One of the trickier
parts to understand is the Block Device Mapping parameters used to connect
specific block devices to computes. This deserves its own deep dive.

Block Device Mapping : One of the trickier
parts to understand is the Block Device Mapping parameters used to connect
specific block devices to computes. This deserves its own deep dive.

- Metadata : Provide information to the guest instance
when it is created.

Metadata : Provide information to the guest instance
when it is created.

Nova can be configured to emit notifications over RPC.

- Versioned Notifications : This
provides information on the notifications emitted by nova.

Versioned Notifications : This
provides information on the notifications emitted by nova.

Other end-user guides can be found under User Documentation .

## For Operators Â¶

### Architecture Overview Â¶

- Nova architecture : An overview of how all the parts in
nova fit together.

Nova architecture : An overview of how all the parts in
nova fit together.

### Installation Â¶

The detailed install guide for nova. A functioning nova will also require
having installed keystone , glance , neutron , and placement . Ensure that you follow their install
guides first.

- Compute service Overview Compute service overview Install and configure controller node Install and configure a compute node Verify operation

- Overview

- Compute service overview

- Install and configure controller node

- Install and configure a compute node

- Verify operation

### Deployment Considerations Â¶

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

- Running nova-api on wsgi : Considerations for deploying
under WSGI.

Running nova-api on wsgi : Considerations for deploying
under WSGI.

### Maintenance Â¶

Once you are running nova, the following information is extremely useful.

- Admin Guide : A collection of guides for administrating
nova.

Admin Guide : A collection of guides for administrating
nova.

- Flavors : What flavors are and why they are used.

Flavors : What flavors are and why they are used.

- Upgrades : How nova is designed to be upgraded for minimal
service impact, and the order you should do them in.

Upgrades : How nova is designed to be upgraded for minimal
service impact, and the order you should do them in.

- Quotas : Managing project quotas in nova.

Quotas : Managing project quotas in nova.

- Aggregates : Aggregates are a useful way of grouping
hosts together for scheduling purposes.

Aggregates : Aggregates are a useful way of grouping
hosts together for scheduling purposes.

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

### Reference Material Â¶

- Nova CLI Command References : the complete command reference
for all the daemons and admin tools that come with nova.

Nova CLI Command References : the complete command reference
for all the daemons and admin tools that come with nova.

- Configuration Guide : Information on configuring
the system, including role-based access control policy rules.

Configuration Guide : Information on configuring
the system, including role-based access control policy rules.

## For Contributors Â¶

- So You Want to Contributeâ¦ : If you are a new contributor this should
help you to start contributing to Nova.

So You Want to Contributeâ¦ : If you are a new contributor this should
help you to start contributing to Nova.

- Contributor Documentation : If you are new to Nova, this should help you start
to understand what Nova actually does, and why.

Contributor Documentation : If you are new to Nova, this should help you start
to understand what Nova actually does, and why.

- Technical Reference Deep Dives : There are also a number of technical references on
both current and future looking parts of our architecture.
These are collected here.

Technical Reference Deep Dives : There are also a number of technical references on
both current and future looking parts of our architecture.
These are collected here.

## Search Â¶

- Nova document search : Search the contents of this document.

Nova document search : Search the contents of this document.

- OpenStack wide search : Search the wider
set of OpenStack documentation, including forums.

OpenStack wide search : Search the wider
set of OpenStack documentation, including forums.
