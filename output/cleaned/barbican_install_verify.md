# Verify operation ¶

Verify operation of the Key Manager (barbican) service.

Note

Perform these commands on the controller node.

- Install python-barbicanclient package: For Red Hat Enterprise Linux and CentOS: $ dnf install python-barbicanclient For Ubuntu: $ apt-get install python-barbicanclient

Install python-barbicanclient package:

- For Red Hat Enterprise Linux and CentOS: $ dnf install python-barbicanclient

For Red Hat Enterprise Linux and CentOS:

$ dnf install python-barbicanclient

- For Ubuntu: $ apt-get install python-barbicanclient

For Ubuntu:

$ apt-get install python-barbicanclient

- Source the admin credentials to be able to perform Barbican
API calls: $ . admin-openrc

Source the admin credentials to be able to perform Barbican
API calls:

$ . admin-openrc

- Use the OpenStack CLI to store a secret: $ openstack secret store --name mysecret --payload j4 =] d21 +---------------+-----------------------------------------------------------------------+ | Field         | Value                                                                 | +---------------+-----------------------------------------------------------------------+ | Secret href   | http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa | | Name          | mysecret                                                              | | Created       | None                                                                  | | Status        | None                                                                  | | Content types | None                                                                  | | Algorithm     | aes                                                                   | | Bit length    | 256                                                                   | | Secret type   | opaque                                                                | | Mode          | cbc                                                                   | | Expiration    | None                                                                  | +---------------+-----------------------------------------------------------------------+

Use the OpenStack CLI to store a secret:

$ openstack secret store --name mysecret --payload j4 =] d21 +---------------+-----------------------------------------------------------------------+ | Field         | Value                                                                 | +---------------+-----------------------------------------------------------------------+ | Secret href   | http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa | | Name          | mysecret                                                              | | Created       | None                                                                  | | Status        | None                                                                  | | Content types | None                                                                  | | Algorithm     | aes                                                                   | | Bit length    | 256                                                                   | | Secret type   | opaque                                                                | | Mode          | cbc                                                                   | | Expiration    | None                                                                  | +---------------+-----------------------------------------------------------------------+

- Confirm that the secret was stored by retrieving it: $ openstack secret get http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa +---------------+-----------------------------------------------------------------------+ | Field         | Value                                                                 | +---------------+-----------------------------------------------------------------------+ | Secret href   | http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa | | Name          | mysecret                                                              | | Created       | 2016-08-16 16:04:10+00:00                                             | | Status        | ACTIVE                                                                | | Content types | {'default': 'application/octet-stream'}                               | | Algorithm     | aes                                                                   | | Bit length    | 256                                                                   | | Secret type   | opaque                                                                | | Mode          | cbc                                                                   | | Expiration    | None                                                                  | +---------------+-----------------------------------------------------------------------+ Note Some items are populated after the secret has been created and will only
display when retrieving it.

Confirm that the secret was stored by retrieving it:

$ openstack secret get http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa +---------------+-----------------------------------------------------------------------+ | Field         | Value                                                                 | +---------------+-----------------------------------------------------------------------+ | Secret href   | http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa | | Name          | mysecret                                                              | | Created       | 2016-08-16 16:04:10+00:00                                             | | Status        | ACTIVE                                                                | | Content types | {'default': 'application/octet-stream'}                               | | Algorithm     | aes                                                                   | | Bit length    | 256                                                                   | | Secret type   | opaque                                                                | | Mode          | cbc                                                                   | | Expiration    | None                                                                  | +---------------+-----------------------------------------------------------------------+

Note

Some items are populated after the secret has been created and will only
display when retrieving it.

- Confirm that the secret payload was stored by retrieving it: $ openstack secret get http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa --payload +---------+---------+ | Field   | Value   | +---------+---------+ | Payload | j4=]d21 | +---------+---------+

Confirm that the secret payload was stored by retrieving it:

$ openstack secret get http://10.0.2.15:9311/v1/secrets/655d7d30-c11a-49d9-a0f1-34cdf53a36fa --payload +---------+---------+ | Field   | Value   | +---------+---------+ | Payload | j4=]d21 | +---------+---------+
