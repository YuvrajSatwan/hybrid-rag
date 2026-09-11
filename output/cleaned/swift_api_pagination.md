# Page through large lists of containers or objects Â¶

If you have a large number of containers or objects, you can use the marker , limit , and end_marker parameters to control
how many items are returned in a list and where the list starts or ends.
If you want to page backwards you can use the reverse parameter.

- marker When you request a list of containers or objects, Object Storage
returns a maximum of 10,000 names for each request. To get
subsequent names, you must make another request with the marker parameter. Set the marker parameter to the name of
the last item returned in the previous list. You must URL-encode the marker value before you send the HTTP request. Object Storage
returns a maximum of 10,000 names starting after the last item
returned.

When you request a list of containers or objects, Object Storage
returns a maximum of 10,000 names for each request. To get
subsequent names, you must make another request with the marker parameter. Set the marker parameter to the name of
the last item returned in the previous list. You must URL-encode the marker value before you send the HTTP request. Object Storage
returns a maximum of 10,000 names starting after the last item
returned.

- limit To return fewer than 10,000 names, use the limit parameter. If
the number of names returned equals the specified limit (or
10,000 if you omit the limit parameter), you can assume there
are more names to list. If the number of names in the list is
exactly divisible by the limit value, the last request has no
content.

To return fewer than 10,000 names, use the limit parameter. If
the number of names returned equals the specified limit (or
10,000 if you omit the limit parameter), you can assume there
are more names to list. If the number of names in the list is
exactly divisible by the limit value, the last request has no
content.

- end_marker Limits the result set to names that are less than the end_marker parameter value. You must URL-encode the end_marker value before you send the HTTP request.

Limits the result set to names that are less than the end_marker parameter value. You must URL-encode the end_marker value before you send the HTTP request.

- reverse By default, listings are returned sorted by name, ascending. If you
include the reverse=true query parameter, the listing will be
returned sorted by name, descending.

By default, listings are returned sorted by name, ascending. If you
include the reverse=true query parameter, the listing will be
returned sorted by name, descending.

## To page through a large list of containers Â¶

Assume the following list of container names:

apples bananas kiwis oranges pears

- Use a limit of two: # curl -i $publicURL /?limit = 2 -X GET -H "X-Auth-Token: $token " apples bananas Because two container names are returned, there are more names to
list.

Use a limit of two:

# curl -i $publicURL /?limit = 2 -X GET -H "X-Auth-Token: $token "

apples bananas

Because two container names are returned, there are more names to
list.

- Make another request with a marker parameter set to the name of
the last item returned: # curl -i $publicURL /?limit = 2 & amp ; marker = bananas -X GET -H \ âX-Auth-Token: $token " kiwis oranges Again, two items are returned, and there might be more.

Make another request with a marker parameter set to the name of
the last item returned:

# curl -i $publicURL /?limit = 2 & amp ; marker = bananas -X GET -H \ âX-Auth-Token: $token "

kiwis oranges

Again, two items are returned, and there might be more.

- Make another request with a marker of the last item returned: # curl -i $publicURL /?limit = 2 & amp ; marker = oranges -X GET -H \" X-Auth-Token: $token" pears You receive a one-item response, which is fewer than the limit number of names. This indicates that this is the end of the list.

Make another request with a marker of the last item returned:

# curl -i $publicURL /?limit = 2 & amp ; marker = oranges -X GET -H \" X-Auth-Token: $token"

pears

You receive a one-item response, which is fewer than the limit number of names. This indicates that this is the end of the list.

- Use the end_marker parameter to limit the result set to object
names that are less than the end_marker parameter value: # curl -i $publicURL /?end_marker = oranges -X GET -H \" X-Auth-Token: $token" apples bananas kiwis You receive a result set of all container names before the end-marker value.

Use the end_marker parameter to limit the result set to object
names that are less than the end_marker parameter value:

# curl -i $publicURL /?end_marker = oranges -X GET -H \" X-Auth-Token: $token"

apples bananas kiwis

You receive a result set of all container names before the end-marker value.

- Use the reverse parameter to work from the back of the
list: # curl -i $publicURL /?reverse = true -X GET -H \" X-Auth-Token: $token" pears oranges kiwis bananas apples

Use the reverse parameter to work from the back of the
list:

# curl -i $publicURL /?reverse = true -X GET -H \" X-Auth-Token: $token"

pears oranges kiwis bananas apples

- You can also combine parameters: # curl -i $publicURL /?reverse = true & end_marker = kiwis -X GET -H \" X-Auth-Token: $token" pears oranges

You can also combine parameters:

# curl -i $publicURL /?reverse = true & end_marker = kiwis -X GET -H \" X-Auth-Token: $token"

pears oranges
