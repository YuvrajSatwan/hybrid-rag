# Middleware Â¶

## Account Quotas Â¶

account_quotas is a middleware which blocks write requests (PUT, POST) if a
given account quota (in bytes) is exceeded while DELETE requests are still
allowed.

account_quotas uses the following metadata entries to store the account
quota

Metadata Use X-Account-Meta-Quota-Bytes (obsoleted) Maximum overall bytes stored
in account across containers. X-Account-Quota-Bytes Maximum overall bytes stored
in account across containers. X-Account-Quota-Bytes-Policy-<policyname> Maximum overall bytes stored
in account across containers,
for the given policy. X-Account-Quota-Count Maximum object count under
account. X-Account-Quota-Count-Policy-<policyname> Maximum object count under
account, for the given policy.

Metadata

Use

X-Account-Meta-Quota-Bytes (obsoleted)

Maximum overall bytes stored
in account across containers.

X-Account-Quota-Bytes

Maximum overall bytes stored
in account across containers.

X-Account-Quota-Bytes-Policy-<policyname>

Maximum overall bytes stored
in account across containers,
for the given policy.

X-Account-Quota-Count

Maximum object count under
account.

X-Account-Quota-Count-Policy-<policyname>

Maximum object count under
account, for the given policy.

Write requests to those metadata entries are only permitted for resellers.
There is no overall byte or object count limit set if the corresponding
metadata entries are not set.

Additionally, account quotas, of type quota-bytes or quota-count, may be set
for each storage policy, using metadata of the form x-account-<quota type>-policy-<policy name> . Again, only resellers may update these metadata, and
there will be no limit for a particular policy if the corresponding metadata
is not set.

Note

Per-policy quotas need not sum to the overall account quota, and the sum of
all Container quotas for a given policy need not sum to the accountâs
policy quota.

The account_quotas middleware should be added to the pipeline in your /etc/swift/proxy-server.conf file just after any auth middleware.
For example:

[ pipeline : main ] pipeline = catch_errors cache tempauth account_quotas proxy - server [ filter : account_quotas ] use = egg : swift #account_quotas

To set the quota on an account:

swift - A http : // 127.0.0.1 : 8080 / auth / v1 .0 - U account : reseller - K secret post - m quota - bytes : 10000

Remove the quota:

swift - A http : // 127.0.0.1 : 8080 / auth / v1 .0 - U account : reseller - K secret post - m quota - bytes :

The same limitations apply for the account quotas as for the container quotas.

For example, when uploading an object without a content-length header the proxy
server doesnât know the final size of the currently uploaded object and the
upload will be allowed if the current account size is within the quota.
Due to the eventual consistency further uploads might be possible until the
account size has been updated.

Bases: object

Account quota middleware

See above for a full description.

Returns a WSGI filter app for use with paste.deploy.

## AWS S3 Api Â¶

The s3api middleware will emulate the S3 REST api on top of swift.

To enable this middleware to your configuration, add the s3api middleware
in front of the auth middleware. See proxy-server.conf-sample for more
detail and configurable options.

To set up your client, ensure you are using the tempauth or keystone auth
system for swift project.
When your swift on a SAIO environment, make sure you have setting the tempauth
middleware configuration in proxy-server.conf , and the access key will be
the concatenation of the account and user strings that should look like
test:tester, and the secret access key is the account password. The host should
also point to the swift storage hostname.

The tempauth option example:

[filter:tempauth] use = egg:swift #tempauth user_admin_admin = admin .admin .reseller_admin user_test_tester = testing

An example client using tempauth with the python boto library is as follows:

from boto.s3.connection import S3Connection connection = S3Connection ( aws_access_key_id = 'test:tester' , aws_secret_access_key = 'testing' , port = 8080 , host = '127.0.0.1' , is_secure = False , calling_format = boto . s3 . connection . OrdinaryCallingFormat ())

And if you using keystone auth, you need the ec2 credentials, which can
be downloaded from the API Endpoints tab of the dashboard or by openstack
ec2 command.

Here is showing to create an EC2 credential:

# openstack ec2 credentials create +------------+---------------------------------------------------+ | Field      | Value                                             | +------------+---------------------------------------------------+ | access     | c2e30f2cd5204b69a39b3f1130ca8f61                  | | links      | {u'self': u'http://controller:5000/v3/......'}    | | project_id | 407731a6c2d0425c86d1e7f12a900488                  | | secret     | baab242d192a4cd6b68696863e07ed59                  | | trust_id   | None                                              | | user_id    | 00f0ee06afe74f81b410f3fe03d34fbc                  | +------------+---------------------------------------------------+

An example client using keystone auth with the python boto library will be:

from boto.s3.connection import S3Connection connection = S3Connection ( aws_access_key_id = 'c2e30f2cd5204b69a39b3f1130ca8f61' , aws_secret_access_key = 'baab242d192a4cd6b68696863e07ed59' , port = 8080 , host = '127.0.0.1' , is_secure = False , calling_format = boto . s3 . connection . OrdinaryCallingFormat ())

### Deployment Â¶

#### Proxy-Server Setting Â¶

Set s3api before your auth in your pipeline in proxy-server.conf file.
To enable all compatibility currently supported, you should make sure that
bulk, slo, and your auth middleware are also included in your proxy
pipeline setting.

Using tempauth, the minimum example config is:

[pipeline:main] pipeline = proxy-logging cache s3api tempauth bulk slo proxy-logging proxy-server

When using keystone, the config will be:

[pipeline:main] pipeline = proxy-logging cache authtoken s3api s3token keystoneauth bulk slo proxy-logging proxy-server

Finally, add the s3api middleware section:

[filter:s3api] use = egg:swift #s3api

Note

keystonemiddleware.authtoken can be located before/after s3api but
we recommend to put it before s3api because when authtoken is after s3api,
both authtoken and s3token will issue the acceptable token to keystone
(i.e. authenticate twice). And in the keystonemiddleware.authtoken middleware , you should set delay_auth_decision option to True .

### Constraints Â¶

Currently, the s3api is being ported from https://github.com/openstack/swift3 so any existing issues in swift3 are still remaining. Please make sure
descriptions in the example proxy-server.conf and what happens with the
config, before enabling the options.

### Supported API Â¶

The compatibility will continue to be improved upstream, you can keep and
eye on compatibility via a check tool build by SwiftStack. See https://github.com/swiftstack/s3compat in detail.

Bases: object

S3Api: S3 compatibility middleware

Check that required filters are present in order in the pipeline.

Check that proxy-server.conf has an appropriate pipeline for s3api.

Standard filter factory to use the middleware with paste.deploy

### S3 Token Middleware Â¶

s3token middleware is for authentication with s3api + keystone.
This middleware:

- Gets a request from the s3api middleware with an S3 Authorization
access key.

Gets a request from the s3api middleware with an S3 Authorization
access key.

- Validates s3 token with Keystone.

Validates s3 token with Keystone.

- Transforms the account name to AUTH_%(tenant_name).

Transforms the account name to AUTH_%(tenant_name).

- Optionally can retrieve and cache secret from keystone
to validate signature locally

Optionally can retrieve and cache secret from keystone
to validate signature locally

Note

If upgrading from swift3, the auth_version config option has been
removed, and the auth_uri option now includes the Keystone API
version. If you previously had a configuration like

[filter:s3token] use = egg:swift3 #s3token auth_uri = https://keystonehost:35357 auth_version = 3

you should now use

[filter:s3token] use = egg:swift #s3token auth_uri = https://keystonehost:35357/v3

Bases: object

Middleware that handles S3 authentication.

Returns a WSGI filter app for use with paste.deploy.

Bases: InputProxy

wsgi.input wrapper to calculate the X-Amz-Checksum-* of the input as itâs
read. The calculated value is checked against an expected value that is
sent in either the request headers or trailers. To allow for the latter,
the expected value is lazy fetched once the input has been read.

- wsgi_input â file-like object to be wrapped.

wsgi_input â file-like object to be wrapped.

- content_length â the expected number of bytes to be read.

content_length â the expected number of bytes to be read.

- checksum_hasher â a hasher to calculate the checksum of read bytes.

checksum_hasher â a hasher to calculate the checksum of read bytes.

- checksum_key â the name of the header or trailer that will have
the expected checksum value to be checked.

checksum_key â the name of the header or trailer that will have
the expected checksum value to be checked.

- checksum_source â a dict that will have the checksum_key .

checksum_source â a dict that will have the checksum_key .

Called each time a chunk of bytes is read from the wrapped input.

- chunk â the chunk of bytes that has been read.

chunk â the chunk of bytes that has been read.

- eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

Bases: InputProxy

wsgi.input wrapper to read a single chunk from an aws-chunked input and
validate its signature.

- wsgi_input â a wsgi input.

wsgi_input â a wsgi input.

- chunk_size â number of bytes to read.

chunk_size â number of bytes to read.

- validator â function to call to validate the chunkâs content.

validator â function to call to validate the chunkâs content.

- chunk_params â string of params from the chunkâs header.

chunk_params â string of params from the chunkâs header.

Called each time a chunk of bytes is read from the wrapped input.

- chunk â the chunk of bytes that has been read.

chunk â the chunk of bytes that has been read.

- eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

Pass read request to the underlying file-like object and
add bytes read to total.

size â (optional) maximum number of bytes to read; the default None means unlimited.

Pass readline request to the underlying file-like object and
add bytes read to total.

size â (optional) maximum number of bytes to read from the
current line; the default None means unlimited.

Bases: InputProxy

wsgi.input wrapper to verify the SHA256 of the input as itâs read.

Called each time a chunk of bytes is read from the wrapped input.

- chunk â the chunk of bytes that has been read.

chunk â the chunk of bytes that has been read.

- eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

Bases: S3Request

S3Acl request object.

authenticate method will run pre-authenticate request and retrieve
account information.
Note that it currently supports only keystone and tempauth.
(no support for the third party authentication middleware)

Wrapper method of _get_response to add s3 acl information
from response sysmeta headers.

Wrap up get_response call to hook with acl handling method.

Create a Swift request based on this requestâs environment.

Bases: Request

S3 request object.

swob.Request.body is not secure against malicious input.  It consumes
too much memory without any check when the request body is excessively
large.  Use xml() instead.

Get and set the container acl property

check_copy_source checks the copy source existence and if copying an
object to itself, for illegal request parameters

the source HEAD response

Check the md5 of the request body against the content-md5 header if the
header is present.

BadDigest â if the header is present but does not match the
calculated body md5.

True if the header is present, False otherwise.

get_container_info will return a result dict of get_container_info
from the backend Swift.

a dictionary of container info from
swift.controllers.base.get_container_info

NoSuchBucket when the container doesnât exist

InternalError when the request failed without 404

get_response is an entry point to be extended for child classes.
If additional tasks needed at that time of getting swift response,
we can override this method.
swift.common.middleware.s3api.s3request.S3Request need to just call
_get_response to get pure swift response.

Get and set the object acl property

S3Timestamp from Date header. If X-Amz-Date header specified, it
will be prior to Date header.

:return : S3Timestamp instance

Create a Swift request based on this requestâs environment.

Get the partNumber param, if it exists, and check it is valid.

To be valid, a partNumber must satisfy two criteria. First, it must be
an integer between 1 and the maximum allowed parts, inclusive. The
maximum allowed parts is the maximum of the configured max_upload_part_num and, if given, parts_count . Second, the
partNumber must be less than or equal to the parts_count , if it is
given.

parts_count â if given, this is the number of parts in an
existing object.

- InvalidPartArgument â if the partNumber param is invalid i.e.
less than 1 or greater than the maximum allowed parts.

InvalidPartArgument â if the partNumber param is invalid i.e.
less than 1 or greater than the maximum allowed parts.

- InvalidPartNumber â if the partNumber param is valid but greater
than num_parts .

InvalidPartNumber â if the partNumber param is valid but greater
than num_parts .

an integer part number if the partNumber param exists,
otherwise None .

Similar to swob.Request.body, but it checks the content length before
creating a body string.

Bases: object

A request class mixin to provide S3 signature v4 functionality

Return timestamp string according to the auth type
The difference from v2 is v4 have to see âX-Amz-Dateâ even though
itâs query auth type.

Bases: SigV4Mixin , S3Request

Bases: SigV4Mixin , S3AclRequest

Bases: object

wsgi.input wrapper to read a chunked input, verifying each chunk as itâs
read. Once all chunks have been read, any trailers are read.

- input â a wsgi input.

input â a wsgi input.

- decoded_content_length â the number of payload bytes expected to be
extracted from chunks.

decoded_content_length â the number of payload bytes expected to be
extracted from chunks.

- expected_trailers â the set of trailer names expected.

expected_trailers â the set of trailer names expected.

- sig_checker â an instance of SigCheckerV4 that will be called to
verify each chunkâs signature.

sig_checker â an instance of SigCheckerV4 that will be called to
verify each chunkâs signature.

Helper function to find a request class to use from Map

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: S3ResponseBase , HTTPException

S3 error object.

Reference information about S3 errors is available at: http://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html

Provide a summary of the error code and reason.

Bases: ErrorResponse

Bases: HeaderKeyDict

Similar to the Swiftâs normal HeaderKeyDict class, but its key name is
normalized as S3 clients expect.

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: InvalidArgument

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: S3ResponseBase , Response

Similar to the Response class in Swift, but uses our HeaderKeyDict for
headers instead of Swiftâs HeaderKeyDict.  This also translates Swift
specific headers to S3 headers.

Create a new S3 response object based on the given Swift response.

Bases: object

Base class for swift3 responses.

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: ErrorResponse

Bases: BucketNotEmpty

Bases: ErrorResponse

Bases: S3Exception

Bases: S3Exception

Bases: S3Exception

Bases: S3Exception

Bases: S3Exception

Bases: Exception

Bases: S3InputError

Client provided a X-Amz-Checksum-* header, but it doesnât match the data.

This should result in a InvalidRequest going back to the client.

Bases: S3InputError

Client provided a X-Amz-Checksum-* trailer, but it is not a valid format.

This should result in a InvalidRequest going back to the client.

Bases: S3InputError

Client provided a chunk-signature, but it doesnât match the data.

This should result in a 403 going back to the client.

Bases: S3InputError

Bases: BaseException

There was an error with the client input detected on read().

Inherit from BaseException (rather than Exception) so it cuts from the
proxy-server app (which will presumably be the one reading the input)
through all the layers of the pipeline back to s3api. It should never
escape the s3api middleware.

Bases: S3InputError

Bases: S3InputError

Bases: S3InputError

Client provided per-chunk signatures, but we have no secret with which to
verify them.

This happens if the auth middleware responsible for the user never called
the provided check_signature callback.

Bases: S3InputError

Client provided a X-Amz-Content-SHA256, but it doesnât match the data.

This should result in a BadDigest going back to the client.

Bases: S3InputError

Bases: ElementBase

Wrapper Element class of lxml.etree.Element to support
a utf-8 encoded non-ascii string as a text.

Why we need this?:
Original lxml.etree.Element supports only unicode for the text.
It declines maintainability because we have to call a lot of encode/decode
methods to apply account/container/object name (i.e. PATH_INFO) to each
Element instance. When using this class, we can remove such a redundant
codes from swift.common.middleware.s3api middleware.

utf-8 wrapper property of lxml.etree.Element.text

Bases: dict

If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
In either case, this is followed by: for k in F:  D[k] = F[k]

Bases: Timestamp

this format should be like âYYYYMMDDThhmmssZâ

Extract the bucket and object key from the requestâs PATH_INFO. Support
bucket-in-host if storage_domains and HTTP_HOST or SERVER_NAME are
specified. Otherwise the bucket is parsed from PATH_INFO.

- req â a swob.Request instance

req â a swob.Request instance

- storage_domains â a list of storage domains for which bucket-in-host
is supported.

storage_domains â a list of storage domains for which bucket-in-host
is supported.

- dns_compliant_bucket_names â whether to validate that the bucket
name must be dns compliant

dns_compliant_bucket_names â whether to validate that the bucket
name must be dns compliant

a tuple of (bucket, key). If the request path is invalid
the tuple (None, None) is returned.

Return the S3 access_key_id user for the request,
or None if it does not look like an S3 request.

req â a swob.Request instance

access_key_id if available, else None

Check whether a request looks like it ought to be an S3 request.

