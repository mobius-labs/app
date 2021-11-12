# Möbius Labs

🖥️ Access the deployed site on [Heroku](https://mobius-labs-crm.herokuapp.com/).

📄 View our [Confluence space](https://mobius-labs.atlassian.net/wiki/spaces/MLH/overview) for higher-level documentation, architecture and UI design, and project management.

## Table of contents

📖 Read some in-repo documentation inside the [docs](docs/) directory:
  - [docs/assets.md](docs/assets.md) - handling assets (images, fonts, icons, etc...)
  - [docs/code_quality.md](docs/code_quality.md) - maintaining code quality
  - [docs/deployment.md](docs/deployment.md) - how to deploy the application yourself

There's also significant getting-started documentation in the rest of this README.

## Repository structure

Since both the frontend and backend of our app lives in this monorepo, there are some Django (Python)
parts and some Vue.js (JavaScript) parts intertwined together.
Here is a brief overview of the repository structure:

```
                        BACKEND
                        --------
apps/                   Django "apps" correspond to modules of our backend
apps/account/           User registration/authentication backend
apps/contact_book/      Contacts/business cards backend
backend_crm/            Overall backend configuration
manage.py               Django CLI command
requirements.txt        Python dependencies for our application


                        FRONTEND
                        ---------
frontend/               Frontend Vue.js application
frontend/package.json   Specifies all dependencies for the frontend
frontend/src/           Vue app
frontend/public/        Static files to include in the app


                        DEPLOYMENT & CI
                        ---------
package.json            A stub which is used for CI/CD, forwards everything to `frontend` directory 
Procfile                Tells Heroku how to run our application
app.json                Specifies default env-vars for Heroku
```

## Running locally

Here are some of the main technologies used in our app:

#![Technologies used](docs/stack.png)

To get started, we assume you have Python 3.9, Node 16 / npm 8, and Postgresql already installed.

Also in the following commands, we assume `python` refers to Python 3, not Python 2 (on some machines, you may have to explicitly write `python3` instead)

1. First step is to clone this Git repository (https://github.com/mobius-labs/app.git) using the tool of your choice.
   
   If you're using PyCharm, click "get from VCS" and enter https://github.com/mobius-labs/app.git as the Git URL.

2. Create a Python virtual environment

   PyCharm may prompt you to do this automatically, or you can the [instructions](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html).

   Alternatively, through the cmdline, run `python -m venv .venv`  and then activate the virtual environment with `source .venv/bin/activate`.

3. Next we need to install dependencies for both the frontend and backend.

   For the backend, run `pip install -r requirements.txt`.

   For the frontend, run `(cd frontend && npm install)` (the brackets here create a *subshell* so your working directory stays in the project root after installing deps)

4. We need to get Django connected to a database.

    In [settings.py](backend_crm/settings.py) you will notice default environment variable:

    ```
    DATABASE_URL=pgsql://postgres:mobius@localhost/test_db
    ```

    This specifies to connect to a Postgres database named `test_db` with host `localhost`, authenticating with user `postgres` and password `mobius`.
    Now we need to set up postgres so Django can connect.

    Do the following to setup postgres:

   1. Install Postgresql on your computer (if you use Homebrew on a Mac, then: `brew install postgresql`, or alternatively follow the instructions for your system on the [Postgres  website](https://www.postgresql.org/))

   2. Now we will create a database. For now, lets call it `test_db` to match with the dictionary above. You can change it to whatever name as long as you change it in the dictionary too, but for the simplicity of git commits, lets stay with 'test_db for now.
      You can either create a database in pgAdmin4 (a postgres GUI), or with the postgres terminal. To create in terminal run:

    ```
    $ psql -U postgres                 # note here 'postgres' is our username
    > CREATE DATABASE test_db
    ```

   3. Then we need to initialize a Django with the postgres database we just created. We can do so by running:
    ```
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ```
   
5. For the frontend, you can either use the Vue.js (`(cd frontend && npm run serve)`), or build the assets for production and let Django handle them.
   
   For the latter, run `(cd frontend && npm run build) && python manage.py collectstatic`. Then Django will look after serving frontend files.

6. To start a local server for testing, run
    
    ```
    $ python manage.py runserver
    ```
   
    If you're working the frontend, it may be useful to use the Vue.js dev-server as well.

    Run `(cd frontend && npm run serve)`, to start up a separate development server with live-reloading (but it will still talk to the same local backend server when making API calls).

## Editors & tooling

Recommended editors:

- PyCharm Professional Edition with the Vue.js extension,
- VS Code (with the [Vetur](https://vuejs.github.io/vetur/) extension for Vue.js).

There is a Chrome/Firefox extension which lets you debug a Vue.js application more easily:
https://devtools.vuejs.org/guide/installation.html#settings

You can also setup PyCharm / VS Code / other editor with ESLint integration, so that errors and warnings appear while editing:
https://eslint.vuejs.org/user-guide/#editor-integrations

## Running tests

To run Django unit tests, run:

```
> python manage.py test
```
To see Python unit test code coverage, run:
```
> python -m coverage run --source=apps --branch manage.py test
> coverage report
```

To run frontend unit tests:

```
> cd frontend && npm run test:unit
```

To run integration tests (you'll need to have the backend dev-server running with `python manage.py runserver` as well):

```
> cd frontend && npm run test:e2e
```