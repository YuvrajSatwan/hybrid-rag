# Policy configuration Â¶

Warning

JSON formatted policy file is deprecated since Keystone 19.0.0 (Wallaby).
This oslopolicy-convert-json-to-yaml tool will migrate your existing
JSON-formatted policy file to YAML in a backward-compatible way.

## Configuration Â¶

The following is an overview of all available policies in Keystone.

For a sample configuration file, refer to policy.yaml .

### keystone Â¶

role:admin or is_admin:1

(no description provided)

role:service

(no description provided)

rule:admin_required or rule:service_role

(no description provided)

user_id:%(user_id)s

(no description provided)

rule:admin_required or rule:owner

(no description provided)

user_id:%(target.token.user_id)s

(no description provided)

rule:admin_required or rule:token_subject

(no description provided)

rule:service_or_admin or rule:token_subject

(no description provided)

'manager':%(target.role.name)s or 'member':%(target.role.name)s or 'reader':%(target.role.name)s

(no description provided)

(role:reader and system_scope:all) or user_id:%(target.user.id)s

- GET /v3/users/{user_id}/access_rules/{access_rule_id}

GET /v3/users/{user_id}/access_rules/{access_rule_id}

- HEAD /v3/users/{user_id}/access_rules/{access_rule_id}

HEAD /v3/users/{user_id}/access_rules/{access_rule_id}

- system

system

- project

project

Show access rule details.

(role:reader and system_scope:all) or user_id:%(target.user.id)s

- GET /v3/users/{user_id}/access_rules

GET /v3/users/{user_id}/access_rules

- HEAD /v3/users/{user_id}/access_rules

HEAD /v3/users/{user_id}/access_rules

- system

system

- project

project

List access rules for a user.

(role:admin and system_scope:all) or user_id:%(target.user.id)s

- DELETE /v3/users/{user_id}/access_rules/{access_rule_id}

DELETE /v3/users/{user_id}/access_rules/{access_rule_id}

- system

system

- project

project

Delete an access_rule.

rule:admin_required

- PUT /v3/OS-OAUTH1/authorize/{request_token_id}

PUT /v3/OS-OAUTH1/authorize/{request_token_id}

- project

project

Authorize OAUTH1 request token.

rule:admin_required

- GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}

GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}

- project

project

Get OAUTH1 access token for user by access token ID.

rule:admin_required

- GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles/{role_id}

GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles/{role_id}

- project

project

Get role for user OAUTH1 access token.

rule:admin_required

- GET /v3/users/{user_id}/OS-OAUTH1/access_tokens

GET /v3/users/{user_id}/OS-OAUTH1/access_tokens

- project

project

List OAUTH1 access tokens for user.

rule:admin_required

- GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles

GET /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles

- project

project

List OAUTH1 access token roles.

rule:admin_required

- DELETE /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}

DELETE /v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}

- project

project

Delete OAUTH1 access token.

(rule:admin_required) or (role:reader and system_scope:all) or rule:owner

- GET /v3/users/{user_id}/application_credentials/{application_credential_id}

GET /v3/users/{user_id}/application_credentials/{application_credential_id}

- HEAD /v3/users/{user_id}/application_credentials/{application_credential_id}

HEAD /v3/users/{user_id}/application_credentials/{application_credential_id}

- system

system

- project

project

Show application credential details.

(rule:admin_required) or (role:reader and system_scope:all) or rule:owner

- GET /v3/users/{user_id}/application_credentials

GET /v3/users/{user_id}/application_credentials

- HEAD /v3/users/{user_id}/application_credentials

HEAD /v3/users/{user_id}/application_credentials

- system

system

- project

project

List application credentials for a user.

user_id:%(user_id)s

- POST /v3/users/{user_id}/application_credentials

POST /v3/users/{user_id}/application_credentials

- project

project

Create an application credential.

rule:admin_or_owner

- DELETE /v3/users/{user_id}/application_credentials/{application_credential_id}

DELETE /v3/users/{user_id}/application_credentials/{application_credential_id}

- system

system

- project

project

Delete an application credential.

<empty string>

- GET /v3/auth/catalog

GET /v3/auth/catalog

- HEAD /v3/auth/catalog

HEAD /v3/auth/catalog

Get service catalog.

<empty string>

- GET /v3/auth/projects

GET /v3/auth/projects

- HEAD /v3/auth/projects

HEAD /v3/auth/projects

List all projects a user has access to via role assignments.

<empty string>

- GET /v3/auth/domains

GET /v3/auth/domains

- HEAD /v3/auth/domains

HEAD /v3/auth/domains

List all domains a user has access to via role assignments.

<empty string>

- GET /v3/auth/system

GET /v3/auth/system

- HEAD /v3/auth/system

HEAD /v3/auth/system

List systems a user has access to via role assignments.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-OAUTH1/consumers/{consumer_id}

GET /v3/OS-OAUTH1/consumers/{consumer_id}

- system

system

- project

project

Show OAUTH1 consumer details.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-OAUTH1/consumers

GET /v3/OS-OAUTH1/consumers

- system

system

- project

project

List OAUTH1 consumers.

rule:admin_required

- POST /v3/OS-OAUTH1/consumers

POST /v3/OS-OAUTH1/consumers

- system

system

- project

project

Create OAUTH1 consumer.

rule:admin_required

- PATCH /v3/OS-OAUTH1/consumers/{consumer_id}

PATCH /v3/OS-OAUTH1/consumers/{consumer_id}

