# Contributor Documentation Â¶

Contributing to nova gives you the power to help add features, fix bugs,
enhance documentation, and increase testing. Contributions of any type are
valuable, and part of what keeps the project going. Here are a list of
resources to get your started.

## Basic Information Â¶

- So You Want to Contributeâ¦ Communication Contacting the Core Team New Feature Planning Task Tracking Reporting a Bug Getting Your Patch Merged Project Team Lead Duties

- Communication

- Contacting the Core Team

- New Feature Planning

- Task Tracking

- Reporting a Bug

- Getting Your Patch Merged

- Project Team Lead Duties

## Getting Started Â¶

- How to get (more) involved with Nova : Overview of engaging in the project

How to get (more) involved with Nova : Overview of engaging in the project

- Development Quickstart : Get your computer setup to
contribute

Development Quickstart : Get your computer setup to
contribute

- Repo Overview : Terse map of the Nova repository
layout, package structure, and documentation sections.

Repo Overview : Terse map of the Nova repository
layout, package structure, and documentation sections.

- Agentic Coding : Conventions for AI-assisted
development, including the AGENTS.md routing layer and local scratch
files.

Agentic Coding : Conventions for AI-assisted
development, including the AGENTS.md routing layer and local scratch
files.

## Nova Process Â¶

The nova community is a large community. We have lots of users, and they all
have a lot of expectations around upgrade and backwards compatibility.  For
example, having a good stable API, with discoverable versions and capabilities
is important for maintaining the strong ecosystem around nova.

Our process is always evolving, just as nova and the community around nova
evolves over time. If there are things that seem strange, or you have ideas on
how to improve things, please bring them forward on IRC or the openstack-discuss
mailing list, so we continue to improve how the nova community operates.

This section looks at the processes and why. The main aim behind all the
process is to aid communication between all members of the nova community,
while keeping users happy and keeping developers productive.

- Scope of the Nova project : The focus is on features and bug fixes
that make nova work better within this scope

Scope of the Nova project : The focus is on features and bug fixes
that make nova work better within this scope

- Development policies : General guidelines about whatâs supported

Development policies : General guidelines about whatâs supported

- Nova team process : The processes we follow around feature and bug
submission, including how the release calendar works, and the freezes we go
under

Nova team process : The processes we follow around feature and bug
submission, including how the release calendar works, and the freezes we go
under

- Blueprints, Specs and Priorities : An overview of our tracking artifacts.

Blueprints, Specs and Priorities : An overview of our tracking artifacts.

- Chronological PTL guide : A chronological PTL reference guide

Chronological PTL guide : A chronological PTL reference guide

## Code Conventions Â¶

- OpenStack code and documentation guide : General OpenStack contributor
conventions covering style, testing, and documentation standards.

OpenStack code and documentation guide : General OpenStack contributor
conventions covering style, testing, and documentation standards.

- Nova HACKING.rst : Nova-specific style rules and N-check descriptions;
enforced by tox -e pep8 .

Nova HACKING.rst : Nova-specific style rules and N-check descriptions;
enforced by tox -e pep8 .

- Dependencies : Where to declare Python, documentation,
and system package dependencies.

Dependencies : Where to declare Python, documentation,
and system package dependencies.

- Commit Messages : Nova commit message guidance,
including Gerrit footers, DCO sign-off, and AI attribution trailers.

Commit Messages : Nova commit message guidance,
including Gerrit footers, DCO sign-off, and AI attribution trailers.

- Release Notes : When we need a release note for a
contribution.

Release Notes : When we need a release note for a
contribution.

- Internationalization : What we require for i18n in patches.

Internationalization : What we require for i18n in patches.

- Database migrations : How to write schema and data
migrations when adding a feature or bugfix.

Database migrations : How to write schema and data
migrations when adding a feature or bugfix.

- Upgrade checks : How to write automated upgrade checks
when adding a feature or bugfix.

Upgrade checks : How to write automated upgrade checks
when adding a feature or bugfix.

## Reviewing Â¶

- Code Review Guide for Nova : Important cheat sheet for whatâs important
when doing code review in Nova, especially some things that are hard to test
for, but need human eyes.

Code Review Guide for Nova : Important cheat sheet for whatâs important
when doing code review in Nova, especially some things that are hard to test
for, but need human eyes.

- Documentation Guidelines : Guidelines for handling documentation
contributions

Documentation Guidelines : Guidelines for handling documentation
contributions

## Testing Â¶

Because Python is a dynamic language, code that is not tested might not even
be Python code. All new code needs to be validated somehow.

- Test Strategy : An overview of our test taxonomy and the kinds
of testing we do and expect.

Test Strategy : An overview of our test taxonomy and the kinds
of testing we do and expect.

- Testing Guides : There are also specific testing guides for features that
are hard to test in our gate. Testing NUMA related hardware setup with libvirt Testing Serial Console Testing Zero Downtime Upgrade Process Testing Down Cells Testing PCI passthrough and SR-IOV with emulated PCI NIC

Testing Guides : There are also specific testing guides for features that
are hard to test in our gate.

- Testing NUMA related hardware setup with libvirt

Testing NUMA related hardware setup with libvirt

- Testing Serial Console

Testing Serial Console

- Testing Zero Downtime Upgrade Process

Testing Zero Downtime Upgrade Process

- Testing Down Cells

Testing Down Cells

- Testing PCI passthrough and SR-IOV with emulated PCI NIC

Testing PCI passthrough and SR-IOV with emulated PCI NIC

- Profiling Guides : These are guides to profiling nova. Profiling With Eventlet

Profiling Guides : These are guides to profiling nova.

- Profiling With Eventlet

Profiling With Eventlet

## The Nova API Â¶

Because we have many consumers of our API, weâre extremely careful about
changes done to the API, as the impact can be very wide.

- Extending the API : How the code is structured inside the API layer

Extending the API : How the code is structured inside the API layer

- API Microversions : How the API is (micro)versioned and what
you need to do when adding an API exposed feature that needs a new
microversion.

API Microversions : How the API is (micro)versioned and what
you need to do when adding an API exposed feature that needs a new
microversion.

- API reference guideline : The guideline to write the API
reference.

API reference guideline : The guideline to write the API
reference.

Nova also provides notifications over the RPC API, which you may wish to
extend.

- Notifications : How to add your own notifications

Notifications : How to add your own notifications

## Nova Major Subsystems Â¶

Major subsystems in nova have different needs. If you are contributing to one
of these please read the reference guide before
diving in.

- Move operations Evacuate vs Rebuild : Describes the differences between
the often-confused evacuate and rebuild operations. Resize and cold migrate : Describes the differences and
similarities between resize and cold migrate operations.

Move operations

- Evacuate vs Rebuild : Describes the differences between
the often-confused evacuate and rebuild operations.

Evacuate vs Rebuild : Describes the differences between
the often-confused evacuate and rebuild operations.

- Resize and cold migrate : Describes the differences and
similarities between resize and cold migrate operations.

Resize and cold migrate : Describes the differences and
similarities between resize and cold migrate operations.
