# Key Manager service overview ¶

The Key Manager service provides secure storage, provisioning and management of
secrets, such as passwords, encryption keys, etc.

The Key Manager service consists of the following components:

Provides an OpenStack-native RESTful API that supports provisioning and managing
Barbican secrets.

Provides an Openstack RPC interface that interacts with barbican-api and reads from the barbican message queue.  Supports the fulfillment of
Barbican orders.

Listens to messages from the Keystone notification service.
Used to manage the representation of Keystone projects in the Barbican
database when projects are deleted.
