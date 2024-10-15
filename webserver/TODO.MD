# Webserver TODO

This hopes to document some of the things we probably eventually have to get sorted out


### Objective: Get a bunch of useful mocks up and running
- mock out YOLO so we know what to send to the database
- Get a dumb website with just a query field and an image response/text field up and running
- Make a mock raspi for local testing purposes [will likely require some additional web dev knowledge]
  - image workflow
  - mic/recieve workflow


### Objective: Get a fully functional system up and running
- Design decisions cleared up
  - database remote/local, sql/nosql, 
- Docker containerize app, we have made modularity a priority
- Database solidified and implemented
- Make a website that looks nice
- Structure our whole website - home page, login, auth, eventually our other webpage

### Website: user flow
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


### Cloud: Get Learnt
- Is the amazon database accessible the same way from any machine?
- Will we have to change how our app is set up to get it deployed on a cloud machine? Do we have to buy a domain? Do just have an IP address? 
- If we get really ahead of ourselves, We can test scalability


### Raspi: Get testing
- Could we literally run the whole system on a raspberry pi?

### Ensure file diagram in README.MD are up to date
- do it

### Update the things in the top level readme

### Isolate install instructions from run instructions


## Personal notes dump
#### Useful sites:
nginx beginners guide: http://nginx.org/en/docs/beginners_guide.html\
flask mega tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux\
flask quickstart: https://flask.palletsprojects.com/en/3.0.x/quickstart/\
bottom text




