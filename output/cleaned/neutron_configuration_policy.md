# Policy Reference Â¶

Warning

JSON formatted policy file is deprecated since Neutron 18.0.0 (Wallaby).
This oslopolicy-convert-json-to-yaml tool will migrate your existing
JSON-formatted policy file to YAML in a backward-compatible way.

Neutron, like most OpenStack projects, uses a policy language to restrict
permissions on REST API actions.

The following is an overview of all available policies in neutron.

For a sample policy file, refer to Sample Policy File .

## neutron Â¶

role:admin

Rule for cloud admin access

!

Rule for context with global access to the resources

role:service

Default rule for the service-to-service APIs.

project_id:%(project_id)s

Rule for resource owner access

rule:context_is_admin or rule:owner

Rule for admin or owner access

role:advsvc

Rule for advsvc role access

rule:context_is_admin or project_id:%(network:project_id)s

Rule for admin or network owner access

rule:owner or rule:admin_or_network_owner

Rule for resource owner, admin or network owner access

project_id:%(network:project_id)s

Rule for network owner access

rule:context_is_admin

Rule for admin-only access

<empty string>

Rule for regular user access

field:networks:shared=True

Rule of shared network

rule:admin_or_owner

Default access rule

rule:context_is_admin or project_id:%(ext_parent:project_id)s

Rule for common parent owner check

project_id:%(ext_parent:project_id)s

Rule for common parent owner check

project_id:%(security_group:project_id)s

Rule for security group owner access

field:address_groups:shared=True

Definition of a shared address group

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_address_groups

- GET /address-groups

GET /address-groups

- GET /address-groups/{id}

GET /address-groups/{id}

- project

project

Get an address group

field:address_scopes:shared=True

Definition of a shared address scope

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /address-scopes

POST /address-scopes

- project

project

Create an address scope

rule:admin_only

- POST /address-scopes

POST /address-scopes

- project

project

Create a shared address scope

rule:admin_only or role:reader and project_id:%(project_id)s or rule:shared_address_scopes

- GET /address-scopes

GET /address-scopes

- GET /address-scopes/{id}

GET /address-scopes/{id}

- project

project

Get an address scope

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /address-scopes/{id}

PUT /address-scopes/{id}

- project

project

Update an address scope

rule:admin_only

- PUT /address-scopes/{id}

PUT /address-scopes/{id}

- project

project

Update shared attribute of an address scope

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /address-scopes/{id}

DELETE /address-scopes/{id}

- project

project

Delete an address scope

rule:admin_only

- POST /agents/{id}

POST /agents/{id}

- project

project

Create an agent

rule:admin_only

- GET /agents

GET /agents

- GET /agents/{id}

GET /agents/{id}

- project

project

Get an agent

rule:admin_only

- PUT /agents/{id}

PUT /agents/{id}

- project

project

Update an agent

rule:admin_only

- DELETE /agents/{id}

DELETE /agents/{id}

- project

project

Delete an agent

rule:admin_only

- POST /agents/{agent_id}/dhcp-networks

POST /agents/{agent_id}/dhcp-networks

- project

project

Add a network to a DHCP agent

rule:admin_only

- GET /agents/{agent_id}/dhcp-networks

GET /agents/{agent_id}/dhcp-networks

- project

project

List networks on a DHCP agent

rule:admin_only

- DELETE /agents/{agent_id}/dhcp-networks/{network_id}

DELETE /agents/{agent_id}/dhcp-networks/{network_id}

- project

project

Remove a network from a DHCP agent

rule:admin_only

- POST /agents/{agent_id}/l3-routers

POST /agents/{agent_id}/l3-routers

- project

project

Add a router to an L3 agent

rule:admin_only

- GET /agents/{agent_id}/l3-routers

GET /agents/{agent_id}/l3-routers

- project

project

List routers on an L3 agent

rule:admin_only

- DELETE /agents/{agent_id}/l3-routers/{router_id}

DELETE /agents/{agent_id}/l3-routers/{router_id}

- project

project

Remove a router from an L3 agent

rule:admin_only

- GET /networks/{network_id}/dhcp-agents

GET /networks/{network_id}/dhcp-agents

- project

project

List DHCP agents hosting a network

rule:admin_only

- GET /routers/{router_id}/l3-agents

GET /routers/{router_id}/l3-agents

- project

project

List L3 agents hosting a router

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /auto-allocated-topology/{project_id}

GET /auto-allocated-topology/{project_id}

- project

project

Get a projectâs auto-allocated topology

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /auto-allocated-topology/{project_id}

DELETE /auto-allocated-topology/{project_id}

- project

project

Delete a projectâs auto-allocated topology

role:reader

- GET /availability_zones

GET /availability_zones

- project

project

List availability zones

rule:admin_only

- POST /default-security-group-rules

POST /default-security-group-rules

- project

project

Create a templated of the security group rule

role:reader

- GET /default-security-group-rules

GET /default-security-group-rules

- GET /default-security-group-rules/{id}

GET /default-security-group-rules/{id}

- project

project

Get a templated of the security group rule

rule:admin_only

- DELETE /default-security-group-rules/{id}

DELETE /default-security-group-rules/{id}

- project

project

Delete a templated of the security group rule

rule:admin_only

- POST /flavors

POST /flavors

- project

project

Create a flavor

role:reader

- GET /flavors

GET /flavors

- GET /flavors/{id}

GET /flavors/{id}

- project

project

Get a flavor

rule:admin_only

- PUT /flavors/{id}

