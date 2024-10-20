# Webserver TODO

This hopes to document some of the things we probably eventually have to get sorted out


### Objective: Get a fully functional system up and running
- [x] Design decisions cleared up
  - [x] database remote/local, sql/nosql, 
- [x] Docker containerize app, we have made modularity a priority
- [ ] Database solidified and implemented
  - [x] Mock database made
  - [ ] Real databases implemented

### Further Dockerization
- [ ] Create Prod vs Debug dockerfile
  - Prod should just run exactly how we want
  - Debug should take in curr repository state so we don't have to edit from within the docker container, and so we don't have to keep rebuilding it

### Website: user flow
- [ ] Structure our whole website - home page, login, auth, eventually our other webpage
- How should UI look? 
 - How should we give users the option to query, and display all the info?
 - Do we want to invest time into getting a nice web framework thing to work?
- How should authentication flow?
  - Should it be present on local at all?
    - It is maybe free, we will already have the infrastructure
- How does a user register  
- Would be helpful to clarify a couple of details on how the workflow should work
  - For our cloud backend we need some way to authenticate. Should we add authentication to the local version as well?
  - Does anyone know a common way that usernames and passwords are stored?
  - How is session stored?
  - -> For self, sean will probably be useful for this
- What pages do we need? Home page? Login? Our webpage
- I am trash at UI. A few more sketches would be helpful


### Website: Increase security
- Unless we are using https, our http requests pass unencrypted over the network. To prevent this, we should use https. To use https, we should configure nginx. To configure nginx, we need an SSL. To get an ssl "for free", we can go to "Let's Encrypt" For more information go to [THIS DOCUMENT](./notes_private/chattyg_response/ssl_encrypt.md)
- Just to have something working, start using flask-login. I don't know how this interacts with other things, such as proposed gpu queue server.

#### Security dump

TODO: delete everything below this\
TODO: implement jwt security\
-> try not to app.config to start off\
-> create new database for users\
-> have it so that each user gets a table?\
-> have it so that all auth can be turned off\
-> create new login and register pages,\
 -> figure out how to pages automatically redirect?\
-> think about how to add authentication for the raspberry pi\
-> hash passwords appropriately, use hashed passwords appropriately\
-> appropriately change frontend so that it checks login and redirects if not,change backend to give capability of theck login (401 unauthorized response) However, login on any response of this type, fail on any other failure
-> encrypt images
-> come up with scheme to auth and keep camera authenticated
 -> no expiry? better return codes?
 -> should camera auth different to personal? Should logout personal logout camera? 
-> full debugging! 422 implies login again! see what other errors we can run into
-> standardize api results to website before poor web dev person has to implement
 -> jsonify vs not? "error" vs "msg"? error codes?

-> update documentation
-> should we have a user id field? Faster lookup?

Implementation notes:
- new login screen
- need new functionality of the database
  - to begin password database
  - associated access with user
  * add ability to check for user
  * add ability to create new user
  * add ability to get hashed password for user
  - need blacklist for bad tokens
- essentially just add the tokens to all the route functions
- isolate implementation into auth file?
- rename routes if necessary, change params if different interface necessary for actions the website wishes to accomplish


#### Misc
- Do many websites have a robot.txt? do I care?
- Make sure all http error codes make sense


notes:\
-> localStorage seems to be cookies, use to store the token in frontend \
-> document useage of localstorage for swati new frontend \
-> jwt secret key is seemingly used to hash user entries. Probably reset it upon server restart or in debug mode leave it alone?



### Cloud: Get Learnt
- Is the amazon database accessible the same way from any machine?
- Will we have to change how our app is set up to get it deployed on a cloud machine? Do we have to buy a domain? Do just have an IP address? 
- If we get really ahead of ourselves, We can test scalability


### Raspi: Get testing
- Could we literally run the whole system on a raspberry pi?


### Documentation maintenance
- [ ] Isolate install instructions from run instructions
  - Excuse: waiting for design to solidify
- [ ] Update the things in teh gop level readme
  - [ ] Ensure file diagram in README.MD are up to date
  - [ ]do it


### Design decisions
- [ ] Make a stored record for design decisions that happened
- Current list
  - jwt over flask-login due to transparency, flask uses things in a funny pythonic way
  - TODO



## Personal notes dump
#### Useful sites:
nginx beginners guide: http://nginx.org/en/docs/beginners_guide.html\
flask mega tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux\
flask quickstart: https://flask.palletsprojects.com/en/3.0.x/quickstart/\
bottom text


## Completed

### Objective: Get a bunch of useful mocks up and running
- mock out YOLO so we know what to send to the database
- Get a dumb website with just a query field and an image response/text field up and running
- Make a mock raspi for local testing purposes [will likely require some additional web dev knowledge]
  - image workflow
  - mic/recieve workflow




## Dump

TODO maybe document jwt...\\
Has fields like this, look in jwt_claims:
```
{
  "message": "You have access to this protected route!",
  "current_user": "testuser",
  "jwt_claims": {
    "exp": 1634567890,
    "iat": 1634564290,
    "jti": "1234567890abcdef",
    "identity": "testuser",
    "fresh": false,
    "type": "access"
  }
}
```
Claims can be found by doing get_jwt in flask app\
Tokens in my case can be manually blacklisted until they expire, but afterwards it is useless to keep them alive.

For unapproved response, returns "HTTP Status: 401 Unauthorized
Response: A JSON object with a message indicating the token has expired."


-> verify query works
-> authenticate sending
-> verify querying image works

** richard thomson?