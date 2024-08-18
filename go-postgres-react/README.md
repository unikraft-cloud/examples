# go-postgres-react

This is for creating a Contacts application with the following components:

- [x] a Golang backend
- [x] a Postgresql database for saving data
      -- the corresponding Volume for persistent storage
- [] a react frontend app for serving the UI

## Create a volume and deploy postgresql

```console
$ cd github.com/kraftcloud/examples/postgres

github.com/kraftcloud/examples/postgres$ kraft cloud volume create --name postgres --size 200

github.com/kraftcloud/examples/postgres$ kraft cloud deploy --metro fra0 -M 1024 -e POSTGRES_PASSWORD=unikraft -e PGDATA=/volume/postgres -v postgres:/volume -p 5432:5432/tls .
(Search for `service group` in the output)

# Port-forward postgresql to localhost
github.com/kraftcloud/examples/postgres$ kraft cloud tunnel <SERVICE_GROUP_FROM_ABOVE> 5432:5432


$ psql -U postgres -h localhost
Password for user postgres: unikraft
psql (16.2)
Type "help" for help.

postgres=# CREATE TABLE contacts (id SERIAL PRIMARY KEY, name TEXT, email TEXT);
CREATE TABLE
postgres=#


```

## Deploy the backend:

```console
github.com/kraftcloud/examples/go-postgres-react/go$ kraft cloud deploy --metro fra0 -p 443:8080 .
(Search for `domain` in the output)

# Ensure that the backend API works fine by talking to the db

# Empty response first
$ curl -vv https://DOMAIN_FROM_ABOVE.fra0.kraft.host/contacts
null

# Create contact next
$ curl -v https://DOMAIN_FROM_ABOVE.fra0.kraft.host/contacts -d '{ "name": "example1", "email": "one@example.com" }'

# Ensure the new contact is saved and retrieved from db via the backend
$ curl https://DOMAIN_FROM_ABOVE.fra0.kraft.host/contacts
[{"name":"example1","email":"one@example.com"}]

# Above backend API confirms data is saved, but let us check in DB also
$ psql -U postgres -h localhost
Password for user postgres: unikraft
psql (16.2)
Type "help" for help.

postgres=# select * from contacts;
 id |   name   |      email
----+----------+-----------------
  1 | example1 | one@example.com
(1 row)

postgres=#

```
