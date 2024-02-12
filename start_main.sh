#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then echo "Please run as root." >&2; exit 1; fi

. venv/bin/activate

nohup /opt/simplescrape2/main.sh 2>/var/log/simplescrape2/main.err >/var/log/simplescrape2/main.log &
