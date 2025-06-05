$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# Create the data directory if it doesn't exist
if (-not (Test-Path -Path "./data")) {
    New-Item -ItemType Directory -Path "./data" | Out-Null
}

# Check for --clean-db or -c
if ($args -contains "--clean-db" -or $args -contains "-c") {
    Write-Host " * Cleaning the database file."
    Remove-Item -Force -ErrorAction SilentlyContinue "./data/sdkp.db"
}

# Check for --backend or -b
if ($args -contains "--backend" -or $args -contains "-b") {
    # Write-Host " * Running just backend code."
    & .\.venv\Scripts\python.exe "src\backend\tester.py"
} else {
# Run the Flask app
    & .\.venv\Scripts\python.exe -m flask run
}