req â a swob.Request instance

True if access_key_id is available, False if not

mktime creates a float instance in epoch time really like as time.mktime

the difference from time.mktime is allowing to 2 formats string for the
argument for the S3 testing usage.
TODO: support

- timestamp_str â a string of timestamp formatted as
(a) RFC2822 (e.g. date header)
(b) %Y-%m-%dT%H:%M:%S (e.g. copy result)

timestamp_str â a string of timestamp formatted as
(a) RFC2822 (e.g. date header)
(b) %Y-%m-%dT%H:%M:%S (e.g. copy result)

- time_format â a string of format to parse in (b) process

time_format â a string of format to parse in (b) process

a float instance in epoch time

A bucket-in-host request has the bucket name as the first part of a . -separated host. If the host ends with any of
the given storage_domains then the bucket name is returned.
Otherwise None is returned.

- environ â an environment dict

environ â an environment dict

- storage_domains â a list of storage domains for which bucket-in-host
is supported.

storage_domains â a list of storage domains for which bucket-in-host
is supported.

bucket name or None

a swob.Request instance

A bucket-in-host request has the bucket name as
the first part of a . -separated host.

whether to validate that the bucket
name must be dns compliant

WSGI string

Returns the system metadata header for given resource type and name.

Returns the system metadata prefix for given resource type.

Validates the name of the bucket against S3 criteria, http://docs.amazonwebservices.com/AmazonS3/latest/BucketRestrictions.html True is valid, False is invalid.

### s3apiâs ACLs implementation Â¶

s3api uses a different implementation approach to achieve S3 ACLs.

First, we should understand what we have to design to achieve real S3 ACLs.
Current s3api(real S3)âs ACLs Model is as follows:

AccessControlPolicy : Owner : AccessControlList : Grant [ n ]: ( Grantee , Permission )

Each bucket or object has its own acl consisting of Owner and
AcessControlList. AccessControlList can contain some Grants.
By default, AccessControlList has only one Grant to allow FULL
CONTROLL to owner. Each Grant includes single pair with Grantee,
Permission. Grantee is the user (or user group) allowed the given permission.

This module defines the groups and the relation tree.

If you wanna get more information about S3âs ACLs model in detail,
please see official documentation here,

http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html

Bases: object

S3 ACL class.

http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html ):

The sample ACL includes an Owner element identifying the owner via the
AWS accountâs canonical user ID. The Grant element identifies the grantee
(either an AWS account or a predefined group), and the permission granted.
This default ACL has one Grant element for the owner. You grant permissions
by adding Grant elements, each grant identifying the grantee and the
permission.

Check that the user is an owner.

Check that the user has a permission.

Decode the value to an ACL instance.

Convert an ElementTree to an ACL instance

Convert HTTP headers to an ACL instance.

Bases: Group

Access permission to this group allows anyone to access the resource.  The
requests can be signed (authenticated) or unsigned (anonymous).  Unsigned
requests omit the Authentication header in the request.

Note: s3api regards unsigned requests as Swift API accesses, and bypasses
them to Swift.  As a result, AllUsers behaves completely same as
AuthenticatedUsers.

Bases: Group

This group represents all AWS accounts.  Access permission to this group
allows any AWS account to access the resource.  However, all requests must
be signed (authenticated).

Bases: object

A dict-like object that returns canned ACL.

Bases: object

Grant Class which includes both Grantee and Permission

Create an etree element.

Convert an ElementTree to an ACL instance

Bases: object

Base class for grantee.

Methods:

- init: create a Grantee instance

init: create a Grantee instance

- elem: create an ElementTree from itself

elem: create an ElementTree from itself

Static Methods:

- from_header: convert a grantee string in the HTTP header to an Grantee instance.

to an Grantee instance.

- from_elem: convert a ElementTree to an Grantee instance.

from_elem: convert a ElementTree to an Grantee instance.

Get an etree element of this instance.

Convert a grantee string in the HTTP header to an Grantee instance.

Bases: Grantee

Base class for Amazon S3 Predefined Groups

Get an etree element of this instance.

Bases: Group

WRITE and READ_ACP permissions on a bucket enables this group to write
server access logs to the bucket.

Bases: object

Owner class for S3 accounts

Bases: Grantee

Canonical user class for S3 accounts.

Get an etree element of this instance.

A set of predefined grants supported by AWS S3.

Decode Swift metadata to an ACL instance.

Given a resource type and HTTP headers, this method returns an ACL
instance.

Encode an ACL instance to Swift metadata.

Given a resource type and an ACL instance, this method returns HTTP
headers, which can be used for Swift metadata.

Convert a URI to one of the predefined groups.

### Acl Handlers Â¶

#### Why do we need this Â¶

To make controller classes clean, we need these handlers.
It is really useful for customizing acl checking algorithms for
each controller.

#### Basic Information Â¶

BaseAclHandler wraps basic Acl handling.
(i.e. it will check acl from ACL_MAP by using HEAD)

#### How to extend Â¶

Make a handler with the name of the controller.
(e.g. BucketAclHandler is for BucketController)
It consists of method(s) for actual S3 method on controllers as follows.

Example:

class BucketAclHandler ( BaseAclHandler ): def PUT : << put acl handling algorithms here for PUT bucket >>

Note

If the method DONâT need to recall _get_response in outside of
acl checking, the method have to return the response it needs at
the end of method.

Bases: object

BaseAclHandler: Handling ACL for basic requests mapped on ACL_MAP

Get ACL instance from S3 (e.g. x-amz-grant) headers or S3 acl xml body.

Bases: BaseAclHandler

BucketAclHandler: Handler for BucketController

Bases: BaseAclHandler

MultiObjectDeleteAclHandler: Handler for MultiObjectDeleteController

Bases: BaseAclHandler

MultiUpload stuff requires acl checking just once for BASE container
so that MultiUploadAclHandler extends BaseAclHandler to check acl only
when the verb defined. We should define the verb as the first step to
request to backend Swift at incoming request.

- BASE container name is always w/o âMULTIUPLOAD_SUFFIXâ

BASE container name is always w/o âMULTIUPLOAD_SUFFIXâ

- Any check timing is ok but we should check it as soon as possible.

Any check timing is ok but we should check it as soon as possible.

Controller Verb CheckResource Permission Part PUT Container WRITE Uploads GET Container READ Uploads POST Container WRITE Upload GET Container READ Upload DELETE Container WRITE Upload POST Container WRITE

Controller

Verb

CheckResource

Permission

Part

PUT

Container

WRITE

Uploads

GET

Container

READ

Uploads

POST

Container

WRITE

Upload

GET

Container

READ

Upload

DELETE

Container

WRITE

Upload

POST

Container

WRITE

Bases: BaseAclHandler

ObjectAclHandler: Handler for ObjectController

Bases: MultiUploadAclHandler

PartAclHandler: Handler for PartController

Bases: BaseAclHandler

S3AclHandler: Handler for S3AclController

Bases: MultiUploadAclHandler

UploadAclHandler: Handler for UploadController

Bases: MultiUploadAclHandler

UploadsAclHandler: Handler for UploadsController

Handle the x-amz-acl header.
Note that this header currently used for only normal-acl
(not implemented) on s3acl.
TODO: add translation to swift acl like as x-container-read to s3acl

Takes an S3 style ACL and returns a list of header/value pairs that
implement that ACL in Swift, or âNotImplementedâ if there isnât a way to do
that yet.

Bases: object

Base WSGI controller class for the middleware

Returns the target resource type of this controller.

Bases: Controller

Handles unsupported requests.

A decorator to ensure that the request is a bucket operation.  If the
target resource is an object, this decorator updates the request by default
so that the controller handles it as a bucket operation.  If âerr_respâ is
specified, this raises it on error instead.

A decorator to ensure the container existence.

A decorator to ensure that the request is an object operation.  If the
target resource is not an object, this raises an error response.

Bases: Controller

Handles account level requests.

Handle GET Service request

Bases: Controller

Handles bucket request.

Handle DELETE Bucket request

Handle GET Bucket (List Objects) request

Handle HEAD Bucket (Get Metadata) request

Handle POST Bucket request

Handle PUT Bucket request

Bases: Controller

Handles requests on objects

Handle DELETE Object request

Handle GET Object request

Handle HEAD Object request

Handle PUT Object and PUT Object (Copy) request

Bases: Controller

Handles the following APIs:

- GET Bucket acl

GET Bucket acl

- PUT Bucket acl

PUT Bucket acl

- GET Object acl

GET Object acl

- PUT Object acl

PUT Object acl

Those APIs are logged as ACL operations in the S3 server log.

Handles GET Bucket acl and GET Object acl.

Handles PUT Bucket acl and PUT Object acl.

Attempts to construct an S3 ACL based on what is found in the swift headers

Bases: Controller

Handles the following APIs:

- GET Bucket acl

GET Bucket acl

- PUT Bucket acl

PUT Bucket acl

- GET Object acl

GET Object acl

- PUT Object acl

PUT Object acl

Those APIs are logged as ACL operations in the S3 server log.

Handles GET Bucket acl and GET Object acl.

Handles PUT Bucket acl and PUT Object acl.

Implementation of S3 Multipart Upload.

This module implements S3 Multipart Upload APIs with the Swift SLO feature.
The following explains how S3api uses swift container and objects to store S3
upload information:

### [bucket]+segments Â¶

A container to store upload information. [bucket] is the original bucket
where multipart upload is initiated.

### [bucket]+segments/[upload_id] Â¶

An object of the ongoing upload id. The object is empty and used for
checking the target upload status. If the object exists, it means that the
upload is initiated but not either completed or aborted.

### [bucket]+segments/[upload_id]/[part_number] Â¶

The last suffix is the part number under the upload id. When the client uploads
the parts, they will be stored in the namespace with
[bucket]+segments/[upload_id]/[part_number].

Example listing result in the [bucket]+segments container:

[ bucket ] + segments / [ upload_id1 ] # upload id object for upload_id1 [ bucket ] + segments / [ upload_id1 ] / 1 # part object for upload_id1 [ bucket ] + segments / [ upload_id1 ] / 2 # part object for upload_id1 [ bucket ] + segments / [ upload_id1 ] / 3 # part object for upload_id1 [ bucket ] + segments / [ upload_id2 ] # upload id object for upload_id2 [ bucket ] + segments / [ upload_id2 ] / 1 # part object for upload_id2 [ bucket ] + segments / [ upload_id2 ] / 2 # part object for upload_id2 . .

Those part objects are directly used as segments of a Swift
Static Large Object when the multipart upload is completed.

Bases: Controller

Handles the following APIs:

- Upload Part

Upload Part

- Upload Part - Copy

Upload Part - Copy

Those APIs are logged as PART operations in the S3 server log.

Handles Upload Part and Upload Part Copy.

Bases: Controller

Handles the following APIs:

- List Parts

List Parts

- Abort Multipart Upload

Abort Multipart Upload

- Complete Multipart Upload

Complete Multipart Upload

Those APIs are logged as UPLOAD operations in the S3 server log.

Handles Abort Multipart Upload.

Handles List Parts.

Handles Complete Multipart Upload.

Bases: Controller

Handles the following APIs:

- List Multipart Uploads

List Multipart Uploads

- Initiate Multipart Upload

Initiate Multipart Upload

Those APIs are logged as UPLOADS operations in the S3 server log.

Handles List Multipart Uploads

Handles Initiate Multipart Upload.

Bases: Controller

Handles Delete Multiple Objects, which is logged as a MULTI_OBJECT_DELETE
operation in the S3 server log.

Handles Delete Multiple Objects.

Bases: Controller

Handles the following APIs:

- GET Bucket versioning

GET Bucket versioning

- PUT Bucket versioning

PUT Bucket versioning

Those APIs are logged as VERSIONING operations in the S3 server log.

Handles GET Bucket versioning.

Handles PUT Bucket versioning.

Bases: Controller

Handles GET Bucket location, which is logged as a LOCATION operation in the
S3 server log.

Handles GET Bucket location.

Bases: Controller

Handles the following APIs:

- GET Bucket logging

GET Bucket logging

- PUT Bucket logging

PUT Bucket logging

Those APIs are logged as LOGGING_STATUS operations in the S3 server log.

Handles GET Bucket logging.

Handles PUT Bucket logging.

## Backend Ratelimit Â¶

Bases: object

Backend rate-limiting middleware.

Rate-limits requests to backend storage node devices. Each (device, request
method) combination is independently rate-limited. All requests with a
âGETâ, âHEADâ, âPUTâ, âPOSTâ, âDELETEâ, âUPDATEâ or âREPLICATEâ method are
rate limited on a per-device basis by both a method-specific rate and an
overall device rate limit.

If a request would cause the rate-limit to be exceeded for the method
and/or device then a response with a 529 status code is returned.

## Bulk Operations (Delete and Archive Auto Extraction) Â¶

Middleware that will perform many operations on a single request.

### Extract Archive Â¶

Expand tar files into a Swift account. Request must be a PUT with the
query parameter ?extract-archive=format specifying the format of archive
file. Accepted formats are tar, tar.gz, and tar.bz2.

For a PUT to the following url:

/v1/AUTH_Account/$UPLOAD_PATH?extract-archive=tar.gz

UPLOAD_PATH is where the files will be expanded to. UPLOAD_PATH can be a
container, a pseudo-directory within a container, or an empty string. The
destination of a file in the archive will be built as follows:

/v1/AUTH_Account/$UPLOAD_PATH/$FILE_PATH

Where FILE_PATH is the file name from the listing in the tar file.

If the UPLOAD_PATH is an empty string, containers will be auto created
accordingly and files in the tar that would not map to any container (files
in the base directory) will be ignored.

Only regular files will be uploaded. Empty directories, symlinks, etc will
not be uploaded.

### Content Type Â¶

If the content-type header is set in the extract-archive call, Swift will
assign that content-type to all the underlying files. The bulk middleware
will extract the archive file and send the internal files using PUT
operations using the same headers from the original request
(e.g. auth-tokens, content-Type, etc.). Notice that any middleware call
that follows the bulk middleware does not know if this was a bulk request
or if these were individual requests sent by the user.

In order to make Swift detect the content-type for the files based on the
file extension, the content-type in the extract-archive call should not be
set. Alternatively, it is possible to explicitly tell Swift to detect the
content type using this header:

X - Detect - Content - Type : true

For example:

curl -X PUT http://127.0.0.1/v1/AUTH_acc/cont/$?extract-archive=tar
 -T backup.tar
 -H "Content-Type: application/x-tar"
 -H "X-Auth-Token: xxx"
 -H "X-Detect-Content-Type: true"

### Assigning Metadata Â¶

The tar file format (1) allows for UTF-8 key/value pairs to be associated
with each file in an archive. If a file has extended attributes, then tar
will store those as key/value pairs. The bulk middleware can read those
extended attributes and convert them to Swift object metadata. Attributes
starting with âuser.metaâ are converted to object metadata, and
âuser.mime_typeâ is converted to Content-Type.

For example:

setfattr - n user . mime_type - v "application/python-setup" setup . py setfattr - n user . meta . lunch - v "burger and fries" setup . py setfattr - n user . meta . dinner - v "baked ziti" setup . py setfattr - n user . stuff - v "whee" setup . py

Will get translated to headers:

Content - Type : application / python - setup X - Object - Meta - Lunch : burger and fries X - Object - Meta - Dinner : baked ziti

The bulk middleware  will handle xattrs stored by both GNU and BSD tar (2).
Only xattrs user.mime_type and user.meta.* are processed. Other
attributes are ignored.

In addition to the extended attributes, the object metadata and the
x-delete-at/x-delete-after headers set in the request are also assigned to the
extracted objects.

Notes:

(1) The POSIX 1003.1-2001 (pax) format. The default format on GNU tar
1.27.1 or later.

(2) Even with pax-format tarballs, different encoders store xattrs slightly
differently; for example, GNU tar stores the xattr âuser.userattributeâ as
pax header âSCHILY.xattr.user.userattributeâ, while BSD tar (which uses
libarchive) stores it as âLIBARCHIVE.xattr.user.userattributeâ.

### Response Â¶

