# Contributor Guide Â¶

In this section you will find information on how to contribute to Cinder.
Content includes architectural overviews, tips and tricks for setting up a
development environment, and information on Cinderâs lower level programming
APIs.

## Getting Started Â¶

- So You Want to Contributeâ¦ Communication Contacting the Core Team Project Team Lead New Feature Planning Task Tracking Reporting a Bug Getting Your Patch Merged

- Communication

- Contacting the Core Team

- Project Team Lead

- New Feature Planning

- Task Tracking

- Reporting a Bug

- Getting Your Patch Merged

- Repo Overview Root files and directories Service code Tests Related contributor docs

- Root files and directories

- Service code

- Tests

- Related contributor docs

- Agentic Coding Philosophy Principles AGENTS.md Local scratch files Local tool configuration Tool invocation Commit messages

- Philosophy

- Principles

- AGENTS.md

- Local scratch files

- Local tool configuration

- Tool invocation

- Commit messages

- Commit Messages Message style Gerrit Change-Id Developer Certificate of Origin AI attribution trailers Example footer block

- Message style

- Gerrit Change-Id

- Developer Certificate of Origin

- AI attribution trailers

- Example footer block

- Dependencies Python dependencies Driver dependencies System packages Packaging metadata

- Python dependencies

- Driver dependencies

- System packages

- Packaging metadata

- Backporting a Fix Backport CI Testing

- Backport CI Testing

- Cinder Project Releases Where Stuff Is How Stuff Works

- Where Stuff Is

- How Stuff Works

## Writing Release Notes Â¶

Please follow the format, it will make everyoneâs life easier.  Thereâs
even a special section on writing release notes for Cinder drivers.

- Release notes Reviewing release note content Fixing a release note Bugs Drivers Creating the note

- Reviewing release note content

- Fixing a release note

- Bugs

- Drivers

- Creating the note

## Programming HowTos and Tutorials Â¶

- Setting Up a Development Environment Virtual environments Linux Systems macOS Systems Getting the code Running unit tests Manually installing and using the virtualenv Contributing Your Work

- Virtual environments

- Linux Systems

- macOS Systems

- Getting the code

- Running unit tests

- Manually installing and using the virtualenv

- Contributing Your Work

- Testing Test Types Running the tests Running a subset of tests using tox Gotchas Debugging

- Test Types

- Running the tests

- Running a subset of tests using tox

- Gotchas

- Debugging

- API Microversions Background When do I need a new Microversion? In Code Other necessary changes Allocating a microversion Testing Microversioned API Methods REST API Version History

- Background

- When do I need a new Microversion?

- In Code

- Other necessary changes

- Allocating a microversion

- Testing Microversioned API Methods

- REST API Version History

- API Races - Conditional Updates Background Conditional Update Basic Usage Returning Errors Building filters on the API Using DB fields for assignment Conditional value setting reflect_changes considerations Limitations Considerations for new ORM & Versioned Objects

- Background

- Conditional Update

- Basic Usage

- Returning Errors

- Building filters on the API

- Using DB fields for assignment

- Conditional value setting

- reflect_changes considerations

- Limitations

- Considerations for new ORM & Versioned Objects

- Adding a Method to the OpenStack API Routing Controllers and actions Serialization Errors

- Routing

- Controllers and actions

- Serialization

- Errors

- Drivers Basic attributes Configuration options Minimum Features Core Functionality Security Requirements Volume Stats Feature Enforcement New Driver Review Checklist Driver Development Documentations

- Basic attributes

- Configuration options

- Minimum Features

- Core Functionality

- Security Requirements

- Volume Stats

- Feature Enforcement

- New Driver Review Checklist

- Driver Development Documentations

- High Availability Overview Job distribution Heartbeats Cleanup Mutual exclusion Cinder-API Cinder-Volume Cinder-Scheduler Cinder-Backups

- Overview

- Job distribution

- Heartbeats

- Cleanup

- Mutual exclusion

- Cinder-API

- Cinder-Volume

- Cinder-Scheduler

- Cinder-Backups

- Guru Meditation Reports Generating a GMR Structure of a GMR Adding Support for GMRs to New Executables Extending the GMR

- Generating a GMR

- Structure of a GMR

- Adding Support for GMRs to New Executables

- Extending the GMR

- Replication Overview Storage Device configuration Service configuration Capabilities reporting Volume Types / Extra Specs Volume creation Failover Failback Initialization Freeze / Thaw

- Overview

- Storage Device configuration

- Service configuration

- Capabilities reporting

- Volume Types / Extra Specs

- Volume creation

- Failover

- Failback

- Initialization

- Freeze / Thaw

- User Messages General information Example Adding user messages Usage patterns Module documentation

- General information

- Example

- Adding user messages

