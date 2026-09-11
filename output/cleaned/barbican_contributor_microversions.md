# API Microversions Â¶

## Background Â¶

Barbican uses a framework we call âAPI Microversionsâ for allowing changes
to the API while preserving backward compatibility. The basic idea is
that a user has to explicitly ask for their request to be treated with
a particular version of the API. So breaking changes can be added to
the API without breaking users who donât specifically ask for it. This
is done with an HTTP header OpenStack-API-Version which has as its
value a string containing the name of the service, key-manager , and a
monotonically increasing semantic version number starting from 1.0 .
The full form of the header takes the form:

OpenStack - API - Version : key - manager 1.1

If a user makes a request without specifying a version, they will get
the MIN_API_VERSION as calculated from the defined _MIN_MICROVERSION in barbican/api/controllers/versions.py .  This value is currently 1.0 and
is expected to remain so for quite a long time.

There is a special value latest which can be specified, which will
allow a client to always receive the most recent version of API
responses from the server.

Warning

The latest value is mostly meant for integration testing and
would be dangerous to rely on in client code since microversions are not
following semver and therefore backward compatibility is not guaranteed.
Clients, like python-barbicanclient, should always require a specific
microversion but limit what is acceptable to the version range that it
understands at the time.

For full details please read the Microversion Specification .

## When do I need a new Microversion? Â¶

A microversion is needed when the contract to the user is
changed. The user contract covers many kinds of information such as:

- the Request the list of resource urls which exist on the server Example: adding a new servers/{ID}/foo which didnât exist in a
previous version of the code the list of query parameters that are valid on urls Example: adding a new parameter is_yellow servers/{ID}?is_yellow=True the list of query parameter values for non free form fields Example: parameter filter_by takes a small set of constants/enums âAâ,
âBâ, âCâ. Adding support for new enum âDâ. new headers accepted on a request the list of attributes and data structures accepted. Example: adding a new attribute âconsumerâ: ââ¦â to the request body

the Request

- the list of resource urls which exist on the server Example: adding a new servers/{ID}/foo which didnât exist in a
previous version of the code

the list of resource urls which exist on the server

Example: adding a new servers/{ID}/foo which didnât exist in a
previous version of the code

- the list of query parameters that are valid on urls Example: adding a new parameter is_yellow servers/{ID}?is_yellow=True

the list of query parameters that are valid on urls

Example: adding a new parameter is_yellow servers/{ID}?is_yellow=True

- the list of query parameter values for non free form fields Example: parameter filter_by takes a small set of constants/enums âAâ,
âBâ, âCâ. Adding support for new enum âDâ.

the list of query parameter values for non free form fields

Example: parameter filter_by takes a small set of constants/enums âAâ,
âBâ, âCâ. Adding support for new enum âDâ.

- new headers accepted on a request

new headers accepted on a request

- the list of attributes and data structures accepted. Example: adding a new attribute âconsumerâ: ââ¦â to the request body

the list of attributes and data structures accepted.

Example: adding a new attribute âconsumerâ: ââ¦â to the request body

- the Response the list of attributes and data structures returned Example: adding a new attribute âconsumersâ: [] to the output
of secrets/{ID} the allowed values of non free form fields Example: adding a new allowed secret_type to secrets/{ID} the list of status codes allowed for a particular request Example: an API previously could return 200, 400, 403, 404 and the
change would make the API now also be allowed to return 409. See [ 2 ] for the 400, 403, 404 and 415 cases. changing a status code on a particular response Example: changing the return code of an API from 501 to 400. Note Fixing a bug so that a 400+ code is returned rather than a 500 or
503 does not require a microversion change. Itâs assumed that clients are
not expected to handle a 500 or 503 response and therefore should not
need to opt-in to microversion changes that fixes a 500 or 503 response
from happening.
According to the OpenStack API Working Group, a 500 Internal Server Error should not be returned to the user for
failures due to user error that can be fixed by changing the request on
the client side. See [ 1 ] . new headers returned on a response