The response from bulk operations functions differently from other Swift
responses. This is because a short request body sent from the client could
result in many operations on the proxy server and precautions need to be
made to prevent the request from timing out due to lack of activity. To
this end, the client will always receive a 200 OK response, regardless of
the actual success of the call.  The body of the response must be parsed to
determine the actual success of the operation. In addition to this the
client may receive zero or more whitespace characters prepended to the
actual response body while the proxy server is completing the request.

The format of the response body defaults to text/plain but can be either
json or xml depending on the Accept header. Acceptable formats are text/plain , application/json , application/xml , and text/xml .
An example body is as follows:

{ "Response Status" : "201 Created" , "Response Body" : "" , "Errors" : [], "Number Files Created" : 10 }

If all valid files were uploaded successfully the Response Status will be
201 Created.  If any files failed to be created the response code
corresponds to the subrequestâs error. Possible codes are 400, 401, 502 (on
server errors), etc. In both cases the response body will specify the
number of files successfully uploaded and a list of the files that failed.

There are proxy logs created for each file (which becomes a subrequest) in
the tar. The subrequestâs proxy log will have a swift.source set to âEAâ
the logâs content length will reflect the unzipped size of the file. If
double proxy-logging is used the leftmost logger will not have a
swift.source set and the content length will reflect the size of the
payload sent to the proxy (the unexpanded size of the tar.gz).

### Bulk Delete Â¶

Will delete multiple objects or containers from their account with a
single request. Responds to POST requests with query parameter ?bulk-delete set. The request url is your storage url. The Content-Type
should be set to text/plain . The body of the POST request will be a
newline separated list of url encoded objects to delete. You can delete
10,000 (configurable) objects per request. The objects specified in the
POST request body must be URL encoded and in the form:

/ container_name / obj_name

or for a container (which must be empty at time of delete):

/ container_name

The response is similar to extract archive as in every response will be a
200 OK and you must parse the response body for actual results. An example
response is:

{ "Number Not Found" : 0 , "Response Status" : "200 OK" , "Response Body" : "" , "Errors" : [], "Number Deleted" : 6 }

If all items were successfully deleted (or did not exist), the Response
Status will be 200 OK. If any failed to delete, the response code
corresponds to the subrequestâs error. Possible codes are 400, 401, 502 (on
server errors), etc. In all cases the response body will specify the number
of items successfully deleted, not found, and a list of those that failed.
The return body will be formatted in the way specified in the requestâs Accept header. Acceptable formats are text/plain , application/json , application/xml , and text/xml .

There are proxy logs created for each object or container (which becomes a
subrequest) that is deleted. The subrequestâs proxy log will have a
swift.source set to âBDâ the logâs content length of 0. If double
proxy-logging is used the leftmost logger will not have a
swift.source set and the content length will reflect the size of the
payload sent to the proxy (the list of objects/containers to be deleted).

Bases: Exception

## CatchErrors Â¶

Bases: Exception

Bases: object

Enforces that inner_iter yields exactly <nbytes> bytes before
exhaustion.

If inner_iter fails to do so, BadResponseLength is raised.

- inner_iter â iterable of bytestrings

inner_iter â iterable of bytestrings

- nbytes â number of bytes expected

nbytes â number of bytes expected

N.B. since we require the nbytes param and require the inner_iter to yield
exactly that many bytes we can support the __len__ interface for anyone
happens to expect non chunked resp iterables to support that
(e.g.  eventletâs wsgi.server).

Bases: object

Middleware that provides high-level error handling and ensures that a
transaction id will be set for every request.

Bases: WSGIContext

## CNAME Lookup Â¶

CNAME Lookup Middleware

Middleware that translates an unknown domain in the host header to
something that ends with the configured storage_domain by looking up
the given domainâs CNAME record in DNS.

This middleware will continue to follow a CNAME chain in DNS until it finds
a record ending in the configured storage domain or it reaches the configured
maximum lookup depth. If a match is found, the environmentâs Host header is
rewritten and the request is passed further down the WSGI chain.

Bases: object

CNAME Lookup Middleware

See above for a full description.

- app â The next WSGI filter or app in the paste.deploy
chain.

app â The next WSGI filter or app in the paste.deploy
chain.

- conf â The configuration dict for the middleware.

conf â The configuration dict for the middleware.

Given a domain, returns its DNS CNAME mapping and DNS ttl.

- domain â domain to query on

domain â domain to query on

- resolver â dns.resolver.Resolver() instance used for executing DNS
queries

resolver â dns.resolver.Resolver() instance used for executing DNS
queries

(ttl, result)

## Container Quotas Â¶

The container_quotas middleware implements simple quotas that can be
imposed on swift containers by a user with the ability to set container
metadata, most likely the account administrator.  This can be useful for
limiting the scope of containers that are delegated to non-admin users, exposed
to formpost uploads, or just as a self-imposed sanity check.

Any object PUT operations that exceed these quotas return a 413 response
(request entity too large) with a descriptive body.

Quotas are subject to several limitations: eventual consistency, the timeliness
of the cached container_info (60 second ttl by default), and itâs unable to
reject chunked transfer uploads that exceed the quota (though once the quota
is exceeded, new chunked transfers will be refused).

Quotas are set by adding meta values to the container, and are validated when
set:

Metadata Use X-Container-Meta-Quota-Bytes Maximum size of the
container, in bytes. X-Container-Meta-Quota-Count Maximum object count of the
container.

Metadata

Use

X-Container-Meta-Quota-Bytes

Maximum size of the
container, in bytes.

X-Container-Meta-Quota-Count

Maximum object count of the
container.

The container_quotas middleware should be added to the pipeline in your /etc/swift/proxy-server.conf file just after any auth middleware.
For example:

[ pipeline : main ] pipeline = catch_errors cache tempauth container_quotas proxy - server [ filter : container_quotas ] use = egg : swift #container_quotas

## Container Sync Middleware Â¶

Bases: object

WSGI middleware that validates an incoming container sync request
using the container-sync-realms.conf style of container sync.

## Cross Domain Policies Â¶

Bases: object

Cross domain middleware used to respond to requests for cross domain
policy information.

If the path is /crossdomain.xml it will respond with an xml cross
domain policy document. This allows web pages hosted elsewhere to use
client side technologies such as Flash, Java and Silverlight to interact
with the Swift API.

To enable this middleware, add it to the pipeline in your proxy-server.conf
file. It should be added before any authentication (e.g., tempauth or
keystone) middleware. In this example ellipsis (â¦) indicate other
middleware you may have chosen to use:

[pipeline:main] pipeline = ... crossdomain ... authtoken ... proxy-server

And add a filter section, such as:

[filter:crossdomain] use = egg:swift #crossdomain cross_domain_policy = <allow-access-from domain = "*.example.com" /> <allow-access-from domain = "www.example.com" secure = "false" />

For continuation lines, put some whitespace before the continuation
text. Ensure you put a completely blank line to terminate the cross_domain_policy value.

The cross_domain_policy name/value is optional. If omitted, the policy
defaults as if you had specified:

cross_domain_policy = <allow-access-from domain = "*" secure = "false" />

Note

The default policy is very permissive; this is appropriate
for most public cloud deployments, but may not be appropriate
for all deployments. See also: CWE-942

Returns a 200 response with cross domain policy information

## Discoverability Â¶

Swift will by default provide clients with an interface providing details
about the installation. Unless disabled (i.e expose_info=false in Proxy Server Configuration ), a GET request to /info will return configuration
data in JSON format.  An example response:

{ "swift" : { "version" : "1.11.0" }, "staticweb" : {}, "tempurl" : {}}

This would signify to the client that swift version 1.11.0 is running and that
staticweb and tempurl are available in this installation.

There may be administrator-only information available via /info . To
retrieve it, one must use an HMAC-signed request, similar to TempURL.
The signature may be produced like so:

swift tempurl GET 3600 / info secret 2 >/ dev / null | sed s / temp_url / swiftinfo / g

## Domain Remap Â¶

Domain Remap Middleware

Middleware that translates container and account parts of a domain to path
parameters that the proxy server understands.

Translation is only performed when the request URLâs host domain matches one of
a list of domains. This list may be configured by the option storage_domain , and defaults to the single domain example.com .

If not already present, a configurable path_root , which defaults to v1 ,
will be added to the start of the translated path.

For example, with the default configuration:

container . AUTH - account . example . com / object container . AUTH - account . example . com / v1 / object

would both be translated to:

container . AUTH - account . example . com / v1 / AUTH_account / container / object

and:

AUTH - account . example . com / container / object AUTH - account . example . com / v1 / container / object

would both be translated to:

AUTH - account . example . com / v1 / AUTH_account / container / object

Additionally, translation is only performed when the account name in the
translated path starts with a reseller prefix matching one of a list configured
by the option reseller_prefixes , or when no match is found but a default_reseller_prefix has been configured.

The reseller_prefixes list defaults to the single prefix AUTH . The default_reseller_prefix is not configured by default.

Browsers can convert a host header to lowercase, so the middleware checks that
the reseller prefix on the account name is the correct case. This is done by
comparing the items in the reseller_prefixes config option to the found
prefix. If they match except for case, the item from reseller_prefixes will
be used instead of the found reseller prefix. The middleware will also replace
any hyphen (â-â) in the account name with an underscore (â_â).

For example, with the default configuration:

auth - account . example . com / container / object AUTH - account . example . com / container / object auth_account . example . com / container / object AUTH_account . example . com / container / object

would all be translated to:

< unchanged >. example . com / v1 / AUTH_account / container / object

When no match is found in reseller_prefixes , the default_reseller_prefix config option is used. When no default_reseller_prefix is configured, any request with an account prefix
not in the reseller_prefixes list will be ignored by this middleware.

For example, with default_reseller_prefix = AUTH :

account . example . com / container / object

would be translated to:

account . example . com / v1 / AUTH_account / container / object

Note that this middleware requires that container names and account names
(except as described above) must be DNS-compatible. This means that the account
name created in the system and the containers created by users cannot exceed 63
characters or have UTF-8 characters. These are restrictions over and above what
Swift requires and are not explicitly checked. Simply put, this middleware
will do a best-effort attempt to derive account and container names from
elements in the domain name and put those derived values into the URL path
(leaving the Host header unchanged).

Also note that using Container to Container Synchronization with remapped domain names
is not advised. With Container to Container Synchronization , you should use the true
storage end points as sync destinations.

Bases: object

Domain Remap Middleware

See above for a full description.

- app â The next WSGI filter or app in the paste.deploy
chain.

app â The next WSGI filter or app in the paste.deploy
chain.

- conf â The configuration dict for the middleware.

conf â The configuration dict for the middleware.

## Dynamic Large Objects Â¶

DLO support centers around a user specified filter that matches
segments and concatenates them together in object listing order. Please see
the DLO docs for Dynamic Large Objects further details.

## Encryption Â¶

Encryption middleware should be deployed in conjunction with the Keymaster middleware.

Implements middleware for object encryption which comprises an instance of a Decrypter combined with an
instance of an Encrypter .

Provides a factory function for loading encryption middleware.

Bases: InputProxy

File-like object to be swapped in for wsgi.input.

Called each time a chunk of bytes is read from the wrapped input.

- chunk â the chunk of bytes that has been read.

chunk â the chunk of bytes that has been read.

- eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

Bases: object

Middleware for encrypting data and user metadata.

By default all PUT or POSTâed object data and/or metadata will be
encrypted. Encryption of new data and/or metadata may be disabled by
setting the disable_encryption option to True. However, this middleware
should remain in the pipeline in order for existing encrypted data to be
read.

Bases: CryptoWSGIContext

Encrypt user-metadata header values. Replace each x-object-meta-<key>
user metadata header with a corresponding
x-object-transient-sysmeta-crypto-meta-<key> header which has the
crypto metadata required to decrypt appended to the encrypted value.

- req â a swob Request

req â a swob Request

- keys â a dict of encryption keys

keys â a dict of encryption keys

Encrypt the new object headers with a new iv and the current crypto.
Note that an object may have encrypted headers while the body may
remain unencrypted.

Encrypt a header value using the supplied key.

- crypto â a Crypto instance

crypto â a Crypto instance

- value â value to encrypt

value â value to encrypt

- key â crypto key to use

key â crypto key to use

a tuple of (encrypted value, crypto_meta) where crypto_meta is a
dict of form returned by get_crypto_meta()

ValueError â if value is empty

Bases: CryptoWSGIContext

Base64-decode and decrypt a value using the crypto_meta provided.

- value â a base64-encoded value to decrypt

value â a base64-encoded value to decrypt

- key â crypto key to use

key â crypto key to use

- crypto_meta â a crypto-meta dict of form returned by get_crypto_meta()

crypto_meta â a crypto-meta dict of form returned by get_crypto_meta()

- decoder â function to turn the decrypted bytes into useful data

decoder â function to turn the decrypted bytes into useful data

decrypted value

Base64-decode and decrypt a value if crypto meta can be extracted from
the value itself, otherwise return the value unmodified.

A value should either be a string that does not contain the â;â
character or should be of the form:

< base64 - encoded ciphertext > ; swift_meta =< crypto meta >

- value â value to decrypt

value â value to decrypt

- key â crypto key to use

key â crypto key to use

- required â if True then the value is required to be decrypted
and an EncryptionException will be raised if the
header cannot be decrypted due to missing crypto meta.

required â if True then the value is required to be decrypted
and an EncryptionException will be raised if the
header cannot be decrypted due to missing crypto meta.

- decoder â function to turn the decrypted bytes into useful data

decoder â function to turn the decrypted bytes into useful data

decrypted value if crypto meta is found, otherwise the
unmodified value

EncryptionException â if an error occurs while parsing crypto
meta or if the header value was required
to be decrypted but crypto meta was not
found.

Extract a crypto_meta dict from a header.

- header_name â name of header that may have crypto_meta

header_name â name of header that may have crypto_meta

- check â if True validate the crypto meta

check â if True validate the crypto meta

A dict containing crypto_meta items

EncryptionException â if an error occurs while parsing the
crypto meta

Determine if a response should be decrypted, and if so then fetch keys.

- req â a Request object

req â a Request object

- crypto_meta â a dict of crypto metadata

crypto_meta â a dict of crypto metadata

a dict of decryption keys

Get a wrapped key from crypto-meta and unwrap it using the provided
wrapping key.

- crypto_meta â a dict of crypto-meta

crypto_meta â a dict of crypto-meta

- wrapping_key â key to be used to decrypt the wrapped key

wrapping_key â key to be used to decrypt the wrapped key

an unwrapped key

HTTPInternalServerError â if the crypto-meta has no wrapped key
or the unwrapped key is invalid

Bases: object

Middleware for decrypting data and user metadata.

Bases: BaseDecrypterContext

Parses json body listing and decrypt encrypted entries. Updates
Content-Length header with new body length and return a body iter.

Bases: BaseDecrypterContext

Find encrypted headers and replace with the decrypted versions.

- put_keys â a dict of decryption keys used for object PUT.

put_keys â a dict of decryption keys used for object PUT.

- post_keys â a dict of decryption keys used for object POST.

post_keys â a dict of decryption keys used for object POST.

A list of headers with any encrypted headers replaced by their
decrypted values.

HTTPInternalServerError â if any error occurs while decrypting
headers

Decrypts a multipart mime doc response body.

- resp â application response

resp â application response

- boundary â multipart boundary string

boundary â multipart boundary string

- body_key â decryption key for the response body

body_key â decryption key for the response body

- crypto_meta â crypto_meta for the response body

crypto_meta â crypto_meta for the response body

generator for decrypted response body

Decrypts a response body.

- resp â application response

resp â application response

- body_key â decryption key for the response body

body_key â decryption key for the response body

- crypto_meta â crypto_meta for the response body

crypto_meta â crypto_meta for the response body

- offset â offset into object content at which response body starts

offset â offset into object content at which response body starts

generator for decrypted response body

## Etag Quoter Â¶

This middleware fix the Etag header of responses so that it is RFC compliant. RFC 7232 specifies that
the value of the Etag header must be double quoted.

It must be placed at the beggining of the pipeline, right after cache:

[ pipeline : main ] pipeline = ... cache etag - quoter ... [ filter : etag - quoter ] use = egg : swift #etag_quoter

Set X-Account-Rfc-Compliant-Etags: true at the account
level to have any Etags in object responses be double quoted, as in "d41d8cd98f00b204e9800998ecf8427e" . Alternatively, you may
only fix Etags in a single container by setting X-Container-Rfc-Compliant-Etags: true on the container.
This may be necessary for Swift to work properly with some CDNs.

