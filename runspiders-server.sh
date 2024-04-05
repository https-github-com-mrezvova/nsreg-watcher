#!/usr/bin/env bash

if [ -f /home/ecodomen/ecodomen-dev/.env ]; then
  export $(echo $(cat /home/ecodomen/ecodomen-dev/.env | sed 's/#.*//g'| xargs) | envsubst)
fi

source /home/ecodomen/ecodomen-dev/env/bin/activate

ERROR_LOG="$(cd "$(dirname "logs/grabber_errors.log")"; pwd)/$(basename "logs/grabber_errors.log")"
LOG_LEVEL=ERROR
DATE=$(date +”%d-%b-%Y_%H:%M”)

echo "truncating error file:  $ERROR_LOG"
echo -n '' > $ERROR_LOG

cd /home/ecodomen/ecodomen-dev/src/grabber/nsreg

scrapy crawl monitor --logfile $ERROR_LOG --loglevel $LOG_LEVEL
scrapy list | awk '$1 != "monitor" {print $1}' | xargs -n 1 scrapy crawl --logfile $ERROR_LOG --loglevel $LOG_LEVEL

deactivate
cd ../../..
