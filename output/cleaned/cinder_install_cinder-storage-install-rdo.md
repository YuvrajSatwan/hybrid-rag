# Install and configure a storage node ¶

## Prerequisites ¶

Before you install and configure the Block Storage service on the
storage node, you must prepare the storage device.

Note

Perform these steps on the storage node.

- Install the supporting utility packages: Install the LVM packages: # dnf install lvm2 device-mapper-persistent-data This is not required for CentOS 8 or later, which comes with a
version of LVM that does not use the lvmetad service: # systemctl enable lvm2-lvmetad.service # systemctl start lvm2-lvmetad.service Note Some distributions include LVM by default.

Install the supporting utility packages:

- Install the LVM packages: # dnf install lvm2 device-mapper-persistent-data

Install the LVM packages:

# dnf install lvm2 device-mapper-persistent-data

- This is not required for CentOS 8 or later, which comes with a
version of LVM that does not use the lvmetad service: # systemctl enable lvm2-lvmetad.service # systemctl start lvm2-lvmetad.service

This is not required for CentOS 8 or later, which comes with a
version of LVM that does not use the lvmetad service:

# systemctl enable lvm2-lvmetad.service # systemctl start lvm2-lvmetad.service

Note

Some distributions include LVM by default.

- Create the LVM physical volume /dev/sdb : # pvcreate /dev/sdb Physical volume "/dev/sdb" successfully created

Create the LVM physical volume /dev/sdb :

# pvcreate /dev/sdb Physical volume "/dev/sdb" successfully created

- Create the LVM volume group cinder-volumes : # vgcreate cinder-volumes /dev/sdb Volume group "cinder-volumes" successfully created The Block Storage service creates logical volumes in this volume group.

Create the LVM volume group cinder-volumes :

# vgcreate cinder-volumes /dev/sdb Volume group "cinder-volumes" successfully created

The Block Storage service creates logical volumes in this volume group.

