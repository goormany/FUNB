python manage.py createsuperuser


python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver


sudo service postgresql restart

sudo -u postgres psql

CREATE DATABASE ad_board_db;

CREATE USER ad_board WITH PASSWORD 'ad_board';

ALTER ROLE ad_board SET client_encoding TO 'utf8';

ALTER ROLE ad_board SET default_transaction_isolation TO 'read committed';

ALTER ROLE ad_board SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE ad_board_db TO ad_board;

python3 manage.py collectstatic

sudo fuser -k 8000/tcp

celery -A ad_board worker -l INFO -B

git rm -r --cached /home/linux/github/Fan_Blog/ad_board/secret/SECRET_KEY.txt
