# Database Migrations Â¶

Database migrations are managed using the Alembic library. The consensus for OpenStack and SQLAlchemy is that this library is preferred over
sqlalchemy-migrate.

Database migrations can be performed two ways: (1) via the API startup
process, and (2) via a separate script.

Database migrations can be optionally enabled during the API startup process.
Corollaries for this are that a new deployment should begin with only one node
to avoid migration race conditions.

## Policy Â¶

A Barbican deployment goal is to update application and schema versions with
zero downtime. The challenge is that at all times the database schema must be
able to support two deployed application versions, so that a single migration
does not break existing nodes running the previous deployment. For example,
when deleting a column we would first deploy a new version that ignores the
column. Once all nodes are ignoring the column, a second deployment would be
made to remove the column from the database.

To achieve this goal, the following rules will be observed for schema changes:

- Do not remove columns or tables directly, but rather: Create a version of the application not dependent on the removed
column/table Replace all nodes with this new application version Create an Alembic version file to remove the column/table Apply this change in production manually, or automatically with a future
version of the application

Do not remove columns or tables directly, but rather:

- Create a version of the application not dependent on the removed
column/table

Create a version of the application not dependent on the removed
column/table

- Replace all nodes with this new application version

Replace all nodes with this new application version

- Create an Alembic version file to remove the column/table

Create an Alembic version file to remove the column/table

- Apply this change in production manually, or automatically with a future
version of the application

Apply this change in production manually, or automatically with a future
version of the application

- Changing column attributes (types, names or widths) should be handled as
follows: TODO: This Stack Overflow Need to alter column types in production
database page and many others summarize the grief involved in doing
these sorts of migrations TODO: What about old and new application versions happening
simultaneously? Maybe have the new code perform migration to new column on each read
â¦similar to how a no-sql db migration would occur?

Changing column attributes (types, names or widths) should be handled as
follows:

- TODO: This Stack Overflow Need to alter column types in production
database page and many others summarize the grief involved in doing
these sorts of migrations

TODO: This Stack Overflow Need to alter column types in production
database page and many others summarize the grief involved in doing
these sorts of migrations

- TODO: What about old and new application versions happening
simultaneously? Maybe have the new code perform migration to new column on each read
â¦similar to how a no-sql db migration would occur?

TODO: What about old and new application versions happening
simultaneously?

- Maybe have the new code perform migration to new column on each read
â¦similar to how a no-sql db migration would occur?

Maybe have the new code perform migration to new column on each read
â¦similar to how a no-sql db migration would occur?

- Transforming column attributes (ex: splitting one name column into a first and last name): TODO: An Alembic example , but not robust for large datasets.

Transforming column attributes (ex: splitting one name column into a first and last name):

- TODO: An Alembic example , but not robust for large datasets.

TODO: An Alembic example , but not robust for large datasets.

## Overview Â¶

Prior to invoking any migration steps below, change to your barbican projectâs
folder and activate your virtual environment per the Developer Guide .

If you are using PostgreSQL, please ensure you are using SQLAlchemy version
0.9.3 or higher, otherwise the generated version files will not be correct.

You cannot use these migration tools and techniques with SQLite databases.

Consider taking a look at the Alembic tutorial . As a brief summary: Alembic
keeps track of a linked list of version files, each one applying a set of
changes to the database schema that a previous version file in the linked list
modified. Each version file has a unique Alembic-generated ID associated with
it. Alembic generates a table in the project table space called alembic_version that keeps track of the unique ID of the last version file
applied to the schema. During an update, Alembic uses this stored version ID
to determine what if any follow on version files to process.

## Generating Change Versions Â¶

To make schema changes, new version files need to be added to the barbican/model/migration/alembic_migrations/versions/ folder. This section
discusses two ways to add these files.

### Automatically Â¶

Alembic autogenerates a new script by comparing a clean database (i.e., one
without your recent changes) with any modifications you make to the Models.py
or other files. This being said, automatic generation may miss changesâ¦ it
is more of an âautomatic assist with expert reviewâ. See What does
Autogenerate Detect in the Alembic documentation for more details.

First, you must start Barbican using a version of the code that does not
include your changes, so that it creates a clean database. This example uses
Barbican launched with DevStack (see Barbican DevStack wiki page for
instructions).