PUT /flavors/{id}

- project

project

Update a flavor

rule:admin_only

- DELETE /flavors/{id}

DELETE /flavors/{id}

- project

project

Delete a flavor

rule:admin_only

- POST /service_profiles

POST /service_profiles

- project

project

Create a service profile

rule:admin_only

- GET /service_profiles

GET /service_profiles

- GET /service_profiles/{id}

GET /service_profiles/{id}

- project

project

Get a service profile

rule:admin_only

- PUT /service_profiles/{id}

PUT /service_profiles/{id}

- project

project

Update a service profile

rule:admin_only

- DELETE /service_profiles/{id}

DELETE /service_profiles/{id}

- project

project

Delete a service profile

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- project

project

Get a flavor associated with a given service profiles. There is no corresponding GET operations in API currently. This rule is currently referred only in the DELETE of flavor_service_profile.

rule:admin_only

- POST /flavors/{flavor_id}/service_profiles

POST /flavors/{flavor_id}/service_profiles

- project

project

Associate a flavor with a service profile

rule:admin_only

- DELETE /flavors/{flavor_id}/service_profiles/{profile_id}

DELETE /flavors/{flavor_id}/service_profiles/{profile_id}

- project

project

Disassociate a flavor with a service profile

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /floatingips

POST /floatingips

- project

project

Create a floating IP

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /floatingips

POST /floatingips

- project

project

Create a floating IP with a specific IP address

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /floatingips/{id}/tags

POST /floatingips/{id}/tags

- project

project

Create the floating IP tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /floatingips

GET /floatingips

- GET /floatingips/{id}

GET /floatingips/{id}

- project

project

Get a floating IP

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /floatingips/{id}/tags

GET /floatingips/{id}/tags

- GET /floatingips/{id}/tags/{tag_id}

GET /floatingips/{id}/tags/{tag_id}

- project

project

Get the floating IP tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /floatingips/{id}

PUT /floatingips/{id}

- project

project

Update a floating IP

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /floatingips/{id}/tags

PUT /floatingips/{id}/tags

- PUT /floatingips/{id}/tags/{tag_id}

PUT /floatingips/{id}/tags/{tag_id}

- project

project

Update the floating IP tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /floatingips/{id}

DELETE /floatingips/{id}

- project

project

Delete a floating IP

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /floatingips/{id}/tags

DELETE /floatingips/{id}/tags

- DELETE /floatingips/{id}/tags/{tag_id}

DELETE /floatingips/{id}/tags/{tag_id}

- project

project

Delete the floating IP tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /floatingip_pools

GET /floatingip_pools

- project

project

Get floating IP pools

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- POST /floatingips/{floatingip_id}/port_forwardings

POST /floatingips/{floatingip_id}/port_forwardings

- project

project

Create a floating IP port forwarding

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /floatingips/{floatingip_id}/port_forwardings

GET /floatingips/{floatingip_id}/port_forwardings

- GET /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

GET /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

- project

project

Get a floating IP port forwarding

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- PUT /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

PUT /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

- project

project

Update a floating IP port forwarding

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- DELETE /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

DELETE /floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

- project

project

Delete a floating IP port forwarding

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- POST /routers/{router_id}/conntrack_helpers

POST /routers/{router_id}/conntrack_helpers

- project

project

Create a router conntrack helper

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /routers/{router_id}/conntrack_helpers

GET /routers/{router_id}/conntrack_helpers

- GET /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

GET /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

- project

project

Get a router conntrack helper

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- PUT /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

PUT /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

- project

project

Update a router conntrack helper

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- DELETE /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

DELETE /routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

- project

project

Delete a router conntrack helper

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /local-ips

POST /local-ips

- project

project

Create a Local IP

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /local-ips

GET /local-ips

- GET /local-ips/{id}

GET /local-ips/{id}

- project

project

Get a Local IP

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /local-ips/{id}

PUT /local-ips/{id}

- project

project

Update a Local IP

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /local-ips/{id}

DELETE /local-ips/{id}

- project

project

Delete a Local IP

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- POST /local_ips/{local_ip_id}/port_associations

POST /local_ips/{local_ip_id}/port_associations

- project

project

Create a Local IP port association

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /local_ips/{local_ip_id}/port_associations

GET /local_ips/{local_ip_id}/port_associations

- GET /local_ips/{local_ip_id}/port_associations/{fixed_port_id}

GET /local_ips/{local_ip_id}/port_associations/{fixed_port_id}

- project

project

Get a Local IP port association

(rule:admin_only) or (role:member and rule:ext_parent_owner)

- DELETE /local_ips/{local_ip_id}/port_associations/{fixed_port_id}

DELETE /local_ips/{local_ip_id}/port_associations/{fixed_port_id}

- project

project

Delete a Local IP port association

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- GET /log/loggable-resources

GET /log/loggable-resources

- project

project

Get loggable resources

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /log/logs

POST /log/logs

- project

project

Create a network log

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- GET /log/logs

GET /log/logs

- GET /log/logs/{id}

GET /log/logs/{id}

- project

project

Get a network log

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- PUT /log/logs/{id}

PUT /log/logs/{id}

- project

project

Update a network log

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- DELETE /log/logs/{id}

DELETE /log/logs/{id}

- project

project

Delete a network log

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /metering/metering-labels

POST /metering/metering-labels

- project

project

Create a metering label

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /metering/metering-labels

GET /metering/metering-labels

- GET /metering/metering-labels/{id}

GET /metering/metering-labels/{id}

- project

project

