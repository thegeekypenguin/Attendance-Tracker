# Documentation

## APIs
### Home

```js
GET   /
```

just a dummy welcome page..

### User routes

**Add a new user**

```js
POST /api/user
```

requires name, email, password and profile picture<br/>
returns json containing success field and message field

**Get user's details**

```js
GET /api/user/<userId>
```

requires userId in the url itself <br/>
returns user details or not_found

**Update any user's profile**

```js
PUT /api/user
```

requires \_id, and updated details <br/>
return json containing success field and message field

**Delete any user**

```js
DELETE /api/user/<userId>
```

requires userId in the url itself <br/>
return json containing success field and message field