Either option may also be explicitly disabled , so you may enable quoted
Etags account-wide as above but turn them off for individual containers
with X-Container-Rfc-Compliant-Etags: false . This may be
useful if some subset of applications expect Etags to be bare MD5s.

## FormPost Â¶

FormPost Middleware

Translates a browser form post into a regular Swift object PUT.

The format of the form is:

< form action = "<swift-url>" method = "POST" enctype = "multipart/form-data" > < input type = "hidden" name = "redirect" value = "<redirect-url>" /> < input type = "hidden" name = "max_file_size" value = "<bytes>" /> < input type = "hidden" name = "max_file_count" value = "<count>" /> < input type = "hidden" name = "expires" value = "<unix-timestamp>" /> < input type = "hidden" name = "signature" value = "<hmac>" /> < input type = "file" name = "file1" />< br /> < input type = "submit" /> </ form >

Optionally, if you want the uploaded files to be temporary you can set
x-delete-at or x-delete-after attributes by adding one of these as a
form input:

< input type = "hidden" name = "x_delete_at" value = "<unix-timestamp>" /> < input type = "hidden" name = "x_delete_after" value = "<seconds>" />

If you want to specify the content type or content encoding of the files you
can set content-encoding or content-type by adding them to the form input:

< input type = "hidden" name = "content-type" value = "text/html" /> < input type = "hidden" name = "content-encoding" value = "gzip" />

The above example applies these parameters to all uploaded files. You can also
set the content-type and content-encoding on a per-file basis by adding the
parameters to each part of the upload.

The <swift-url> is the URL of the Swift destination, such as:

https : // swift - cluster . example . com / v1 / AUTH_account / container / object_prefix

The name of each file uploaded will be appended to the <swift-url>
given. So, you can upload directly to the root of container with a
url like:

https : // swift - cluster . example . com / v1 / AUTH_account / container /

Optionally, you can include an object prefix to better separate
different usersâ uploads, such as:

https : // swift - cluster . example . com / v1 / AUTH_account / container / object_prefix

Note the form method must be POST and the enctype must be set as
âmultipart/form-dataâ.

The redirect attribute is the URL to redirect the browser to after the upload
completes. This is an optional parameter. If you are uploading the form via an
XMLHttpRequest the redirect should not be included. The URL will have status
and message query parameters added to it, indicating the HTTP status code for
the upload (2xx is success) and a possible message for further information if
there was an error (such as âmax_file_size exceededâ).

The max_file_size attribute must be included and indicates the
largest single file upload that can be done, in bytes.

The max_file_count attribute must be included and indicates the
maximum number of files that can be uploaded with the form. Include
additional <input type="file" name="filexx" /> attributes if
desired.

The expires attribute is the Unix timestamp before which the form
must be submitted before it is invalidated.

The signature attribute is the HMAC signature of the form. Here is
sample code for computing the signature:

import hmac from hashlib import sha512 from time import time path = '/v1/account/container/object_prefix' redirect = 'https://srv.com/some-page' # set to '' if redirect not in form max_file_size = 104857600 max_file_count = 10 expires = int ( time () + 600 ) key = 'mykey' hmac_body = ' %s \n %s \n %s \n %s \n %s ' % ( path , redirect , max_file_size , max_file_count , expires ) signature = hmac . new ( key , hmac_body , sha512 ) . hexdigest ()

The key is the value of either the account (X-Account-Meta-Temp-URL-Key,
X-Account-Meta-Temp-Url-Key-2) or the container
(X-Container-Meta-Temp-URL-Key, X-Container-Meta-Temp-Url-Key-2) TempURL keys.

Be certain to use the full path, from the /v1/ onward.
Note that x_delete_at and x_delete_after are not used in signature generation
as they are both optional attributes.

The command line tool swift-form-signature may be used (mostly
just when testing) to compute expires and signature.

Also note that the file attributes must be after the other attributes
in order to be processed correctly. If attributes come after the
file, they wonât be sent with the subrequest (there is no way to
parse all the attributes on the server-side without reading the whole
thing into memory â to service many requests, some with large files,
there just isnât enough memory on the server, so attributes following
the file are simply ignored).

Bases: object

FormPost Middleware

See above for a full description.

The proxy logs created for any subrequests made will have swift.source set
to âFPâ.

- app â The next WSGI filter or app in the paste.deploy
chain.

app â The next WSGI filter or app in the paste.deploy
chain.

- conf â The configuration dict for the middleware.

conf â The configuration dict for the middleware.

The next WSGI application/filter in the paste.deploy pipeline.

The filter configuration dict.

The maximum size of any attributeâs value. Any additional data will be
truncated.

The size of data to read from the form at any given time.

Returns the WSGI filter for use with paste.deploy.

## GateKeeper Â¶

The gatekeeper middleware imposes restrictions on the headers that
may be included with requests and responses. Request headers are filtered
to remove headers that should never be generated by a client. Similarly,
response headers are filtered to remove private headers that should
never be passed to a client.

The gatekeeper middleware must always be present in the proxy server
wsgi pipeline. It should be configured close to the start of the pipeline
specified in /etc/swift/proxy-server.conf , immediately after catch_errors
and before any other middleware. It is essential that it is configured ahead
of all middlewares using system metadata in order that they function
correctly.

If gatekeeper middleware is not configured in the pipeline then it will be
automatically inserted close to the start of the pipeline by the proxy server.

A list of python regular expressions that will be used to
match against outbound response headers. Matching headers will
be removed from the response.

## Healthcheck Â¶

Bases: object

Healthcheck middleware used for monitoring.

If the path is /healthcheck, it will respond 200 with âOKâ as the body.

If the optional config parameter âdisable_pathâ is set, and a file is
present at that path, it will respond 503 with âDISABLED BY FILEâ as the
body.

Returns a 503 response with âDISABLED BY FILEâ in the body.

Returns a 200 response with âOKâ in the body.

## Keymaster Â¶

Keymaster middleware should be deployed in conjunction with the Encryption middleware.

Bases: object

Base middleware for providing encryption keys.

This provides some basic helpers for:

- loading from a separate config path,

loading from a separate config path,

- deriving keys based on path, and

deriving keys based on path, and

- installing a swift.callback.fetch_crypto_keys hook
in the request environment.

installing a swift.callback.fetch_crypto_keys hook
in the request environment.

Subclasses should define log_route , keymaster_opts , and keymaster_conf_section attributes, and implement the _get_root_secret function.

Creates an encryption key that is unique for the given path.

- path â the (WSGI string) path of the resource being encrypted.

path â the (WSGI string) path of the resource being encrypted.

- secret_id â the id of the root secret from which the key should
be derived.

secret_id â the id of the root secret from which the key should
be derived.

an encryption key.

UnknownSecretIdError â if the secret_id is not recognised.

Bases: BaseKeyMaster

Middleware for providing encryption keys.

The middleware requires its encryption root secret to be set. This is the
root secret from which encryption keys are derived. This must be set before
first use to a value that is at least 256 bits. The security of all
encrypted data critically depends on this key, therefore it should be set
to a high-entropy value. For example, a suitable value may be obtained by
generating a 32 byte (or longer) value using a cryptographically secure
random number generator. Changing the root secret is likely to result in
data loss.

Bases: WSGIContext

The simple scheme for key derivation is as follows: every path is
associated with a key, where the key is derived from the path itself in a
deterministic fashion such that the key does not need to be stored.
Specifically, the key for any path is an HMAC of a root key and the path
itself, calculated using an SHA256 hash function:

< path_key > = HMAC_SHA256 ( < root_secret > , < path > )

Setup container and object keys based on the request path.

Keys are derived from request path. The âidâ entry in the results dict
includes the part of the path used to derive keys. Other keymaster
implementations may use a different strategy to generate keys and may
include a different type of âidâ, so callers should treat the âidâ as
opaque keymaster-specific data.

key_id â if given this should be a dict with the items included
under the id key of a dict returned by this method.

A dict containing encryption keys for âobjectâ and
âcontainerâ, and entries âidâ and âall_idsâ. The âall_idsâ entry is a
list of key id dicts for all root secret ids including the one used
to generate the returned keys.

## KeystoneAuth Â¶

Bases: object

Swift middleware to Keystone authorization system.

In Swiftâs proxy-server.conf add this keystoneauth middleware and the
authtoken middleware to your pipeline. Make sure you have the authtoken
middleware before the keystoneauth middleware.

The authtoken middleware will take care of validating the user and
keystoneauth will authorize access.

The sample proxy-server.conf shows a sample pipeline that uses keystone.

proxy-server.conf-sample

The authtoken middleware is shipped with keystonemiddleware - it
does not have any other dependencies than itself so you can either
install it by copying the file directly in your python path or by
installing keystonemiddleware.

If support is required for unvalidated users (as with anonymous
access) or for formpost/staticweb/tempurl middleware, authtoken will
need to be configured with delay_auth_decision set to true.  See
the Keystone documentation for more detail on how to configure the
authtoken middleware.

In proxy-server.conf you will need to have the setting account
auto creation to true:

[ app : proxy - server ] account_autocreate = true

And add a swift authorization filter section, such as:

[ filter : keystoneauth ] use = egg : swift #keystoneauth operator_roles = admin , swiftoperator

The user who is able to give ACL / create Containers permissions
will be the user with a role listed in the operator_roles setting which by default includes the admin and the swiftoperator
roles.

The keystoneauth middleware maps a Keystone project/tenant to an account
in Swift by adding a prefix ( AUTH_ by default) to the tenant/project
id.. For example, if the project id is 1234 , the path is /v1/AUTH_1234 .

If you need to have a different reseller_prefix to be able to
mix different auth servers you can configure the option reseller_prefix in your keystoneauth entry like this:

reseller_prefix = NEWAUTH

Donât forget to also update the Keystone service endpoint configuration to
use NEWAUTH in the path.

It is possible to have several accounts associated with the same project.
This is done by listing several prefixes as shown in the following
example:

reseller_prefix = AUTH , SERVICE

This means that for project id â1234â, the paths â/v1/AUTH_1234â and
â/v1/SERVICE_1234â are associated with the project and are authorized
using roles that a user has with that project. The core use of this feature
is that it is possible to provide different rules for each account
prefix. The following parameters may be prefixed with the appropriate
prefix:

operator_roles service_roles

For backward compatibility, if either of these parameters is specified
without a prefix then it applies to all reseller_prefixes. Here is an
example, using two prefixes:

reseller_prefix = AUTH , SERVICE # The next three lines have identical effects (since the first applies # to both prefixes). operator_roles = admin , swiftoperator AUTH_operator_roles = admin , swiftoperator SERVICE_operator_roles = admin , swiftoperator # The next line only applies to accounts with the SERVICE prefix SERVICE_operator_roles = admin , some_other_role

X-Service-Token tokens are supported by the inclusion of the service_roles
configuration option. When present, this option requires that the
X-Service-Token header supply a token from a user who has a role listed
in service_roles. Here is an example configuration:

reseller_prefix = AUTH , SERVICE AUTH_operator_roles = admin , swiftoperator SERVICE_operator_roles = admin , swiftoperator SERVICE_service_roles = service

The keystoneauth middleware supports cross-tenant access control using the
syntax <tenant>:<user> to specify a grantee in container Access Control
Lists (ACLs). For a request to be granted by an ACL, the grantee <tenant> must match the UUID of the tenant to which the request
X-Auth-Token is scoped and the grantee <user> must match the UUID of
the user authenticated by that token.

Note that names must no longer be used in cross-tenant ACLs because with
the introduction of domains in keystone names are no longer globally
unique.

For backwards compatibility, ACLs using names will be granted by
keystoneauth when it can be established that the grantee tenant,
the grantee user and the tenant being accessed are either not yet in a
domain (e.g. the X-Auth-Token has been obtained via the keystone v2
API) or are all in the default domain to which legacy accounts would
have been migrated. The default domain is identified by its UUID,
which by default has the value default . This can be changed by
setting the default_domain_id option in the keystoneauth
configuration:

default_domain_id = default

The backwards compatible behavior can be disabled by setting the config
option allow_names_in_acls to false:

allow_names_in_acls = false

To enable this backwards compatibility, keystoneauth will attempt to
determine the domain id of a tenant when any new account is created,
and persist this as account metadata. If an account is created for a tenant
using a token with reselleradmin role that is not scoped on that tenant,
keystoneauth is unable to determine the domain id of the tenant;
keystoneauth will assume that the tenant may not be in the default domain
and therefore not match names in ACLs for that account.

By default, middleware higher in the WSGI pipeline may override auth
processing, useful for middleware such as tempurl and formpost. If you know
youâre not going to use such middleware and you want a bit of extra
security you can disable this behaviour by setting the allow_overrides option to false :

allow_overrides = false

- app â The next WSGI app in the pipeline

app â The next WSGI app in the pipeline

- conf â The dict of configuration values

conf â The dict of configuration values

Authorize an anonymous request.

None if authorization is granted, an error page otherwise.

Deny WSGI Response.

Returns a standard WSGI response callable with the status of 403 or 401
depending on whether the REMOTE_USER is set or not.

Returns a WSGI filter app for use with paste.deploy.

## List Endpoints Â¶

List endpoints for an object, account or container.

This middleware makes it possible to integrate swift with software
that relies on data locality information to avoid network overhead,
such as Hadoop.

Using the original API, answers requests of the form:

/ endpoints / { account } / { container } / { object } / endpoints / { account } / { container } / endpoints / { account } / endpoints / v1 / { account } / { container } / { object } / endpoints / v1 / { account } / { container } / endpoints / v1 / { account }

with a JSON-encoded list of endpoints of the form:

http : // { server }:{ port } / { dev } / { part } / { acc } / { cont } / { obj } http : // { server }:{ port } / { dev } / { part } / { acc } / { cont } http : // { server }:{ port } / { dev } / { part } / { acc }

correspondingly, e.g.:

http : // 10.1.1.1 : 6200 / sda1 / 2 / a / c2 / o1 http : // 10.1.1.1 : 6200 / sda1 / 2 / a / c2 http : // 10.1.1.1 : 6200 / sda1 / 2 / a

Using the v2 API, answers requests of the form:

/ endpoints / v2 / { account } / { container } / { object } / endpoints / v2 / { account } / { container } / endpoints / v2 / { account }

with a JSON-encoded dictionary containing a key âendpointsâ that maps to a list
of endpoints having the same form as described above, and a key âheadersâ that
maps to a dictionary of headers that should be sent with a request made to
the endpoints, e.g.:

{ "endpoints" : { "http://10.1.1.1:6210/sda1/2/a/c3/o1" , "http://10.1.1.1:6230/sda3/2/a/c3/o1" , "http://10.1.1.1:6240/sda4/2/a/c3/o1" }, "headers" : { "X-Backend-Storage-Policy-Index" : "1" }}

In this example, the âheadersâ dictionary indicates that requests to the
endpoint URLs should include the header âX-Backend-Storage-Policy-Index: 1â
because the objectâs container is using storage policy index 1.

The â/endpoints/â path is customizable (âlist_endpoints_pathâ
configuration parameter).

Intended for consumption by third-party services living inside the
cluster (as the endpoints make sense only inside the cluster behind
the firewall); potentially written in a different language.

This is why itâs provided as a REST API and not just a Python API:
to avoid requiring clients to write their own ring parsers in their
languages, and to avoid the necessity to distribute the ring file
to clients and keep it up-to-date.

Note that the call is not authenticated, which means that a proxy
with this middleware enabled should not be open to an untrusted
environment (everyone can query the locality data using this middleware).

Bases: object

List endpoints for an object, account or container.

See above for a full description.

Uses configuration parameter swift_dir (default /etc/swift ).

- app â The next WSGI filter or app in the paste.deploy
chain.

app â The next WSGI filter or app in the paste.deploy
chain.

- conf â The configuration dict for the middleware.

conf â The configuration dict for the middleware.

Get the ring object to use to handle a request based on its policy.

policy index as defined in swift.conf

appropriate ring object

## Memcache Â¶

Bases: object

Caching middleware that manages caching in swift.

## Name Check (Forbidden Character Filter) Â¶

Created on February 27, 2012

A filter that disallows any paths that contain defined forbidden characters or
that exceed a defined length.

