# Compute service overview ¶

Todo

Update a lot of the links in here.

Use OpenStack Compute to host and manage cloud computing systems.  OpenStack
Compute is a major part of an Infrastructure-as-a-Service (IaaS) system. The
main modules are implemented in Python.

OpenStack Compute interacts with OpenStack Identity for authentication,
OpenStack Placement for resource inventory tracking and selection, OpenStack
Image service for disk and server images, and OpenStack Dashboard for the user
and administrative interface. Image access is limited by projects, and by
users; quotas are limited per project (the number of instances, for example).
OpenStack Compute can scale horizontally on standard hardware, and download
images to launch instances.

OpenStack Compute consists of two WSGI APIs and a number
of services:

Accepts and responds to end user compute API calls. The service supports the
OpenStack Compute API.  It enforces some policies and initiates most
orchestration activities, such as running an instance.

Accepts metadata requests from instances. For more information, refer to Metadata service .

A worker daemon that creates and terminates virtual machine instances through
hypervisor APIs. The default hypervisor is libvirt with KVM or QEMU, but
other hypervisors are supported.

Processing is fairly complex. Basically, the daemon accepts actions from the
queue and performs a series of system commands such as launching a KVM
instance and updating its state in the database.

Takes a virtual machine instance request from the queue and determines on
which compute server host it runs.

Mediates interactions between the nova-compute service and the database.
It eliminates direct accesses to the cloud database made by the nova-compute service. The nova-conductor module scales horizontally.
However, do not deploy it on nodes where the nova-compute service runs.
For more information, see the conductor section in the Configuration Options .

Provides a proxy for accessing running instances through a VNC connection.
Supports browser-based novnc clients.

Provides a proxy for accessing running instances through a SPICE connection.
Supports browser-based HTML5 client.

A central hub for passing messages between daemons. Usually implemented with RabbitMQ but other options are available .

Stores most build-time and run-time states for a cloud infrastructure,
including:

- Available instance types

Available instance types

- Instances in use

Instances in use

- Available networks

Available networks

- Projects

Projects

Theoretically, OpenStack Compute can support any database that SQLAlchemy
supports. Common databases are SQLite3 for test and development work, MySQL,
MariaDB, and PostgreSQL.
