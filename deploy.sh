#/bin/sh

cd "${0%/*}"
git pull
poetry shell
poetry install
pucadmin/manage.py migrate
pucadmin/manage.py collectstatic --noinput
touch RELOAD
