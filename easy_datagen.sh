#!/bin/bash



if [[ $# -eq 0 ]] ; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)

    if [[ $ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    fi

    export PROBLEM=algorithmic_math_deepmind_all
    # datagen will recognise the "easy part and select only the train-easy data"
    export DATA_DIR=${STORAGE_BUCKET}/t2t-easy-data
    export TMP_DIR=${STORAGE_BUCKET}/t2t-easy-data-incomplete
    export SPECIFIC_SPLITS=easy

    echo
    echo "Running..."
    echo "t2t-datagen \\"
    echo "  --problem=$PROBLEM \\"
    echo "  --data_dir=$DATA_DIR \\"
    echo "  --tmp_dir=$TMP_DIR \\"
    echo "  --specific_splits=$SPECIFIC_SPLITS"
    echo


    t2t-datagen \
      --problem=$PROBLEM \
      --data_dir=$DATA_DIR \
      --tmp_dir=$TMP_DIR \
      --specific_splits=$SPECIFIC_SPLITS


elif [[ $# -eq 1 && $1 == "--dry-run" ]]; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)

    if [[ $ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    fi

    export PROBLEM=algorithmic_math_deepmind_all
    # datagen will recognise the "easy part and select only the train-easy data"
    export DATA_DIR=${STORAGE_BUCKET}/t2t-easy-data
    export TMP_DIR=${STORAGE_BUCKET}/t2t-easy-data-incomplete
    export SPECIFIC_SPLITS=easy

    echo
    echo "Process will run the following:"
    echo "t2t-datagen \\"
    echo "  --problem=$PROBLEM \\"
    echo "  --data_dir=$DATA_DIR \\"
    echo "  --tmp_dir=$TMP_DIR \\"
    echo "  --specific_splits=$SPECIFIC_SPLITS"
    echo

fi
