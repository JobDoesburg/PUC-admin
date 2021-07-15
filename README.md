# How to install (on CNCZ Apache with uWSGI)

0. Clone this repo in `/www/pucadmin/live/repo`
1. Create python 3.8 venv with `/www/pucadmin/live/repo/env`
2. Install the dependencies in requirements.txt
3. Create `/www/pucadmin/live/repo/pucadmin/PUCadmin/settings/production.py` and `/www/pucadmin/live/repo/pucadmin/PUCadmin/settings/management.py` based on the `.example` files (set secret key and passwords).
4. `touch RELOAD` to trigger uWSGI to reload the django application

Note that the webserver runs on a different machine then how you access it via lilo. The file system is mounted differently, so using relative paths is required. Also, for example, the password to access the database is different from lilo (via `manage.py`) the on real production. This requires the different `settings` files. Specifically, `wsgi.py` (ran by the webserver) needs a different settings file then `manage.py` (ran on lilo).

To run management commands on production, first activate the python env with `source env/bin/activate` and then set an env variable to run `manage.py` with the correct settings: `export DJANGO_SETTINGS_MODULE=PUCadmin.settings.management` 


# Data minimisation
##### Competitions
Personal information from students and supervisors for competition submissions, is minimised 100 days after the competition has ended. Address, email and phone number are deleted. Name, school and the submitted document, together with the reports are kept indefinitely.

##### Questions
All personal information from students that submitted a question is deleted 30 days after the question has been marked completed. The content of the question itself and the school are stored indefinitely, but name and email are deleted. 