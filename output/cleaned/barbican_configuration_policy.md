# Policy configuration ¶

Warning

JSON formatted policy file is deprecated since Barbican 12.0.0 (Wallaby).
This oslopolicy-convert-json-to-yaml tool will migrate your existing
JSON-formatted policy file to YAML in a backward-compatible way.

## Configuration ¶

The following is an overview of all available policies in Barbican. For a sample
configuration file.

### barbican ¶

project_id:%(target.secret.project_id)s

(no description provided)

role:reader and rule:secret_project_match

(no description provided)

role:member and rule:secret_project_match

(no description provided)

role:admin and rule:secret_project_match

(no description provided)

user_id:%(target.secret.creator_id)s

(no description provided)

True:%(target.secret.read_project_access)s

(no description provided)

'read':%(target.secret.read)s

(no description provided)

project_id:%(target.container.project_id)s

(no description provided)

role:member and rule:container_project_match

(no description provided)

role:admin and rule:container_project_match

(no description provided)

user_id:%(target.container.creator_id)s

(no description provided)

True:%(target.container.read_project_access)s

(no description provided)

'read':%(target.container.read)s

(no description provided)

project_id:%(target.order.project_id)s

(no description provided)

role:member and rule:order_project_match

(no description provided)

role:audit

(no description provided)

role:observer

(no description provided)

role:creator

(no description provided)

role:admin

(no description provided)

role:key-manager:service-admin

(no description provided)

rule:admin or rule:observer or rule:creator or rule:audit or rule:service_admin

(no description provided)

rule:admin or rule:observer or rule:creator

(no description provided)

rule:admin or rule:creator

(no description provided)

user_id:%(target.secret.creator_id)s

(no description provided)

'False':%(target.secret.read_project_access)s

(no description provided)

rule:all_users and rule:secret_project_match and not rule:secret_private_read

(no description provided)

rule:all_but_audit and rule:secret_project_match and not rule:secret_private_read

(no description provided)

rule:creator and rule:secret_project_match and rule:secret_creator_user

(no description provided)

rule:creator and rule:secret_project_match

(no description provided)

'False':%(target.container.read_project_access)s

(no description provided)

user_id:%(target.container.creator_id)s

(no description provided)

rule:all_users and rule:container_project_match and not rule:container_private_read

(no description provided)

rule:creator and rule:container_project_match and rule:container_creator_user

(no description provided)

rule:creator and rule:container_project_match

(no description provided)

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- GET /v1/secrets/{secret-id}/acl

GET /v1/secrets/{secret-id}/acl

- project

project

Retrieve the ACL settings for a given secret.If no ACL is defined for that secret, then Default ACL is returned.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- DELETE /v1/secrets/{secret-id}/acl

DELETE /v1/secrets/{secret-id}/acl

- project

project

Delete the ACL settings for a given secret.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- PUT /v1/secrets/{secret-id}/acl

PUT /v1/secrets/{secret-id}/acl

- PATCH /v1/secrets/{secret-id}/acl

PATCH /v1/secrets/{secret-id}/acl

- project

project

Create new, replaces, or updates existing ACL for a given secret.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- GET /v1/containers/{container-id}/acl

GET /v1/containers/{container-id}/acl

- project

project

Retrieve the ACL settings for a given container.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- DELETE /v1/containers/{container-id}/acl

DELETE /v1/containers/{container-id}/acl

- project

project

Delete ACL for a given container. No content is returned in the case of successful deletion.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- PUT /v1/containers/{container-id}/acl

PUT /v1/containers/{container-id}/acl

- PATCH /v1/containers/{container-id}/acl

PATCH /v1/containers/{container-id}/acl

- project

project

Create new or replaces existing ACL for a given container.

True:%(enforce_new_defaults)s and (role:admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private) or rule:container_acl_read)

- GET /v1/containers/{container-id}/consumers/{consumer-id}

GET /v1/containers/{container-id}/consumers/{consumer-id}

- project

project

DEPRECATED: show information for a specific consumer

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private) or rule:container_acl_read)

- GET /v1/containers/{container-id}/consumers

GET /v1/containers/{container-id}/consumers

- project

project

List a containers consumers.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private) or rule:container_acl_read)

- POST /v1/containers/{container-id}/consumers

POST /v1/containers/{container-id}/consumers

- project

project

Creates a consumer.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private) or rule:container_acl_read)

- DELETE /v1/containers/{container-id}/consumers

DELETE /v1/containers/{container-id}/consumers

- project

project

Deletes a consumer.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- GET /v1/secrets/{secret-id}/consumers

GET /v1/secrets/{secret-id}/consumers

- project

project

List consumers for a secret.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- POST /v1/secrets/{secrets-id}/consumers

POST /v1/secrets/{secrets-id}/consumers

- project

project

Creates a consumer.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- DELETE /v1/secrets/{secrets-id}/consumers

DELETE /v1/secrets/{secrets-id}/consumers

- project

project

Deletes a consumer.

True:%(enforce_new_defaults)s and role:member

- POST /v1/containers

POST /v1/containers

- project

project

Creates a container.

True:%(enforce_new_defaults)s and role:member

- GET /v1/containers

GET /v1/containers

- project

project

Lists a projects containers.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private) or rule:container_acl_read)

- GET /v1/containers/{container-id}

GET /v1/containers/{container-id}

- project

project

Retrieves a single container.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- DELETE /v1/containers/{uuid}

DELETE /v1/containers/{uuid}

- project

project

Deletes a container.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- POST /v1/containers/{container-id}/secrets

POST /v1/containers/{container-id}/secrets

- project

project

Add a secret to an existing container.

True:%(enforce_new_defaults)s and (rule:container_project_admin or (rule:container_project_member and rule:container_owner) or (rule:container_project_member and rule:container_is_not_private))

