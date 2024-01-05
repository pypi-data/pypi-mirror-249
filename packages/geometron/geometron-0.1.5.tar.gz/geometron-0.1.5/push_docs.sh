#!/bin/bash
. utils.sh

confirm "Update the docs on the html server" "Yes" READY
if [[ "$READY" == "Yes" ]]; then
    echo -e "Copying html files to the server..."
    scp -r -P 65432 ./docs/build/html/* root@gfa-server.umons.ac.be:/root/docker/apache-geometron-app/htdocs/geometron/
else
    echo -e "OK."
fi
