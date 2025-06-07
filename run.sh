#!/bin/sh
FLASK_APP="src/app.py"
FLASK_ENV=development
FLASK_DEBUG=1

mkdir -p data

if [[ \ $*\  == *\ --clean-db\ * ]] || [[ \ $*\  == *\ -c\ * ]]; then
    echo " * Cleaning the database file."
    rm -rf ./data/sdkp.db
fi

if [[ \ $*\  == *\ --backend\ * ]] || [[ \ $*\  == *\ -b\ * ]]; then
    ./.venv/bin/python src/backend/tester.py
else
    flask --app "src/app.py" run 
fi

