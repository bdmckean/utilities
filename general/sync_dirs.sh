#!/bin/bash
set -x
set -v


SEARCH_DIR='.'

# sync dirs that start with number to google bucket
for file in $(find $SEARCH_DIR -type d -name '[0-9]*' ) ; do
  echo $file
done
