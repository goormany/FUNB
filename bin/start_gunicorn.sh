#!/bin/bash
source /home/linux/github/venv/bin/activate
exec gunicorn  -c "/home/linux/github/Fan_Blog/ad_board/gunicorn_config.py" ad_board.wsgi
