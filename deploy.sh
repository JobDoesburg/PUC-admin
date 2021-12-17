#/bin/sh

cd "${0%/*}"
git pull
source env/bin/activate
pucadmin/manage.py migrate
pucadmin/manage.py collectstatic --noinput
touch RELOAD