- Make changes to the âbarbican/model/models.pyâ SQLAlchemy models or
checkout your branch that includes your changes using git.

Make changes to the âbarbican/model/models.pyâ SQLAlchemy models or
checkout your branch that includes your changes using git.

- Execute barbican-db-manage -d <Full URL to database, including user/pw> revision -m '<your-summary-of-changes>' --autogenerate For example: barbican-db-manage -d mysql+pymysql://root:password@127.0.0.1/barbican?charset=utf8 revision -m 'Make unneeded verification columns nullable' --autogenerate

Execute barbican-db-manage -d <Full URL to database, including user/pw> revision -m '<your-summary-of-changes>' --autogenerate

- For example: barbican-db-manage -d mysql+pymysql://root:password@127.0.0.1/barbican?charset=utf8 revision -m 'Make unneeded verification columns nullable' --autogenerate

For example: barbican-db-manage -d mysql+pymysql://root:password@127.0.0.1/barbican?charset=utf8 revision -m 'Make unneeded verification columns nullable' --autogenerate

- Examine the generated version file, found in barbican/model/migration/alembic_migrations/versions/ : Verify generated update/rollback steps, especially for modifications
to existing columns/tables Remove autogenerated comments such as: ### commands auto generated by Alembic - please adjust! ### If you added new columns, follow this guidance : For non-nullable columns you will need to add default values for the
records already in the table, per what you configured in the barbican.model.models.py module. You can add the server_default keyword argument for the SQLAlchemy Column call
per SQLAlchemyâs server_default . For boolean attributes, use server_default=â0â for False, or server_default=â1â for True. For
DateTime attributes, use server_default=str(timeutils.utcnow()) to
default to the current time. If you add any constraint, please always name them in the
barbican.model.models.py module, and also in the Alembic version
modules when creating/dropping constraints, otherwise MySQL migrations
might crash. If you added new tables, follow this guidance : Make sure you added your new table to the MODELS element of the barbican/model/models.py module. Note that when Barbican boots up, it will add the new table to the
database. It will also try to apply the database version (that also
tries to add this table) via alembic. Therefore, please edit the
generated script file to add these lines: ctx = op.get_context() (to get the alembic migration context in
current transaction) con = op.get_bind() (get the database connection) table_exists = ctx.dialect.has_table(con.engine, 'your-new-table-name-here') if not table_exists: ...remaining create table logic here...

Examine the generated version file, found in barbican/model/migration/alembic_migrations/versions/ :

- Verify generated update/rollback steps, especially for modifications
to existing columns/tables

Verify generated update/rollback steps, especially for modifications
to existing columns/tables

- Remove autogenerated comments such as: ### commands auto generated by Alembic - please adjust! ###

Remove autogenerated comments such as: ### commands auto generated by Alembic - please adjust! ###

- If you added new columns, follow this guidance : For non-nullable columns you will need to add default values for the
records already in the table, per what you configured in the barbican.model.models.py module. You can add the server_default keyword argument for the SQLAlchemy Column call
per SQLAlchemyâs server_default . For boolean attributes, use server_default=â0â for False, or server_default=â1â for True. For
DateTime attributes, use server_default=str(timeutils.utcnow()) to
default to the current time. If you add any constraint, please always name them in the
barbican.model.models.py module, and also in the Alembic version
modules when creating/dropping constraints, otherwise MySQL migrations
might crash.

If you added new columns, follow this guidance :

- For non-nullable columns you will need to add default values for the
records already in the table, per what you configured in the barbican.model.models.py module. You can add the server_default keyword argument for the SQLAlchemy Column call
per SQLAlchemyâs server_default . For boolean attributes, use server_default=â0â for False, or server_default=â1â for True. For
DateTime attributes, use server_default=str(timeutils.utcnow()) to
default to the current time.

For non-nullable columns you will need to add default values for the
records already in the table, per what you configured in the barbican.model.models.py module. You can add the server_default keyword argument for the SQLAlchemy Column call
per SQLAlchemyâs server_default . For boolean attributes, use server_default=â0â for False, or server_default=â1â for True. For
DateTime attributes, use server_default=str(timeutils.utcnow()) to
default to the current time.