- system

system

- project

project

Update OAUTH1 consumer.

rule:admin_required

- DELETE /v3/OS-OAUTH1/consumers/{consumer_id}

DELETE /v3/OS-OAUTH1/consumers/{consumer_id}

- system

system

- project

project

Delete OAUTH1 consumer.

(rule:admin_required) or (role:reader and system_scope:all) or user_id:%(target.credential.user_id)s

- GET /v3/credentials/{credential_id}

GET /v3/credentials/{credential_id}

- system

system

- domain

domain

- project

project

Show credentials details.

(rule:admin_required) or (role:reader and system_scope:all) or user_id:%(target.credential.user_id)s

- GET /v3/credentials

GET /v3/credentials

- system

system

- domain

domain

- project

project

List credentials.

(rule:admin_required) or user_id:%(target.credential.user_id)s

- POST /v3/credentials

POST /v3/credentials

- system

system

- domain

domain

- project

project

Create credential.

(rule:admin_required) or user_id:%(target.credential.user_id)s

- PATCH /v3/credentials/{credential_id}

PATCH /v3/credentials/{credential_id}

- system

system

- domain

domain

- project

project

Update credential.

(rule:admin_required) or user_id:%(target.credential.user_id)s

- DELETE /v3/credentials/{credential_id}

DELETE /v3/credentials/{credential_id}

- system

system

- domain

domain

- project

project

Delete credential.

rule:admin_required or (role:reader and system_scope:all) or token.domain.id:%(target.domain.id)s or token.project.domain.id:%(target.domain.id)s

- GET /v3/domains/{domain_id}

GET /v3/domains/{domain_id}

- system

system

- domain

domain

- project

project

Show domain details.

rule:admin_required or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain.id)s)

- GET /v3/domains

GET /v3/domains

- system

system

- domain

domain

- project

project

List domains.

rule:admin_required

- POST /v3/domains

POST /v3/domains

- system

system

- project

project

Create domain.

rule:admin_required

- PATCH /v3/domains/{domain_id}

PATCH /v3/domains/{domain_id}

- system

system

- project

project

Update domain.

rule:admin_required

- DELETE /v3/domains/{domain_id}

DELETE /v3/domains/{domain_id}

- system

system

- project

project

Delete domain.

rule:admin_required

- PUT /v3/domains/{domain_id}/config

PUT /v3/domains/{domain_id}/config

- system

system

- project

project

Create domain configuration.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/domains/{domain_id}/config

GET /v3/domains/{domain_id}/config

- HEAD /v3/domains/{domain_id}/config

HEAD /v3/domains/{domain_id}/config

- GET /v3/domains/{domain_id}/config/{group}

GET /v3/domains/{domain_id}/config/{group}

- HEAD /v3/domains/{domain_id}/config/{group}

HEAD /v3/domains/{domain_id}/config/{group}

- GET /v3/domains/{domain_id}/config/{group}/{option}

GET /v3/domains/{domain_id}/config/{group}/{option}

- HEAD /v3/domains/{domain_id}/config/{group}/{option}

HEAD /v3/domains/{domain_id}/config/{group}/{option}

- system

system

- project

project

Get the entire domain configuration for a domain, an option group within a domain, or a specific configuration option within a group for a domain.

<empty string>

- GET /v3/domains/{domain_id}/config/security_compliance

GET /v3/domains/{domain_id}/config/security_compliance

- HEAD /v3/domains/{domain_id}/config/security_compliance

HEAD /v3/domains/{domain_id}/config/security_compliance

- GET /v3/domains/{domain_id}/config/security_compliance/{option}

GET /v3/domains/{domain_id}/config/security_compliance/{option}

- HEAD /v3/domains/{domain_id}/config/security_compliance/{option}

HEAD /v3/domains/{domain_id}/config/security_compliance/{option}

- system

system

- domain

domain

- project

project

Get security compliance domain configuration for either a domain or a specific option in a domain.

rule:admin_required

- PATCH /v3/domains/{domain_id}/config

PATCH /v3/domains/{domain_id}/config

- PATCH /v3/domains/{domain_id}/config/{group}

PATCH /v3/domains/{domain_id}/config/{group}

- PATCH /v3/domains/{domain_id}/config/{group}/{option}

PATCH /v3/domains/{domain_id}/config/{group}/{option}

- system

system

- project

project

Update domain configuration for either a domain, specific group or a specific option in a group.

rule:admin_required

- DELETE /v3/domains/{domain_id}/config

DELETE /v3/domains/{domain_id}/config

- DELETE /v3/domains/{domain_id}/config/{group}

DELETE /v3/domains/{domain_id}/config/{group}

- DELETE /v3/domains/{domain_id}/config/{group}/{option}

DELETE /v3/domains/{domain_id}/config/{group}/{option}

- system

system

- project

project

Delete domain configuration for either a domain, specific group or a specific option in a group.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/domains/config/default

GET /v3/domains/config/default

- HEAD /v3/domains/config/default

HEAD /v3/domains/config/default

- GET /v3/domains/config/{group}/default

GET /v3/domains/config/{group}/default

- HEAD /v3/domains/config/{group}/default

HEAD /v3/domains/config/{group}/default

- GET /v3/domains/config/{group}/{option}/default

GET /v3/domains/config/{group}/{option}/default

- HEAD /v3/domains/config/{group}/{option}/default

HEAD /v3/domains/config/{group}/{option}/default

