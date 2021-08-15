## Kitesurfing School Management Webapp


**Used:**
* Python 3.6.9
* Django 3.2.5
* Currently working with built-in SQLite for convenience, will be switching to PostgreSQL in near future

**Run:**

1. Navigate to root directory where manage.py lives
2. Add environment variable

    ``` export DJANGO_DEVELOPMENT=True ```

4. Create secrets.json file with your settings or set them manually in settings.py:

    ```json
    {
      "SECRET_KEY": "<your_key>",
      "DB_PASSWORD": "<pswd>",
      "EMAIL_HOST_USER": "<whatever>",
      "EMAIL_HOST_PASS": "<whatever>"
    }
    ```

4. ``` pip install -r requirements.txt ```
5. ``` python manage.py makemigrations ```
6. ``` python manage.py migrate ```
7. ``` python manage.py createsuperuser ```
8. Have fun


DEPLOY
======

Create envs dir:

      $ mkdir .envs

Copy envs from example.envs:

      $ cp example.envs .envs/.develop
   
Build project:

      $ docker-compose build

Run 

      $ docker-compose up
   
App run on:

      http://0.0.0.0:8000


COMMANDS
========

Make migrations:

      $ docker-compose run --rm app python manage.py makemigrations

Migrate:

      $ docker-compose run --rm app python manage.py migrate

Any manage.py command:

      $ docker-compose run --rm app python manage.py <ur_manage_py_command>

Shut down:

      $ docker-compose down --remove-orphans

Yolo Shut down (remove DB data):

      $ docker-compose down --volume --remove-orphans

Black format:

      $ black -S --config black.conf app/