- If you add any constraint, please always name them in the
barbican.model.models.py module, and also in the Alembic version
modules when creating/dropping constraints, otherwise MySQL migrations
might crash.

If you add any constraint, please always name them in the
barbican.model.models.py module, and also in the Alembic version
modules when creating/dropping constraints, otherwise MySQL migrations
might crash.

- If you added new tables, follow this guidance : Make sure you added your new table to the MODELS element of the barbican/model/models.py module. Note that when Barbican boots up, it will add the new table to the
database. It will also try to apply the database version (that also
tries to add this table) via alembic. Therefore, please edit the
generated script file to add these lines: ctx = op.get_context() (to get the alembic migration context in
current transaction) con = op.get_bind() (get the database connection) table_exists = ctx.dialect.has_table(con.engine, 'your-new-table-name-here') if not table_exists: ...remaining create table logic here...

If you added new tables, follow this guidance :

- Make sure you added your new table to the MODELS element of the barbican/model/models.py module.

Make sure you added your new table to the MODELS element of the barbican/model/models.py module.

- Note that when Barbican boots up, it will add the new table to the
database. It will also try to apply the database version (that also
tries to add this table) via alembic. Therefore, please edit the
generated script file to add these lines: ctx = op.get_context() (to get the alembic migration context in
current transaction) con = op.get_bind() (get the database connection) table_exists = ctx.dialect.has_table(con.engine, 'your-new-table-name-here') if not table_exists: ...remaining create table logic here...

Note that when Barbican boots up, it will add the new table to the
database. It will also try to apply the database version (that also
tries to add this table) via alembic. Therefore, please edit the
generated script file to add these lines:

- ctx = op.get_context() (to get the alembic migration context in
current transaction)

ctx = op.get_context() (to get the alembic migration context in
current transaction)

- con = op.get_bind() (get the database connection)

con = op.get_bind() (get the database connection)

- table_exists = ctx.dialect.has_table(con.engine, 'your-new-table-name-here')

table_exists = ctx.dialect.has_table(con.engine, 'your-new-table-name-here')

- if not table_exists:

if not table_exists:

- ...remaining create table logic here...

...remaining create table logic here...

Note: For anything but trivial or brand new columns/tables, database backups
and maintenance-window downtimes might be called for.

### Manually Â¶

- Execute: barbican-db-manage revision -m "<insert your change description here>"

Execute: barbican-db-manage revision -m "<insert your change description here>"

- This will generate a new file in the barbican/model/migration/alembic_migrations/versions/ folder, with this
sort of file format: <unique-Alembic-ID>_<your-change-description-from-above-but-truncated>.py .
Note that only the first 20 characters of the description are used.

This will generate a new file in the barbican/model/migration/alembic_migrations/versions/ folder, with this
sort of file format: <unique-Alembic-ID>_<your-change-description-from-above-but-truncated>.py .
Note that only the first 20 characters of the description are used.

- You can then edit this file per tutorial and the Alembic Operation
Reference page for available operations you may make from the version
files. You must properly fill in the upgrade() methods.

You can then edit this file per tutorial and the Alembic Operation
Reference page for available operations you may make from the version
files. You must properly fill in the upgrade() methods.

## Applying Changes Â¶

Barbican utilizes the Alembic version files as managing delta changes to the
database. Therefore the first Alembic version file does not contain all
time-zero database tables.

To create the initial Barbican tables in the database, execute the Barbican
application per the âVia Applicationâ section.

Thereafter, it is suggested that only the barbican-db-manage command
above be used to update the database schema per the âManuallyâ section. Also,
automatic database updates from the Barbican application should be disabled by
adding/updating db_auto_create = False in the barbican.conf configuration file.

Note : Before attempting any upgrade, you should make a full database
backup of your production data. As of Kilo, database downgrades are not
supported in OpenStack, and the only method available to get back to a
prior database version will be to restore from backup.

### Via Application Â¶

The last section of the Alembic tutorial describes the process used by the
Barbican application to create and update the database table space
automatically.

