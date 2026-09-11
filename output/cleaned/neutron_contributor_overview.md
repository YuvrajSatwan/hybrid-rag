# Contributor Guide Â¶

This document describes Neutron for contributors of the project, and assumes
that you are already familiar with Neutron from an end-user perspective .

## Basic Information Â¶

- Repo Overview Root Files neutron/ Package doc/ Structure API Docs CI and DevStack

- Root Files

- neutron/ Package

- doc/ Structure

- API Docs

- CI and DevStack

- So You Want to Contributeâ¦ Communication Contacting the Core Team New Feature Planning Task Tracking Reporting a Bug Getting Your Patch Merged Project Team Lead Duties

- Communication

- Contacting the Core Team

- New Feature Planning

- Task Tracking

- Reporting a Bug

- Getting Your Patch Merged

- Project Team Lead Duties

## Neutron Policies Â¶

- Neutron Policies Blueprints and Specs Bugs Code Reviews Contributor Onboarding Gate Failure Triage Release checklist Team Structure Third-party CI

- Blueprints and Specs

- Bugs

- Code Reviews

- Contributor Onboarding

- Gate Failure Triage

- Release checklist

- Team Structure

- Third-party CI

## Gerrit Rechecks Â¶

- Recheck Failed CI jobs in Neutron

## Neutron Stadium Â¶

- Neutron Stadium Stadium Governance Sub-Project Guidelines

- Stadium Governance

- Sub-Project Guidelines

## Developer Guide Â¶

In the Developer Guide, you will find information on Neutronâs lower level
programming APIs. There are sections that cover the core pieces of Neutron,
including its database, message queue, and scheduler components. There are
also subsections that describe specific plugins inside Neutron. Finally,
the developer guide includes information about Neutron testing infrastructure.

- Effective Neutron: 100 specific ways to improve your Neutron contributions Developing better software Landing patches more rapidly

- Developing better software

- Landing patches more rapidly

- Setting Up a Development Environment Getting the code About ignore files Testing Neutron

- Getting the code

- About ignore files

- Testing Neutron

- Deploying an OVN Development Environment with vagrant Vagrant prerequisites Sparse architecture

- Vagrant prerequisites

- Sparse architecture

- Contributing new extensions to Neutron Introduction Contribution Process Design and Development Testing and Continuous Integration Defect Management Backport Management Strategies DevStack Integration Strategies Documentation Project Initial Setup Internationalization support Integrating with the Neutron system

- Introduction

- Contribution Process

- Design and Development

- Testing and Continuous Integration

- Defect Management

- Backport Management Strategies

- DevStack Integration Strategies

- Documentation

- Project Initial Setup

- Internationalization support

- Integrating with the Neutron system

- Neutron public API Breakages

- Breakages

- Client command extension support

- Alembic Migrations Introduction The Migration Wrapper Migration Branches Developers

- Introduction

- The Migration Wrapper

- Migration Branches

- Developers

- Upgrade checks Introduction 3rd party plugins checks

- Introduction

- 3rd party plugins checks

- Testing Testing Neutron Full Stack Testing ML2 OVS with DevStack Neutron Jobs Running in Zuul CI OVN with DevStack Tempest Testing Template for ModelMigrationSync for external repos Test Coverage Transient DB Failure Injection Neutron WSGI API server

- Testing Neutron

- Full Stack Testing

- ML2 OVS with DevStack

- Neutron Jobs Running in Zuul CI

- OVN with DevStack

- Tempest Testing

- Template for ModelMigrationSync for external repos

- Test Coverage

- Transient DB Failure Injection

- Neutron WSGI API server

## Neutron Internals Â¶

- Neutron Internals Address Scopes and Subnet Pools Agent Extensions API Extensions API Layer for Neutron WSGI/HTTP Calling the ML2 Plugin Code Profiling Database Layer Database Models Relocation DNS Nameserver Order Consistency External DNS Service Integration i18n for the Neutron Stadium L2 Agent Extensions L2 Agent Networking L3 Agent Extensions Layer 3 Networking via Layer 3 & OpenVSwitch Agents Live-migration Local IP Metadata Service Architectural Overview ML2 Extension Manager Network IP Availability Extension Objects Open vSwitch L2 Agent Open vSwitch Firewall Driver OVN Design Notes Neutron Open vSwitch vhost-user Support Neutron Plugin Architecture Policy Enforcement and Authorization Provisioning Blocks in relation to Composite Object Status Quality of Service Quota Management and Enforcement Retrying Operations RPC API Layer RPC Messaging Callback System Security Group API Segments Extension Service Extensions Services and Agents SR-IOV Networking L2 Agent Tags in Neutron Resources Upgrade strategy

- Address Scopes and Subnet Pools

- Agent Extensions

- API Extensions

- API Layer for Neutron WSGI/HTTP

- Calling the ML2 Plugin

- Code Profiling

- Database Layer

- Database Models Relocation

- DNS Nameserver Order Consistency

- External DNS Service Integration

- i18n for the Neutron Stadium

- L2 Agent Extensions

- L2 Agent Networking

- L3 Agent Extensions

- Layer 3 Networking via Layer 3 & OpenVSwitch Agents

- Live-migration

- Local IP

- Metadata Service Architectural Overview

- ML2 Extension Manager

- Network IP Availability Extension

- Objects

- Open vSwitch L2 Agent

- Open vSwitch Firewall Driver

- OVN Design Notes

- Neutron Open vSwitch vhost-user Support

- Neutron Plugin Architecture

- Policy Enforcement and Authorization

- Provisioning Blocks in relation to Composite Object Status

- Quality of Service

- Quota Management and Enforcement

- Retrying Operations

- RPC API Layer

- RPC Messaging Callback System

- Security Group API

- Segments Extension

- Service Extensions

- Services and Agents

- SR-IOV Networking L2 Agent

- Tags in Neutron Resources

- Upgrade strategy

- Module Reference

## OVN Driver Â¶

- OVN backend OVN Tools

- OVN Tools

## Dashboards Â¶

There is a collection of dashboards to help developers and reviewers
located here.

- CI Status Dashboards Gerrit Dashboards Grafana Dashboards

- Gerrit Dashboards

- Grafana Dashboards
