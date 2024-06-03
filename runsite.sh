#!/usr/bin/env bash

if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

source env/bin/activate

python src/website/manage.py migrate
python src/website/manage.py runserver
