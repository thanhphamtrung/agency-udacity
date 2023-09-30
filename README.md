# URL where the application is hosted
https://agency-udacity-1-701c21941a76.herokuapp.com/

## Login
https://thanhphamtrung.jp.auth0.com/authorize?
  audience=agency&
  response_type=token&
  client_id=AT1aiWyL9ncM3dH6VFtVTlJqWCgHEL8k&
  redirect_uri=https://127.0.0.1:8080/login-results

The access token will be displayed on the URL bar after login.

## THIRD-PARTY AUTHENTICATION
### RABC
- There are 3 roles 'Casting Assistant', 'Casting Director' and 'Executive Producer'.
- To get access token for 'Casting Assistant', login with account:
    - username: castingassistant377@gmail.com
    - password: Thanh123#
- To get access token for 'Casting Director', login with account:
    - username: castingdirector174@gmail.com
    - password: Thanh123#
- To get access token for 'Executive Producer', login with account:
    - username: executiveproducer90@gmail.com
    - password: Thanh123#

### auth.py
Auth0 is set up and running. The following configurations are in a setup.sh file which is exported by the app:
1. AuthError Exception: This custom exception is defined to handle authentication and authorization errors and return them as JSON responses with appropriate HTTP status codes.

2. get_token_auth_header(): This function retrieves the JWT (JSON Web Token) from the request's Authorization header. It checks if the header is present, starts with "Bearer," and contains a valid token.

3. check_permissions(permission, payload): This function checks if a given permission (scope) is included in the JWT payload's "permissions" claim. If the permission is not found, it raises an AuthError with a 403 Forbidden status.

4. verify_decode_jwt(token): This function verifies and decodes a JWT using Auth0's JSON Web Key Set (JWKS). It fetches the JWKS data from Auth0's JWKS endpoint, validates the token's signature, expiration, audience, and issuer claims, and returns the decoded payload.

5. requires_auth(permission=''): This is a decorator function used to protect specific routes in the Flask application. It takes a required permission as an argument and applies authorization checks to the wrapped route function. If the checks pass, the route function is executed with the JWT payload as an argument.

### models.py
1. Database Configuration: It configures the database using the SQLALCHEMY_DATABASE_URI provided in the environment variable DATABASE_URL. If the database does not exist, it creates it. It also disables SQLAlchemy's modification tracking to avoid unnecessary overhead.

2. Movie Model: This class represents the "movie" table in the database. It defines the fields for movie data, including id, title, and release_date. The class includes methods for inserting, updating, deleting, and formatting movie records.

3. Actor Model: This class represents the "actor" table in the database. It defines the fields for actor data, including id, name, age, and gender. Similar to the Movie model, it includes methods for inserting, updating, deleting, and formatting actor records.

## Use API
#### GET '/movies'

- Return a list of movies in database
- Sample curl:

    ```
      curl -X GET http://localhost:3000/movies -H "Authorization: Bearer ACCESS_TOKEN"
    ```

- Sample response

    ``` json
        {
            "success": true,
            "movies": [
                {
                "id": 1,
                "title": "Movie 1",
                "release_date": "2022-01-01"
                },
                {
                "id": 2,
                "title": "Movie 2",
                "release_date": "2022-02-01"
                }
            ],
            "total_movies": 2
        }

    ```

#### GET '/movies/{movie_id}'
- Get Movie by id
- Sample curl:

    ```
    curl -X GET http://localhost:3000/movies/1 -H "Authorization: Bearer ACCESS_TOKEN"
    ```

- Sample response

    ``` json
        {
            "success": true,
            "movie": {
                "id": 1,
                "title": "Movie 1",
                "release_date": "2022-01-01"
            }
        }

    ```

#### PATCH '/movies/{movie_id}'
- Update an exiting movie
- Sample curl:

    ```
        curl -X PATCH http://localhost:3000/movies/1 -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" -d '{
        "title": "Updated Movie Title"
        }'

    ```

- Sample response

    ``` json
        {
            "success": true,
            "updated_movie": {
                "id": 1,
                "title": "Updated Movie Title",
                "release_date": "2022-01-01"
            }
        }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### POST '/movies'
- Create a new movie
- Sample curl:
  
    ```
        curl -X POST http://localhost:3000/movies -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" -d '{
        "title": "New Movie",
        "release_date": "2023-01-01"
        }'
    ```

- Sample response

    ``` json
        {
            "success": true,
            "movie": {
                "id": 3,
                "title": "New Movie",
                "release_date": "2023-01-01"
            }
        }
    ```

#### DELETE '/movies/{movie_id}'
- Delete a movie 
- Sample curl:

    ```
        curl -X DELETE http://localhost:3000/movies/3 -H "Authorization: Bearer ACCESS_TOKEN"

    ```

- Sample response

    ``` json
        {
            "success": true,
            "deleted_movie_id": 3
        }
    ```

#### GET '/actors'
- Retrieve List of Actors:
- Sample curl:

    ```
    curl -X GET http://localhost:3000/actors -H "Authorization: Bearer ACCESS_TOKEN"
    ```
  
- Sample response:

    ``` json
    {
    "success": true,
    "actors": [
        {
        "id": 1,
        "name": "Actor 1",
        "age": 30,
        "gender": "Male"
        },
        {
        "id": 2,
        "name": "Actor 2",
        "age": 25,
        "gender": "Female"
        }
    ],
    "total_actors": 2
    }
    ```

#### GET '/actors/{actor_id}'
- Retrieve an Actor by ID:
- Sample curl:

    ```
    curl -X GET http://localhost:3000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN"
    ```

- Sample response:

    ``` json
    {
    "success": true,
    "actor": {
        "id": 1,
        "name": "Actor 1",
        "age": 30,
        "gender": "Male"
    }
    }
    ```

#### PATCH '/actors/{actor_id}'
- Update an Existing Actor:
- Sample curl:

    ```
    curl -X PATCH http://localhost:3000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" -d '{
  "name": "Updated Actor Name"
}'
    ```

- Sample response:

    ``` json
    {
    "success": true,
    "updated_actor": {
        "id": 1,
        "name": "Updated Actor Name",
        "age": 30,
        "gender": "Male"
    }
    }
    ```

#### POST '/actors'
- Create a New Actor:
- Sample curl

    ```
    curl -X POST http://localhost:3000/actors -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" -d '{
    "name": "New Actor",
    "age": 28,
    "gender": "Female"
    }'
    ```

- Sample response

    ``` json
    {
    "success": true,
    "actor": {
        "id": 3,
        "name": "New Actor",
        "age": 28,
        "gender": "Female"
    }
    }
    ```

#### DELETE '/actors/{actor_id}'
- Delete an actor 
- Sample curl

    ```
    curl -X DELETE http://localhost:3000/actors/3 -H "Authorization: Bearer ACCESS_TOKEN"
    ```

- Sample response

    ``` json
    {
    "success": true,
    "deleted_actor_id": 3
    }
    ```