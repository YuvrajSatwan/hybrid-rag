# API Discovery with JSON Home Â¶

## What is JSON Home? Â¶

JSON Home describes a method of API discovery for non-browser HTTP clients. The draft is still in review, but keystone supplies an implementation accessible
to end-users. The result of calling keystoneâs JSON Home API is a JSON document
that informs the user about API endpoints, where to find them, and even
information about the APIâs status (e.g. experimental, supported, deprecated).
More information keystoneâs implementation of JSON Home can be found in the specification .

## Requesting JSON Home Documents Â¶

Requesting keystoneâs JSON Home document is easy. The API does not require a
token, but future implementations might expand in itâs protection with token
validation and enforcement. To get a JSON Home document, just query a keystone
endpoint with application/json-home specified in the Accept header:

curl -X GET -H "Accept: application/json-home" http://example.com/identity/

The result will be a JSON document containing a list of resources :

{ "resources": [ "https://docs.openstack.org/api/openstack-identity/3/ext/OS-TRUST/1.0/rel/trusts": { "href": "/v3/OS-TRUST/trusts" }, "https://docs.openstack.org/api/openstack-identity/3/ext/s3tokens/1.0/rel/s3tokens": { "href": "/v3/s3tokens" }, "https://docs.openstack.org/api/openstack-identity/3/rel/application_credential": { "href-template": "/v3/users/{user_id}/application_credentials/{application_credential_id}", "href-vars": { "application_credential_id": "https://docs.openstack.org/api/openstack-identity/3/param/application_credential_id", "user_id": "https://docs.openstack.org/api/openstack-identity/3/param/user_id" } }, "https://docs.openstack.org/api/openstack-identity/3/rel/auth_catalog": { "href": "/v3/auth/catalog" }, "https://docs.openstack.org/api/openstack-identity/3/rel/auth_domains": { "href": "/v3/auth/domains" }, "https://docs.openstack.org/api/openstack-identity/3/rel/auth_projects": { "href": "/v3/auth/projects" }, "https://docs.openstack.org/api/openstack-identity/3/rel/auth_system": { "href": "/v3/auth/system" }, ... ] }

The list of resources can then be parsed based on the relationship key for a
dictionary of data about that endpoint. This includes a path where users can
find interact with the endpoint for that specific resources. API status
information will also be present.
