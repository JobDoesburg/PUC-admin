# How to install (on CNCZ Apache with uWSGI)

0. Clone this repo in `/www/pucadmin/live/repo`
1. Create python 3.8 venv with `/www/pucadmin/live/repo/env`
2. Install the dependencies in requirements.txt
3. Create `/www/pucadmin/live/repo/pucadmin/PUCadmin/settings/production.py` and `/www/pucadmin/live/repo/pucadmin/PUCadmin/settings/management.py` based on the `.example` files (set secret key and passwords).
4. `touch RELOAD` to trigger uWSGI to reload the django application

Note that the webserver runs on a different machine then how you access it via lilo. The file system is mounted differently, so using relative paths is required. Also, for example, the password to access the database is different from lilo (via `manage.py`) the on real production. This requires the different `settings` files. Specifically, `wsgi.py` (ran by the webserver) needs a different settings file then `manage.py` (ran on lilo).

To run management commands on production, first activate the python env with `source env/bin/activate` and then set an env variable to run `manage.py` with the correct settings: `export DJANGO_SETTINGS_MODULE=PUCadmin.settings.management` 