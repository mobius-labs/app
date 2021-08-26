# Backend Documentation
Below is a short guide on how to install and set up Django and PostgreSQL. This is only the initial setup and does not include integrating Vue or REST.

There are two different ways to go about setting up Django. I recommend setting up through PyCharm but if you prefer Visual Studio Code and doing everything in the terminal feel free to do the second way. 

## Option 1: Through PyCharm (Recommended)

1. Download PyCharm Professional edition. As students you can get it for free in a matter of minutes. Just go to this link  and click ‘Apply Now’ and follow the steps.

2. Open PyCharm and click get from VCS and enter https://github.com/mobius-labs/backend.git  as the git URL to clone the repository.

3. Create a new Virtual Environment (I am unsure if PyCharm will prompt you to do this in step 2)

4. To install the same software as I have run pip install -r requirements.txt in your terminal within this Virtual Environment. 

5. Now try running the server with the following command python3 manage.py runserver. If the server runs Django should be installed correctly.

## Option 2: Setup Django Through Terminal 

1. Clone the repository backed https://github.com/mobius-labs/backend.git 

2. Create a new Virtual Environment with virtualenv .venv  and then open it with source .venv/bin/activate.

3. To install the same software as I have run pip install -r requirements.txt in your terminal within this Virtual Environment. 

4. Now try running the server with the following command python3 manage.py runserver. If the server runs Django should be installed correctly.
