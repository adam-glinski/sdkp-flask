#!/bin/sh
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

if [[ \ $*\  == *\ --clean-db\ * ]] || [[ \ $*\  == *\ -c\ * ]]; then
    echo " * Cleaning the database file."
    rm -rf ./data/sdkp.db
fi

./.venv/bin/python -m flask run
