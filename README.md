# Backend Documentation
Below is a short guide on how to install and set up Django and PostgreSQL. This is only the initial setup and does not include integrating Vue or REST.

There are two different ways to go about setting up Django. I recommend setting up through PyCharm but if you prefer Visual Studio Code and doing everything in the terminal feel free to do the second way. 

## PART 1 - INITIAL SETUP

### Option 1: Through PyCharm (Recommended)

1. Download PyCharm Professional edition. As students you can get it for free in a matter of minutes. Just go to this link  and click ‘Apply Now’ and follow the steps.

2. Open PyCharm and click get from VCS and enter https://github.com/mobius-labs/backend.git  as the git URL to clone the repository.

3. Create a new Virtual Environment (I am unsure if PyCharm will prompt you to do this in step 2)

4. To install the same software as I have run pip install -r requirements.txt in your terminal within this Virtual Environment. 

5. Now try running the server with the following command python3 manage.py runserver. If the server runs Django should be installed correctly.

### Option 2: Setup Django Through Terminal 

1. Clone the repository backed https://github.com/mobius-labs/backend.git 

2. Create a new Virtual Environment with virtualenv .venv  and then open it with source .venv/bin/activate.

3. To install the same software as I have run pip install -r requirements.txt in your terminal within this Virtual Environment. 

4. Now try running the server with the following command python3 manage.py runserver. If the server runs Django should be installed correctly.


## PART 2 - POSTGRES SETUP

In the settings.py file you will notice the following dictionary:

```

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_db',
        'USER': 'postgres',
        'PASSWORD': 'mobius',
        'HOST': 'localhost',
        'PORT': '',
         # From: https://devcenter.heroku.com/articles/python-concurrency-and-database-connections
         # Constantly opening new connections is an expensive operation, and
         # can be mitigated with the use Django’s persistent connections.
        'CONN_MAX_AGE': 500
    }
}
```
Do the following to set up postgres:

1. Install postgres either from your terminal if you are on a mac (brew install postgresql) or from their website https://www.postgresql.org/

2. You want to create a database and match its name to the name in the dictionary above (here it is called 'test_db). Also you want to match your postresql username and password with the dictionary above. For now, it is probably best to keep this consistent with the names above.
  
  2.1. To create a database you can either use pgAdmin 4, which is a GUI to interact with postgres databases, or you can use the postgres terminal and run
  > CREATE DATABASE test_db;
