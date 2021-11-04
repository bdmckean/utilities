#!/bin/bash
# Gets licenses used in python repos
# Three things need to be handled manually
# Does not get modules installed with pip in dockerfiles
# (But a manual check showed that these are already covered with this process)
# Does not handle running setup.py in aii-py
# Does not handle dependency like GDAL
set -e

while IFS= read -r line
do
    repo=$line
    echo $repo
    rm -fr ~/virtualenv/temp/
    python3 -m venv ~/virtualenv/temp
    source ~/virtualenv/temp/bin/activate
    pip install --upgrade pip

    git clone git@github.com:AuroraInsight/$repo.git
    cd $repo
    # Some requirements.txt files have a prefix
    REQ_FILES=$(find . -iname '*requirements.txt')

    for i in "${REQ_FILES[@]}"
    do
            echo $i
            while IFS= read -r line
            do
            # Some lines are blank
            if [ -n "$line" ] 
            then		
                echo "$line"
                pip install ${line%==*}
            fi
            done < "$i"
            sleep 1
            echo "file done"
    done

    pip install pip-licenses

    pip-licenses --with-urls  --format=csv
    pip-licenses --with-urls  --format=csv  > ../$repo.csv

    deactivate
    cd ..
# List of repos, one per line
done < "repo_list.txt"


