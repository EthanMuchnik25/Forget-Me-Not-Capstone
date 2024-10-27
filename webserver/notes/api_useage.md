# API Useage Documentation


## HTML pages

### `/`
`Type: GET`\
This is the home page. Querying this endpoint will return `index.html`, which will redirect the user to the appropriate page depending if they are authenticated or not.

### `/img_search.html`
`Type: GET`

This is the page where the user can search for their images.

### `/login.html`
`Type: GET`

This is the page where the user logs into their account.

### `/register.html`
`Type: GET`

This is the page where the user can register an account.

## Authentication

### Note:
Endpoints that require authentication will return an HTTP code in the 200-range if they are successful, and an error code in the 400-range if they are not

### `/login`
`Type: POST`

This endpoint is used to gain an authentication token, to be used in future authenticated requests.\
You must have `'username'` and `'password'` fields in the request body, with containing the username and password you wish to login with. Upon success, this will return a response with your token in response body field `access_token`.

See example of use in `login.html`.\ 
For examples in a python script, check the `reauthenticate()` function in `raspi-scripts/raspi_runtime/img_send/img_send.py`

### `/register`
`Type: POST`

This endpoint is used to register an account.\
You must have `'username'` and `'password'` fields in the request body, with containing the username and password you wish to login with.

See example of use in `register.html`.

### `/logout`
`Type: POST`\
`@requires authentication`

This endpoint is used to log out of your account.\
Currently, calling this will invalidate the current token use to authenticate this request.

Cameras will still need to store their usernames/passwords in plaintext and be prepared to reauthenticate when necessary, as token issuing currently does have an expiration date.

See example of use in `img_search.html`

### `/deregister`
`Type: POST`\
`@requires authentication`

This endpoint is used to deregister a user.\
All of the user's data is wiped upon calling this endpoint.

### `/test_auth`
`Type: GET`\
`@requires authentication`

This endpoint can be used to test if you are authenticated or not. 

## Image querying

### `/text_query`
`Type: GET`\
`@requires authentication`

This api is used to submit a text query for the user.\
Currently, this query should contain only the word for the category of the object the user is looking for. This should have `query` and `index` as parameters in its URL, with `query` containing the name of the object, and `index` specifying, "I would like to see the `index`th most recent occurence of this item.\

This returns a response with a body field `success`, which contains whether the object was successfully found.\
On failure, a field called `message` contains the cause of error.\
On success, a field called `imageUrl` contains a url to the image.\

**NOTE!!!** This is different from how the other APIs pass arguments!!\
**NOTE 2!!!** This endpoint will likely change when we change the frontend.

See example of use in `img_search.html`
<!-- TODO this currently puts arguments in the url, probably change for consistency -->

### `/get_room_img`
`Type: GET`\
`@requires authentication`

This api is used to get the image from a url provided to the user.\
You should never manually call this api. The url to the image provided by `/text_query` should point to this endpoint, just make sure to add the appropriate authentication when invoking this URL.

See example of use in `img_search.html`

### `/post_img`
`Type: POST`\
`@requires authentication`

This endpoint is used by the raspberry pi to send an image to an account's storage. It can also be used by non-raspberry-pi devices.\
This request should contain a file, called `file`.

See example of use in `raspi-scripts/raspi_runtime/img_send/img_send.py`



###  `/get_username`
`Type: GET`\
`@requires authentication`

This endpoint simply returns the username associated with a token.\
The response has a parameter called `username` in its body.