the Response

- the list of attributes and data structures returned Example: adding a new attribute âconsumersâ: [] to the output
of secrets/{ID}

the list of attributes and data structures returned

Example: adding a new attribute âconsumersâ: [] to the output
of secrets/{ID}

- the allowed values of non free form fields Example: adding a new allowed secret_type to secrets/{ID}

the allowed values of non free form fields

Example: adding a new allowed secret_type to secrets/{ID}

- the list of status codes allowed for a particular request Example: an API previously could return 200, 400, 403, 404 and the
change would make the API now also be allowed to return 409. See [ 2 ] for the 400, 403, 404 and 415 cases.

the list of status codes allowed for a particular request

Example: an API previously could return 200, 400, 403, 404 and the
change would make the API now also be allowed to return 409.

See [ 2 ] for the 400, 403, 404 and 415 cases.

- changing a status code on a particular response Example: changing the return code of an API from 501 to 400. Note Fixing a bug so that a 400+ code is returned rather than a 500 or
503 does not require a microversion change. Itâs assumed that clients are
not expected to handle a 500 or 503 response and therefore should not
need to opt-in to microversion changes that fixes a 500 or 503 response
from happening.
According to the OpenStack API Working Group, a 500 Internal Server Error should not be returned to the user for
failures due to user error that can be fixed by changing the request on
the client side. See [ 1 ] .

changing a status code on a particular response

Example: changing the return code of an API from 501 to 400.

Note

Fixing a bug so that a 400+ code is returned rather than a 500 or
503 does not require a microversion change. Itâs assumed that clients are
not expected to handle a 500 or 503 response and therefore should not
need to opt-in to microversion changes that fixes a 500 or 503 response
from happening.
According to the OpenStack API Working Group, a 500 Internal Server Error should not be returned to the user for
failures due to user error that can be fixed by changing the request on
the client side. See [ 1 ] .

- new headers returned on a response

new headers returned on a response

The following flow chart attempts to walk through the process of âdo
we need a microversionâ.

Footnotes

When fixing 500 errors that previously caused stack traces, try
to map the new error into the existing set of errors that API call
could previously return (400 if nothing else is appropriate). Changing
the set of allowed status codes from a request is changing the
contract, and should be part of a microversion (except in [ 2 ] ).

The reason why we are so strict on contract is that weâd like
application writers to be able to know, for sure, what the contract is
at every microversion in Barbican. If they do not, they will need to write
conditional code in their application to handle ambiguities.

When in doubt, consider application authors. If it would work with no
client side changes on both Barbican versions, you probably donât need a
microversion. If, on the other hand, there is any ambiguity, a
microversion is probably needed.

The exception to not needing a microversion when returning a
previously unspecified error code is the 400, 403, 404 and 415 cases. This is
considered OK to return even if previously unspecified in the code since
itâs implied given keystone authentication can fail with a 403 and API
validation can fail with a 400 for invalid json request body. Request to
url/resource that does not exist always fails with 404. Invalid content types
are handled before API methods are called which results in a 415.

## When a microversion is not needed Â¶

A microversion is not needed in the following situation:

- the response Changing the error message without changing the response code
does not require a new microversion. Removing an inapplicable HTTP header, for example, suppose the Retry-After
HTTP header is being returned with a 4xx code. This header should only be
returned with a 503 or 3xx response, so it may be removed without bumping
the microversion. An obvious regression bug in an admin-only API where the bug can still
be fixed upstream on active stable branches. Admin-only APIs are less of
a concern for interoperability and generally a regression in behavior can
be dealt with as a bug fix when the documentation clearly shows the API
behavior was unexpectedly regressed. See [ 3 ] for an example from Nova.
Intentional behavior changes to an admin-only API do require a
microversion.

the response

- Changing the error message without changing the response code
does not require a new microversion.

Changing the error message without changing the response code
does not require a new microversion.

