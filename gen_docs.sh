cd docs
sphinx-apidoc -o . ../src --module-first --separate
make $1
cd ..