- system

system

- project

project

Get domain configuration default for either a domain, specific group or a specific option in a group.

(rule:admin_required) or (role:reader and system_scope:all) or user_id:%(target.credential.user_id)s

- GET /v3/users/{user_id}/credentials/OS-EC2/{credential_id}

GET /v3/users/{user_id}/credentials/OS-EC2/{credential_id}

- system

system

- project

project

Show ec2 credential details.

(rule:admin_required) or (role:reader and system_scope:all) or rule:owner

- GET /v3/users/{user_id}/credentials/OS-EC2

GET /v3/users/{user_id}/credentials/OS-EC2

- system

system

- project

project

List ec2 credentials.

(rule:admin_required) or (role:member and user_id:%(target.credential.user_id)s)

- POST /v3/users/{user_id}/credentials/OS-EC2

POST /v3/users/{user_id}/credentials/OS-EC2

- system

system

- project

project

Create ec2 credential.

(rule:admin_required) or (role:member and user_id:%(target.credential.user_id)s)

- DELETE /v3/users/{user_id}/credentials/OS-EC2/{credential_id}

DELETE /v3/users/{user_id}/credentials/OS-EC2/{credential_id}

- system

system

- project

project

Delete ec2 credential.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/endpoints/{endpoint_id}

GET /v3/endpoints/{endpoint_id}

- system

system

- project

project

Show endpoint details.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/endpoints

GET /v3/endpoints

- system

system

- project

project

List endpoints.

rule:admin_required

- POST /v3/endpoints

POST /v3/endpoints

- system

system

- project

project

Create endpoint.

rule:admin_required

- PATCH /v3/endpoints/{endpoint_id}

PATCH /v3/endpoints/{endpoint_id}

- system

system

- project

project

Update endpoint.

rule:admin_required

- DELETE /v3/endpoints/{endpoint_id}

DELETE /v3/endpoints/{endpoint_id}

- system

system

- project

project

Delete endpoint.

rule:admin_required

- POST /v3/OS-EP-FILTER/endpoint_groups

POST /v3/OS-EP-FILTER/endpoint_groups

- system

system

- project

project

Create endpoint group.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoint_groups

GET /v3/OS-EP-FILTER/endpoint_groups

- system

system

- project

project

List endpoint groups.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

- HEAD /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

HEAD /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

- system

system

- project

project

Get endpoint group.

rule:admin_required

- PATCH /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

PATCH /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

- system

system

- project

project

Update endpoint group.

rule:admin_required

- DELETE /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

DELETE /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}

- system

system

- project

project

Delete endpoint group.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects

GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects

- system

system

- project

project

List all projects associated with a specific endpoint group.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/endpoints

GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/endpoints

- system

system

- project

project

List all endpoints associated with an endpoint group.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

GET /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

- HEAD /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

HEAD /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

- system

system

- project

project

Check if an endpoint group is associated with a project.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/projects/{project_id}/endpoint_groups

GET /v3/OS-EP-FILTER/projects/{project_id}/endpoint_groups

- system

system

- project

project

List endpoint groups associated with a specific project.

rule:admin_required

- PUT /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

PUT /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

- system

system

- project

project

Allow a project to access an endpoint group.

rule:admin_required

- DELETE /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

DELETE /v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}

- system

system

- project

project

Remove endpoint group from project.

