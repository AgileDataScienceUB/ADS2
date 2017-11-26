# Web application skeleton based on: flask-angular2-starter

Starter app with a simple flask backend, and an Angular2 frontend. Somewhat opinionated. Full docker support, webpack, hot module reload, and more.

## Application Structure

`/src/server` directory contains the flask backend with simple authentication methods

`/src/client` directory contains the angular2 frontend based on  [angular-webpack-starter](https://github.com/AngularClass/angular2-webpack-starter)

### Running locally

#### Flask Backend

Install necessary Python modules:

```bash
cd src/server
sudo pip install -r requirements.txt
```

Then start the app locally:

    python manage.py runserver

Or start the app through your IDE, using the same manage.py command or by invoking app.py run() directly.

To test the Flask API manually, navigate to http://localhost:8081/api/test

Also, you can check the data is correctly served by accesing: http://localhost:8081/api/flats_rental/neighborhoods

#### AngularJS Frontend

All the dependencies have been added from CDN so it does not require any installation

Just execute:
```bash
cd src/client
 python -m SimpleHTTPServer --port=8081   (In Unix)
 python http.server 8081       (In Windows)
```

To have the app accessible in your browser at: http://localhost:8081/



