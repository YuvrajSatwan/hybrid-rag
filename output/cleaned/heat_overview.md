# Welcome to the Heat documentation! Â¶

Heat is a service to orchestrate composite cloud applications
using a declarative template format through an OpenStack-native REST API.

## Heatâs purpose and vision Â¶

- Heat provides a template based orchestration for describing a cloud
application by executing appropriate OpenStack API calls to generate
running cloud applications.

Heat provides a template based orchestration for describing a cloud
application by executing appropriate OpenStack API calls to generate
running cloud applications.

- A Heat template describes the infrastructure for a cloud application in text
files which are readable and writable by humans, and can be managed by
version control tools.

A Heat template describes the infrastructure for a cloud application in text
files which are readable and writable by humans, and can be managed by
version control tools.

- Templates specify the relationships between resources (e.g. this
volume is connected to this server). This enables Heat to call out to the
OpenStack APIs to create all of your infrastructure in the correct order to
completely launch your application.

Templates specify the relationships between resources (e.g. this
volume is connected to this server). This enables Heat to call out to the
OpenStack APIs to create all of your infrastructure in the correct order to
completely launch your application.

- The software integrates other components of OpenStack. The templates allow
creation of most OpenStack resource types (such as instances, floating ips,
volumes, security groups, users, etc), as well as some more advanced
functionality such as instance high availability, instance autoscaling, and
nested stacks.

The software integrates other components of OpenStack. The templates allow
creation of most OpenStack resource types (such as instances, floating ips,
volumes, security groups, users, etc), as well as some more advanced
functionality such as instance high availability, instance autoscaling, and
nested stacks.

- Heat primarily manages infrastructure, but the templates
integrate well with software configuration management tools such as Puppet
and Ansible.

Heat primarily manages infrastructure, but the templates
integrate well with software configuration management tools such as Puppet
and Ansible.

- Operators can customise the capabilities of Heat by installing plugins.

Operators can customise the capabilities of Heat by installing plugins.

This documentation offers information aimed at end-users, operators and
developers of Heat.

## Operating Heat Â¶

- Installing Heat

- Running Heat API services in HTTP Server

- Configuring Heat

- Administering Heat

- Scaling a Deployment

- Upgrades Guideline

- Man pages for services and utilities

## Using Heat Â¶

- Creating your first stack

- Glossary

### Working with Templates Â¶

- Template Guide

- Example Templates

### Using the Heat Service Â¶

- OpenStack Orchestration API v1 Reference

OpenStack Orchestration API v1 Reference

- Python and CLI client

Python and CLI client

## Developing Heat Â¶

- Heat Developer Guidelines Heat and DevStack Blueprints and Specs Heat architecture Heat Resource Plug-in Development Guide Heat Stack Lifecycle Scheduler Hints Guru Meditation Reports Heat Support Status usage Guide Using Rally on Heat gates

- Heat and DevStack

- Blueprints and Specs

- Heat architecture

- Heat Resource Plug-in Development Guide

- Heat Stack Lifecycle Scheduler Hints

- Guru Meditation Reports

- Heat Support Status usage Guide

- Using Rally on Heat gates

- Source Code Index

## For Contributors Â¶

- If you are a new contributor to Heat please refer: So You Want to Contributeâ¦ Heat Contributor Guidelines So You Want to Contributeâ¦

If you are a new contributor to Heat please refer: So You Want to Contributeâ¦

- Heat Contributor Guidelines So You Want to Contributeâ¦

- So You Want to Contributeâ¦

## Indices and tables Â¶

- Index

Index

- Module Index

Module Index

- Search Page

Search Page
