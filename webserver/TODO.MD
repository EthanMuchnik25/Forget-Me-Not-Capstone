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

### ***After making the initial draft, further website discussion
- Would be helpful to clarify a couple of details on how the workflow should work
  - For our cloud backend we need some way to authenticate. Should we add authentication to the local version as well?
  - Does anyone know a common way that usernames and passwords are stored?
  - How is session stored?
  - -> For self, sean will probably be useful for this
- What pages do we need? Home page? Login? Our webpage
- I am trash at UI. A few more sketches would be helpful

### Webserver refactoring
- refactor the way recommended by chattyg
- add necessary responses for website to work

### Ensure file diagram in README.MD are up to date
- do it

## Personal notes dump
#### Useful sites:
nginx beginners guide: http://nginx.org/en/docs/beginners_guide.html\
flask mega tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux\
flask quickstart: https://flask.palletsprojects.com/en/3.0.x/quickstart/\
bottom text