Get a metering label

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- DELETE /metering/metering-labels/{id}

DELETE /metering/metering-labels/{id}

- project

project

Delete a metering label

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /metering/metering-label-rules

POST /metering/metering-label-rules

- project

project

Create a metering label rule

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /metering/metering-label-rules

GET /metering/metering-label-rules

- GET /metering/metering-label-rules/{id}

GET /metering/metering-label-rules/{id}

- project

project

Get a metering label rule

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- DELETE /metering/metering-label-rules/{id}

DELETE /metering/metering-label-rules/{id}

- project

project

Delete a metering label rule

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /ndp_proxies

POST /ndp_proxies

- project

project

Create a ndp proxy

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /ndp_proxies

GET /ndp_proxies

- GET /ndp_proxies/{id}

GET /ndp_proxies/{id}

- project

project

Get a ndp proxy

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /ndp_proxies/{id}

PUT /ndp_proxies/{id}

- project

project

Update a ndp proxy

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /ndp_proxies/{id}

DELETE /ndp_proxies/{id}

- project

project

Delete a ndp proxy

field:networks:router:external=True

Definition of an external network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /networks

POST /networks

- project

project

Create a network

rule:admin_only

- POST /networks

POST /networks

- project

project

Create a shared network

rule:admin_only

- POST /networks

POST /networks

- project

project

Create an external network

rule:admin_only

- POST /networks

POST /networks

- project

project

Specify is_default attribute when creating a network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /networks

POST /networks

- project

project

Specify port_security_enabled attribute when creating a network

rule:admin_only

- POST /networks

POST /networks

- project

project

Specify segments attribute when creating a network

rule:admin_only

- POST /networks

POST /networks

- project

project

Specify provider:network_type when creating a network

rule:admin_only

- POST /networks

POST /networks

- project

project

Specify provider:physical_network when creating a network

rule:admin_only

- POST /networks

POST /networks

- project

project

Specify provider:segmentation_id when creating a network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /networks/{id}/tags

POST /networks/{id}/tags

- project

project

Create the network tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:service_api or rule:shared or rule:external or rule:context_is_advsvc

- GET /networks

GET /networks

- GET /networks/{id}

GET /networks/{id}

- project

project

Get a network

rule:admin_only

- GET /networks

GET /networks

- GET /networks/{id}

GET /networks/{id}

- project

project

Get segments attribute of a network

rule:admin_only

- GET /networks

GET /networks

- GET /networks/{id}

GET /networks/{id}

- project

project

Get provider:network_type attribute of a network

rule:admin_only

- GET /networks

GET /networks

- GET /networks/{id}

GET /networks/{id}

- project

project

Get provider:physical_network attribute of a network

rule:admin_only

- GET /networks

GET /networks

- GET /networks/{id}

GET /networks/{id}

- project

project

Get provider:segmentation_id attribute of a network

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared or rule:external or rule:context_is_advsvc

- GET /networks/{id}/tags

GET /networks/{id}/tags

- GET /networks/{id}/tags/{tag_id}

GET /networks/{id}/tags/{tag_id}

- project

project

Get the network tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update segments attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update shared attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update provider:network_type attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update provider:physical_network attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update provider:segmentation_id attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update router:external attribute of a network

rule:admin_only

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update is_default attribute of a network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /networks/{id}

PUT /networks/{id}

- project

project

Update port_security_enabled attribute of a network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /networks/{id}/tags

PUT /networks/{id}/tags

- PUT /networks/{id}/tags/{tag_id}

PUT /networks/{id}/tags/{tag_id}

- project

project

Update the network tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /networks/{id}

DELETE /networks/{id}

- project

project

Delete a network

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /networks/{id}/tags

DELETE /networks/{id}/tags

- DELETE /networks/{id}/tags/{tag_id}

DELETE /networks/{id}/tags/{tag_id}

- project

project

Delete the network tags

(rule:admin_only) or (rule:service_api)

- GET /network-ip-availabilities

GET /network-ip-availabilities

- GET /network-ip-availabilities/{network_id}

GET /network-ip-availabilities/{network_id}

- project

project

Get network IP availability

rule:admin_only

- POST /network_segment_ranges

POST /network_segment_ranges

- project

project

Create a network segment range

rule:admin_only

- POST /network_segment_ranges/{id}/tags

POST /network_segment_ranges/{id}/tags

- project

project

Create the network segment range tags

rule:admin_only

- GET /network_segment_ranges

GET /network_segment_ranges

- GET /network_segment_ranges/{id}

GET /network_segment_ranges/{id}

- project

project

Get a network segment range

rule:admin_only

- GET /network_segment_ranges/{id}/tags

GET /network_segment_ranges/{id}/tags

- GET /network_segment_ranges/{id}/tags/{tag_id}

GET /network_segment_ranges/{id}/tags/{tag_id}

- project

project

Get the network segment range tags

rule:admin_only

- PUT /network_segment_ranges/{id}

PUT /network_segment_ranges/{id}

- project

project

Update a network segment range

rule:admin_only

- PUT /network_segment_ranges/{id}/tags

PUT /network_segment_ranges/{id}/tags

- PUT /network_segment_ranges/{id}/tags/{tag_id}

PUT /network_segment_ranges/{id}/tags/{tag_id}

- project

project

Update the network segment range tags

rule:admin_only

- DELETE /network_segment_ranges/{id}

DELETE /network_segment_ranges/{id}

- project

project

Delete a network segment range

rule:admin_only

- DELETE /network_segment_ranges/{id}/tags