- Removing an inapplicable HTTP header, for example, suppose the Retry-After
HTTP header is being returned with a 4xx code. This header should only be
returned with a 503 or 3xx response, so it may be removed without bumping
the microversion.

Removing an inapplicable HTTP header, for example, suppose the Retry-After
HTTP header is being returned with a 4xx code. This header should only be
returned with a 503 or 3xx response, so it may be removed without bumping
the microversion.

- An obvious regression bug in an admin-only API where the bug can still
be fixed upstream on active stable branches. Admin-only APIs are less of
a concern for interoperability and generally a regression in behavior can
be dealt with as a bug fix when the documentation clearly shows the API
behavior was unexpectedly regressed. See [ 3 ] for an example from Nova.
Intentional behavior changes to an admin-only API do require a
microversion.

An obvious regression bug in an admin-only API where the bug can still
be fixed upstream on active stable branches. Admin-only APIs are less of
a concern for interoperability and generally a regression in behavior can
be dealt with as a bug fix when the documentation clearly shows the API
behavior was unexpectedly regressed. See [ 3 ] for an example from Nova.
Intentional behavior changes to an admin-only API do require a
microversion.

Footnotes

https://review.opendev.org/#/c/523194/

## In Code Â¶

In barbican/api/controllers/versions.py we define the is_supported function which is intended to be used in Controller methods to check if API
request version satisfies version restrictions. The function accepts min_version and max_version arguments, and returns True when the
requested version meets those constrainst.

Note

Originally Nova also implemented a decorator API, but it frequently
lead to code duplication. In Barbican it was decided to limit the
microversion API to just the is_supported function.

If you are adding a patch which adds a new microversion, it is
necessary to add changes to other places which describe your change:

- Update _MAX_MICROVERSION and bump _LAST_UPDATED in barbican/api/controllers/versions.py

Update _MAX_MICROVERSION and bump _LAST_UPDATED in barbican/api/controllers/versions.py

- Add a verbose description to doc/source/api/microversion_history.rst .

Add a verbose description to doc/source/api/microversion_history.rst .

- Add a release note with a features section announcing the new or
changed feature and the microversion.

Add a release note with a features section announcing the new or
changed feature and the microversion.

- Update the expected versions in affected tests, add new tests to test
both the old and new behavior to avoid regressions.

Update the expected versions in affected tests, add new tests to test
both the old and new behavior to avoid regressions.

- Make a new commit to python-barbicanclient and update corresponding
files to enable the newly added microversion API.

Make a new commit to python-barbicanclient and update corresponding
files to enable the newly added microversion API.

- If the microversion changes the response schema, a new schema and test for
the microversion must be added to Tempest.

If the microversion changes the response schema, a new schema and test for
the microversion must be added to Tempest.

- Update the API Reference documentation as appropriate.  The source is
located under doc/source/api/reference/ .

Update the API Reference documentation as appropriate.  The source is
located under doc/source/api/reference/ .

## Allocating a microversion Â¶

If you are adding a patch which adds a new microversion, it is
necessary to allocate the next microversion number. Except under
extremely unusual circumstances and this would have been mentioned in
the barbican spec for the change, the _MAX_MICROVERSION will be
incremented. This will also be the new minor version number for the API
change.

It is possible that multiple microversion patches would be proposed in
parallel and the microversions would conflict between patches.  This
will cause a merge conflict. We donât reserve a microversion for each
patch in advance as we donât know the final merge order. Developers
may need over time to rebase their patch calculating a new version
number as above based on the updated value of _MAX_MICROVERSION .

## Testing Microversioned API Methods Â¶

Testing a microversioned API method is very similar to a normal controller
method test, you just need to add the OpenStack-API-Version header
For unit tests, âbarbican.test.utils.set_versionâ function can be used,
for example:

def test_should_get_secret_as_json_v1 ( self ): utils . set_version ( self . app , '1.1' ) secret = self . _test_should_get_secret_as_json () self . assertIn ( 'consumers' , secret )
