#!/bin/bash
if [[ $# -eq 3 ]] ; then
    export count=0
    while ./single_smart_evaluate.sh $1 $2 $3 $count; do (( count++ )) ; done
elif [[ $# -eq 4 && ${!#} == "--dry-run" ]]; then
    ./single_smart_evaluate.sh $1 $2 $3 0 --dry-run
else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <task>  <MODEL>                <MODEL_TAG>             (--dry-run)\n\
E.g. ./$(basename "$0")  Q8     universal_transformer  base_test-loss-0001-2020-06-21 \n"
fi
