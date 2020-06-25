#!/bin/bash
if [[ $# -eq 2 ]] ; then
    ./smart_datagen.sh $1 $2 True
elif [[ $# -eq 3 && ${!#} == "--dry-run" ]]; then
    ./smart_datagen.sh $1 $2 True --dry-run
else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <DATA_DIR>  <task>  (--dry-run)\n\
E.g. ./$(basename "$0")  t2t-data    Q12\n"
fi