DELETE /network_segment_ranges/{id}/tags

- DELETE /network_segment_ranges/{id}/tags/{tag_id}

DELETE /network_segment_ranges/{id}/tags/{tag_id}

- project

project

Delete the network segment range tags

(rule:admin_only) or (rule:service_api)

- GET /ports/{port_id}/bindings/

GET /ports/{port_id}/bindings/

- project

project

Get port binding information

rule:service_api

- POST /ports/{port_id}/bindings/

POST /ports/{port_id}/bindings/

- project

project

Create port binding on the host

rule:service_api

- DELETE /ports/{port_id}/bindings/

DELETE /ports/{port_id}/bindings/

- project

project

Delete port binding on the host

rule:service_api

- PUT /ports/{port_id}/bindings/{host}

PUT /ports/{port_id}/bindings/{host}

- project

project

Activate port binding on the host

field:port:device_owner=~^network:

Definition of port with network device_owner

rule:context_is_admin or role:data_plane_integrator

Rule for data plane integration

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:service_api

- POST /ports

POST /ports

- project

project

Create a port

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:service_api

- POST /ports

POST /ports

- project

project

Specify device_id attribute when creating a port

not rule:network_device or (rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- POST /ports

POST /ports

- project

project

Specify device_owner attribute when creating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- POST /ports

POST /ports

- project

project

Specify mac_address attribute when creating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner or rule:shared

- POST /ports

POST /ports

- project

project

Specify fixed_ips information when creating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- POST /ports

POST /ports

- project

project

Specify IP address in fixed_ips when creating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner or rule:shared

- POST /ports

POST /ports

- project

project

Specify subnet ID in fixed_ips when creating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- POST /ports

POST /ports

- project

project

Specify port_security_enabled attribute when creating a port

(rule:admin_only) or (rule:service_api)

- POST /ports

POST /ports

- project

project

Specify binding:host_id attribute when creating a port

rule:service_api

- POST /ports

POST /ports

- project

project

Specify binding:profile attribute when creating a port

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:service_api

- POST /ports

POST /ports

- project

project

Specify binding:vnic_type attribute when creating a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- POST /ports

POST /ports

- project

project

Specify allowed_address_pairs attribute when creating a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- POST /ports

POST /ports

- project

project

Specify mac_address` of `allowed_address_pairs attribute when creating a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- POST /ports

POST /ports

- project

project

Specify ip_address of allowed_address_pairs attribute when creating a port

rule:admin_only

- POST /ports

POST /ports

- project

project

Specify hints attribute when creating a port

rule:admin_only

- POST /ports

POST /ports

- project

project

Specify trusted attribute when creating a port

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:context_is_advsvc

- POST /ports/{id}/tags

POST /ports/{id}/tags

- project

project

Create the port tags

(rule:admin_only) or (rule:service_api) or role:reader and rule:network_owner or role:reader and project_id:%(project_id)s

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get a port

(rule:admin_only) or (rule:service_api)

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get binding:vif_type attribute of a port

(rule:admin_only) or (rule:service_api)

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get binding:vif_details attribute of a port

(rule:admin_only) or (rule:service_api)

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get binding:host_id attribute of a port

(rule:admin_only) or (rule:service_api)

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get binding:profile attribute of a port

rule:admin_only

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get resource_request attribute of a port

rule:admin_only

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get hints attribute of a port

rule:admin_only

- GET /ports

GET /ports

- GET /ports/{id}

GET /ports/{id}

- project

project

Get trusted attribute of a port

rule:context_is_advsvc or (rule:admin_only) or (role:reader and rule:network_owner) or role:reader and project_id:%(project_id)s

- GET /ports/{id}/tags

GET /ports/{id}/tags

- GET /ports/{id}/tags/{tag_id}

GET /ports/{id}/tags/{tag_id}

- project

project

Get the port tags

(rule:admin_only) or (rule:service_api) or role:member and project_id:%(project_id)s

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update a port

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:service_api

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update device_id attribute of a port

not rule:network_device or (rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update device_owner attribute of a port

(rule:admin_only) or (rule:service_api) or role:manager and rule:network_owner

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update mac_address attribute of a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Specify fixed_ips information when updating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Specify IP address in fixed_ips information when updating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner or rule:shared

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Specify subnet ID in fixed_ips information when updating a port

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update port_security_enabled attribute of a port

(rule:admin_only) or (rule:service_api)

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update binding:host_id attribute of a port

rule:service_api

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update binding:profile attribute of a port

(rule:admin_only) or (rule:service_api) or role:member and project_id:%(project_id)s

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update binding:vnic_type attribute of a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update allowed_address_pairs attribute of a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update mac_address of allowed_address_pairs attribute of a port

(rule:admin_only) or (role:member and rule:network_owner) or rule:service_api

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update ip_address of allowed_address_pairs attribute of a port

rule:admin_only or role:data_plane_integrator

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update data_plane_status attribute of a port

rule:admin_only

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update hints attribute of a port

rule:admin_only

- PUT /ports/{id}

PUT /ports/{id}

- project

project

Update trusted attribute of a port

(rule:admin_only) or (role:member and project_id:%(project_id)s) or rule:context_is_advsvc

- PUT /ports/{id}/tags

PUT /ports/{id}/tags

- PUT /ports/{id}/tags/{tag_id}

PUT /ports/{id}/tags/{tag_id}

- project

project

Update the port tags

(rule:admin_only) or (rule:service_api) or role:member and rule:network_owner or role:member and project_id:%(project_id)s

- DELETE /ports/{id}

DELETE /ports/{id}

- project

project

Delete a port

rule:context_is_advsvc or role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- DELETE /ports/{id}/tags

DELETE /ports/{id}/tags

- DELETE /ports/{id}/tags/{tag_id}

DELETE /ports/{id}/tags/{tag_id}

- project

project

Delete the port tags

field:policies:shared=True

Rule of shared qos policy

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_qos_policy

- GET /qos/policies

GET /qos/policies

- GET /qos/policies/{id}

GET /qos/policies/{id}

- project

project

Get QoS policies

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_qos_policy

- GET /qos/policies/{id}/tags

GET /qos/policies/{id}/tags

- GET /qos/policies/{id}/tags/{tag_id}

GET /qos/policies/{id}/tags/{tag_id}

- project

project

Get QoS policy tags

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /qos/policies

POST /qos/policies

- project

project

Create a QoS policy

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- POST /qos/policies/{id}/tags

POST /qos/policies/{id}/tags

- project

project

Create the QoS policy tags

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- PUT /qos/policies/{id}

PUT /qos/policies/{id}

- project

project

Update a QoS policy

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- PUT /qos/policies/{id}/tags

PUT /qos/policies/{id}/tags

- PUT /qos/policies/{id}/tags/{tag_id}

PUT /qos/policies/{id}/tags/{tag_id}

- project

project

Update the QoS policy tags

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- DELETE /qos/policies/{id}

DELETE /qos/policies/{id}

- project

project

Delete a QoS policy

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- DELETE /qos/policies/{id}/tags

DELETE /qos/policies/{id}/tags

- DELETE /qos/policies/{id}/tags/{tag_id}

DELETE /qos/policies/{id}/tags/{tag_id}

- project

project

Delete the QoS policy tags

role:reader

- GET /qos/rule-types

GET /qos/rule-types

- GET /qos/rule-types/{rule_type}

GET /qos/rule-types/{rule_type}

- project

project

Get available QoS rule types

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/policies/{policy_id}/bandwidth_limit_rules

GET /qos/policies/{policy_id}/bandwidth_limit_rules

- GET /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

GET /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

- project

project

Get a QoS bandwidth limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- POST /qos/policies/{policy_id}/bandwidth_limit_rules

POST /qos/policies/{policy_id}/bandwidth_limit_rules

- project

project

Create a QoS bandwidth limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

PUT /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

- project

project

Update a QoS bandwidth limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

DELETE /qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

- project

project

Delete a QoS bandwidth limit rule

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/policies/{policy_id}/packet_rate_limit_rules

GET /qos/policies/{policy_id}/packet_rate_limit_rules

- GET /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

GET /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

- project

project

Get a QoS packet rate limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- POST /qos/policies/{policy_id}/packet_rate_limit_rules

POST /qos/policies/{policy_id}/packet_rate_limit_rules

- project

project

Create a QoS packet rate limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

PUT /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

- project

project

Update a QoS packet rate limit rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

DELETE /qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

- project

project

Delete a QoS packet rate limit rule

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/policies/{policy_id}/dscp_marking_rules

GET /qos/policies/{policy_id}/dscp_marking_rules

- GET /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

GET /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

- project

project

Get a QoS DSCP marking rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- POST /qos/policies/{policy_id}/dscp_marking_rules

POST /qos/policies/{policy_id}/dscp_marking_rules

- project

project

Create a QoS DSCP marking rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

PUT /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

- project

project

Update a QoS DSCP marking rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

DELETE /qos/policies/{policy_id}/dscp_marking_rules/{rule_id}

- project

project

Delete a QoS DSCP marking rule

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/policies/{policy_id}/minimum_bandwidth_rules

GET /qos/policies/{policy_id}/minimum_bandwidth_rules

- GET /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

GET /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

- project

project

Get a QoS minimum bandwidth rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- POST /qos/policies/{policy_id}/minimum_bandwidth_rules

POST /qos/policies/{policy_id}/minimum_bandwidth_rules

- project

project

Create a QoS minimum bandwidth rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

PUT /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

- project

project

Update a QoS minimum bandwidth rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

DELETE /qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

- project

project

Delete a QoS minimum bandwidth rule

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/policies/{policy_id}/minimum_packet_rate_rules

GET /qos/policies/{policy_id}/minimum_packet_rate_rules

- GET /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

GET /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

- project

project

Get a QoS minimum packet rate rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- POST /qos/policies/{policy_id}/minimum_packet_rate_rules

POST /qos/policies/{policy_id}/minimum_packet_rate_rules

- project

project

Create a QoS minimum packet rate rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

PUT /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

- project

project

Update a QoS minimum packet rate rule

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

DELETE /qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

- project

project

Delete a QoS minimum packet rate rule

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/alias_bandwidth_limit_rules/{rule_id}/

GET /qos/alias_bandwidth_limit_rules/{rule_id}/

- project

project

Get a QoS bandwidth limit rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/alias_bandwidth_limit_rules/{rule_id}/

PUT /qos/alias_bandwidth_limit_rules/{rule_id}/

- project

project

Update a QoS bandwidth limit rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/alias_bandwidth_limit_rules/{rule_id}/

DELETE /qos/alias_bandwidth_limit_rules/{rule_id}/

- project

project

Delete a QoS bandwidth limit rule through alias

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/alias_dscp_marking_rules/{rule_id}/

GET /qos/alias_dscp_marking_rules/{rule_id}/

- project

project

Get a QoS DSCP marking rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/alias_dscp_marking_rules/{rule_id}/

PUT /qos/alias_dscp_marking_rules/{rule_id}/

- project

project

Update a QoS DSCP marking rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/alias_dscp_marking_rules/{rule_id}/

DELETE /qos/alias_dscp_marking_rules/{rule_id}/

- project

project

Delete a QoS DSCP marking rule through alias

(rule:admin_only) or (role:reader and rule:ext_parent_owner)

- GET /qos/alias_minimum_bandwidth_rules/{rule_id}/

GET /qos/alias_minimum_bandwidth_rules/{rule_id}/

- project

project

Get a QoS minimum bandwidth rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- PUT /qos/alias_minimum_bandwidth_rules/{rule_id}/

PUT /qos/alias_minimum_bandwidth_rules/{rule_id}/

- project

project

Update a QoS minimum bandwidth rule through alias

(rule:admin_only) or (role:manager and rule:ext_parent_owner)

- DELETE /qos/alias_minimum_bandwidth_rules/{rule_id}/

DELETE /qos/alias_minimum_bandwidth_rules/{rule_id}/

- project

project

Delete a QoS minimum bandwidth rule through alias

rule:get_policy_minimum_packet_rate_rule

- GET /qos/alias_minimum_packet_rate_rules/{rule_id}/

GET /qos/alias_minimum_packet_rate_rules/{rule_id}/

- project

project

Get a QoS minimum packet rate rule through alias

rule:update_policy_minimum_packet_rate_rule

- PUT /qos/alias_minimum_packet_rate_rules/{rule_id}/

PUT /qos/alias_minimum_packet_rate_rules/{rule_id}/

- project

project

Update a QoS minimum packet rate rule through alias

rule:delete_policy_minimum_packet_rate_rule

- DELETE /qos/alias_minimum_packet_rate_rules/{rule_id}/

DELETE /qos/alias_minimum_packet_rate_rules/{rule_id}/

- project

project

Delete a QoS minimum packet rate rule through alias

(rule:admin_only) or (role:manager and project_id:%(project_id)s)

- GET /quota

GET /quota

- GET /quota/{id}

GET /quota/{id}

- project

project

Get a resource quota

rule:admin_only

- PUT /quota/{id}

PUT /quota/{id}

- project

project

Update a resource quota

rule:admin_only

- DELETE /quota/{id}

DELETE /quota/{id}

- project

project

Delete a resource quota

(not field:rbac_policy:target_tenant=* and not field:rbac_policy:target_project=*) or rule:admin_only

Definition of a wildcard target_project

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /rbac-policies

POST /rbac-policies

- project

project

Create an RBAC policy

rule:admin_only or (not field:rbac_policy:target_tenant=* and not field:rbac_policy:target_project=*)

- POST /rbac-policies

POST /rbac-policies

- project

project

Specify target_tenant when creating an RBAC policy

rule:admin_only or not field:rbac_policy:target_project=*

- POST /rbac-policies

POST /rbac-policies

- project

project

Specify target_project when creating an RBAC policy

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /rbac-policies/{id}

PUT /rbac-policies/{id}

- project

project

Update an RBAC policy

rule:admin_only or (not field:rbac_policy:target_tenant=* and not field:rbac_policy:target_project=*)

- PUT /rbac-policies/{id}

PUT /rbac-policies/{id}

- project

project

Update target_tenant attribute of an RBAC policy

rule:admin_only or not field:rbac_policy:target_project=*

- PUT /rbac-policies/{id}

PUT /rbac-policies/{id}

- project

project

Update target_project attribute of an RBAC policy

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /rbac-policies

GET /rbac-policies

- GET /rbac-policies/{id}

GET /rbac-policies/{id}

- project

project

Get an RBAC policy

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /rbac-policies/{id}

DELETE /rbac-policies/{id}

- project

project

Delete an RBAC policy

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /routers

POST /routers

- project

project

Create a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify distributed attribute when creating a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify ha attribute when creating a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /routers

POST /routers

- project

project

Specify external_gateway_info information when creating a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /routers

POST /routers

- project

project

Specify network_id in external_gateway_info information when creating a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify enable_snat in external_gateway_info information when creating a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify external_fixed_ips in external_gateway_info information when creating a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify enable_default_route_bfd attribute when creating a router

rule:admin_only

- POST /routers

POST /routers

- project

project

Specify enable_default_route_ecmp attribute when creating a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /routers/{id}/tags

POST /routers/{id}/tags

- project

project

Create the router tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /routers

GET /routers

- GET /routers/{id}

GET /routers/{id}

- project

project

Get a router

rule:admin_only

- GET /routers

GET /routers

- GET /routers/{id}

GET /routers/{id}

- project

project

Get distributed attribute of a router

rule:admin_only

- GET /routers

GET /routers

- GET /routers/{id}

GET /routers/{id}

- project

project

Get ha attribute of a router

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /routers/{id}/tags

GET /routers/{id}/tags

- GET /routers/{id}/tags/{tag_id}

GET /routers/{id}/tags/{tag_id}

- project

project

Get the router tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update distributed attribute of a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update ha attribute of a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update external_gateway_info information of a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update network_id attribute of external_gateway_info information of a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update enable_snat attribute of external_gateway_info information of a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update external_fixed_ips attribute of external_gateway_info information of a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Specify enable_default_route_bfd attribute when updating a router

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Specify enable_default_route_ecmp attribute when updating a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}/tags

PUT /routers/{id}/tags

- PUT /routers/{id}/tags/{tag_id}

PUT /routers/{id}/tags/{tag_id}

- project

project

Update the router tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /routers/{id}

DELETE /routers/{id}

- project

project

Delete a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /routers/{id}/tags

DELETE /routers/{id}/tags

- DELETE /routers/{id}/tags/{tag_id}

DELETE /routers/{id}/tags/{tag_id}

- project

project

Delete the router tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}/add_router_interface

