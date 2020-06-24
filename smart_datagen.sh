#!/bin/bash
if [[ $# -eq 2 ]] ; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)
    export TPU_INFO=$(gcloud compute tpus list --zone=$VM_ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)

    if [[ $VM_ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $VM_ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    else
        echo
        echo
        echo
        echo "ZONE variable is weird... ZONE = "$ZONE
        echo
        echo
        echo
    fi

    export PROBLEM=algorithmic_math_deepmind_all
    # datagen will recognise the "easy part and select only the train-easy data"
    export DATA_DIR=${STORAGE_BUCKET}/$1 # where the dataset goes
    export TMP_DIR=${STORAGE_BUCKET} # /mathematics_dataset-v1.0 -   where the data comes from
    export SPECIFIC_SPLIT=$2

    echo
    echo "Running..."
    echo "t2t-datagen \\"
    echo "  --problem=$PROBLEM \\"
    echo "  --data_dir=$DATA_DIR \\"
    echo "  --tmp_dir=$TMP_DIR \\"
    echo "  --specific_split=$SPECIFIC_SPLIT"
    echo


    t2t-datagen \
      --problem=$PROBLEM \
      --data_dir=$DATA_DIR \
      --tmp_dir=$TMP_DIR \
      --specific_split=$SPECIFIC_SPLIT


elif [[ $# -eq 3 && $3 == "--dry-run" ]]; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)
    export TPU_INFO=$(gcloud compute tpus list --zone=$VM_ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)

    if [[ $VM_ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $VM_ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    else
        echo
        echo
        echo
        echo "ZONE variable is weird... ZONE = "$ZONE
        echo
        echo
        echo
    fi

    export PROBLEM=algorithmic_math_deepmind_all
    # datagen will recognise the "easy part and select only the train-easy data"
    export DATA_DIR=${STORAGE_BUCKET}/$1
    export TMP_DIR=${STORAGE_BUCKET}
    export SPECIFIC_SPLIT=$2

    echo
    echo "Process will run the following:"
    echo "t2t-datagen \\"
    echo "  --problem=$PROBLEM \\"
    echo "  --data_dir=$DATA_DIR \\"
    echo "  --tmp_dir=$TMP_DIR"
    echo "  --specific_split=$SPECIFIC_SPLIT"
    echo
else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <DATA_DIR>  <SPECIFIC_SPLIT>  (--dry-run)\n\
E.g. ./$(basename "$0")  t2t-data    True\n"
fi
