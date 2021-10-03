# Möbius Labs

For frontend getting-started docs, see the [frontend](frontend/README.md) directory.

For backend documentation, continue reading.

## Django setup

There are two different ways to go about setting up Django.

I recommend setting up through PyCharm but if you prefer to do everything in the terminal, feel free to do the second way.

#### Option 1: PyCharm (Recommended)

1. Download PyCharm Professional edition. As students you can get it for free in a matter of minutes. Just go to this link  and click ‘Apply Now’ and follow the steps.

2. Open PyCharm and click get from VCS and enter https://github.com/mobius-labs/app.git  as the git URL to clone the repository.

3. Create a new Virtual Environment (I am unsure if PyCharm will prompt you to do this in step 2)

4. To install the same software as I have run pip install -r requirements.txt in your terminal within this Virtual Environment. 

5. Now try running the server with the following command: `python3 manage.py runserver`. If the server runs Django should be installed correctly.

#### Option 2: Terminal 

1. Clone the repository backed https://github.com/mobius-labs/backend.git 

2. Create a new Virtual Environment with virtualenv `.venv`  and then open it with `source .venv/bin/activate`.

3. To install the same software as I have run `pip install -r requirements.txt` in your terminal within this Virtual Environment. 

4. Now try running the server with the following command `python3 manage.py runserver`. If the server runs Django should be installed correctly.

## Postgres setup

In the [.env.default](.env.default) file you will notice the following variable:

```
DATABASE_URL=pgsql://postgres:mobius@localhost/test_db
```

This specifies to connect to a Postgres database named `test_db` with host `localhost`, authenticating with user `postgres` and password `mobius`.
Now we need to set up postgres so Django can connect.

Do the following to setup postgres:

1. Install postgres on your computer (if you use Homebrew on a Mac, then: `brew install postgresql`, or alternatively follow the instructions for your system on the [Postgres  website](https://www.postgresql.org/))

2. Now we will create a database. For now, lets call it `test_db` to match with the dictionary above. You can change it to whatever name as long as you change it in the dictionary too, but for the simplicity of git commits, lets stay with 'test_db for now.
   You can either create a database in pgAdmin4 (a postgres GUI), or with the postgres terminal. To create in terminal run:

```
> psql -U postgres                 # note here 'postgres' is our username
> CREATE DATABASE test_db
```

3. Then we need to initialize a Django with the postgres database we just created. We can do so by running:
```
> python manage.py migrate
> python manage.py createsuperuser
```