Place early in the proxy-server pipeline after the left-most occurrence of the proxy-logging middleware (if present) and before the final proxy-logging middleware (if present) or the proxy-serer app itself,
e.g.:

[ pipeline : main ] pipeline = catch_errors healthcheck proxy - logging name_check cache ratelimit tempauth sos proxy - logging proxy - server [ filter : name_check ] use = egg : swift #name_check forbidden_chars = '"`<> maximum_length = 255

There are default settings for forbidden_chars (FORBIDDEN_CHARS) and
maximum_length (MAX_LENGTH)

The filter returns HTTPBadRequest if path is invalid.

@author: eamonn-otoole

## Object Versioning Â¶

Object versioning in Swift has 3 different modes. There are two legacy modes that have similar API with a slight
difference in behavior and this middleware introduces a new mode with a
completely redesigned API and implementation.

In terms of the implementation, this middleware relies heavily on the use of
static links to reduce the amount of backend data movement that was part of the
two legacy modes. It also introduces a new API for enabling the feature and to
interact with older versions of an object.

### Compatibility between modes Â¶

This new mode is not backwards compatible or interchangeable with the
two legacy modes. This means that existing containers that are being versioned
by the two legacy modes cannot enable the new mode. The new mode can only be
enabled on a new container or a container without either X-Versions-Location or X-History-Location header set. Attempting to
enable the new mode on a container with either header will result in a 400 Bad Request response.

### Enable Object Versioning in a Container Â¶

After the introduction of this feature containers in a Swift cluster will be
in one of either 3 possible states: 1. Object versioning never enabled,
2. Object Versioning Enabled or 3. Object Versioning Disabled. Once versioning
has been enabled on a container, it will always have a flag stating whether it
is either enabled or disabled.

Clients enable object versioning on a container by performing either a PUT or
POST request with the header X-Versions-Enabled: true . Upon enabling the
versioning for the first time, the middleware will create a hidden container
where object versions are stored. This hidden container will inherit the same
Storage Policy as its parent container.

To disable, clients send a POST request with the header X-Versions-Enabled: false . When versioning is disabled, the old versions
remain unchanged.

To delete a versioned container, versioning must be disabled and all versions
of all objects must be deleted before the container can be deleted. At such
time, the hidden container will also be deleted.

### Object CRUD Operations to a Versioned Container Â¶

When data is PUT into a versioned container (a container with the
versioning flag enabled), the actual object is written to a hidden container
and a symlink object is written to the parent container. Every object is
assigned a version id. This id can be retrieved from the X-Object-Version-Id header in the PUT response.

Note

When object versioning is disabled on a container, new data will no longer
be versioned, but older versions remain untouched. Any new data PUT will result in a object with a null version-id. The versioning API can
be used to both list and operate on previous versions even while versioning
is disabled.

If versioning is re-enabled and an overwrite occurs on a null id object.
The object will be versioned off with a regular version-id.

A GET to a versioned object will return the current version of the object.
The X-Object-Version-Id header is also returned in the response.

A POST to a versioned object will update the most current object metadata
as normal, but will not create a new version of the object. In other words,
new versions are only created when the content of the object changes.

On DELETE , the middleware will write a zero-byte âdelete markerâ object
version that notes when the delete took place. The symlink object will also
be deleted from the versioned container. The object will no longer appear in
container listings for the versioned container and future requests there will
return 404 Not Found . However, the previous versions content will still be
recoverable.

### Object Versioning API Â¶

Clients can now operate on previous versions of an object using this new
versioning API.

First to list previous versions, issue a a GET request to the versioned
container with query parameter:

?versions

To list a container with a large number of object versions, clients can
also use the version_marker parameter together with the marker parameter.  While the marker parameter is used to specify an object name
the version_marker will be used specify the version id.

All other pagination parameters can be used in conjunction with the versions parameter.

During container listings, delete markers can be identified with the
content-type application/x-deleted;swift_versions_deleted=1 . The most
current version of an object can be identified by the field is_latest .

To operate on previous versions, clients can use the query parameter:

?version-id=<id>

where the <id> is the value from the X-Object-Version-Id header.

Only COPY, HEAD, GET and DELETE operations can be performed on previous
versions. Either a PUT or POST request with a version-id parameter will
result in a 400 Bad Request response.

A HEAD/GET request to a delete-marker will result in a 404 Not Found response.

When issuing DELETE requests with a version-id parameter, delete markers
are not written down. A DELETE request with a version-id parameter to
the current object will result in a both the symlink and the backing data
being deleted. A DELETE to any other version will result in that version only
be deleted and no changes made to the symlink pointing to the current version.

### How to Enable Object Versioning in a Swift Cluster Â¶

To enable this new mode in a Swift cluster the versioned_writes and symlink middlewares must be added to the proxy pipeline, you must also set
the option allow_object_versioning to True .

Bases: ObjectVersioningContext

Bases: object

Counts bytes read from file_like so we know how big the object is that
the client just PUT.

This is particularly important when the client sends a chunk-encoded body,
so we donât have a Content-Length header available.

Bases: ObjectVersioningContext

Handle request to delete a userâs container.

As part of deleting a container, this middleware will also delete
the hidden container holding object versions.

Before a userâs container can be deleted, swift must check
if there are still old object versions from that container.
Only after disabling versioning and deleting all object versions
can a container be deleted.

Handle request for container resource.

On PUT, POST set version location and enabled flag sysmeta.
For container listings of a versioned container, update the objectâs
bytes and etag to use the targetâs instead of using the symlink info.

Bases: ObjectVersioningContext

Handle DELETE requests.

Copy current version of object to versions_container and write a
delete marker before proceeding with original request.

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- api_version â api version.

api_version â api version.

- account_name â account name.

account_name â account name.

- object_name â name of object of original request

object_name â name of object of original request

Handle a POST request to an object in a versioned container.

If the response is a 307 because the POST went to a symlink,
follow the symlink and send the request to the versioned object

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- account â account name.

account â account name.

Check if the current version of the object is a versions-symlink
if not, itâs because this object was added to the container when
versioning was not enabled. Weâll need to copy it into the versions
containers now that versioning is enabled.

Also, put the new data from the client into the versions container
and add a static symlink in the versioned container.

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- api_version â api version.

api_version â api version.

- account_name â account name.

account_name â account name.

- object_name â name of object of original request

object_name â name of object of original request

Handle a PUT?version-id request and create/update the is_latest link to
point to the specific version. Expects a valid âversionâ id.

Handle âversion-idâ request for object resource. When a request
contains a version-id=<id> parameter, the request is acted upon
the actual version of that object. Version-aware operations
require that the container is versioned, but do not require that
the versioning is currently enabled. Users should be able to
operate on older versions of an object even if versioning is
currently suspended.

PUT and POST requests are not allowed as that would overwrite
the contents of the versioned object.

- req â The original request

req â The original request

- versions_cont â container holding versions of the requested obj

versions_cont â container holding versions of the requested obj

- api_version â should be v1 unless swift bumps api version

api_version â should be v1 unless swift bumps api version

- account â account name string

account â account name string

- container â container name string

container â container name string

- object â object name string

object â object name string

- is_enabled â is versioning currently enabled

is_enabled â is versioning currently enabled

- version â version of the object to act on

version â version of the object to act on

Bases: WSGIContext

Convert a timestamp value to a version string. The offset of the timestamp
is ignored.

timestamp â timestamp value to convert. Can be a string or instance
of BaseTimestamp.

version string.

## Proxy Logging Â¶

Logging middleware for the Swift proxy.

This serves as both the default logging implementation and an example of how
to plug in your own logging format/method.

The logging format implemented below is as follows:

client_ip remote_addr end_time . datetime method path protocol status_int referer user_agent auth_token bytes_recvd bytes_sent client_etag transaction_id headers request_time source log_info start_time end_time policy_index

These values are space-separated, and each is url-encoded, so that they can
be separated with a simple .split() .

- remote_addr is the contents of the REMOTE_ADDR environment variable,
while client_ip is swiftâs best guess at the end-user IP, extracted
variously from the X-Forwarded-For header, X-Cluster-Ip header, or the
REMOTE_ADDR environment variable.

remote_addr is the contents of the REMOTE_ADDR environment variable,
while client_ip is swiftâs best guess at the end-user IP, extracted
variously from the X-Forwarded-For header, X-Cluster-Ip header, or the
REMOTE_ADDR environment variable.

- status_int is the integer part of the status string passed to this
middlewareâs start_response function, unless the WSGI environment has an item
with key swift.proxy_logging_status , in which case the value of that item
is used. Other middlewareâs may set swift.proxy_logging_status to
override the logging of status_int . In either case, the logged status_int value is forced to 499 if a client disconnect is detected
while this middleware is handling a request, or 500 if an exception is caught
while handling a request.

status_int is the integer part of the status string passed to this
middlewareâs start_response function, unless the WSGI environment has an item
with key swift.proxy_logging_status , in which case the value of that item
is used. Other middlewareâs may set swift.proxy_logging_status to
override the logging of status_int . In either case, the logged status_int value is forced to 499 if a client disconnect is detected
while this middleware is handling a request, or 500 if an exception is caught
while handling a request.

- source ( swift.source in the WSGI environment) indicates the code
that generated the request, such as most middleware. (See below for
more detail.)

source ( swift.source in the WSGI environment) indicates the code
that generated the request, such as most middleware. (See below for
more detail.)

- log_info ( swift.log_info in the WSGI environment) is for additional
information that could prove quite useful, such as any x-delete-at value or other âbehind the scenesâ activity that might not
otherwise be detectable from the plain log information. Code that
wishes to add additional log information should use code like env.setdefault('swift.log_info', []).append(your_info) so as to
not disturb othersâ log information.

log_info ( swift.log_info in the WSGI environment) is for additional
information that could prove quite useful, such as any x-delete-at value or other âbehind the scenesâ activity that might not
otherwise be detectable from the plain log information. Code that
wishes to add additional log information should use code like env.setdefault('swift.log_info', []).append(your_info) so as to
not disturb othersâ log information.

- Values that are missing (e.g. due to a header not being present) or zero
are generally represented by a single hyphen (â-â).

Values that are missing (e.g. due to a header not being present) or zero
are generally represented by a single hyphen (â-â).

Note

The message format may be configured using the log_msg_template option,
allowing fields to be added, removed, re-ordered, and even anonymized. For
more information, see https://docs.openstack.org/swift/latest/logs.html

The proxy-logging can be used twice in the proxy serverâs pipeline when there
is middleware installed that can return custom responses that donât follow the
standard pipeline to the proxy server.

For example, with staticweb, the middleware might intercept a request to
/v1/AUTH_acc/cont/, make a subrequest to the proxy to retrieve
/v1/AUTH_acc/cont/index.html and, in effect, respond to the clientâs original
request using the 2nd requestâs body. In this instance the subrequest will be
logged by the rightmost middleware (with a swift.source set) and the
outgoing request (with body overridden) will be logged by leftmost middleware.

Requests that follow the normal pipeline (use the same wsgi environment
throughout) will not be double logged because an environment variable
( swift.proxy_access_log_made ) is checked/set when a log is made.

All middleware making subrequests should take care to set swift.source when
needed. With the doubled proxy logs, any consumer/processor of swiftâs proxy
logs should look at the swift.source field, the rightmost log value, to
decide if this is a middleware subrequest or not. A log processor calculating
bandwidth usage will want to only sum up logs with no swift.source .

Bases: InputProxy

- wsgi_input â file-like object to be wrapped

wsgi_input â file-like object to be wrapped

- callback â a function or a callable that
accept args (chunk, eof),
and returns chunk or a modified chunk.
eof is True if there are no more bytes to
read from the wrapped input, False otherwise.

callback â a function or a callable that
accept args (chunk, eof),
and returns chunk or a modified chunk.
eof is True if there are no more bytes to
read from the wrapped input, False otherwise.

Called each time a chunk of bytes is read from the wrapped input.

- chunk â the chunk of bytes that has been read.

chunk â the chunk of bytes that has been read.

- eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

eof â True if there are no more bytes to read from the
wrapped input, False otherwise. If read() has been called
this will be True when the size of chunk is less than the
requested size or the requested size is None. If readline has
been called this will be True when an incomplete line is read
(i.e. not ending with b'\n' ) whose length is less than the
requested size or the requested size is None. If read() or readline() are called with a requested size that exactly
matches the number of bytes remaining in the wrapped input then eof will be False . A subsequent call to read() or readline() with non-zero size would result in eof being True . Alternatively, the end of the input could be inferred
by comparing bytes_received with the expected length of the
input.

Bases: object

Middleware that logs Swift proxy requests in the swift log format.

Get access user ID from request environ.

req â swob.Request object for the request

User ID for logging if available, None otherwise

Log a request.

- req â swob.Request object for the request

req â swob.Request object for the request

- status_int â integer code for the response status

status_int â integer code for the response status

- bytes_received â bytes successfully read from the request body

bytes_received â bytes successfully read from the request body

- bytes_sent â bytes yielded to the WSGI server

bytes_sent â bytes yielded to the WSGI server

- start_time â timestamp request started

start_time â timestamp request started

- end_time â timestamp request completed

end_time â timestamp request completed

- resp_headers â dict of the response headers

resp_headers â dict of the response headers

- ttfb â time to first byte

ttfb â time to first byte

- wire_status_int â the on the wire status int

wire_status_int â the on the wire status int

## Ratelimit Â¶

Bases: Exception

Bases: object

Rate limiting middleware

Rate limits requests on both an Account and Container level.  Limits are
configurable.

Returns a list of key (used in memcache), ratelimit tuples. Keys
should be checked in order.

- req â swob request

req â swob request

- account_name â account name from path

account_name â account name from path

- container_name â container name from path

container_name â container name from path

- obj_name â object name from path

obj_name â object name from path

- global_ratelimit â this account has an account wide
ratelimit on all writes combined

global_ratelimit â this account has an account wide
ratelimit on all writes combined

Performs rate limiting and account white/black listing.  Sleeps
if necessary. If self.memcache_client is not set, immediately returns
None.

- account_name â account name from path

account_name â account name from path

- container_name â container name from path

container_name â container name from path

- obj_name â object name from path

obj_name â object name from path

paste.deploy app factory for creating WSGI proxy apps.

Returns number of requests allowed per second for given size.

Parses general parms for rate limits looking for things that
start with the provided name_prefix within the provided conf
and returns lists for both internal use and for /info

- conf â conf dict to parse

conf â conf dict to parse

- name_prefix â prefix of config parms to look for

name_prefix â prefix of config parms to look for

- info â set to return extra stuff for /info registration

info â set to return extra stuff for /info registration

## Read Only Â¶

Bases: object

Middleware that make an entire cluster or individual accounts read only.

Check whether an account should be read-only.

This considers both the cluster-wide config value as well as the
per-account override in X-Account-Sysmeta-Read-Only.

paste.deploy app factory for creating WSGI proxy apps.

## Recon Â¶

Bases: object

Recon middleware used for monitoring.

/recon/load|mem|asyncâ¦ will return various system metrics.

Needs to be added to the pipeline and requires a filter
declaration in the [account|container|object]-server conf file:

[filter:recon]
use = egg:swift#recon
recon_cache_path = /var/cache/swift

get # of async pendings

get auditor info

get devices

get disk utilization statistics

get # of drive audit errors

get expirer info

get info from /proc/loadavg

get info from /proc/meminfo

get ALL mounted fs from /proc/mounts

get obj/container/account quarantine counts

get reconstruction info

get relinker info, if any

get replication info

get all ring md5sumâs

get sharding info

get info from /proc/net/sockstat and sockstat6

Note: The mem value is actually kernel pages, but we return bytes
allocated based on the systems page size.

get md5 of swift.conf

get current time

list unmounted (failed?) devices

get updater info

get swift version

## Server Side Copy Â¶

Server side copy is a feature that enables users/clients to COPY objects
between accounts and containers without the need to download and then
re-upload objects, thus eliminating additional bandwidth consumption and
also saving time. This may be used when renaming/moving an object which
in Swift is a (COPY + DELETE) operation.

The server side copy middleware should be inserted in the pipeline after auth
and before the quotas and large object middlewares. If it is not present in the
pipeline in the proxy-server configuration file, it will be inserted
automatically. There is no configurable option provided to turn off server
side copy.

