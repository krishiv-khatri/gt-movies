cd /home/krishiv2409/gt-movies
git pull origin main
python3.13 manage.py collectstatic --noinput
python3.13 manage.py migrate