- DELETE /v1/containers/{container-id}/secrets/{secret-id}

DELETE /v1/containers/{container-id}/secrets/{secret-id}

- project

project

Remove a secret from a container.

True:%(enforce_new_defaults)s and role:member

- GET /v1/orders

GET /v1/orders

- project

project

Gets list of all orders associated with a project.

True:%(enforce_new_defaults)s and role:member

- POST /v1/orders

POST /v1/orders

- project

project

Creates an order.

True:%(enforce_new_defaults)s and role:member

- PUT /v1/orders

PUT /v1/orders

- project

project

Unsupported method for the orders API.

True:%(enforce_new_defaults)s and rule:order_project_member

- GET /v1/orders/{order-id}

GET /v1/orders/{order-id}

- project

project

Retrieves an orders metadata.

True:%(enforce_new_defaults)s and rule:order_project_member

- DELETE /v1/orders/{order-id}

DELETE /v1/orders/{order-id}

- project

project

Deletes an order.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/quotas

GET /v1/quotas

- project

project

List quotas for the project the user belongs to.

True:%(enforce_new_defaults)s and role:admin

- GET /v1/project-quotas

GET /v1/project-quotas

- GET /v1/project-quotas/{uuid}

GET /v1/project-quotas/{uuid}

- project

project

List quotas for the specified project.

True:%(enforce_new_defaults)s and role:admin

- PUT /v1/project-quotas/{uuid}

PUT /v1/project-quotas/{uuid}

- project

project

Create or update the configured project quotas for the project with the specified UUID.

True:%(enforce_new_defaults)s and role:admin

- DELETE /v1/quotas}

DELETE /v1/quotas}

- project

project

Delete the project quotas configuration for the project with the requested UUID.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- GET /v1/secrets/{secret-id}/metadata

GET /v1/secrets/{secret-id}/metadata

- GET /v1/secrets/{secret-id}/metadata/{meta-key}

GET /v1/secrets/{secret-id}/metadata/{meta-key}

- project

project

metadata/: Lists a secrets user-defined metadata. || metadata/{key}: Retrieves a secrets user-added metadata.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- POST /v1/secrets/{secret-id}/metadata/{meta-key}

POST /v1/secrets/{secret-id}/metadata/{meta-key}

- project

project

Adds a new key/value pair to the secrets user-defined metadata.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- PUT /v1/secrets/{secret-id}/metadata

PUT /v1/secrets/{secret-id}/metadata

- PUT /v1/secrets/{secret-id}/metadata/{meta-key}

PUT /v1/secrets/{secret-id}/metadata/{meta-key}

- project

project

metadata/: Sets the user-defined metadata for a secret || metadata/{key}: Updates an existing key/value pair in the secrets user-defined metadata.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- DELETE /v1/secrets/{secret-id}/metadata/{meta-key}

DELETE /v1/secrets/{secret-id}/metadata/{meta-key}

- project

project

Delete secret user-defined metadata by key.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- GET /v1/secrets/{uuid}/payload

GET /v1/secrets/{uuid}/payload

- project

project

Retrieve a secrets payload.

True:%(enforce_new_defaults)s and (role:admin or rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private) or rule:secret_acl_read)

- GET /v1/secrets/{secret-id}

GET /v1/secrets/{secret-id}

- project

project

Retrieves a secrets metadata.

True:%(enforce_new_defaults)s and (rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- PUT /v1/secrets/{secret-id}

PUT /v1/secrets/{secret-id}

- project

project

Add the payload to an existing metadata-only secret.

True:%(enforce_new_defaults)s and (role:admin or rule:secret_project_admin or (rule:secret_project_member and rule:secret_owner) or (rule:secret_project_member and rule:secret_is_not_private))

- DELETE /v1/secrets/{secret-id}

DELETE /v1/secrets/{secret-id}

- project

project

Delete a secret by uuid.

True:%(enforce_new_defaults)s and role:member

- POST /v1/secrets

POST /v1/secrets

- project

project

Creates a Secret entity.

True:%(enforce_new_defaults)s and role:member

- GET /v1/secrets

GET /v1/secrets

- project

project

Lists a projects secrets.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/secret-stores

GET /v1/secret-stores

- project

project

Get list of available secret store backends.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/secret-stores/global-default

GET /v1/secret-stores/global-default

- project

project

Get a reference to the secret store that is used as default secret store backend for the deployment.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/secret-stores/preferred

GET /v1/secret-stores/preferred

- project

project

Get a reference to the preferred secret store if assigned previously.

True:%(enforce_new_defaults)s and role:admin

- POST /v1/secret-stores/{ss-id}/preferred

POST /v1/secret-stores/{ss-id}/preferred

- project

project

Set a secret store backend to be preferred store backend for their project.

True:%(enforce_new_defaults)s and role:admin

- DELETE /v1/secret-stores/{ss-id}/preferred

DELETE /v1/secret-stores/{ss-id}/preferred

- project

project

Remove preferred secret store backend setting for their project.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/secret-stores/{ss-id}

GET /v1/secret-stores/{ss-id}

- project

project

Get details of secret store by its ID.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/transport_keys/{key-id}}

GET /v1/transport_keys/{key-id}}

- project

project

Get a specific transport key.

True:%(enforce_new_defaults)s and role:admin

- DELETE /v1/transport_keys/{key-id}

DELETE /v1/transport_keys/{key-id}

- project

project

Delete a specific transport key.

True:%(enforce_new_defaults)s and role:reader

- GET /v1/transport_keys

GET /v1/transport_keys

- project

project

Get a list of all transport keys.

True:%(enforce_new_defaults)s and role:admin

- POST /v1/transport_keys

POST /v1/transport_keys

- project

project

Create a new transport key.