### Metadata Â¶

- All metadata of source object is preserved during object copy.

All metadata of source object is preserved during object copy.

- One can also provide additional metadata during PUT/COPY request. This will
over-write any existing conflicting keys.

One can also provide additional metadata during PUT/COPY request. This will
over-write any existing conflicting keys.

- Server side copy can also be used to change content-type of an existing
object.

Server side copy can also be used to change content-type of an existing
object.

### Object Copy Â¶

- The destination container must exist before requesting copy of the object.

The destination container must exist before requesting copy of the object.

- When several replicas exist, the system copies from the most recent replica.
That is, the copy operation behaves as though the X-Newest header is in the
request.

When several replicas exist, the system copies from the most recent replica.
That is, the copy operation behaves as though the X-Newest header is in the
request.

- The request to copy an object should have no body (i.e. content-length of the
request must be zero).

The request to copy an object should have no body (i.e. content-length of the
request must be zero).

There are two ways in which an object can be copied:

- Send a PUT request to the new object (destination/target) with an additional
header named X-Copy-From specifying the source object
(in â/container/objectâ format). Example: curl - i - X PUT http : //< storage_url >/ container1 / destination_obj - H 'X-Auth-Token: <token>' - H 'X-Copy-From: /container2/source_obj' - H 'Content-Length: 0'

Send a PUT request to the new object (destination/target) with an additional
header named X-Copy-From specifying the source object
(in â/container/objectâ format). Example:

curl - i - X PUT http : //< storage_url >/ container1 / destination_obj - H 'X-Auth-Token: <token>' - H 'X-Copy-From: /container2/source_obj' - H 'Content-Length: 0'

- Send a COPY request with an existing object in URL with an additional header
named Destination specifying the destination/target object
(in â/container/objectâ format). Example: curl - i - X COPY http : //< storage_url >/ container2 / source_obj - H 'X-Auth-Token: <token>' - H 'Destination: /container1/destination_obj' - H 'Content-Length: 0'

Send a COPY request with an existing object in URL with an additional header
named Destination specifying the destination/target object
(in â/container/objectâ format). Example:

curl - i - X COPY http : //< storage_url >/ container2 / source_obj - H 'X-Auth-Token: <token>' - H 'Destination: /container1/destination_obj' - H 'Content-Length: 0'

Note that if the incoming request has some conditional headers (e.g. Range , If-Match ), the source object will be evaluated for these headers (i.e. if
PUT with both X-Copy-From and Range , Swift will make a partial copy to
the destination object).

### Cross Account Object Copy Â¶

Objects can also be copied from one account to another account if the user
has the necessary permissions (i.e. permission to read from container
in source account and permission to write to container in destination account).

Similar to examples mentioned above, there are two ways to copy objects across
accounts:

- Like the example above, send PUT request to copy object but with an
additional header named X-Copy-From-Account specifying the source
account. Example: curl - i - X PUT http : //< host > : < port >/ v1 / AUTH_test1 / container / destination_obj - H 'X-Auth-Token: <token>' - H 'X-Copy-From: /container/source_obj' - H 'X-Copy-From-Account: AUTH_test2' - H 'Content-Length: 0'

Like the example above, send PUT request to copy object but with an
additional header named X-Copy-From-Account specifying the source
account. Example:

curl - i - X PUT http : //< host > : < port >/ v1 / AUTH_test1 / container / destination_obj - H 'X-Auth-Token: <token>' - H 'X-Copy-From: /container/source_obj' - H 'X-Copy-From-Account: AUTH_test2' - H 'Content-Length: 0'

- Like the previous example, send a COPY request but with an additional header
named Destination-Account specifying the name of destination account.
Example: curl - i - X COPY http : //< host > : < port >/ v1 / AUTH_test2 / container / source_obj - H 'X-Auth-Token: <token>' - H 'Destination: /container/destination_obj' - H 'Destination-Account: AUTH_test1' - H 'Content-Length: 0'

Like the previous example, send a COPY request but with an additional header
named Destination-Account specifying the name of destination account.
Example:

curl - i - X COPY http : //< host > : < port >/ v1 / AUTH_test2 / container / source_obj - H 'X-Auth-Token: <token>' - H 'Destination: /container/destination_obj' - H 'Destination-Account: AUTH_test1' - H 'Content-Length: 0'

### Large Object Copy Â¶

The best option to copy a large object is to copy segments individually.
To copy the manifest object of a large object, add the query parameter to
the copy request:

?multipart-manifest=get

If a request is sent without the query parameter, an attempt will be made to
copy the whole object but will fail if the object size is
greater than 5GB.

Bases: WSGIContext

## Static Large Objects Â¶

Please see
the SLO docs for Static Large Objects further details.

## StaticWeb Â¶

This StaticWeb WSGI middleware will serve container data as a static web site
with index file and error file resolution and optional file listings. This mode
is normally only active for anonymous requests. When using keystone for
authentication set delay_auth_decision = true in the authtoken middleware
configuration in your /etc/swift/proxy-server.conf file.  If you want to
use it with authenticated requests, set the X-Web-Mode: true header on the
request.

The staticweb filter should be added to the pipeline in your /etc/swift/proxy-server.conf file just after any auth middleware. Also, the
configuration section for the staticweb middleware itself needs to be
added. For example:

[ DEFAULT ] ... [ pipeline : main ] pipeline = catch_errors healthcheck proxy - logging cache ratelimit tempauth staticweb proxy - logging proxy - server ... [ filter : staticweb ] use = egg : swift #staticweb

Any publicly readable containers (for example, X-Container-Read: .r:* , see ACLs for more information on this) will be checked for
X-Container-Meta-Web-Index and X-Container-Meta-Web-Error header values:

X - Container - Meta - Web - Index < index . name > X - Container - Meta - Web - Error < error . name . suffix >

If X-Container-Meta-Web-Index is set, any <index.name> files will be served
without having to specify the <index.name> part. For instance, setting X-Container-Meta-Web-Index: index.html will be able to serve the object
â¦/pseudo/path/index.html with just â¦/pseudo/path or â¦/pseudo/path/

If X-Container-Meta-Web-Error is set, any errors (currently just 401
Unauthorized and 404 Not Found) will instead serve the
â¦/<status.code><error.name.suffix> object. For instance, setting X-Container-Meta-Web-Error: error.html will serve â¦/404error.html for
requests for paths not found.

For pseudo paths that have no <index.name>, this middleware can serve HTML file
listings if you set the X-Container-Meta-Web-Listings: true metadata item
on the container. Note that the listing must be authorized; you may want a
container ACL like X-Container-Read: .r:*,.rlistings .

If listings are enabled, the listings can have a custom style sheet by setting
the X-Container-Meta-Web-Listings-CSS header. For instance, setting X-Container-Meta-Web-Listings-CSS: listing.css will make listings link to
the â¦/listing.css style sheet. If you âview sourceâ in your browser on a
listing page, you will see the well defined document structure that can be
styled.

Additionally, prefix-based TempURL parameters may be used to authorize
requests instead of making the whole container publicly readable. This gives
clients dynamic discoverability of the objects available within that prefix.

Note

temp_url_prefix values should typically end with a slash ( / ) when
used with StaticWeb. StaticWebâs redirects will not carry over any TempURL
parameters, as they likely indicate that the user created an overly-broad
TempURL.

By default, the listings will be rendered with a label of
âListing of /v1/account/container/pathâ.  This can be altered by
setting a X-Container-Meta-Web-Listings-Label: <label> .  For example,
if the label is set to âexample.comâ, a label of
âListing of example.com/pathâ will be used instead.

The content-type of directory marker objects can be modified by setting
the X-Container-Meta-Web-Directory-Type header.  If the header is not set,
application/directory is used by default.  Directory marker objects are
0-byte objects that represent directories to create a simulated hierarchical
structure.

Example usage of this middleware via swift :

Make the container publicly readable:

swift post - r '.r:*' container

You should be able to get objects directly, but no index.html resolution or
listings.

Set an index file directive:

swift post - m 'web-index:index.html' container

You should be able to hit paths that have an index.html without needing to
type the index.html part.

Turn on listings:

swift post - r '.r:*,.rlistings' container swift post - m 'web-listings: true' container

Now you should see object listings for paths and pseudo paths that have no
index.html.

Enable a custom listings style sheet:

swift post - m 'web-listings-css:listings.css' container

Set an error file:

swift post - m 'web-error:error.html' container

Now 401âs should load 401error.html, 404âs should load 404error.html, etc.

Set Content-Type of directory marker object:

swift post - m 'web-directory-type:text/directory' container

Now 0-byte objects with a content-type of text/directory will be treated
as directories rather than objects.

Bases: object

The Static Web WSGI middleware filter; serves container data as a static
web site. See staticweb for an overview.

The proxy logs created for any subrequests made will have swift.source set
to âSWâ.

- app â The next WSGI application/filter in the paste.deploy pipeline.

app â The next WSGI application/filter in the paste.deploy pipeline.

- conf â The filter configuration dict.

conf â The filter configuration dict.

The next WSGI application/filter in the paste.deploy pipeline.

The filter configuration dict. Only used in tests.

Returns a Static Web WSGI filter for use with paste.deploy.

## Symlink Â¶

Symlink Middleware

Symlinks are objects stored in Swift that contain a reference to another
object (hereinafter, this is called âtarget objectâ). They are analogous to
symbolic links in Unix-like operating systems. The existence of a symlink
object does not affect the target object in any way. An important use case is
to use a path in one container to access an object in a different container,
with a different policy. This allows policy cost/performance trade-offs to be
made on individual objects.

Clients create a Swift symlink by performing a zero-length PUT request
with the header X-Symlink-Target: <container>/<object> . For a cross-account
symlink, the header X-Symlink-Target-Account: <account> must be included.
If omitted, it is inserted automatically with the account of the symlink
object in the PUT request process.

Symlinks must be zero-byte objects. Attempting to PUT a symlink with a
non-empty request body will result in a 400-series error. Also, POST with X-Symlink-Target header always results in a 400-series error. The target
object need not exist at symlink creation time.

Clients may optionally include a X-Symlink-Target-Etag: <etag> header
during the PUT. If present, this will create a âstatic symlinkâ instead of a
âdynamic symlinkâ.  Static symlinks point to a specific object rather than a
specific name.  They do this by using the value set in their X-Symlink-Target-Etag header when created to verify it still matches the
ETag of the object theyâre pointing at on a GET.  In contrast to a dynamic
symlink the target object referenced in the X-Symlink-Target header must
exist and its ETag must match the X-Symlink-Target-Etag or the symlink
creation will return a client error.

A GET/HEAD request to a symlink will result in a request to the target
object referenced by the symlinkâs X-Symlink-Target-Account and X-Symlink-Target headers. The response of the GET/HEAD request will contain
a Content-Location header with the path location of the target object. A
GET/HEAD request to a symlink with the query parameter ?symlink=get will
result in the request targeting the symlink itself.

A symlink can point to another symlink. Chained symlinks will be traversed
until the target is not a symlink. If the number of chained symlinks exceeds
the limit symloop_max an error response will be produced. The value of symloop_max can be defined in the symlink config section of proxy-server.conf . If not specified, the default symloop_max value is 2.
If a value less than 1 is specified, the default value will be used.

If a static symlink (i.e. a symlink created with a X-Symlink-Target-Etag header) targets another static symlink, both of the X-Symlink-Target-Etag headers must match the target object for the GET to succeed.  If a static
symlink targets a dynamic symlink (i.e. a symlink created without a X-Symlink-Target-Etag header) then the X-Symlink-Target-Etag header of
the static symlink must be the Etag of the zero-byte object.  If a symlink with
a X-Symlink-Target-Etag targets a large object manifest it must match the
ETag of the manifest (e.g. the ETag as returned by multipart-manifest=get or value in the X-Manifest-Etag header).

A HEAD/GET request to a symlink object behaves as a normal HEAD/GET request
to the target object. Therefore issuing a HEAD request to the symlink will
return the target metadata, and issuing a GET request to the symlink will
return the data and metadata of the target object. To return the symlink
metadata (with its empty body) a GET/HEAD request with the ?symlink=get query parameter must be sent to a symlink object.

A POST request to a symlink will result in a 307 Temporary Redirect response.
The response will contain a Location header with the path of the target
object as the value. The request is never redirected to the target object by
Swift. Nevertheless, the metadata in the POST request will be applied to the
symlink because object servers cannot know for sure if the current object is a
symlink or not in eventual consistency.

A symlinkâs Content-Type is completely independent from its target.  As a
convenience Swift will automatically set the Content-Type on a symlink PUT
if not explicitly set by the client.  If the client sends a X-Symlink-Target-Etag Swift will set the symlinkâs Content-Type to that
of the target, otherwise it will be set to application/symlink .  You can
review a symlinkâs Content-Type using the ?symlink=get interface.  You
can change a symlinkâs Content-Type using a POST request.  The symlinkâs Content-Type will appear in the container listing.

A DELETE request to a symlink will delete the symlink itself. The target
object will not be deleted.

A COPY request, or a PUT request with a X-Copy-From header, to a symlink
will copy the target object. The same request to a symlink with the query
parameter ?symlink=get will copy the symlink itself.

An OPTIONS request to a symlink will respond with the options for the symlink
only; the request will not be redirected to the target object. Please note that
if the symlinkâs target object is in another container with CORS settings, the
response will not reflect the settings.

Tempurls can be used to GET/HEAD symlink objects, but PUT is not allowed and
will result in a 400-series error. The GET/HEAD tempurls honor the scope of
the tempurl key. Container tempurl will only work on symlinks where the target
container is the same as the symlink. In case a symlink targets an object
in a different container, a GET/HEAD request will result in a 401 Unauthorized
error. The account level tempurl will allow cross-container symlinks, but not
cross-account symlinks.

If a symlink object is overwritten while it is in a versioned container, the
symlink object itself is versioned, not the referenced object.

A GET request with query parameter ?format=json to a container which
contains symlinks will respond with additional information symlink_path for each symlink object in the container listing. The symlink_path value
is the target path of the symlink. Clients can differentiate symlinks and
other objects by this function. Note that responses in any other format
(e.g. ?format=xml ) wonât include symlink_path info.  If a X-Symlink-Target-Etag header was included on the symlink, JSON container
listings will include that value in a symlink_etag key and the target
objectâs Content-Length will be included in the key symlink_bytes .

If a static symlink targets a static large object manifest it will carry
forward the SLOâs size and slo_etag in the container listing using the symlink_bytes and slo_etag keys.  However, manifests created before
swift v2.12.0 (released Dec 2016) do not contain enough metadata to propagate
the extra SLO information to the listing.  Clients may recreate the manifest
(COPY w/ ?multipart-manfiest=get ) before creating a static symlink to add
the requisite metadata.

Errors

- PUT with the header X-Symlink-Target with non-zero Content-Length
will produce a 400 BadRequest error.

PUT with the header X-Symlink-Target with non-zero Content-Length
will produce a 400 BadRequest error.

- POST with the header X-Symlink-Target will produce a
400 BadRequest error.

POST with the header X-Symlink-Target will produce a
400 BadRequest error.

- GET/HEAD traversing more than symloop_max chained symlinks will
produce a 409 Conflict error.

GET/HEAD traversing more than symloop_max chained symlinks will
produce a 409 Conflict error.

- PUT/GET/HEAD on a symlink that inclues a X-Symlink-Target-Etag header
that does not match the target will poduce a 409 Conflict error.

PUT/GET/HEAD on a symlink that inclues a X-Symlink-Target-Etag header
that does not match the target will poduce a 409 Conflict error.

- POSTs will produce a 307 Temporary Redirect error.

POSTs will produce a 307 Temporary Redirect error.

### Deployment Â¶

Symlinks are enabled by adding the symlink middleware to the proxy server
WSGI pipeline and including a corresponding filter configuration section in the proxy-server.conf file. The symlink middleware should be placed after slo , dlo and versioned_writes middleware, but before encryption middleware in the pipeline. See the proxy-server.conf-sample file for further
details. Additional steps are
required if the container sync feature is being used.

Note

Once you have deployed symlink middleware in your pipeline, you should
neither remove the symlink middleware nor downgrade swift to a version
earlier than symlinks being supported. Doing so may result in unexpected
container listing results in addition to symlink objects behaving like a
normal object.