(rule:admin_required) or ((role:reader and system_scope:all) or ((role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s))

- HEAD /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

HEAD /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

- GET /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

GET /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

- HEAD /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

HEAD /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

- GET /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

GET /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

- HEAD /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

HEAD /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

- GET /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

GET /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

- HEAD /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

HEAD /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

- GET /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

GET /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

- HEAD /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

HEAD /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- GET /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

GET /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- HEAD /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

HEAD /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- GET /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

GET /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- HEAD /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

HEAD /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- GET /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

GET /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- HEAD /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

HEAD /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- GET /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

GET /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- system

system

- domain

domain

- project

project

Check a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable.

(rule:admin_required) or ((role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s))

- GET /v3/projects/{project_id}/users/{user_id}/roles

GET /v3/projects/{project_id}/users/{user_id}/roles

- HEAD /v3/projects/{project_id}/users/{user_id}/roles

HEAD /v3/projects/{project_id}/users/{user_id}/roles

- GET /v3/projects/{project_id}/groups/{group_id}/roles

GET /v3/projects/{project_id}/groups/{group_id}/roles

- HEAD /v3/projects/{project_id}/groups/{group_id}/roles

HEAD /v3/projects/{project_id}/groups/{group_id}/roles

- GET /v3/domains/{domain_id}/users/{user_id}/roles

GET /v3/domains/{domain_id}/users/{user_id}/roles

- HEAD /v3/domains/{domain_id}/users/{user_id}/roles

HEAD /v3/domains/{domain_id}/users/{user_id}/roles

- GET /v3/domains/{domain_id}/groups/{group_id}/roles

GET /v3/domains/{domain_id}/groups/{group_id}/roles

- HEAD /v3/domains/{domain_id}/groups/{group_id}/roles

HEAD /v3/domains/{domain_id}/groups/{group_id}/roles

- GET /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects

GET /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects

- GET /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/inherited_to_projects

GET /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/inherited_to_projects

- system

system

- domain

domain

- project

project

List roles granted to an actor on a target. A target can be either a domain or a project. An actor can be either a user or a group. For the OS-INHERIT APIs, it is possible to list inherited role grants for actors on domains, where grants are inherited to all projects in the specified domain.

(rule:admin_required) or ((role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s) or ((role:manager and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:manager and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and rule:domain_managed_target_role

- PUT /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

PUT /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

- PUT /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

PUT /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

- PUT /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

PUT /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

- PUT /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

PUT /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

- PUT /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

PUT /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- PUT /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

PUT /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- PUT /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

PUT /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- PUT /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

PUT /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- system

system

- domain

domain

- project

project

Create a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable.

(rule:admin_required) or ((role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s) or ((role:manager and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:manager and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and rule:domain_managed_target_role

- DELETE /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

DELETE /v3/projects/{project_id}/users/{user_id}/roles/{role_id}

- DELETE /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

DELETE /v3/projects/{project_id}/groups/{group_id}/roles/{role_id}

- DELETE /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

DELETE /v3/domains/{domain_id}/users/{user_id}/roles/{role_id}

- DELETE /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

DELETE /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}

- DELETE /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

DELETE /v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- DELETE /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

DELETE /v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- DELETE /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

DELETE /v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects

- DELETE /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

DELETE /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects

- system

system

- domain

domain

- project

project

Revoke a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable. In that case, revoking the role grant in the target would remove the logical effect of inheriting it to the targetâs projects subtree.

rule:admin_required or (role:reader and system_scope:all)

- [âHEADâ, âGETâ] /v3/system/users/{user_id}/roles

[âHEADâ, âGETâ] /v3/system/users/{user_id}/roles

- system

system

- project

project

List all grants a specific user has on the system.

rule:admin_required or (role:reader and system_scope:all)

- [âHEADâ, âGETâ] /v3/system/users/{user_id}/roles/{role_id}

[âHEADâ, âGETâ] /v3/system/users/{user_id}/roles/{role_id}

- system

system

- project

project

Check if a user has a role on the system.

rule:admin_required

- [âPUTâ] /v3/system/users/{user_id}/roles/{role_id}

[âPUTâ] /v3/system/users/{user_id}/roles/{role_id}

- system

system

- project

project

Grant a user a role on the system.

rule:admin_required

- [âDELETEâ] /v3/system/users/{user_id}/roles/{role_id}

[âDELETEâ] /v3/system/users/{user_id}/roles/{role_id}

- system

system

- project

project

Remove a role from a user on the system.

rule:admin_required or (role:reader and system_scope:all)

- [âHEADâ, âGETâ] /v3/system/groups/{group_id}/roles

[âHEADâ, âGETâ] /v3/system/groups/{group_id}/roles

- system

system

- project

project

List all grants a specific group has on the system.

rule:admin_required or (role:reader and system_scope:all)

- [âHEADâ, âGETâ] /v3/system/groups/{group_id}/roles/{role_id}

[âHEADâ, âGETâ] /v3/system/groups/{group_id}/roles/{role_id}

- system

system

- project

project

Check if a group has a role on the system.

rule:admin_required

- [âPUTâ] /v3/system/groups/{group_id}/roles/{role_id}

[âPUTâ] /v3/system/groups/{group_id}/roles/{role_id}

- system

system

- project

project

Grant a group a role on the system.

rule:admin_required

- [âDELETEâ] /v3/system/groups/{group_id}/roles/{role_id}

[âDELETEâ] /v3/system/groups/{group_id}/roles/{role_id}

- system

system

- project

project

Remove a role from a group on the system.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)

- GET /v3/groups/{group_id}

GET /v3/groups/{group_id}

- HEAD /v3/groups/{group_id}

HEAD /v3/groups/{group_id}

- system

system

- domain

domain

- project

project

Show group details.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)

- GET /v3/groups

GET /v3/groups

- HEAD /v3/groups

HEAD /v3/groups

- system

system

- domain

domain

- project

project

List groups.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s) or user_id:%(user_id)s

- GET /v3/users/{user_id}/groups

GET /v3/users/{user_id}/groups

- HEAD /v3/users/{user_id}/groups

HEAD /v3/users/{user_id}/groups

- system

system

- domain

domain

- project

project

List groups to which a user belongs.

(rule:admin_required) or (role:manager and domain_id:%(target.group.domain_id)s)

- POST /v3/groups

POST /v3/groups

- system

system

- domain

domain

- project

project

Create group.

(rule:admin_required) or (role:manager and domain_id:%(target.group.domain_id)s)

- PATCH /v3/groups/{group_id}

PATCH /v3/groups/{group_id}

- system

system

- domain

domain

- project

project

Update group.

(rule:admin_required) or (role:manager and domain_id:%(target.group.domain_id)s)

- DELETE /v3/groups/{group_id}

DELETE /v3/groups/{group_id}

- system

system

- domain

domain

- project

project

Delete group.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)

- GET /v3/groups/{group_id}/users

GET /v3/groups/{group_id}/users

- HEAD /v3/groups/{group_id}/users

HEAD /v3/groups/{group_id}/users

- system

system

- domain

domain

- project

project

List members of a specific group.

(rule:admin_required) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)

- DELETE /v3/groups/{group_id}/users/{user_id}

DELETE /v3/groups/{group_id}/users/{user_id}

- system

system

- domain

domain

- project

project

Remove user from group.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)

- HEAD /v3/groups/{group_id}/users/{user_id}

HEAD /v3/groups/{group_id}/users/{user_id}

- GET /v3/groups/{group_id}/users/{user_id}

