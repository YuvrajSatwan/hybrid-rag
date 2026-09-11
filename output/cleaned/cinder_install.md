# Cinder Installation Guide Â¶

The Block Storage service (cinder) provides block storage devices
to guest instances. The method in which the storage is provisioned and
consumed is determined by the Block Storage driver, or drivers
in the case of a multi-backend configuration. There are a variety of
drivers that are available: NAS/SAN, NFS, iSCSI, Ceph, and more.

The Block Storage API and scheduler services typically run on the controller
nodes. Depending upon the drivers used, the volume service can run
on controller nodes, compute nodes, or standalone storage nodes.

For more information, see the Configuration
Reference .

## Prerequisites Â¶

This documentation specifically covers the installation of the Cinder Block
Storage service. Before following this guide you will need to prepare your
OpenStack environment using the instructions in the OpenStack Installation Guide .

Once able to âLaunch an instanceâ in your OpenStack environment follow the
instructions below to add Cinder to the base environment.

## Adding Cinder to your OpenStack Environment Â¶

The following links describe how to install the Cinder Block Storage Service:

Warning

For security reasons Service Tokens must be configured in OpenStack
for Cinder to operate securely. Pay close attention to the specific
section describing it: . See https://bugs.launchpad.net/nova/+bug/2004555 for details.

- Cinder Block Storage service overview The default volume type

- The default volume type

- Cinder Installation Guide for openSUSE and SUSE Linux Enterprise Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation Install and configure a storage node Prerequisites Install and configure components Finalize installation Install and configure the backup service Install and configure components Finalize installation Verify Cinder operation

- Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation

- Prerequisites

- Install and configure components

- Configure Compute to use Block Storage

- Finalize installation

- Install and configure a storage node Prerequisites Install and configure components Finalize installation

- Prerequisites

- Install and configure components

- Finalize installation

- Install and configure the backup service Install and configure components Finalize installation

- Install and configure components

- Finalize installation

- Verify Cinder operation

- Cinder Installation Guide for Red Hat Enterprise Linux and CentOS Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation Install and configure a storage node Prerequisites Install and configure components Finalize installation Install and configure the backup service Install and configure components Finalize installation Verify Cinder operation

- Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation

- Prerequisites

- Install and configure components

- Configure Compute to use Block Storage

- Finalize installation

- Install and configure a storage node Prerequisites Install and configure components Finalize installation

- Prerequisites

- Install and configure components

- Finalize installation

- Install and configure the backup service Install and configure components Finalize installation

- Install and configure components

- Finalize installation

- Verify Cinder operation

- Cinder Installation Guide for Ubuntu Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation Install and configure a storage node Prerequisites Install and configure components Finalize installation Install and configure the backup service Install and configure components Finalize installation Verify Cinder operation

- Install and configure controller node Prerequisites Install and configure components Configure Compute to use Block Storage Finalize installation

- Prerequisites

- Install and configure components

- Configure Compute to use Block Storage

- Finalize installation

- Install and configure a storage node Prerequisites Install and configure components Finalize installation

- Prerequisites

- Install and configure components

- Finalize installation

- Install and configure the backup service Install and configure components Finalize installation

- Install and configure components

- Finalize installation

- Verify Cinder operation
