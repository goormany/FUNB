#!/bin/bash
source /home/linux/github/venv/bin/activate
cd /home/linux/github/Fan_Blog/ad_board
exec celery -A ad_board worker -l INFO -B