GET /v3/groups/{group_id}/users/{user_id}

- system

system

- domain

domain

- project

project

Check whether a user is a member of a group.

(rule:admin_required) or (role:manager and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)

- PUT /v3/groups/{group_id}/users/{user_id}

PUT /v3/groups/{group_id}/users/{user_id}

- system

system

- domain

domain

- project

project

Add user to group.

rule:admin_required

- PUT /v3/OS-FEDERATION/identity_providers/{idp_id}

PUT /v3/OS-FEDERATION/identity_providers/{idp_id}

- system

system

- project

project

Create identity provider.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/identity_providers

GET /v3/OS-FEDERATION/identity_providers

- HEAD /v3/OS-FEDERATION/identity_providers

HEAD /v3/OS-FEDERATION/identity_providers

- system

system

- project

project

List identity providers.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/identity_providers/{idp_id}

GET /v3/OS-FEDERATION/identity_providers/{idp_id}

- HEAD /v3/OS-FEDERATION/identity_providers/{idp_id}

HEAD /v3/OS-FEDERATION/identity_providers/{idp_id}

- system

system

- project

project

Get identity provider.

rule:admin_required

- PATCH /v3/OS-FEDERATION/identity_providers/{idp_id}

PATCH /v3/OS-FEDERATION/identity_providers/{idp_id}

- system

system

- project

project

Update identity provider.

rule:admin_required

- DELETE /v3/OS-FEDERATION/identity_providers/{idp_id}

DELETE /v3/OS-FEDERATION/identity_providers/{idp_id}

- system

system

- project

project

Delete identity provider.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/roles/{prior_role_id}/implies/{implied_role_id}

GET /v3/roles/{prior_role_id}/implies/{implied_role_id}

- system

system

- project

project

Get information about an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/roles/{prior_role_id}/implies

GET /v3/roles/{prior_role_id}/implies

- HEAD /v3/roles/{prior_role_id}/implies

HEAD /v3/roles/{prior_role_id}/implies

- system

system

- project

project

List associations between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role. This will return all the implied roles that would be assumed by the user who gets the specified prior role.

rule:admin_required

- PUT /v3/roles/{prior_role_id}/implies/{implied_role_id}

PUT /v3/roles/{prior_role_id}/implies/{implied_role_id}

- system

system

- project

project

Create an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.

rule:admin_required

- DELETE /v3/roles/{prior_role_id}/implies/{implied_role_id}

DELETE /v3/roles/{prior_role_id}/implies/{implied_role_id}

- system

system

- project

project

Delete the association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role. Removing the association will cause that effect to be eliminated.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/role_inferences

GET /v3/role_inferences

- HEAD /v3/role_inferences

HEAD /v3/role_inferences

- system

system

- project

project

List all associations between two roles in the system. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.

rule:admin_required or (role:reader and system_scope:all)

- HEAD /v3/roles/{prior_role_id}/implies/{implied_role_id}

HEAD /v3/roles/{prior_role_id}/implies/{implied_role_id}

- system

system

- project

project

Check an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.

<empty string>

- GET /v3/limits/model

GET /v3/limits/model

- HEAD /v3/limits/model

HEAD /v3/limits/model

- system

system

- domain

domain

- project

project

Get limit enforcement model.

rule:admin_required or (role:reader and system_scope:all) or (domain_id:%(target.limit.domain.id)s or domain_id:%(target.limit.project.domain_id)s) or (project_id:%(target.limit.project_id)s and not None:%(target.limit.project_id)s)

- GET /v3/limits/{limit_id}

GET /v3/limits/{limit_id}

- HEAD /v3/limits/{limit_id}

HEAD /v3/limits/{limit_id}

- system

system

- domain

domain

- project

project

Show limit details.

<empty string>

- GET /v3/limits

GET /v3/limits

- HEAD /v3/limits

HEAD /v3/limits

- system

system

- domain

domain

- project

project

List limits.

rule:admin_required

- POST /v3/limits

POST /v3/limits

- system

system

- project

project

Create limits.

rule:admin_required

- PATCH /v3/limits/{limit_id}

PATCH /v3/limits/{limit_id}

- system

system

- project

project

Update limit.

rule:admin_required

- DELETE /v3/limits/{limit_id}

DELETE /v3/limits/{limit_id}

- system

system

- project

project

Delete limit.

rule:admin_required

- PUT /v3/OS-FEDERATION/mappings/{mapping_id}

PUT /v3/OS-FEDERATION/mappings/{mapping_id}

- system

system

- project

project

Create a new federated mapping containing one or more sets of rules.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/mappings/{mapping_id}

GET /v3/OS-FEDERATION/mappings/{mapping_id}

- HEAD /v3/OS-FEDERATION/mappings/{mapping_id}

HEAD /v3/OS-FEDERATION/mappings/{mapping_id}

- system

system

- project

project

Get a federated mapping.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/mappings

GET /v3/OS-FEDERATION/mappings

- HEAD /v3/OS-FEDERATION/mappings

HEAD /v3/OS-FEDERATION/mappings

- system

system

- project

project

List federated mappings.

rule:admin_required

- DELETE /v3/OS-FEDERATION/mappings/{mapping_id}

DELETE /v3/OS-FEDERATION/mappings/{mapping_id}

- system

system

- project

project

Delete a federated mapping.

rule:admin_required

- PATCH /v3/OS-FEDERATION/mappings/{mapping_id}

