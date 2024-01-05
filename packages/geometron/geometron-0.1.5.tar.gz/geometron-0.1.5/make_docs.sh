. utils.sh

CWD="${PWD}"  # project directory
DCD="$CWD/docs"

. create_favicon.sh
cp "$CWD/definitions.py" "$DCD/source/definitions.py" # for publication on https://readthedocs.org
cd "$DCD" || exit 1
rm -rf build/*
make html
cd "$CWD" || exit 1

firefox "file://$DCD/build/html/index.html"