#### Container sync configuration Â¶

If container sync is being used then the symlink middleware
must be added to the container sync internal client pipeline. The following
configuration steps are required:

- Create a custom internal client configuration file for container sync (if
one is not already in use) based on the sample file internal-client.conf-sample . For example, copy internal-client.conf-sample to /etc/swift/container-sync-client.conf .

Create a custom internal client configuration file for container sync (if
one is not already in use) based on the sample file internal-client.conf-sample . For example, copy internal-client.conf-sample to /etc/swift/container-sync-client.conf .

- Modify this file to include the symlink middleware in the pipeline in
the same way as described above for the proxy server.

Modify this file to include the symlink middleware in the pipeline in
the same way as described above for the proxy server.

- Modify the container-sync section of all container server config files to
point to this internal client config file using the internal_client_conf_path option. For example: internal_client_conf_path = / etc / swift / container - sync - client . conf

Modify the container-sync section of all container server config files to
point to this internal client config file using the internal_client_conf_path option. For example:

internal_client_conf_path = / etc / swift / container - sync - client . conf

Note

These container sync configuration steps will be necessary for container
sync probe tests to pass if the symlink middleware is included in the
proxy pipeline of a test cluster.

Bases: WSGIContext

Handle container requests.

- req â a Request

req â a Request

- start_response â start_response function

start_response â start_response function

Response Iterator after start_response called.

Bases: object

Middleware that implements symlinks.

Symlinks are objects stored in Swift that contain a reference to another
object (i.e., the target object). An important use case is to use a path in
one container to access an object in a different container, with a
different policy. This allows policy cost/performance trade-offs to be made
on individual objects.

Bases: WSGIContext

Handle get/head request and in case the response is a symlink,
redirect request to target object.

req â HTTP GET or HEAD object request

Response Iterator

Handle get/head request when client sent parameter ?symlink=get

req â HTTP GET or HEAD object request with param ?symlink=get

Response Iterator

Handle object requests.

- req â a Request

req â a Request

- start_response â start_response function

start_response â start_response function

Response Iterator after start_response has been called

Handle post request. If POSTing to a symlink, a HTTPTemporaryRedirect
error message is returned to client.

Clients that POST to symlinks should understand that the POST is not
redirected to the target object like in a HEAD/GET request. POSTs to a
symlink will be handled just like a normal object by the object server.
It cannot reject it because it may not have symlink state when the POST
lands.  The object server has no knowledge of what is a symlink object
is. On the other hand, on POST requests, the object server returns all
sysmeta of the object. This method uses that sysmeta to determine if
the stored object is a symlink or not.

req â HTTP POST object request

HTTPTemporaryRedirect if POSTing to a symlink.

Response Iterator

Handle put request when it contains X-Symlink-Target header.

Symlink headers are validated and moved to sysmeta namespace.
:param req: HTTP PUT object request
:returns: Response Iterator

Helper function to translate from cluster-facing
X-Object-Sysmeta-Symlink-* headers to client-facing X-Symlink-* headers.

headers â request headers dict. Note that the headers dict
will be updated directly.

Helper function to translate from client-facing X-Symlink-* headers
to cluster-facing X-Object-Sysmeta-Symlink-* headers.

headers â request headers dict. Note that the headers dict
will be updated directly.

## TempAuth Â¶

Test authentication and authorization system.

Add to your pipeline in proxy-server.conf, such as:

[ pipeline : main ] pipeline = catch_errors cache tempauth proxy - server

Set account auto creation to true in proxy-server.conf:

[ app : proxy - server ] account_autocreate = true

And add a tempauth filter section, such as:

[ filter : tempauth ] use = egg : swift #tempauth user_admin_admin = admin . admin . reseller_admin user_test_tester = testing . admin user_test2_tester2 = testing2 . admin user_test_tester3 = testing3 # To allow accounts/users with underscores you can base64 encode them. # Here is the account "under_score" and username "a_b" (note the lack # of padding equal signs): user64_dW5kZXJfc2NvcmU_YV9i = testing4

See the proxy-server.conf-sample for more information.

### Account/User List Â¶

All accounts/users are listed in the filter section. The format is:

user_ < account > _ < user > = < key > [ group ] [ group ] [ ... ] [ storage_url ]

If you want to be able to include underscores in the <account> or <user> portions, you can base64 encode them (with no equal signs)
in a line like this:

user64_ < account_b64 > _ < user_b64 > = < key > [ group ] [ ... ] [ storage_url ]

There are three special groups:

- .reseller_admin â can do anything to any account for this auth

.reseller_admin â can do anything to any account for this auth

- .reseller_reader â can GET/HEAD anything in any account for this auth

.reseller_reader â can GET/HEAD anything in any account for this auth

- .admin â can do anything within the account

.admin â can do anything within the account

If none of these groups are specified, the user can only access
containers that have been explicitly allowed for them by a .admin or .reseller_admin .

The trailing optional storage_url allows you to specify an alternate
URL to hand back to the user upon authentication. If not specified, this
defaults to:

$HOST/v1/<reseller_prefix>_<account>

Where $HOST will do its best to resolve to what the requester would
need to use to reach this host, <reseller_prefix> is from this section,
and <account> is from the user_<account>_<user> name. Note that $HOST cannot possibly handle when you have a load balancer in front of
it that does https while TempAuth itself runs with http; in such a case,
youâll have to specify the storage_url_scheme configuration value as
an override.

### Multiple Reseller Prefix Items Â¶

The reseller prefix specifies which parts of the account namespace this
middleware is responsible for managing authentication and authorization.
By default, the prefix is AUTH so accounts and tokens are prefixed
by AUTH_ . When a requestâs token and/or path start with AUTH_ , this
middleware knows it is responsible.

We allow the reseller prefix to be a list. In tempauth, the first item
in the list is used as the prefix for tokens and user groups. The
other prefixes provide alternate accounts that userâs can access. For
example if the reseller prefix list is AUTH, OTHER , a user with
admin access to AUTH_account also has admin access to OTHER_account .

### Required Group Â¶

The group .admin is normally needed to access an account (ACLs provide
an additional way to access an account). You can specify the require_group parameter. This means that you also need the named group
to access an account. If you have several reseller prefix items, prefix
the require_group parameter with the appropriate prefix.

### X-Service-Token Â¶

If an X-Service-Token is presented in the request headers, the groups
derived from the token are appended to the roles derived from X-Auth-Token . If X-Auth-Token is missing or invalid, X-Service-Token is not processed.

The X-Service-Token is useful when combined with multiple reseller
prefix items. In the following configuration, accounts prefixed SERVICE_ are only accessible if X-Auth-Token is from the end-user
and X-Service-Token is from the glance user:

[ filter : tempauth ] use = egg : swift #tempauth reseller_prefix = AUTH , SERVICE SERVICE_require_group = . service user_admin_admin = admin . admin . reseller_admin user_joeacct_joe = joepw . admin user_maryacct_mary = marypw . admin user_glance_glance = glancepw . service

The name .service is an example. Unlike .admin , .reseller_admin , .reseller_reader it is not a reserved name.

Please note that ACLs can be set on service accounts and are matched
against the identity validated by X-Auth-Token . As such ACLs can grant
access to a service accountâs container without needing to provide a
service token, just like any other cross-reseller request using ACLs.

### Account ACLs Â¶

If a swift_owner issues a POST or PUT to the account with the X-Account-Access-Control header set in the request, then this may
allow certain types of access for additional users.

- Read-Only: Users with read-only access can list containers in the
account, list objects in any container, retrieve objects, and view
unprivileged account/container/object metadata.

Read-Only: Users with read-only access can list containers in the
account, list objects in any container, retrieve objects, and view
unprivileged account/container/object metadata.

- Read-Write: Users with read-write access can (in addition to the
read-only privileges) create objects, overwrite existing objects,
create new containers, and set unprivileged container/object
metadata.

Read-Write: Users with read-write access can (in addition to the
read-only privileges) create objects, overwrite existing objects,
create new containers, and set unprivileged container/object
metadata.

- Admin: Users with admin access are swift_owners and can perform
any action, including viewing/setting privileged metadata (e.g.
changing account ACLs).

Admin: Users with admin access are swift_owners and can perform
any action, including viewing/setting privileged metadata (e.g.
changing account ACLs).

To generate headers for setting an account ACL:

from swift.common.middleware.acl import format_acl acl_data = { 'admin' : [ 'alice' ], 'read-write' : [ 'bob' , 'carol' ] } header_value = format_acl ( version = 2 , acl_dict = acl_data )

To generate a curl command line from the above:

token =... storage_url =... python - c ' from swift.common.middleware.acl import format_acl acl_data = { 'admin' : [ 'alice' ], 'read-write' : [ 'bob' , 'carol' ] } headers = { 'X-Account-Access-Control' : format_acl ( version = 2 , acl_dict = acl_data )} header_str = ' ' . join ([ "-H ' %s : %s '" % ( k , v ) for k , v in headers . items ()]) print ( 'curl -D- -X POST -H "x-auth-token: $token" %s ' '$storage_url' % header_str ) '

Bases: object

- app â The next WSGI app in the pipeline

app â The next WSGI app in the pipeline

- conf â The dict of configuration values from the Paste config file

conf â The dict of configuration values from the Paste config file

Return a dict of ACL data from the account server via get_account_info.

Auth systems may define their own format, serialization, structure,
and capabilities implemented in the ACL headers and persisted in the
sysmeta data.  However, auth systems are strongly encouraged to be
interoperable with Tempauth.

X-Account-Access-Control

- swift.common.middleware.acl.parse_acl()

swift.common.middleware.acl.parse_acl()

- swift.common.middleware.acl.format_acl()

swift.common.middleware.acl.format_acl()

Returns None if the request is authorized to continue or a standard
WSGI response callable if not.

Returns a standard WSGI response callable with the status of 403 or 401
depending on whether the REMOTE_USER is set or not.

Return a user-readable string indicating the errors in the input ACL,
or None if there are no errors.

Get groups for the given token.

- env â The current WSGI environment dictionary.

env â The current WSGI environment dictionary.

- token â Token to validate and return a group string for.

token â Token to validate and return a group string for.

None if the token is invalid or a string containing a comma
separated list of groups the authenticated user is a member
of. The first group in the list is also considered a unique
identifier for that user.

WSGI entry point for auth requests (ones that match the
self.auth_prefix).
Wraps env in swob.Request object and passes it down.

- env â WSGI environment dictionary

env â WSGI environment dictionary

- start_response â WSGI callable

start_response â WSGI callable

Handles the various request for token and service end point(s) calls.
There are various formats to support the various auth servers in the
past. Examples:

GET < auth - prefix >/ v1 /< act >/ auth X - Auth - User : < act > : < usr > or X - Storage - User : < usr > X - Auth - Key : < key > or X - Storage - Pass : < key > GET < auth - prefix >/ auth X - Auth - User : < act > : < usr > or X - Storage - User : < act > : < usr > X - Auth - Key : < key > or X - Storage - Pass : < key > GET < auth - prefix >/ v1 .0 X - Auth - User : < act > : < usr > or X - Storage - User : < act > : < usr > X - Auth - Key : < key > or X - Storage - Pass : < key >

On successful authentication, the response will have X-Auth-Token and
X-Storage-Token set to the token to use with Swift and X-Storage-URL
set to the URL to the default Swift cluster to use.

req â The swob.Request to process.

swob.Response, 2xx on success with data set as explained
above.

Entry point for auth requests (ones that match the self.auth_prefix).
Should return a WSGI-style callable (such as swob.Response).

req â swob.Request object

Returns a WSGI filter app for use with paste.deploy.

## TempURL Â¶

TempURL Middleware

Allows the creation of URLs to provide temporary access to objects.

For example, a website may wish to provide a link to download a large
object in Swift, but the Swift account has no public access. The
website can generate a URL that will provide GET access for a limited
time to the resource. When the web browser user clicks on the link,
the browser will download the object directly from Swift, obviating
the need for the website to act as a proxy for the request.

If the user were to share the link with all his friends, or
accidentally post it on a forum, etc. the direct access would be
limited to the expiration time set when the website created the link.

Beyond that, the middleware provides the ability to create URLs, which
contain signatures which are valid for all objects which share a
common prefix. These prefix-based URLs are useful for sharing a set
of objects.

Restrictions can also be placed on the ip that the resource is allowed
to be accessed from. This can be useful for locking down where the urls
can be used from.

### Client Usage Â¶

To create temporary URLs, first an X-Account-Meta-Temp-URL-Key header must be set on the Swift account. Then, an HMAC (RFC 2104)
signature is generated using the HTTP method to allow ( GET , PUT , DELETE , etc.), the Unix timestamp until which the access should be allowed,
the full path to the object, and the key set on the account.

The digest algorithm to be used may be configured by the operator. By default,
HMAC-SHA256 and HMAC-SHA512 are supported. Check the tempurl.allowed_digests entry in the clusterâs capabilities response to
see which algorithms are supported by your deployment; see Discoverability for more information. On older clusters,
the tempurl key may be present while the allowed_digests subkey
is not; in this case, only HMAC-SHA1 is supported.

For example, here is code generating the signature for a GET for 60
seconds on /v1/AUTH_account/container/object :

import hmac from hashlib import sha256 from time import time method = 'GET' expires = int ( time () + 60 ) path = '/v1/AUTH_account/container/object' key = 'mykey' hmac_body = ' %s \n %s \n %s ' % ( method , expires , path ) sig = hmac . new ( key , hmac_body , sha256 ) . hexdigest ()

Be certain to use the full path, from the /v1/ onward.

Letâs say sig ends up equaling 732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b and expires ends up 1512508563 . Then, for example, the website could
provide a link to:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563

For longer hashes, a hex encoding becomes unwieldy. Base64 encoding is also
supported, and indicated by prefixing the signature with "<digest name>:" .
This is required for HMAC-SHA512 signatures. For example, comparable code
for generating a HMAC-SHA512 signature would be:

import base64 import hmac from hashlib import sha512 from time import time method = 'GET' expires = int ( time () + 60 ) path = '/v1/AUTH_account/container/object' key = 'mykey' hmac_body = ' %s \n %s \n %s ' % ( method , expires , path ) sig = 'sha512:' + base64 . urlsafe_b64encode ( hmac . new ( key , hmac_body , sha512 ) . digest ())

Supposing that sig ends up equaling sha512:ZrSijn0GyDhsv1ltIj9hWUTrbAeE45NcKXyBaz7aPbSMvROQ4jtYH4nRAmm 5ErY2X11Yc1Yhy2OMCyN3yueeXg== and expires ends up 1516741234 , then the website could provide a link to:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=sha512:ZrSijn0GyDhsv1ltIj9hWUTrbAeE45NcKXyBaz7aPbSMvRO
Q4jtYH4nRAmm5ErY2X11Yc1Yhy2OMCyN3yueeXg==&
temp_url_expires=1516741234

You may also use ISO 8601 UTC timestamps with the format "%Y-%m-%dT%H:%M:%SZ" instead of UNIX timestamps in the URL
(but NOT in the code above for generating the signature!).
So, the above HMAC-SHA246 URL could also be formulated as:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=2017-12-05T21:16:03Z

If a prefix-based signature with the prefix pre is desired, set path to:

path = 'prefix:/v1/AUTH_account/container/pre'

The generated signature would be valid for all objects starting
with pre . The middleware detects a prefix-based temporary URL by
a query parameter called temp_url_prefix . So, if sig and expires would end up like above, following URL would be valid:

https://swift-cluster.example.com/v1/AUTH_account/container/pre/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563&
temp_url_prefix=pre

Another valid URL:

https://swift-cluster.example.com/v1/AUTH_account/container/pre/
subfolder/another_object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563&
temp_url_prefix=pre

If you wish to lock down the ip ranges from where the resource can be accessed
to the ip 1.2.3.4 :

import hmac from hashlib import sha256 from time import time method = 'GET' expires = int ( time () + 60 ) path = '/v1/AUTH_account/container/object' ip_range = '1.2.3.4' key = b 'mykey' hmac_body = 'ip= %s \n %s \n %s \n %s ' % ( ip_range , method , expires , path ) sig = hmac . new ( key , hmac_body . encode ( 'ascii' ), sha256 ) . hexdigest ()

