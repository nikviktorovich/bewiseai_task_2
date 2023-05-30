# Overview
This is a test task #2 from _bewise.ai_ company

# Installation and deployment
To install and deploy this project you'll need Docker (`https://docs.docker.com/engine/install/`).

The first step is cloning the repository:
```bash
git clone https://github.com/nikviktorovich/bewiseai_task_2.git
cd bewiseai_task_2
```

The next step is running `docker compose`:
```bash
POSTGRES_DB=bewiseaidb \
POSTGRES_USER=testuser \
POSTGRES_PASSWORD=testuser \
docker compose up -d
```

Another options is to store the environment variables inside, for example, `.env` file. 
In this case, the command above will look like this:
```bash
docker compose --env-file .env up -d
```

...and `.env` file would look like this:
```
POSTGRES_DB=bewiseaidb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testuser
```

And this is pretty much it! After succesful deployment you can navigate to `http://127.0.0.1:8000/docs` in your browser and use the interactive documentation. As an alternative option, you might wanna use CLI tools, for example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"username": "someusername"}'
```

To stop and remove the containers use:
```bash
docker compose down
```

# Endpoints
## __`/users`__
### Overview
This endpoint allows to create a new user by username

### Methods
__`POST`__

Request JSON Schema:
```
{
    "username": string
}
```

Example JSON request:
```json
{
    "username": "someusername"
}
```

Response JSON Schema:
```
{
    "username": string,
    "id": integer,
    "access_token": string
}
```

Example JSON response:
```json
{
    "username": "someusername",
    "id": 10,
    "access_token": "f81f82654aa3454698787966877c75f9"
}
```


## __`/record`__
### Overview
This endpoint allows to convert and download converted audio.

### Methods
__`GET`__

Query URL parameters:
- `id` - Audio UUID indentifier
- `user` - User ID
- `access_token` - User UUID access token (originally, task requires only user id, but since it doesn't make much sense I decided to add access_token param as well)

Response:
- Binary audio file with content type `audio/mpeg`

__`POST`__

Query URL parameters:
- `user` - User ID
- `access_token` - User UUID access token

Body content:
- `audio` - Binary wav-audio file with content type either `audio/wav` or `audio/x-wav`

Response JSON Schema:
```
{
    "uuid": string,
    "user_id": integer,
    "audio_url": string
}
```

Example JSON response:
```json
{
    "uuid": "125872f44b8f484187989eb7dca5f051",
    "user_id": 10,
    "audio_url": "http://127.0.0.1:8000/record/?id=125872f44b8f484187989eb7dca5f051&user=10&access_token=f81f82654aa3454698787966877c75f9"
}
```


# Database
## Tables
### `users`
#### Overview
This table contains information about created users

#### Fields
- `id` - Integer (autoincrement), primary key
- `username` - Varchar (string), unique
- `access_token` - UUID, unique

### `audio`
#### Overview
This table contains information about saved audio

#### Fields
- `uuid` - UUID, primary key
- `user_id` - Integer, not null, foreign key