PATCH /v3/OS-FEDERATION/mappings/{mapping_id}

- system

system

- project

project

Update a federated mapping.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies/{policy_id}

GET /v3/policies/{policy_id}

- system

system

- project

project

Show policy details.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies

GET /v3/policies

- system

system

- project

project

List policies.

rule:admin_required

- POST /v3/policies

POST /v3/policies

- system

system

- project

project

Create policy.

rule:admin_required

- PATCH /v3/policies/{policy_id}

PATCH /v3/policies/{policy_id}

- system

system

- project

project

Update policy.

rule:admin_required

- DELETE /v3/policies/{policy_id}

DELETE /v3/policies/{policy_id}

- system

system

- project

project

Delete policy.

rule:admin_required

- PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

- system

system

- project

project

Associate a policy to a specific endpoint.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

- HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

- system

system

- project

project

Check policy association for endpoint.

rule:admin_required

- DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}

- system

system

- project

project

Delete policy association for endpoint.

rule:admin_required

- PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

- system

system

- project

project

Associate a policy to a specific service.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

- HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

- system

system

- project

project

Check policy association for service.

rule:admin_required

- DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}

- system

system

- project

project

Delete policy association for service.

rule:admin_required

- PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

PUT /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

- system

system

- project

project

Associate a policy to a specific region and service combination.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

- HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

HEAD /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

- system

system

- project

project

Check policy association for region and service.

rule:admin_required

- DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

DELETE /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}

- system

system

- project

project

Delete policy association for region and service.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy

GET /v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy

- HEAD /v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy

HEAD /v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy

- system

system

- project

project

Get policy for endpoint.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints

GET /v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints

- system

system

- project

project

List endpoints for policy.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s) or project_id:%(target.project.id)s

- GET /v3/projects/{project_id}

GET /v3/projects/{project_id}

- system

system

- domain

domain

- project

project

Show project details.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)

- GET /v3/projects

GET /v3/projects

- system

system

- domain

domain

- project

project

List projects.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s) or user_id:%(target.user.id)s

- GET /v3/users/{user_id}/projects

GET /v3/users/{user_id}/projects

- system

system

- domain

domain

- project

project

List projects for user.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- POST /v3/projects

POST /v3/projects

- system

system

- domain

domain

- project

project

Create project.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- PATCH /v3/projects/{project_id}

PATCH /v3/projects/{project_id}

- system

system

- domain

domain

- project

project

Update project.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- DELETE /v3/projects/{project_id}

DELETE /v3/projects/{project_id}

- system

system

- domain

domain

- project

project

Delete project.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s) or project_id:%(target.project.id)s

- GET /v3/projects/{project_id}/tags

GET /v3/projects/{project_id}/tags

- HEAD /v3/projects/{project_id}/tags

HEAD /v3/projects/{project_id}/tags

- system

system

- domain

domain

- project

project

List tags for a project.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s) or project_id:%(target.project.id)s

- GET /v3/projects/{project_id}/tags/{value}

GET /v3/projects/{project_id}/tags/{value}

- HEAD /v3/projects/{project_id}/tags/{value}

HEAD /v3/projects/{project_id}/tags/{value}

- system

system

- domain

domain

- project

project

Check if project contains a tag.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- PUT /v3/projects/{project_id}/tags

PUT /v3/projects/{project_id}/tags

- system

system

- domain

domain

- project

project

Replace all tags on a project with the new set of tags.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- PUT /v3/projects/{project_id}/tags/{value}

PUT /v3/projects/{project_id}/tags/{value}

- system

system

- domain

domain

- project

project

Add a single tag to a project.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- DELETE /v3/projects/{project_id}/tags

DELETE /v3/projects/{project_id}/tags

- system

system

- domain

domain

- project

project

Remove all tags from a project.

(rule:admin_required) or (role:manager and domain_id:%(target.project.domain_id)s and not None:%(target.project.domain_id)s)

- DELETE /v3/projects/{project_id}/tags/{value}

DELETE /v3/projects/{project_id}/tags/{value}

- system

system

- domain

domain

- project

project

Delete a specified tag from project.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/endpoints/{endpoint_id}/projects

GET /v3/OS-EP-FILTER/endpoints/{endpoint_id}/projects

- system

system

- project

project

List projects allowed to access an endpoint.

rule:admin_required

- PUT /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

PUT /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

- system

system

- project

project

Allow project to access an endpoint.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

GET /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

- HEAD /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

HEAD /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

- system

system

- project

project

Check if a project is allowed to access an endpoint.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-EP-FILTER/projects/{project_id}/endpoints

GET /v3/OS-EP-FILTER/projects/{project_id}/endpoints

- system

system

- project

project

List the endpoints a project is allowed to access.

rule:admin_required

- DELETE /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

DELETE /v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}

- system

system

- project

project

Remove access to an endpoint from a project that has previously been given explicit access.

rule:admin_required

- PUT /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

PUT /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

- system

system

- project

project

Create federated protocol.

rule:admin_required

- PATCH /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

PATCH /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

- system

system

- project

project

Update federated protocol.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

GET /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

- system

system

- project

project

Get federated protocol.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols

GET /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols

- system

system

- project

project

List federated protocols.

rule:admin_required

- DELETE /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

DELETE /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}

- system

system

- project

project

Delete federated protocol.

<empty string>

- GET /v3/regions/{region_id}

GET /v3/regions/{region_id}

- HEAD /v3/regions/{region_id}