PUT /routers/{id}/add_router_interface

- project

project

Add an interface to a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}/remove_router_interface

PUT /routers/{id}/remove_router_interface

- project

project

Remove an interface from a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}/add_extraroutes

PUT /routers/{id}/add_extraroutes

- project

project

Add extra route to a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}/remove_extraroutes

PUT /routers/{id}/remove_extraroutes

- project

project

Remove extra route from a router

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Add router external gateways

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Add router external gateways

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Add router external gateways with defined network ID

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Add router external gateways specifying SNAT flag

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Add router external gateways specifying the fixed IPs

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update router external gateways

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update router external gateways

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update router external gateways network ID

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update router external gateways SNAT flag

rule:admin_only

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Update router external gateways fixed IPs

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Remove router external gateways

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /routers/{id}

PUT /routers/{id}

- project

project

Remove router external gateways

rule:context_is_admin or project_id:%(security_group:project_id)s

Rule for admin or security group owner access

rule:owner or rule:admin_or_sg_owner

Rule for resource owner, admin or security group owner access

field:security_groups:shared=True

Definition of a shared security group

field:security_group_rules:belongs_to_default_sg=True

Definition of a security group rule that belongs to the project default security group

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /security-groups

POST /security-groups

- project

project

Create a security group

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /security-groups/{id}/tags

