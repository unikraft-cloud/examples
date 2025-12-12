# Prisma

This app comes from [Prisma's REST API Example](https://github.com/prisma/prisma-examples/tree/latest/javascript/rest-express) and shows how to create a **REST API** using [Express](https://expressjs.com/) and [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client) and deploy it onto Unikraft Cloud.
It uses a SQLite database file with some initial dummy data which you can find at [`./prisma/store.db`](./prisma/store.db).
 To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node18-prisma-rest-express/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node18-prisma-rest-express/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -M 512 -p 443:3000 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: node18-prisma-hdof1
 ├────────── uuid: 066f55cb-bcbd-45e5-9f6b-b3866c3a3a4c
 ├───────── state: running
 ├─────────── url: https://funky-sun-4bf8v7g9.fra.unikraft.app
 ├───────── image: node18-prisma@sha256:770d4af1d490daea11171c680eaf99e2a6017a262ba9fbf1ba8d708f5fc32bfe
 ├───── boot time: 37.94 ms
 ├──────── memory: 512 MiB
 ├─────── service: funky-sun-4bf8v7g9
 ├── private fqdn: node18-prisma-hdof1.internal
 ├──── private ip: 172.16.28.2
 └────────── args: /usr/bin/node /usr/src/server.js
```

In this case, the instance name is `node18-prisma-hdof1` and the address is `https://funky-sun-4bf8v7g9.fra.unikraft.app`.
They're different for each run.

Use `curl` to test the REST API, such as the `/users` endpoint:

```bash
curl https://funky-sun-4bf8v7g9.fra.unikraft.app/users
```

```json
[{"id":1,"email":"alice@prisma.io","name":"Alice"},
 {"id":2,"email":"nilu@prisma.io","name":"Nilu"},
 {"id":3,"email":"mahmoud@prisma.io","name":"Mahmoud"}]
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME                 FQDN                                 STATE    STATUS        IMAGE                   MEMORY   VCPUS  ARGS                              BOOT TIME
node18-prisma-hdof1  funky-sun-4bf8v7g9.fra.unikraft.app  running  1 minute ago  node18-prisma@sha25...  512 MiB  1      /usr/bin/node /usr/src/server.js  37935us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove node18-prisma-hdof1
```

## Using the app

You can access the REST API of the server using the following endpoints:

### Endpoints

- `GET /post/:id`: Fetch a single post by its `id`
- `GET /feed?searchString={searchString}&take={take}&skip={skip}&orderBy={orderBy}`: Fetch all _published_ posts
  - Query Parameters
    - `searchString` (optional): This filters posts by `title` or `content`
    - `take` (optional): This specifies how many objects the list should return
    - `skip` (optional): This specifies how many of the returned objects in the list to skip
    - `orderBy` (optional): The sort order for posts in either ascending or descending order. The value can either `asc` or `desc`
- `GET /user/:id/drafts`: Fetch user's drafts by their `id`
- `GET /users`: Fetch all users
- `POST /post`: Create a new post
  - Body:
    - `title: String` (required): The title of the post
    - `content: String` (optional): The content of the post
    - `authorEmail: String` (required): The email of the user that creates the post
- `POST /signup`: Create a new user
  - Body:
    - `email: String` (required): The email address of the user
    - `name: String` (optional): The name of the user
    - `postData: PostCreateInput[]` (optional): The posts of the user
- `PUT /publish/:id`: Toggle the publish value of a post by its `id`
- `PUT /post/:id/views`: Increases the `viewCount` of a `Post` by one `id`
- `DELETE /post/:id`: Delete a post by its `id`

## Evolving the app

Evolving the app typically requires two steps:

1. Migrate your database using Prisma Migrate
1. Update your app code

For the following example scenario, assume you want to add a "profile" feature to the app where users can create a profile and write a short bio about themselves.

### 1. Migrate your database using Prisma Migrate

The first step is to add a new table, for example called `Profile`, to the database.
You can do this by adding a new model to your [Prisma schema file](./prisma/schema.prisma) file and then running a migration afterward:

```diff
// ./prisma/schema.prisma

model User {
  id      Int      @default(autoincrement()) @id
  name    String?
  email   String   @unique
  posts   Post[]
+ profile Profile?
}

model Post {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  title     String
  content   String?
  published Boolean  @default(false)
  viewCount Int      @default(0)
  author    User?    @relation(fields: [authorId], references: [id])
  authorId  Int?
}

+model Profile {
+  id     Int     @default(autoincrement()) @id
+  bio    String?
+  user   User    @relation(fields: [userId], references: [id])
+  userId Int     @unique
+}
```

Once you've updated your data model, you can execute the changes against your database with the following command:

```console
npx prisma migrate dev --name add-profile
```

This adds another migration to the `prisma/migrations` directory and creates the new `Profile` table in the database.

### 2. Update your app code

You can now use your `PrismaClient` instance to perform operations against the new `Profile` table.
Those operations can create API endpoints in the REST API.

#### 2.1 Add the app programming interface endpoint to your app

Update your `src/index.js` file by adding a new endpoint to your API:

```js
app.post('/user/:id/profile', async (req, res) => {
  const { id } = req.params
  const { bio } = req.body

  const profile = await prisma.profile.create({
    data: {
      bio,
      user: {
        connect: {
          id: Number(id)
        }
      }
    }
  })

  res.send(profile)
})
```

#### 2.2 Testing out your new endpoint

Restart your app server and test out your new endpoint.

##### Create endpoint

- `/user/:id/profile`: Create a new profile based on the user id
  - Body:
    - `bio: String` : The bio of the user

Here are some more sample Prisma Client queries on the new Profile model:

##### Create a new profile for an existing user

```ts
const profile = await prisma.profile.create({
  data: {
    bio: 'Hello World',
    user: {
      connect: { email: 'alice@prisma.io' },
    },
  },
})
```

##### Create a new user with a new profile

```ts
const user = await prisma.user.create({
  data: {
    email: 'john@prisma.io',
    name: 'John',
    profile: {
      create: {
        bio: 'Hello World',
      },
    },
  },
})
```

##### Update the profile of an existing user

```ts
const userWithUpdatedProfile = await prisma.user.update({
  where: { email: 'alice@prisma.io' },
  data: {
    profile: {
      update: {
        bio: 'Hello Friends',
      },
    },
  },
})
```

## Switch to another database

If you want to try this example with another database than SQLite, you can adjust the database connection in [`prisma/schema.prisma`](./prisma/schema.prisma) by reconfiguring the `datasource` block.

Learn more about the different connection configurations in the [docs](https://www.prisma.io/docs/reference/database-reference/connection-urls).

### PostgreSQL

For PostgreSQL, the connection address has the following structure:

```prisma
datasource db {
  provider = "postgresql"
  url      = "postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=SCHEMA"
}
```

Here is an example connection string with a local PostgreSQL database:

```prisma
datasource db {
  provider = "postgresql"
  url      = "postgresql://janedoe:mypassword@localhost:5432/notesapi?schema=public"
}
```

### MySQL

For MySQL, the connection address has the following structure:

```prisma
datasource db {
  provider = "mysql"
  url      = "mysql://USER:PASSWORD@HOST:PORT/DATABASE"
}
```

Here is an example connection string with a local MySQL database:

```prisma
datasource db {
  provider = "mysql"
  url      = "mysql://janedoe:mypassword@localhost:3306/notesapi"
}
```

### Microsoft structured query language server database

Here is an example connection string with a local Microsoft SQL Server database:

```prisma
datasource db {
  provider = "sqlserver"
  url      = "sqlserver://localhost:1433;initial catalog=sample;user=sa;password=mypassword;"
}
```

### MongoDB

Here is an example connection string with a local MongoDB database:

```prisma
datasource db {
  provider = "mongodb"
  url      = "mongodb://USERNAME:PASSWORD@HOST/DATABASE?authSource=admin&retryWrites=true&w=majority"
}
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
