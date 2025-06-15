$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "0"

if (-not (Test-Path -Path "./data")) {
    New-Item -ItemType Directory -Path "./data" | Out-Null
}

if ($args -contains "--clean-db" -or $args -contains "-c") {
    Write-Host " * Cleaning the database file."
    Remove-Item -Force -ErrorAction SilentlyContinue "./data/sdkp.db"
}

if ($args -contains "--backend" -or $args -contains "-b") {
    # Write-Host " * Running just backend code."
    & .\.venv\Scripts\python.exe "src\backend\tester.py"
} else {
    # & .\.venv\Scripts\python.exe -m flask run
    flask --app "src/app.py" run
}