POST /security-groups/{id}/tags

- project

project

Create the security group tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_security_group

- GET /security-groups

GET /security-groups

- GET /security-groups/{id}

GET /security-groups/{id}

- project

project

Get a security group

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_security_group

- GET /security-groups/{id}/tags

GET /security-groups/{id}/tags

- GET /security-groups/{id}/tags/{tag_id}

GET /security-groups/{id}/tags/{tag_id}

- project

project

Get the security group tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /security-groups/{id}

PUT /security-groups/{id}

- project

project

Update a security group

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /security-groups/{id}/tags

PUT /security-groups/{id}/tags

- PUT /security-groups/{id}/tags/{tag_id}

PUT /security-groups/{id}/tags/{tag_id}

- project

project

Update the security group tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /security-groups/{id}

DELETE /security-groups/{id}

- project

project

Delete a security group

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /security-groups/{id}/tags

DELETE /security-groups/{id}/tags

- DELETE /security-groups/{id}/tags/{tag_id}

DELETE /security-groups/{id}/tags/{tag_id}

- project

project

Delete the security group tags

(rule:admin_only) or (role:member and rule:sg_owner)

- POST /security-group-rules

POST /security-group-rules

- project

project

Create a security group rule

(rule:admin_only) or (role:reader and rule:sg_owner)

