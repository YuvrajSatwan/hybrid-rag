# Placement Usage Â¶

## Tracking Resources Â¶

The placement service enables other projects to track their own resources.
Those projects can register/delete their own resources to/from placement
via the placement HTTP API .

The placement service originated in the Nova project . As a
result much of the functionality in placement was driven by novaâs
requirements. However, that functionality was designed to be sufficiently
generic to be used by any service that needs to manage the selection and
consumption of resources.

### How Nova Uses Placement Â¶

Two processes, nova-compute and nova-scheduler , host most of novaâs
interaction with placement.

The nova resource tracker in nova-compute is responsible for creating the
resource provider record corresponding to the compute host on which the
resource tracker runs, setting the inventory that describes the quantitative
resources that are available for workloads to consume (e.g., VCPU ), and setting the traits that describe qualitative aspects of the resources (e.g., STORAGE_DISK_SSD ).

If other projects â for example, Neutron or Cyborg â wish to manage resources
on a compute host, they should create resource providers as children of the
compute host provider and register their own managed resources as inventory on
those child providers. For more information, see the Modeling with Provider Trees .

The nova-scheduler is responsible for selecting a set of suitable
destination hosts for a workload. It begins by formulating a request to
placement for a list of allocation candidates . That request expresses
quantitative and qualitative requirements, membership in aggregates, and in
more complex cases, the topology of related resources. That list is reduced and
ordered by filters and weighers within the scheduler process. An allocation is made against a resource provider representing a destination, consuming a
portion of the inventory set by the resource tracker.

## REST API Â¶

The placement API service provides a well-documented, JSON-based HTTP API and data model. It is designed to be easy to use from whatever HTTP client is
suitable. There is a plugin to the openstackclient command line tool called osc-placement which is useful for occasional inspection and manipulation of
the resources in the placement service.

### Microversions Â¶

The placement API uses microversions for making incremental changes to the
API which client requests must opt into.

It is especially important to keep in mind that nova-compute is a client of
the placement REST API and based on how Nova supports rolling upgrades the
nova-compute service could be Newton level code making requests to an Ocata
placement API, and vice-versa, an Ocata compute service in a cells v2 cell
could be making requests to a Newton placement API.

This history of placement microversions may be found in the following
subsection.

- REST API Version History Newton Ocata Pike Queens Rocky Stein Train Xena

- Newton

- Ocata

- Pike

- Queens

- Rocky

- Stein

- Train

- Xena
