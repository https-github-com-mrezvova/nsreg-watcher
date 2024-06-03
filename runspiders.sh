#!/usr/bin/env bash

if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

source env/bin/activate

DATE=$(date +"%Y-%m-%d")
ERROR_LOG="$(cd "$(dirname "logs/${DATE}_grabber_errors.log")"; pwd)/$(basename "logs/${DATE}_grabber_errors.log")"
LOG_LEVEL=ERROR

echo "truncating error file:  $ERROR_LOG"
echo -n '' > $ERROR_LOG

cd src/grabber/nsreg

scrapy crawl monitor --logfile $ERROR_LOG --loglevel $LOG_LEVEL
scrapy list | awk '$1 != "monitor" {print $1}' | xargs -n 1 scrapy crawl --logfile $ERROR_LOG --loglevel $LOG_LEVEL