- Usage patterns

- Module documentation

- Migration Introduction to volume migration How to do volume migration via CLI Configurations What can be tracked during volume migration How to implement volume migration for a back-end driver Required methods

- Introduction to volume migration

- How to do volume migration via CLI

- Configurations

- What can be tracked during volume migration

- How to implement volume migration for a back-end driver

- Required methods

- Running Cinder API under Apache Files Access Control

- Files

- Access Control

- Upgrades Database schema and data migrations RPC API changes RPC payload changes (oslo.versionedobjects) Upgrade Checks

- Database schema and data migrations

- RPC API changes

- RPC payload changes (oslo.versionedobjects)

- Upgrade Checks

- Generic Volume Groups Introduction to generic volume groups Action items for drivers supporting consistency groups Group Type and Group Specs / Volume Types and Extra Specs Capabilities reporting Driver methods Migrate CGs to Generic Volume Groups References

- Introduction to generic volume groups

- Action items for drivers supporting consistency groups

- Group Type and Group Specs / Volume Types and Extra Specs

- Capabilities reporting

- Driver methods

- Migrate CGs to Generic Volume Groups

- References

- Database migrations Schema migrations Data migrations

- Schema migrations

- Data migrations

## Managing the Development Cycle Â¶

- Release Cycle Tasks

- Cinder Groups in Gerrit and Launchpad

## Documentation Contribution Â¶

- Contributing Documentation to Cinder Documentation Content Using RST Building Cinderâs Documentation Review and Release Process Doc Directory Structure Finding something to contribute

- Documentation Content

- Using RST

- Building Cinderâs Documentation

- Review and Release Process

- Doc Directory Structure

- Finding something to contribute

## Background Concepts for Cinder Â¶

- Cinder System Architecture Components Service interaction example Related documents

- Components

- Service interaction example

- Related documents

- Volume Attach/Detach workflow Attach/Detach Operations are multi-part commands Attach workflow reserve_volume(self, context, volume) initialize_connection(self, context, volume, connector) attach(self, context, volume, instance_uuid, host_name, mountpoint, mode) Detach workflow begin_detaching(self, context, volume) terminate_connection(self, context, volume, connector, force=False) detach(self, context, volume, attachment_id)

- Attach/Detach Operations are multi-part commands

- Attach workflow reserve_volume(self, context, volume) initialize_connection(self, context, volume, connector) attach(self, context, volume, instance_uuid, host_name, mountpoint, mode)

- reserve_volume(self, context, volume)

- initialize_connection(self, context, volume, connector)

- attach(self, context, volume, instance_uuid, host_name, mountpoint, mode)

- Detach workflow begin_detaching(self, context, volume) terminate_connection(self, context, volume, connector, force=False) detach(self, context, volume, attachment_id)

- begin_detaching(self, context, volume)

- terminate_connection(self, context, volume, connector, force=False)

- detach(self, context, volume, attachment_id)

- Volume Attach/Detach workflow - V2 Attachment Object New API and Flow attachment-create attachment-update attachment-delete

- Attachment Object

- New API and Flow attachment-create attachment-update attachment-delete

- attachment-create

- attachment-update

- attachment-delete

- Cinder Thin provisioning and Oversubscription Background Core concepts and terminology Stats to be reported Mandatory Fields Optional Fields

- Background

- Core concepts and terminology

- Stats to be reported Mandatory Fields Optional Fields

- Mandatory Fields

- Optional Fields

- Threading model Yielding the thread in long-running tasks MySQL access and eventlet

- Yielding the thread in long-running tasks

- MySQL access and eventlet

- Internationalization

- AMQP and Cinder Cinder RPC Mappings RPC Calls RPC Casts AMQP Broker Load RabbitMQ Gotchas

- Cinder RPC Mappings

- RPC Calls

- RPC Casts

- AMQP Broker Load

- RabbitMQ Gotchas

## Other Resources Â¶

- Project hosting with Launchpad Launchpad credentials Mailing list Bug tracking Feature requests (Blueprints) Technical support (Answers)

- Launchpad credentials

- Mailing list

- Bug tracking

- Feature requests (Blueprints)

- Technical support (Answers)

- Code Reviews Gerrit Targeting Milestones Reviewing Vendor Patches Unit Tests CI Job rechecks Efficient Review Guidelines

- Gerrit

- Targeting Milestones

- Reviewing Vendor Patches

- Unit Tests

- CI Job rechecks

- Efficient Review Guidelines

- Continuous Integration with Zuul

- Module Reference cinder package Subpackages Submodules Module contents

- cinder package Subpackages Submodules Module contents

- Subpackages

- Submodules

- Module contents

## Indices and tables Â¶

- Index

Index

- Module Index

Module Index

- Search Page

Search Page
