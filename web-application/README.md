# Web application skeleton based on: flask-angular2-starter

Starter app with a simple flask backend, and an Angular2 frontend. Somewhat opinionated. Full docker support, webpack, hot module reload, and more.

## Application Structure

`/src/server` directory contains the flask backend with simple authentication methods

`/src/client` directory contains the angular2 frontend based on  [angular-webpack-starter](https://github.com/AngularClass/angular2-webpack-starter)

## Setup Instructions

Clone the repo

```bash
git clone --depth 1 https://github.com/cacois/flask-angular2-starter.git
cd flask-angular2-starter
```

Set your local env variable FLASK_CONFIGURATION to "development" if you plan on using Docker or command line:

```bash
export FLASK_CONFIGURATION=development
```

Or set it to "ide_development" if you are using an IDE with step-through debugger:

```bash
export FLASK_CONFIGURATION=ide_development
```

### Running using Docker

The app runs in two Docker containers, one for the Flask server, and one for the Angular2 client. Use docker-compose to build and stand up both containers:

```bash
docker-compose up
```

Note: The FLASK_CONFIGURATION environment variable will be picked up from your host machine and passed through to the Flask container, setting the server configuration mode.

To build only the flask server container:

```bash
docker-compose build server
```

To build only the angular2 container:

```bash
docker-compose build client
```

To run the flask server container:

```bash
docker-compose up server
```

To run the angular2 container:

```bash
docker-compose up client
```

To connect to a running container:
```bash
docker exec -it server /bin/sh
```
or
```bash
docker exec -it client /bin/sh
```

### Running locally

#### Flask Backend

Install necessary Python modules:

```bash
cd src/server
sudo pip install -r requirements.txt
```

First initialize the database and put in some test data (including an admin user):

    python manage.py initdb
    python manage.py insert_data

Then start the app locally:

    python manage.py runserver

Or start the app through your IDE, using the same manage.py command or by invoking app.py run() directly.

To test the Flask API manually, navigate to http://localhost:8081/api/test

#### Angular2 Frontend

All the dependencies have been added from CDN

    python -m SimpleHTTPServer