HEAD /v3/regions/{region_id}

- system

system

- domain

domain

- project

project

Show region details.

<empty string>

- GET /v3/regions

GET /v3/regions

- HEAD /v3/regions

HEAD /v3/regions

- system

system

- domain

domain

- project

project

List regions.

rule:admin_required

- POST /v3/regions

POST /v3/regions

- PUT /v3/regions/{region_id}

PUT /v3/regions/{region_id}

- system

system

- project

project

Create region.

rule:admin_required

- PATCH /v3/regions/{region_id}

PATCH /v3/regions/{region_id}

- system

system

- project

project

Update region.

rule:admin_required

- DELETE /v3/regions/{region_id}

DELETE /v3/regions/{region_id}

- system

system

- project

project

Delete region.

<empty string>

- GET /v3/registered_limits/{registered_limit_id}

GET /v3/registered_limits/{registered_limit_id}

- HEAD /v3/registered_limits/{registered_limit_id}

HEAD /v3/registered_limits/{registered_limit_id}

- system

system

- domain

domain

- project

project

Show registered limit details.

<empty string>

- GET /v3/registered_limits

GET /v3/registered_limits

- HEAD /v3/registered_limits

HEAD /v3/registered_limits

- system

system

- domain

domain

- project

project

List registered limits.

rule:admin_required

- POST /v3/registered_limits

POST /v3/registered_limits

- system

system

- project

project

Create registered limits.

rule:admin_required

- PATCH /v3/registered_limits/{registered_limit_id}

PATCH /v3/registered_limits/{registered_limit_id}

- system

system

- project

project

Update registered limit.

rule:admin_required

- DELETE /v3/registered_limits/{registered_limit_id}

DELETE /v3/registered_limits/{registered_limit_id}

- system

system

- project

project

Delete registered limit.

rule:service_or_admin

- GET /v3/OS-REVOKE/events

GET /v3/OS-REVOKE/events

- system

system

- project

project

List revocation events.

(rule:admin_required or (role:reader and system_scope:all)) or (role:manager and rule:domain_managed_target_role)

- GET /v3/roles/{role_id}

GET /v3/roles/{role_id}

- HEAD /v3/roles/{role_id}

HEAD /v3/roles/{role_id}

- system

system

- domain

domain

- project

project

Show role details.

(rule:admin_required or (role:reader and system_scope:all)) or (role:manager and not domain_id:None)

- GET /v3/roles

GET /v3/roles

- HEAD /v3/roles

HEAD /v3/roles

- system

system

- domain

domain

- project

project

List roles.

rule:admin_required

- POST /v3/roles

POST /v3/roles

- system

system

- project

project

Create role.

rule:admin_required

- PATCH /v3/roles/{role_id}

PATCH /v3/roles/{role_id}

- system

system

- project

project

Update role.

rule:admin_required

- DELETE /v3/roles/{role_id}

DELETE /v3/roles/{role_id}

- system

system

- project

project

Delete role.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/roles/{role_id}

GET /v3/roles/{role_id}

- HEAD /v3/roles/{role_id}

HEAD /v3/roles/{role_id}

- system

system

- project

project

Show domain role.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/roles?domain_id={domain_id}

GET /v3/roles?domain_id={domain_id}

- HEAD /v3/roles?domain_id={domain_id}

HEAD /v3/roles?domain_id={domain_id}

- system

system

- project

project

List domain roles.

rule:admin_required

- POST /v3/roles

POST /v3/roles

- system

system

- project

project

Create domain role.

rule:admin_required

- PATCH /v3/roles/{role_id}

PATCH /v3/roles/{role_id}

- system

system

- project

project

Update domain role.

rule:admin_required

- DELETE /v3/roles/{role_id}

DELETE /v3/roles/{role_id}

- system

system

- project

project

Delete domain role.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)

- GET /v3/role_assignments

GET /v3/role_assignments

- HEAD /v3/role_assignments

HEAD /v3/role_assignments

- system

system

- domain

domain

- project

project

List role assignments.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)

- GET /v3/role_assignments?include_subtree

GET /v3/role_assignments?include_subtree

- HEAD /v3/role_assignments?include_subtree

HEAD /v3/role_assignments?include_subtree

- system

system

- domain

domain

- project

project

List all role assignments for a given tree of hierarchical projects.

rule:service_or_admin

- POST /v3/s3tokens

POST /v3/s3tokens

- system

system

- domain

domain

- project

project

Validate S3 credentials and create a Keystone token. Restricted to service users or administrators to prevent exploitation via presigned URLs.

rule:service_or_admin

- POST /v3/ec2tokens

POST /v3/ec2tokens

- system

system

- domain

domain

- project

project

Validate EC2 credentials and create a Keystone token. Restricted to service users or administrators.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/services/{service_id}

GET /v3/services/{service_id}

- system

system

- project

project

Show service details.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/services

GET /v3/services

- system

system

- project

project

List services.

rule:admin_required

- POST /v3/services

POST /v3/services

- system

system

- project

project

Create service.

rule:admin_required

- PATCH /v3/services/{service_id}

PATCH /v3/services/{service_id}

- system

system

- project

project

Update service.

rule:admin_required

- DELETE /v3/services/{service_id}

DELETE /v3/services/{service_id}

- system

system

- project

project

Delete service.

rule:admin_required

- PUT /v3/OS-FEDERATION/service_providers/{service_provider_id}