The generated signature would only be valid from the ip 1.2.3.4 . The
middleware detects an ip-based temporary URL by a query parameter called temp_url_ip_range . So, if sig and expires would end up like
above, following URL would be valid:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=3f48476acaf5ec272acd8e99f7b5bad96c52ddba53ed27c60613711774a06f0c&
temp_url_expires=1648082711&
temp_url_ip_range=1.2.3.4

Similarly to lock down the ip to a range of 1.2.3.X so starting
from the ip 1.2.3.0 to 1.2.3.255 :

import hmac from hashlib import sha256 from time import time method = 'GET' expires = int ( time () + 60 ) path = '/v1/AUTH_account/container/object' ip_range = '1.2.3.0/24' key = b 'mykey' hmac_body = 'ip= %s \n %s \n %s \n %s ' % ( ip_range , method , expires , path ) sig = hmac . new ( key , hmac_body . encode ( 'ascii' ), sha256 ) . hexdigest ()

Then the following url would be valid:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=6ff81256b8a3ba11d239da51a703b9c06a56ffddeb8caab74ca83af8f73c9c83&
temp_url_expires=1648082711&
temp_url_ip_range=1.2.3.0/24

Any alteration of the resource path or query arguments of a temporary URL
would result in 401 Unauthorized . Similarly, a PUT where GET was
the allowed method would be rejected with 401 Unauthorized .
However, HEAD is allowed if GET , PUT , or POST is allowed.

Using this in combination with browser form post translation
middleware could also allow direct-from-browser uploads to specific
locations in Swift.

TempURL supports both account and container level keys.  Each allows up to two
keys to be set, allowing key rotation without invalidating all existing
temporary URLs.  Account keys are specified by X-Account-Meta-Temp-URL-Key and X-Account-Meta-Temp-URL-Key-2 , while container keys are specified by X-Container-Meta-Temp-URL-Key and X-Container-Meta-Temp-URL-Key-2 .
Signatures are checked against account and container keys, if
present.

With GET TempURLs, a Content-Disposition header will be set on the
response so that browsers will interpret this as a file attachment to
be saved. The filename chosen is based on the object name, but you
can override this with a filename query parameter. Modifying the
above example:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563&filename=My+Test+File.pdf

If you do not want the object to be downloaded, you can cause Content-Disposition: inline to be set on the response by adding the inline parameter to the query string, like so:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563&inline

In some cases, the client might not able to present the content of the object,
but you still want the content able to save to local with the specific
filename. So you can cause Content-Disposition: inline; filename=... to be
set on the response by adding the inline&filename=... parameter to the
query string, like so:

https://swift-cluster.example.com/v1/AUTH_account/container/object?
temp_url_sig=732fcac368abb10c78a4cbe95c3fab7f311584532bf779abd5074e13cbe8b88b&
temp_url_expires=1512508563&inline&filename=My+Test+File.pdf

### Cluster Configuration Â¶

This middleware understands the following configuration settings:

A whitespace-delimited list of the headers to remove from
incoming requests. Names may optionally end with * to
indicate a prefix match. incoming_allow_headers is a
list of exceptions to these removals.
Default: x-timestamp x-open-expired

A whitespace-delimited list of the headers allowed as
exceptions to incoming_remove_headers . Names may
optionally end with * to indicate a prefix match.

Default: None

A whitespace-delimited list of the headers to remove from
outgoing responses. Names may optionally end with * to
indicate a prefix match. outgoing_allow_headers is a
list of exceptions to these removals.

Default: x-object-meta-*

A whitespace-delimited list of the headers allowed as
exceptions to outgoing_remove_headers . Names may
optionally end with * to indicate a prefix match.

Default: x-object-meta-public-*

A whitespace delimited list of request methods that are
allowed to be used with a temporary URL.

Default: GET HEAD PUT POST DELETE

A whitespace delimited list of digest algorithms that are allowed
to be used when calculating the signature for a temporary URL.

Default: sha256 sha512

Default headers as exceptions to DEFAULT_INCOMING_REMOVE_HEADERS. Simply a
whitespace delimited list of header names and names can optionally end with
â*â to indicate a prefix match.

Default headers to remove from incoming requests. Simply a whitespace
delimited list of header names and names can optionally end with â*â to
indicate a prefix match. DEFAULT_INCOMING_ALLOW_HEADERS is a list of
exceptions to these removals.

Default headers as exceptions to DEFAULT_OUTGOING_REMOVE_HEADERS. Simply a
whitespace delimited list of header names and names can optionally end with
â*â to indicate a prefix match.

Default headers to remove from outgoing responses. Simply a whitespace
delimited list of header names and names can optionally end with â*â to
indicate a prefix match. DEFAULT_OUTGOING_ALLOW_HEADERS is a list of
exceptions to these removals.

Bases: object

WSGI Middleware to grant temporary URLs specific access to Swift
resources. See the overview for more information.

The proxy logs created for any subrequests made will have swift.source set
to âTUâ.

- app â The next WSGI filter or app in the paste.deploy
chain.

app â The next WSGI filter or app in the paste.deploy
chain.

- conf â The configuration dict for the middleware.

conf â The configuration dict for the middleware.

HTTP user agent to use for subrequests.

The next WSGI application/filter in the paste.deploy pipeline.

The filter configuration dict.

Headers to allow in incoming requests. Uppercase WSGI env style,
like HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY .

Header with match prefixes to allow in incoming requests. Uppercase
WSGI env style, like HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY_* .

Headers to remove from incoming requests. Uppercase WSGI env style,
like HTTP_X_PRIVATE .

Header with match prefixes to remove from incoming requests.
Uppercase WSGI env style, like HTTP_X_SENSITIVE_* .

Headers to allow in outgoing responses. Lowercase, like x-matches-remove-prefix-but-okay .

Header with match prefixes to allow in outgoing responses.
Lowercase, like x-matches-remove-prefix-but-okay-* .

Headers to remove from outgoing responses. Lowercase, like x-account-meta-temp-url-key .

Header with match prefixes to remove from outgoing responses.
Lowercase, like x-account-meta-private-* .

Returns the WSGI filter for use with paste.deploy.

## Versioned Writes Â¶

Note

This middleware supports two legacy modes of object versioning that is
now replaced by a new mode. It is recommended to use the new Object Versioning mode for new containers.

Object versioning in swift is implemented by setting a flag on the container
to tell swift to version all objects in the container. The value of the flag is
the URL-encoded container name where the versions are stored (commonly referred
to as the âarchive containerâ). The flag itself is one of two headers, which
determines how object DELETE requests are handled:

- X-History-Location On DELETE , copy the current version of the object to the archive
container, write a zero-byte âdelete markerâ object that notes when the
delete took place, and delete the object from the versioned container. The
object will no longer appear in container listings for the versioned
container and future requests there will return 404 Not Found . However,
the content will still be recoverable from the archive container.

X-History-Location

On DELETE , copy the current version of the object to the archive
container, write a zero-byte âdelete markerâ object that notes when the
delete took place, and delete the object from the versioned container. The
object will no longer appear in container listings for the versioned
container and future requests there will return 404 Not Found . However,
the content will still be recoverable from the archive container.

- X-Versions-Location On DELETE , only remove the current version of the object. If any
previous versions exist in the archive container, the most recent one is
copied over the current version, and the copy in the archive container is
deleted. As a result, if you have 5 total versions of the object, you must
delete the object 5 times for that object name to start responding with 404 Not Found .

X-Versions-Location

On DELETE , only remove the current version of the object. If any
previous versions exist in the archive container, the most recent one is
copied over the current version, and the copy in the archive container is
deleted. As a result, if you have 5 total versions of the object, you must
delete the object 5 times for that object name to start responding with 404 Not Found .

Either header may be used for the various containers within an account, but
only one may be set for any given container. Attempting to set both
simulataneously will result in a 400 Bad Request response.

Note

It is recommended to use a different archive container for
each container that is being versioned.

Note

Enabling versioning on an archive container is not recommended.

When data is PUT into a versioned container (a container with the
versioning flag turned on), the existing data in the file is redirected to a
new object in the archive container and the data in the PUT request is
saved as the data for the versioned object. The new object name (for the
previous version) is <archive_container>/<length><object_name>/<timestamp> ,
where length is the 3-character zero-padded hexadecimal length of the <object_name> and <timestamp> is the timestamp of when the previous
version was created.

A GET to a versioned object will return the current version of the object
without having to do any request redirects or metadata lookups.

A POST to a versioned object will update the object metadata as normal,
but will not create a new version of the object. In other words, new versions
are only created when the content of the object changes.

A DELETE to a versioned object will be handled in one of two ways,
as described above.

To restore a previous version of an object, find the desired version in the
archive container then issue a COPY with a Destination header
indicating the original location. This will archive the current version similar
to a PUT over the versioned object. If the client additionally wishes to
permanently delete what was the current version, it must find the newly-created
archive in the archive container and issue a separate DELETE to it.

### How to Enable Object Versioning in a Swift Cluster Â¶

This middleware was written as an effort to refactor parts of the proxy server,
so this functionality was already available in previous releases and every
attempt was made to maintain backwards compatibility. To allow operators to
perform a seamless upgrade, it is not required to add the middleware to the
proxy pipeline and the flag allow_versions in the container server
configuration files are still valid, but only when using X-Versions-Location . In future releases, allow_versions will be
deprecated in favor of adding this middleware to the pipeline to enable or
disable the feature.

In case the middleware is added to the proxy pipeline, you must also
set allow_versioned_writes to True in the middleware options
to enable the information about this middleware to be returned in a /info
request.

Note

You need to add the middleware to the proxy pipeline and set allow_versioned_writes = True to use X-History-Location . Setting allow_versions = True in the container server is not sufficient to
enable the use of X-History-Location .

#### Upgrade considerations Â¶

If allow_versioned_writes is set in the filter configuration, you can leave
the allow_versions flag in the container server configuration files
untouched. If you decide to disable or remove the allow_versions flag, you
must re-set any existing containers that had the X-Versions-Location flag
configured so that it can now be tracked by the versioned_writes middleware.

Clients should not use the X-History-Location header until all proxies in
the cluster have been upgraded to a version of Swift that supports it.
Attempting to use X-History-Location during a rolling upgrade may result
in some requests being served by proxies running old code, leading to data
loss.

### Examples Using curl with X-Versions-Location Â¶

First, create a container with the X-Versions-Location header or add the
header to an existing container. Also make sure the container referenced by
the X-Versions-Location exists. In this example, the name of that
container is âversionsâ:

curl - i - XPUT - H "X-Auth-Token: <token>" - H "X-Versions-Location: versions" http : //< storage_url >/ container curl - i - XPUT - H "X-Auth-Token: <token>" http : //< storage_url >/ versions

Create an object (the first version):

curl - i - XPUT -- data - binary 1 - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject

Now create a new version of that object:

curl - i - XPUT -- data - binary 2 - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject

See a listing of the older versions of the object:

curl -i -H "X-Auth-Token: <token>" http://<storage_url>/versions?prefix=008myobject/

Now delete the current version of the object and see that the older version is
gone from âversionsâ container and back in âcontainerâ container:

curl -i -XDELETE -H "X-Auth-Token: <token>" http://<storage_url>/container/myobject
curl -i -H "X-Auth-Token: <token>" http://<storage_url>/versions?prefix=008myobject/
curl -i -XGET -H "X-Auth-Token: <token>" http://<storage_url>/container/myobject

### Examples Using curl with X-History-Location Â¶

As above, create a container with the X-History-Location header and ensure
that the container referenced by the X-History-Location exists. In this
example, the name of that container is âversionsâ:

curl - i - XPUT - H "X-Auth-Token: <token>" - H "X-History-Location: versions" http : //< storage_url >/ container curl - i - XPUT - H "X-Auth-Token: <token>" http : //< storage_url >/ versions

Create an object (the first version):

curl - i - XPUT -- data - binary 1 - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject

Now create a new version of that object:

curl - i - XPUT -- data - binary 2 - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject

Now delete the current version of the object. Subsequent requests will 404:

curl - i - XDELETE - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject curl - i - H "X-Auth-Token: <token>" http : //< storage_url >/ container / myobject

A listing of the older versions of the object will include both the first and
second versions of the object, as well as a âdelete markerâ object:

curl -i -H "X-Auth-Token: <token>" http://<storage_url>/versions?prefix=008myobject/

To restore a previous version, simply COPY it from the archive container:

curl - i - XCOPY - H "X-Auth-Token: <token>" http : //< storage_url >/ versions / 008 myobject /< timestamp > - H "Destination: container/myobject"

Note that the archive container still has all previous versions of the object,
including the source for the restore:

curl -i -H "X-Auth-Token: <token>" http://<storage_url>/versions?prefix=008myobject/

To permanently delete a previous version, DELETE it from the archive
container:

curl - i - XDELETE - H "X-Auth-Token: <token>" http : //< storage_url >/ versions / 008 myobject /< timestamp >

### How to Disable Object Versioning in a Swift Cluster Â¶

If you want to disable all functionality, set allow_versioned_writes to False in the middleware options.

Disable versioning from a container (x is any value except empty):

curl - i - XPOST - H "X-Auth-Token: <token>" - H "X-Remove-Versions-Location: x" http : //< storage_url >/ container

Bases: WSGIContext

Handle DELETE requests when in stack mode.

Delete current version of object and pop previous version in its place.

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- api_version â api version.

api_version â api version.

- account_name â account name.

account_name â account name.

- container_name â container name.

container_name â container name.

- object_name â object name.

object_name â object name.

Handle DELETE requests when in history mode.

Copy current version of object to versions_container and write a
delete marker before proceeding with original request.

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- api_version â api version.

api_version â api version.

- account_name â account name.

account_name â account name.

- object_name â name of object of original request

object_name â name of object of original request

Copy current version of object to versions_container before proceeding
with original request.

- req â original request.

req â original request.

- versions_cont â container where previous versions of the object
are stored.

versions_cont â container where previous versions of the object
are stored.

- api_version â api version.

api_version â api version.

- account_name â account name.

account_name â account name.

- object_name â name of object of original request

object_name â name of object of original request

## XProfile Â¶

Profiling middleware for Swift Servers.

Note

This middleware is intended for development and testing environments only,
not production. No authentication is expected or required for the web UI,
and profiling may incur noticeable performance penalties.

The current implementation is based on eventlet aware profiler.(For the
future, more profilers could be added in to collect more data for analysis.)
Profiling all incoming requests and accumulating cpu timing statistics
information for performance tuning and optimization. An mini web UI is also
provided for profiling data analysis. It can be accessed from the URL as
below.

Index page for browse profile data:

http : // SERVER_IP : PORT / __profile__

List all profiles to return profile ids in json format:

http : // SERVER_IP : PORT / __profile__ / http : // SERVER_IP : PORT / __profile__ / all

Retrieve specific profile data in different formats:

http://SERVER_IP:PORT/__profile__/PROFILE_ID?format=[default|json|csv|ods]
http://SERVER_IP:PORT/__profile__/current?format=[default|json|csv|ods]
http://SERVER_IP:PORT/__profile__/all?format=[default|json|csv|ods]

Retrieve metrics from specific function in json format:

http://SERVER_IP:PORT/__profile__/PROFILE_ID/NFL?format=json
http://SERVER_IP:PORT/__profile__/current/NFL?format=json
http://SERVER_IP:PORT/__profile__/all/NFL?format=json

NFL is defined by concatenation of file name, function name and the first
line number.
e.g.::
    account.py:50(GETorHEAD)
or with full path:
    opt/stack/swift/swift/proxy/controllers/account.py:50(GETorHEAD)

A list of URL examples:

http://localhost:8080/__profile__    (proxy server)
http://localhost:6200/__profile__/all    (object server)
http://localhost:6201/__profile__/current    (container server)
http://localhost:6202/__profile__/12345?format=json    (account server)

The profiling middleware can be configured in paste file for WSGI servers such
as proxy, account, container and object servers. Please refer to the sample
configuration files in etc directory.

The profiling data is provided with four formats such as binary(by default),
json, csv and odf spreadsheet which requires installing odfpy library:

sudo pip install odfpy

Thereâs also a simple visualization capability which is enabled by using
matplotlib toolkit. it is also required to be installed if you want to use
it to visualize statistic data:

sudo apt - get install python - matplotlib
