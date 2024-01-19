#!/usr/bin/env bash

if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

source env/bin/activate

ERROR_LOG="$(cd "$(dirname "logs/grabber_errors.log")"; pwd)/$(basename "logs/grabber_errors.log")"
LOG_LEVEL=ERROR
DATE=$(date +”%d-%b-%Y_%H:%M”)

echo "truncating error file:  $ERROR_LOG"
echo -n '' > $ERROR_LOG

cd src/grabber/nsreg

scrapy crawl monitor --logfile $ERROR_LOG --loglevel $LOG_LEVEL
scrapy list | awk '$1 != "monitor" {print $1}' | tr '\n' ' ' | xargs scrapy multicrawl --logfile $ERROR_LOG --loglevel $LOG_LEVEL
