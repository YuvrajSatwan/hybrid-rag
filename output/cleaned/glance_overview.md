# Welcome to Glanceâs documentation! Â¶

## About Glance Â¶

The Image service (glance) project provides a service where users can upload
and discover data assets that are meant to be used with other services.
This currently includes images and metadata definitions .

### Images Â¶

Glance image services include discovering, registering, and
retrieving virtual machine (VM) images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

Note

The Images API v1, DEPRECATED in the Newton release, has been
removed.

VM images made available through Glance can be stored in a variety of
locations from simple filesystems to object-storage systems like the
OpenStack Swift project.

### Metadata Definitions Â¶

Glance hosts a metadefs catalog.  This provides the OpenStack community
with a way to programmatically determine various metadata key names and
valid values that can be applied to OpenStack resources.

Note that what weâre talking about here is simply a catalog ; the keys and
values donât actually do anything unless they are applied to individual
OpenStack resources using the APIs or client tools provided by the services
responsible for those resources.

Itâs also worth noting that there is no special relationship between the
Image Service and the Metadefs Service.  If you want to apply the keys and
values defined in the Metadefs Service to images, you must use the Image
Service API or client tools just as you would for any other OpenStack
service.

### Design Principles Â¶

Glance, as with all OpenStack projects, is written with the following design
guidelines in mind:

- Component based architecture : Quickly add new behaviors

Component based architecture : Quickly add new behaviors

- Highly available : Scale to very serious workloads

Highly available : Scale to very serious workloads

- Fault tolerant : Isolated processes avoid cascading failures

Fault tolerant : Isolated processes avoid cascading failures

- Recoverable : Failures should be easy to diagnose, debug, and rectify

Recoverable : Failures should be easy to diagnose, debug, and rectify

- Open standards : Be a reference implementation for a community-driven api

Open standards : Be a reference implementation for a community-driven api

## Glance Documentation Â¶

The Glance Project Team has put together the following documentation for you.
Pick the documents that best match your user profile.

User Profile Links Contributor You want to contribute code, documentation, reviews, or
ideas to the Glance Project. Glance Contribution Guidelines Administrator You want to administer and maintain a Glance installation, including
being aware of changes in Glance from release to release. Glance Administration Guide Glance Utility Programs Glance Release Notes Operator You want to install and configure Glance for your cloud. Glance Installation Glance Configuration Options End User or Third-party Developer You want to use the Image Service APIs provided by Glance. Image Service API Reference Image Service API Guide Glance User Guide

User Profile

Links

- Glance Contribution Guidelines

Glance Contribution Guidelines

- Glance Administration Guide

Glance Administration Guide

- Glance Utility Programs

Glance Utility Programs

- Glance Release Notes

Glance Release Notes

- Glance Installation

Glance Installation

- Glance Configuration Options

Glance Configuration Options

- Image Service API Reference

Image Service API Reference

- Image Service API Guide

Image Service API Guide

- Glance User Guide

Glance User Guide