- GET /security-group-rules

GET /security-group-rules

- GET /security-group-rules/{id}

GET /security-group-rules/{id}

- project

project

Get a security group rule

(rule:admin_only) or (role:member and rule:sg_owner)

- DELETE /security-group-rules/{id}

DELETE /security-group-rules/{id}

- project

project

Delete a security group rule

rule:admin_only

- POST /segments

POST /segments

- project

project

Create a segment

rule:admin_only

- POST /segments/{id}/tags

POST /segments/{id}/tags

- project

project

Create the segment tags

rule:admin_only

- GET /segments

GET /segments

- GET /segments/{id}

GET /segments/{id}

- project

project

Get a segment

rule:admin_only

- GET /segments/{id}/tags

GET /segments/{id}/tags

- GET /segments/{id}/tags/{tag_id}

GET /segments/{id}/tags/{tag_id}

- project

project

Get the segment tags

rule:admin_only

- PUT /segments/{id}

PUT /segments/{id}

- project

project

Update a segment

rule:admin_only

- PUT /segments/{id}/tags

PUT /segments/{id}/tags

- PUT /segments/{id}/tags/{tag_id}

PUT /segments/{id}/tags/{tag_id}

- project

project

Update the segment tags

rule:admin_only

- DELETE /segments/{id}

DELETE /segments/{id}

- project

project

Delete a segment

rule:admin_only

- DELETE /segments/{id}/tags

DELETE /segments/{id}/tags

- DELETE /segments/{id}/tags/{tag_id}

DELETE /segments/{id}/tags/{tag_id}

- project

project

Delete the segment tags

role:reader

- GET /service-providers

GET /service-providers

- project

project

Get service providers

field:subnets:router:external=True

Definition of a subnet that belongs to an external network

(rule:admin_only) or (role:member and rule:network_owner)

- POST /subnets

POST /subnets

- project

project

Create a subnet

rule:admin_only

- POST /subnets

POST /subnets

- project

project

Specify segment_id attribute when creating a subnet

rule:admin_only

- POST /subnets

POST /subnets

- project

project

Specify service_types attribute when creating a subnet

role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- POST /subnets/{id}/tags

POST /subnets/{id}/tags

- project

project

Create the subnet tags

role:reader and project_id:%(project_id)s or rule:shared or rule:external_network or (rule:admin_only) or (role:reader and rule:network_owner) or rule:service_api

- GET /subnets

GET /subnets

- GET /subnets/{id}

