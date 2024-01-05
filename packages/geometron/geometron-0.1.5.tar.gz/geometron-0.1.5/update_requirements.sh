#!/bin/bash
. utils.sh

confirm "Update requirements.txt with pinned versions" "No" UPDATEREQUIREMENTS
if [[ "$UPDATEREQUIREMENTS" == "Yes" ]]; then
    pipenv requirements > requirements.txt
    git add requirements.txt
fi

pipenv requirements > docs/requirements.txt
git add docs/requirements.txt