By default, when the Barbican API boots up it will try to create the Barbican
database tables (using SQLAlchemy), and then try to apply the latest version
files (using Alembic). In this mode, the latest version of the Barbican
application can create a new database table space updated to the latest schema
version, or else it can update an existing database table space to the latest
schema revision (called head in the docs).

To bypass this automatic behavior, add db_auto_create = False to the barbican.conf file .

### Manually Â¶

Run barbican-db-manage -d <Full URL to database, including user/pw> upgrade -v head , which will cause Alembic to apply the changes found in all
version files after the version currently written in the target database, up
until the latest version file in the linked chain of files.

To upgrade to a specific version, run this command: barbican-db-manage -d <Full URL to database, including user/pw> upgrade -v <Alembic-ID-of-version> . The Alembic-ID-of-version is a
unique ID assigned to the change such as1a0c2cdafb38 .

### Downgrade Â¶

Upgrades involve complex operations and can fail. Before attempting any upgrade,
you should make a full database backup of your production data. As of Kilo,
database downgrades are not supported, and the only method available to get back
to a prior database version will be to restore from backup.

You must complete these steps to successfully roll back your environment:

- Roll back configuration files.

Roll back configuration files.

- Restore databases from backup.

Restore databases from backup.

- Roll back packages.

Roll back packages.

Rolling back upgrades is a tricky process because distributions tend to put
much more effort into testing upgrades than downgrades. Broken downgrades
often take significantly more effort to troubleshoot and resolve than broken
upgrades. Only you can weigh the risks of trying to push a failed upgrade
forward versus rolling it back. Generally, consider rolling back as the
very last option.

The backup instructions provided in Backup tutorial ensure that you have
proper backups of your databases and configuration files. Read through this
section carefully and verify that you have the requisite backups to restore.

Note : The backup tutorial reference file only updated to Juno, DB backup
operation will be similar for Kilo. The link will be updated when the reference
has updated.

For more information and examples about downgrade operation please
see Downgrade tutorial as reference.

## TODO Items Â¶

- [Done - It works!] Verify alembic works with the current SQLAlchemy model
configuration in Barbican (which was borrowed from Glance).

[Done - It works!] Verify alembic works with the current SQLAlchemy model
configuration in Barbican (which was borrowed from Glance).

- [Done - It works, I was able to add/remove columns while app was running] Verify that SQLAlchemy is tolerant of schema miss-matches. For example, if
a column is added to a table schema, will this break existing deployments
that arenât expecting this column?

[Done - It works, I was able to add/remove columns while app was running] Verify that SQLAlchemy is tolerant of schema miss-matches. For example, if
a column is added to a table schema, will this break existing deployments
that arenât expecting this column?

- [Done - It works] Add auto-migrate code to the boot up of models (see the barbican\model\repositories.py file).

[Done - It works] Add auto-migrate code to the boot up of models (see the barbican\model\repositories.py file).

- [Done - It works] Add guard in Barbican model logic to guard against
running migrations with SQLite databases.

[Done - It works] Add guard in Barbican model logic to guard against
running migrations with SQLite databases.

- Add detailed deployment steps for production, so how new nodes are rolled
in and old ones rolled out to complete move to new versions.

Add detailed deployment steps for production, so how new nodes are rolled
in and old ones rolled out to complete move to new versions.

- [In Progress] Add a best-practices checklist section to this page. This would provide guidance on safely migrating schemas, doâs and
donâts, etc. This could also provide code guidance, such as ensuring that new schema
changes (eg. that new column) arenât required for proper functionality
of the previous version of the code. If a server bounce is needed, notification guidelines to the devop team
would be spelled out here.

[In Progress] Add a best-practices checklist section to this page.

- This would provide guidance on safely migrating schemas, doâs and
donâts, etc.

This would provide guidance on safely migrating schemas, doâs and
donâts, etc.

- This could also provide code guidance, such as ensuring that new schema
changes (eg. that new column) arenât required for proper functionality
of the previous version of the code.

This could also provide code guidance, such as ensuring that new schema
changes (eg. that new column) arenât required for proper functionality
of the previous version of the code.

- If a server bounce is needed, notification guidelines to the devop team
would be spelled out here.

If a server bounce is needed, notification guidelines to the devop team
would be spelled out here.
