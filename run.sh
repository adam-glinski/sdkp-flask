#!/bin/sh
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Create the directory
mkdir data

if [[ \ $*\  == *\ --clean-db\ * ]] || [[ \ $*\  == *\ -c\ * ]]; then
    echo " * Cleaning the database file."
    rm -rf ./data/sdkp.db
fi

if [[ \ $*\  == *\ --backend\ * ]] || [[ \ $*\  == *\ -b\ * ]]; then
    echo " * Running just backend code."
    ./.venv/bin/python ./backend/tester.py
fi

./.venv/bin/python -m flask run