GET /subnets/{id}

- project

project

Get a subnet

rule:admin_only

- GET /subnets

GET /subnets

- GET /subnets/{id}

GET /subnets/{id}

- project

project

Get segment_id attribute of a subnet

role:reader and project_id:%(project_id)s or rule:shared or rule:external_network or (rule:admin_only) or (role:reader and rule:network_owner)

- GET /subnets/{id}/tags

GET /subnets/{id}/tags

- GET /subnets/{id}/tags/{tag_id}

GET /subnets/{id}/tags/{tag_id}

- project

project

Get the subnet tags

role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- PUT /subnets/{id}

PUT /subnets/{id}

- project

project

Update a subnet

rule:admin_only

- PUT /subnets/{id}

PUT /subnets/{id}

- project

project

Update segment_id attribute of a subnet

rule:admin_only

- PUT /subnets/{id}

PUT /subnets/{id}

- project

project

Update service_types attribute of a subnet

role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- PUT /subnets/{id}/tags

PUT /subnets/{id}/tags

- PUT /subnets/{id}/tags/{tag_id}

PUT /subnets/{id}/tags/{tag_id}

- project

project

Update the subnet tags

role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- DELETE /subnets/{id}

DELETE /subnets/{id}

- project

project

Delete a subnet

role:member and project_id:%(project_id)s or (rule:admin_only) or (role:member and rule:network_owner)

- DELETE /subnets/{id}/tags

DELETE /subnets/{id}/tags

- DELETE /subnets/{id}/tags/{tag_id}

DELETE /subnets/{id}/tags/{tag_id}

- project

project

Delete the subnet tags

field:subnetpools:shared=True

Definition of a shared subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /subnetpools

POST /subnetpools

- project

project

Create a subnetpool

rule:admin_only

- POST /subnetpools

POST /subnetpools

- project

project

Create a shared subnetpool

rule:admin_only

- POST /subnetpools

POST /subnetpools

- project

project

Specify is_default attribute when creating a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /subnetpools/{id}/tags

POST /subnetpools/{id}/tags

- project

project

Create the subnetpool tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_subnetpools

- GET /subnetpools

GET /subnetpools

- GET /subnetpools/{id}

GET /subnetpools/{id}

- project

project

Get a subnetpool

(rule:admin_only) or (role:reader and project_id:%(project_id)s) or rule:shared_subnetpools

- GET /subnetpools/{id}/tags

GET /subnetpools/{id}/tags

- GET /subnetpools/{id}/tags/{tag_id}

GET /subnetpools/{id}/tags/{tag_id}

- project

project

Get the subnetpool tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /subnetpools/{id}

PUT /subnetpools/{id}

- project

project

Update a subnetpool

rule:admin_only

- PUT /subnetpools/{id}

PUT /subnetpools/{id}

- project

project

Update is_default attribute of a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /subnetpools/{id}/tags

PUT /subnetpools/{id}/tags

- PUT /subnetpools/{id}/tags/{tag_id}

PUT /subnetpools/{id}/tags/{tag_id}

- project

project

Update the subnetpool tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /subnetpools/{id}

DELETE /subnetpools/{id}

- project

project

Delete a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /subnetpools/{id}/tags

DELETE /subnetpools/{id}/tags

- DELETE /subnetpools/{id}/tags/{tag_id}

DELETE /subnetpools/{id}/tags/{tag_id}

- project

project

Delete the subnetpool tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /subnetpools/{id}/onboard_network_subnets

PUT /subnetpools/{id}/onboard_network_subnets

- project

project

Onboard existing subnet into a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /subnetpools/{id}/add_prefixes

PUT /subnetpools/{id}/add_prefixes

- project

project

Add prefixes to a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /subnetpools/{id}/remove_prefixes

PUT /subnetpools/{id}/remove_prefixes

- project

project

Remove unallocated prefixes from a subnetpool

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /trunks

POST /trunks

- project

project

Create a trunk

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- POST /trunks/{id}/tags

POST /trunks/{id}/tags

- project

project

Create the trunk tags

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /trunks

GET /trunks

- GET /trunks/{id}

GET /trunks/{id}

- project

project

Get a trunk

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /trunks/{id}/tags

GET /trunks/{id}/tags

- GET /trunks/{id}/tags/{tag_id}

GET /trunks/{id}/tags/{tag_id}

- project

project

Get the trunk tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /trunks/{id}

PUT /trunks/{id}

- project

project

Update a trunk

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /trunks/{id}/tags

PUT /trunks/{id}/tags

- PUT /trunks/{id}/tags/{tag_id}

PUT /trunks/{id}/tags/{tag_id}

- project

project

Update the trunk tags

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /trunks/{id}

DELETE /trunks/{id}

- project

project

Delete a trunk

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- DELETE /trunks/{id}/tags

DELETE /trunks/{id}/tags

- DELETE /trunks/{id}/tags/{tag_id}

DELETE /trunks/{id}/tags/{tag_id}

- project

project

Delete a trunk

(rule:admin_only) or (role:reader and project_id:%(project_id)s)

- GET /trunks/{id}/get_subports

GET /trunks/{id}/get_subports

- project

project

List subports attached to a trunk

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /trunks/{id}/add_subports

PUT /trunks/{id}/add_subports

- project

project

Add subports to a trunk

(rule:admin_only) or (role:member and project_id:%(project_id)s)

- PUT /trunks/{id}/remove_subports

PUT /trunks/{id}/remove_subports

- project

project

Delete subports from a trunk