- Only instances can access Block Storage volumes. However, the
underlying operating system manages the devices associated with
the volumes. By default, the LVM volume scanning tool scans the /dev directory for block storage devices that
contain volumes. If projects use LVM on their volumes, the scanning
tool detects these volumes and attempts to cache them which can cause
a variety of problems with both the underlying operating system
and project volumes. You must reconfigure LVM to scan only the devices
that contain the cinder-volumes volume group. Edit the /etc/lvm/lvm.conf file and complete the following actions: In the devices section, add a filter that accepts the /dev/sdb device and rejects all other devices: devices { ... filter = [ "a/sdb/" , "r/.*/" ] Each item in the filter array begins with a for accept or r for reject and includes a regular expression for the
device name. The array must end with r/.*/ to reject any
remaining devices. You can use the vgs -vvvv command
to test filters. Warning If your storage nodes use LVM on the operating system disk, you
must also add the associated device to the filter. For example,
if the /dev/sda device contains the operating system: filter = [ "a/sda/", "a/sdb/", "r/.*/"] Similarly, if your compute nodes use LVM on the operating
system disk, you must also modify the filter in the /etc/lvm/lvm.conf file on those nodes to include only
the operating system disk. For example, if the /dev/sda device contains the operating system: filter = [ "a/sda/", "r/.*/"]

Only instances can access Block Storage volumes. However, the
underlying operating system manages the devices associated with
the volumes. By default, the LVM volume scanning tool scans the /dev directory for block storage devices that
contain volumes. If projects use LVM on their volumes, the scanning
tool detects these volumes and attempts to cache them which can cause
a variety of problems with both the underlying operating system
and project volumes. You must reconfigure LVM to scan only the devices
that contain the cinder-volumes volume group. Edit the /etc/lvm/lvm.conf file and complete the following actions:

- In the devices section, add a filter that accepts the /dev/sdb device and rejects all other devices: devices { ... filter = [ "a/sdb/" , "r/.*/" ] Each item in the filter array begins with a for accept or r for reject and includes a regular expression for the
device name. The array must end with r/.*/ to reject any
remaining devices. You can use the vgs -vvvv command
to test filters. Warning If your storage nodes use LVM on the operating system disk, you
must also add the associated device to the filter. For example,
if the /dev/sda device contains the operating system: filter = [ "a/sda/", "a/sdb/", "r/.*/"] Similarly, if your compute nodes use LVM on the operating
system disk, you must also modify the filter in the /etc/lvm/lvm.conf file on those nodes to include only
the operating system disk. For example, if the /dev/sda device contains the operating system: filter = [ "a/sda/", "r/.*/"]

In the devices section, add a filter that accepts the /dev/sdb device and rejects all other devices:

devices { ... filter = [ "a/sdb/" , "r/.*/" ]

Each item in the filter array begins with a for accept or r for reject and includes a regular expression for the
device name. The array must end with r/.*/ to reject any
remaining devices. You can use the vgs -vvvv command
to test filters.

Warning

If your storage nodes use LVM on the operating system disk, you
must also add the associated device to the filter. For example,
if the /dev/sda device contains the operating system:

filter = [ "a/sda/", "a/sdb/", "r/.*/"]

Similarly, if your compute nodes use LVM on the operating
system disk, you must also modify the filter in the /etc/lvm/lvm.conf file on those nodes to include only
the operating system disk. For example, if the /dev/sda device contains the operating system:

filter = [ "a/sda/", "r/.*/"]

## Install and configure components ¶

- Install the packages: # dnf install openstack-cinder targetcli

Install the packages:

# dnf install openstack-cinder targetcli

- Edit the /etc/cinder/cinder.conf file
and complete the following actions: In the [database] section, configure database access: [database] # ... connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder Replace CINDER_DBPASS with the password you chose for
the Block Storage database. In the [DEFAULT] section, configure RabbitMQ message queue access: [DEFAULT] # ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for
the openstack account in RabbitMQ . In the [keystone_authtoken] section,
configure Identity service access: [keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = cinder password = CINDER_PASS Replace CINDER_PASS with the password you chose for the cinder user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section. In the [DEFAULT] section, configure the my_ip option: [DEFAULT] # ... my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS Replace MANAGEMENT_INTERFACE_IP_ADDRESS with the IP address
of the management network interface on your storage node,
typically 10.0.0.41 for the first node in the example architecture . In the [lvm] section, configure the LVM back end with the
LVM driver, cinder-volumes volume group, iSCSI protocol,
and appropriate iSCSI service. If the [lvm] section does not exist,
create it: [lvm] volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver volume_group = cinder-volumes target_protocol = iscsi target_helper = lioadm In the [DEFAULT] section, enable the LVM back end: [DEFAULT] # ... enabled_backends = lvm Note Back-end names are arbitrary. As an example, this guide
uses the name of the driver as the name of the back end. In the [DEFAULT] section, configure the location of the
Image service API: [DEFAULT] # ... glance_api_servers = http://controller:9292 In the [oslo_concurrency] section, configure the lock path: [oslo_concurrency] # ... lock_path = /var/lib/cinder/tmp

Edit the /etc/cinder/cinder.conf file
and complete the following actions:

- In the [database] section, configure database access: [database] # ... connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder Replace CINDER_DBPASS with the password you chose for
the Block Storage database.

In the [database] section, configure database access:

[database] # ... connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder

Replace CINDER_DBPASS with the password you chose for
the Block Storage database.

- In the [DEFAULT] section, configure RabbitMQ message queue access: [DEFAULT] # ... transport_url = rabbit://openstack:RABBIT_PASS@controller Replace RABBIT_PASS with the password you chose for
the openstack account in RabbitMQ .

In the [DEFAULT] section, configure RabbitMQ message queue access:

[DEFAULT] # ... transport_url = rabbit://openstack:RABBIT_PASS@controller

Replace RABBIT_PASS with the password you chose for
the openstack account in RabbitMQ .

- In the [keystone_authtoken] section,
configure Identity service access: [keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = cinder password = CINDER_PASS Replace CINDER_PASS with the password you chose for the cinder user in the Identity service. Note Comment out or remove any other options in the [keystone_authtoken] section.

In the [keystone_authtoken] section,
configure Identity service access:

[keystone_authtoken] # ... www_authenticate_uri = http://controller:5000 auth_url = http://controller:5000 memcached_servers = controller:11211 auth_type = password project_domain_name = default user_domain_name = default project_name = service username = cinder password = CINDER_PASS

Replace CINDER_PASS with the password you chose for the cinder user in the Identity service.

Note

Comment out or remove any other options in the [keystone_authtoken] section.

- In the [DEFAULT] section, configure the my_ip option: [DEFAULT] # ... my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS Replace MANAGEMENT_INTERFACE_IP_ADDRESS with the IP address
of the management network interface on your storage node,
typically 10.0.0.41 for the first node in the example architecture .

In the [DEFAULT] section, configure the my_ip option:

[DEFAULT] # ... my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS

Replace MANAGEMENT_INTERFACE_IP_ADDRESS with the IP address
of the management network interface on your storage node,
typically 10.0.0.41 for the first node in the example architecture .

- In the [lvm] section, configure the LVM back end with the
LVM driver, cinder-volumes volume group, iSCSI protocol,
and appropriate iSCSI service. If the [lvm] section does not exist,
create it: [lvm] volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver volume_group = cinder-volumes target_protocol = iscsi target_helper = lioadm

In the [lvm] section, configure the LVM back end with the
LVM driver, cinder-volumes volume group, iSCSI protocol,
and appropriate iSCSI service. If the [lvm] section does not exist,
create it:

[lvm] volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver volume_group = cinder-volumes target_protocol = iscsi target_helper = lioadm

- In the [DEFAULT] section, enable the LVM back end: [DEFAULT] # ... enabled_backends = lvm Note Back-end names are arbitrary. As an example, this guide
uses the name of the driver as the name of the back end.

In the [DEFAULT] section, enable the LVM back end:

[DEFAULT] # ... enabled_backends = lvm

Note

Back-end names are arbitrary. As an example, this guide
uses the name of the driver as the name of the back end.

- In the [DEFAULT] section, configure the location of the
Image service API: [DEFAULT] # ... glance_api_servers = http://controller:9292

In the [DEFAULT] section, configure the location of the
Image service API:

[DEFAULT] # ... glance_api_servers = http://controller:9292

- In the [oslo_concurrency] section, configure the lock path: [oslo_concurrency] # ... lock_path = /var/lib/cinder/tmp

In the [oslo_concurrency] section, configure the lock path:

[oslo_concurrency] # ... lock_path = /var/lib/cinder/tmp

## Finalize installation ¶

- Start the Block Storage volume service with iscsid including
its dependencies and configure them to start when the system boots: # systemctl enable openstack-cinder-volume.service target.service iscsid.service # systemctl start openstack-cinder-volume.service target.service iscsid.service

Start the Block Storage volume service with iscsid including
its dependencies and configure them to start when the system boots:

# systemctl enable openstack-cinder-volume.service target.service iscsid.service # systemctl start openstack-cinder-volume.service target.service iscsid.service
