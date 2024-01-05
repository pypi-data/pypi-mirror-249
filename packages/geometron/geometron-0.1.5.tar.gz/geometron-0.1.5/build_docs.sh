CWD="${PWD}"  # project directory
DCD="$CWD/docs"
ULD="$CWD/uml_diagrams"

. create_favicon.sh
. test_code.sh
cp "$CWD/definitions.py" "$DCD/source/definitions.py" # for publication on https://readthedocs.org
cd "$ULD" || exit 1
python3 update_uml_in_docs.py
cd "$DCD" || exit 1
make html
cd "$CWD" || exit 1
firefox "file://$DCD/build/html/index.html"
. update_requirements.sh

git add "$DCD/*"
git commit -m "Build docs"
git push

. push_docs.sh