PUT /v3/OS-FEDERATION/service_providers/{service_provider_id}

- system

system

- project

project

Create federated service provider.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/service_providers

GET /v3/OS-FEDERATION/service_providers

- HEAD /v3/OS-FEDERATION/service_providers

HEAD /v3/OS-FEDERATION/service_providers

- system

system

- project

project

List federated service providers.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-FEDERATION/service_providers/{service_provider_id}

GET /v3/OS-FEDERATION/service_providers/{service_provider_id}

- HEAD /v3/OS-FEDERATION/service_providers/{service_provider_id}

HEAD /v3/OS-FEDERATION/service_providers/{service_provider_id}

- system

system

- project

project

Get federated service provider.

rule:admin_required

- PATCH /v3/OS-FEDERATION/service_providers/{service_provider_id}

PATCH /v3/OS-FEDERATION/service_providers/{service_provider_id}

- system

system

- project

project

Update federated service provider.

rule:admin_required

- DELETE /v3/OS-FEDERATION/service_providers/{service_provider_id}

DELETE /v3/OS-FEDERATION/service_providers/{service_provider_id}

- system

system

- project

project

Delete federated service provider.

rule:service_or_admin

- GET /v3/auth/tokens/OS-PKI/revoked

GET /v3/auth/tokens/OS-PKI/revoked

- system

system

- project

project

List revoked PKI tokens.

rule:admin_required or (role:reader and system_scope:all) or rule:token_subject

- HEAD /v3/auth/tokens

HEAD /v3/auth/tokens

- system

system

- domain

domain

- project

project

Check a token.

rule:admin_required or (role:reader and system_scope:all) or rule:service_role or rule:token_subject

- GET /v3/auth/tokens

GET /v3/auth/tokens

- system

system

- domain

domain

- project

project

Validate a token.

rule:admin_required or rule:token_subject

- DELETE /v3/auth/tokens

DELETE /v3/auth/tokens

- system

system

- domain

domain

- project

project

Revoke a token.

user_id:%(target.trust.trustor_user_id)s

- POST /v3/OS-TRUST/trusts

POST /v3/OS-TRUST/trusts

- project

project

Create trust.

rule:admin_required or (role:reader and system_scope:all)

- GET /v3/OS-TRUST/trusts

GET /v3/OS-TRUST/trusts

- HEAD /v3/OS-TRUST/trusts

HEAD /v3/OS-TRUST/trusts

- system

system

- project

project

List trusts.

(rule:admin_required) or (role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s)

- GET /v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}

GET /v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}

- HEAD /v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}

HEAD /v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}

- system

system

- project

project

List trusts for trustor.

(rule:admin_required) or (role:reader and system_scope:all or user_id:%(target.trust.trustee_user_id)s)

- GET /v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}

GET /v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}

- HEAD /v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}

HEAD /v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}

- system

system

- project

project

List trusts for trustee.

(rule:admin_required) or (role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s)

- GET /v3/OS-TRUST/trusts/{trust_id}/roles

GET /v3/OS-TRUST/trusts/{trust_id}/roles

- HEAD /v3/OS-TRUST/trusts/{trust_id}/roles

HEAD /v3/OS-TRUST/trusts/{trust_id}/roles

- system

system

- project

project

List roles delegated by a trust.

(rule:admin_required) or (role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s)

- GET /v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}

GET /v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}

- HEAD /v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}

HEAD /v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}

- system

system

- project

project

Check if trust delegates a particular role.

rule:admin_required or user_id:%(target.trust.trustor_user_id)s

- DELETE /v3/OS-TRUST/trusts/{trust_id}

DELETE /v3/OS-TRUST/trusts/{trust_id}

- system

system

- project

project

Revoke trust.

(rule:admin_required) or (role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s)

- GET /v3/OS-TRUST/trusts/{trust_id}

GET /v3/OS-TRUST/trusts/{trust_id}

- HEAD /v3/OS-TRUST/trusts/{trust_id}

HEAD /v3/OS-TRUST/trusts/{trust_id}

- system

system

- project

project

Get trust.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and token.domain.id:%(target.user.domain_id)s) or user_id:%(target.user.id)s

- GET /v3/users/{user_id}

GET /v3/users/{user_id}

- HEAD /v3/users/{user_id}

HEAD /v3/users/{user_id}

- system

system

- domain

domain

- project

project

Show user details.

(rule:admin_required) or (role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)

- GET /v3/users

GET /v3/users

- HEAD /v3/users

HEAD /v3/users

- system

system

- domain

domain

- project

project

List users.

<empty string>

- GET `` /v3/auth/projects``

GET `` /v3/auth/projects``

List all projects a user has access to via role assignments.

<empty string>

- GET /v3/auth/domains

GET /v3/auth/domains

List all domains a user has access to via role assignments.

(rule:admin_required) or (role:manager and token.domain.id:%(target.user.domain_id)s)

- POST /v3/users

POST /v3/users

- system

system

- domain

domain

- project

project

Create a user.

(rule:admin_required) or (role:manager and token.domain.id:%(target.user.domain_id)s)

- PATCH /v3/users/{user_id}

PATCH /v3/users/{user_id}

- system

system

- domain

domain

- project

project

Update a user, including administrative password resets.

(rule:admin_required) or (role:manager and token.domain.id:%(target.user.domain_id)s)

- DELETE /v3/users/{user_id}

DELETE /v3/users/{user_id}

- system

system

- domain

domain

- project

project

Delete a user.
