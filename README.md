# Excuela Flask API Challenge </br>by Jose Morilo👓

Boilerplate desciption

- Integrated with Pipenv for package managing.
- Fast deloyment to render.com or heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## 1) Enviroment variables

You must create an .env file with the following enviroment variables

```
DATABASE_URL=external_database_url
FLASK_APP_KEY="any key works"
FLASK_APP=src/app.py #do not change this value
FLASK_DEBUG=1
JWT_SECRET_KEY="any key works"
```

## 2) Installation

This template installs itself in a few seconds if you open it for free with Codespaces (recommended) or Gitpod.
Skip this installation steps and jump to step 2 if you decide to use any of those services.

> Important: The boiplerplate is made for python 3.10 but you can change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv shell #initialize the virtual enviroment
pipenv install;
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## 2) Folders Structure

- src/main.py (it's where the endpoints are coded)
- src/models.py (database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:

```bash
$ pipenv run migrate # (to make the migrations)
$ pipenv run upgrade  # (to update your databse with the migrations)
```

## API Endpoints

Example Requests

### Request

`POST`
`/register`

```js
HTTP Headers
Content-Type: aplication/json

Response 201

body: {
    "username": "example",
    "email": "example@email.com",
    "password": "example12345"
}

```

### Request

`POST`
`/login`

```js
HTTP Headers
Content-Type: aplication/json

body: {
    "email": "example@email.com",
    "password": "example12345"
}

Response 201

"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJmcmVzaC
6ZmFsc2UsImlhdCI6MTcxOTk0NjczNywianRpIjoiNWQ3MT
dhOTEtNzljMi00YjFkLWEwZTgtZDZiODFiYWVhMWMxIiwid
HlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzE5OTQ2
NzM3LCJjc3JmIjoiZTcwYmNiM2UtZDAwOC00NWFmLWFhMWM
tMzcwZWQxYzgxNGI4IiwiZXhwIjoxNzE5OTQ3NjM3fQUkkE
rZvFd906kXLpIioUGLbVo6VpfKf5nPRZqrc2UE8"
```

### Request

`GET, PUT, DELETE `
`/user`

### GET

```js
HTTP Headers
Content-Type: aplication/json
Authorization: Bearer

Response 200

{
  "created": "Tue, 02 Jul 2024 17:04:39 GMT",
  "email": "test@email.com",
  "id": 1,
  "username": "jose"
}
```

### PUT

```js
HTTP Headers
Content-Type: aplication/json
Authorization: Bearer

body: {
  "email": "test@email.com",
  "username": "jose"
}

Response 200
```

### DELETE

```js
HTTP Headers
Content-Type: aplication/json
Authorization: Bearer

Response 200
```

## Check your API live

1. Once you run the `pipenv run start` command your API will start running live and you can open it by clicking in the "ports" tab and then clicking "open browser".

> ✋ If you are working on a coding cloud like [Codespaces](https://docs.github.com/en/codespaces/developing-in-codespaces/forwarding-ports-in-your-codespace#sharing-a-port) or [Gitpod](https://www.gitpod.io/docs/configure/workspaces/ports#configure-port-visibility) make sure that your forwared port is public.
