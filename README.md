## Kitesurfing School Management Webapp


**Used:**
* Python 3.6.9
* Django 3.1.2
* Currently working with built-in SQLite for convenience, will be switching to PostgreSQL in near future

**Run:**

1. Navigate to root directory where manage.py lives
2. Add environment variable

    ``` export DJANGO_DEVELOPMENT=True ```

4. Create secrets.json file containing:

    ```json
    {"SECRET_KEY": "<your_key>"}
    ```
    
4. ``` pip install requirements.txt ```
5. ``` python manage.py makemigrations ```
6. ``` python manage.py migrate ```
7. ``` python manage.py createsuperuser ```
8. Have fun
