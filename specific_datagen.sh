#!/bin/bash
if [[ $# -eq 1 ]] ; then
    ./smart_datagen.sh $1 True
elif [[ $# -eq 2 && $2 == "--dry-run" ]]; then
    ./smart_datagen.sh $1 True --dry-run
else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <DATA_DIR>  (--dry-run)\n\
E.g. ./$(basename "$0")  t2t-data\n"
fi
