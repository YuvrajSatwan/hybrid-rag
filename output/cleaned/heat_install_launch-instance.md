# Launch an instance ¶

In environments that include the Orchestration service, you can create a stack
that launches an instance.

## Create a template ¶

The Orchestration service uses templates to describe stacks.
To learn about the template language, see the Template Guide .

- Create the demo-template.yml file with the following content: heat_template_version : 2015-10-15 description : Launch a basic instance with CirrOS image using the ``m1.tiny`` flavor, ``mykey`` key,  and one network. parameters : NetID : type : string description : Network ID to use for the instance. resources : server : type : OS::Nova::Server properties : image : cirros flavor : m1.tiny key_name : mykey networks : - network : { get_param : NetID } outputs : instance_name : description : Name of the instance. value : { get_attr : [ server , name ] } instance_ip : description : IP address of the instance. value : { get_attr : [ server , first_address ] }

Create the demo-template.yml file with the following content:

heat_template_version : 2015-10-15 description : Launch a basic instance with CirrOS image using the ``m1.tiny`` flavor, ``mykey`` key,  and one network. parameters : NetID : type : string description : Network ID to use for the instance. resources : server : type : OS::Nova::Server properties : image : cirros flavor : m1.tiny key_name : mykey networks : - network : { get_param : NetID } outputs : instance_name : description : Name of the instance. value : { get_attr : [ server , name ] } instance_ip : description : IP address of the instance. value : { get_attr : [ server , first_address ] }

## Create a stack ¶

Create a stack using the demo-template.yml template.

- Source the demo credentials to perform
the following steps as a non-administrative project: $ . demo-openrc

Source the demo credentials to perform
the following steps as a non-administrative project:

$ . demo-openrc

- Determine available networks. $ openstack network list +--------------------------------------+-------------+--------------------------------------+ | ID                                   | Name        | Subnets                              | +--------------------------------------+-------------+--------------------------------------+ | 4716ddfe-6e60-40e7-b2a8-42e57bf3c31c | selfservice | 2112d5eb-f9d6-45fd-906e-7cabd38b7c7c | | b5b6993c-ddf9-40e7-91d0-86806a42edb8 | provider    | 310911f6-acf0-4a47-824e-3032916582ff | +--------------------------------------+-------------+--------------------------------------+ Note This output may differ from your environment.

Determine available networks.

$ openstack network list +--------------------------------------+-------------+--------------------------------------+ | ID                                   | Name        | Subnets                              | +--------------------------------------+-------------+--------------------------------------+ | 4716ddfe-6e60-40e7-b2a8-42e57bf3c31c | selfservice | 2112d5eb-f9d6-45fd-906e-7cabd38b7c7c | | b5b6993c-ddf9-40e7-91d0-86806a42edb8 | provider    | 310911f6-acf0-4a47-824e-3032916582ff | +--------------------------------------+-------------+--------------------------------------+

Note

This output may differ from your environment.

- Set the NET_ID environment variable to reflect the ID of a network.
For example, using the provider network: $ export NET_ID = $( openstack network list | awk '/ provider / { print $2 }' )

Set the NET_ID environment variable to reflect the ID of a network.
For example, using the provider network:

$ export NET_ID = $( openstack network list | awk '/ provider / { print $2 }' )

- Create a stack of one CirrOS instance on the provider network: $ openstack stack create -t demo-template.yml --parameter "NetID= $NET_ID " stack +--------------------------------------+------------+--------------------+---------------------+--------------+ | ID                                   | Stack Name | Stack Status       | Creation Time       | Updated Time | +--------------------------------------+------------+--------------------+---------------------+--------------+ | dbf46d1b-0b97-4d45-a0b3-9662a1eb6cf3 | stack      | CREATE_IN_PROGRESS | 2015-10-13T15:27:20 | None         | +--------------------------------------+------------+--------------------+---------------------+--------------+

Create a stack of one CirrOS instance on the provider network:

$ openstack stack create -t demo-template.yml --parameter "NetID= $NET_ID " stack +--------------------------------------+------------+--------------------+---------------------+--------------+ | ID                                   | Stack Name | Stack Status       | Creation Time       | Updated Time | +--------------------------------------+------------+--------------------+---------------------+--------------+ | dbf46d1b-0b97-4d45-a0b3-9662a1eb6cf3 | stack      | CREATE_IN_PROGRESS | 2015-10-13T15:27:20 | None         | +--------------------------------------+------------+--------------------+---------------------+--------------+

- After a short time, verify successful creation of the stack: $ openstack stack list +--------------------------------------+------------+-----------------+---------------------+--------------+ | ID                                   | Stack Name | Stack Status    | Creation Time       | Updated Time | +--------------------------------------+------------+-----------------+---------------------+--------------+ | dbf46d1b-0b97-4d45-a0b3-9662a1eb6cf3 | stack      | CREATE_COMPLETE | 2015-10-13T15:27:20 | None         | +--------------------------------------+------------+-----------------+---------------------+--------------+

After a short time, verify successful creation of the stack:

$ openstack stack list +--------------------------------------+------------+-----------------+---------------------+--------------+ | ID                                   | Stack Name | Stack Status    | Creation Time       | Updated Time | +--------------------------------------+------------+-----------------+---------------------+--------------+ | dbf46d1b-0b97-4d45-a0b3-9662a1eb6cf3 | stack      | CREATE_COMPLETE | 2015-10-13T15:27:20 | None         | +--------------------------------------+------------+-----------------+---------------------+--------------+

- Show the name and IP address of the instance and compare with the output
of the OpenStack client: $ openstack stack output show --all stack [ { "output_value": "stack-server-3nzfyfofu6d4", "description": "Name of the instance.", "output_key": "instance_name" }, { "output_value": "10.4.31.106", "description": "IP address of the instance.", "output_key": "instance_ip" } ] $ openstack server list +--------------------------------------+---------------------------+--------+---------------------------------+ | ID                                   | Name                      | Status | Networks                        | +--------------------------------------+---------------------------+--------+---------------------------------+ | 0fc2af0c-ae79-4d22-8f36-9e860c257da5 | stack-server-3nzfyfofu6d4 | ACTIVE | public=10.4.31.106              | +--------------------------------------+---------------------------+--------+---------------------------------+

Show the name and IP address of the instance and compare with the output
of the OpenStack client:

$ openstack stack output show --all stack [ { "output_value": "stack-server-3nzfyfofu6d4", "description": "Name of the instance.", "output_key": "instance_name" }, { "output_value": "10.4.31.106", "description": "IP address of the instance.", "output_key": "instance_ip" } ]

$ openstack server list +--------------------------------------+---------------------------+--------+---------------------------------+ | ID                                   | Name                      | Status | Networks                        | +--------------------------------------+---------------------------+--------+---------------------------------+ | 0fc2af0c-ae79-4d22-8f36-9e860c257da5 | stack-server-3nzfyfofu6d4 | ACTIVE | public=10.4.31.106              | +--------------------------------------+---------------------------+--------+---------------------------------+

- Delete the stack. $ openstack stack delete --yes stack

Delete the stack.

$ openstack stack delete --yes stack
