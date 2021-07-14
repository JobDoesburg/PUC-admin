# How to install (on CNCZ Apache with uWSGI)

0. Clone this repo in `/www/pucadmin/live/repo`
1. Create python 3.8 venv with `./env`
2. Install the dependencies in requirements.txt
3. Create settings.py:
    - `BASE_DIR = Path(__file__).resolve().parent.parent`
    - `ALLOWED_HOSTS = ['puc-admin.science.ru.nl']`
    - 
    ```DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "USER": "pucadmin_admin",
            "PASSWORD": "********",
            "NAME": "pucadmin",
            "HOST": "mysql-pucadmin.science.ru.nl",
            "PORT": "3306",
        }
    }
    ```
    - `STATIC_ROOT = BASE_DIR.parent / "static"` _this becomes `/www/pucadmin/live/repo/static`_
    - `STATIC_URL = "/static/"`
    - `MEDIA_ROOT = BASE_DIR.parent.parent / "writable" / "media"` _this becomes `/www/pucadmin/live/writable/media`_
    - `MEDIA_URL = "/media/"`
4. `touch RELOAD` to trigger uWSGI to reload the django application

Note that the webserver runs on a different machine then how you access it via lilo. The file system is mounted differently, so using relative paths is required. Also, for example, the password to access the database is different from lilo (via `manage.py`) the on real production. This requires different `settings` files. Specifically, `wsgi.py` (ran by the webserver) needs a different settings file then `manage.py` (ran on lilo).
