#!/bin/bash

if [[ $ZONE == "" ]] ; then
    echo "ZONE variable not defined"
elif [[ $# -eq 3 ]] ; then
    if [[ $ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    echo
    echo
    echo
    echo "ZONE variable is weird... ZONE = "$ZONE
    echo
    echo
    echo
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_NAME=$(gcloud compute instances list | grep $VM_IP | cut -d' ' -f1)
    export TPU_INFO=$(gcloud compute tpus list --zone=$ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)

    # Assumed the VM has a tpu already configured
    export TPU_IP_ADDRESS=$TPU_IP
    export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
    export USE_TPU=True
    export CLOUD_TPU_NAME=$TPU_NAME # jonmcwong-tpu
    export PROBLEM=algorithmic_math_deepmind_all
    export MODEL=$1 # transformer
    export MODEL_TAG=$2 # mds_paper_settings-2020-06-12
    # export HPARAMS_SET=transformer_tpu
    # export HPARAMS_SET=adaptive_universal_transformer_base_tpu
    export HPARAMS_SET=$3
    export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
    export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
    export RESULTS_DIR=${STORAGE_BUCKET}/results-$MODEL-$MODEL_TAG
    export EVAL_USE_TEST_SET=True
    # echo "mkdir eval-results-"$MODEL_TAG
    # mkdir "eval-results-"$MODEL_TAG

    for DATASET_SPLIT in \
        extra_add_or_sub_big \
        extra_add_sub_multiple_longer \
        extra_div_big \
        extra_mixed_longer \
        extra_mul_big \
        extra_mul_div_multiple_longer \
        inter_add_or_sub \
        inter_add_sub_multiple \
        inter_div \
        inter_mixed \
        inter_mul \
        inter_mul_div_multiple
    do
        echo
        echo "Process will run the following:"
        echo "TPU_IP_ADDRESS = "$TPU_IP_ADDRESS
        echo "XRT_TPU_CONFIG = "$XRT_TPU_CONFIG
        echo "t2t-eval \\"
        echo "    --problem=$PROBLEM \\"
        echo "    --model=$MODEL \\"
        echo "    --data_dir=$DATA_DIR \\"
        echo "    --output_dir=$TRAIN_DIR \\"
        echo "    --eval_use_test_set=$EVAL_USE_TEST_SET \\"
        echo "    --hparams_set=$HPARAMS_SET \\"
        echo "    --dataset_split=$DATASET_SPLIT \\"
        echo "    --use_tpu=$USE_TPU \\"
        echo "    --cloud_tpu_name=$CLOUD_TPU_NAME \\"
        echo "    --eval_steps=3 \\"
        echo "    --results_dir=$RESULTS_DIR"
        echo
        t2t-eval \
            --problem=$PROBLEM \
            --model=$MODEL \
            --data_dir=$DATA_DIR \
            --output_dir=$TRAIN_DIR \
            --eval_use_test_set=$EVAL_USE_TEST_SET \
            --hparams_set=$HPARAMS_SET \
            --dataset_split=$DATASET_SPLIT \
            --use_tpu=$USE_TPU \
            --cloud_tpu_name=$CLOUD_TPU_NAME \
            --eval_steps=3 \
            --results_dir=$RESULTS_DIR
    done
elif [[ $# -eq 4 && $4 == "--dry-run" ]]; then
    if [[ $ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
        echo
        echo
        echo
        echo "ZONE variable is weird... ZONE = "$ZONE
        echo
        echo
        echo
    fi
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_NAME=$(gcloud compute instances list | grep $VM_IP | cut -d' ' -f1)
    export TPU_INFO=$(gcloud compute tpus list --zone=$ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)
    export TPU_IP_ADDRESS=$TPU_IP
    export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
    export USE_TPU=True
    export CLOUD_TPU_NAME=$TPU_NAME # jonmcwong-tpu
    export PROBLEM=algorithmic_math_deepmind_all
    export MODEL=$1 # transformer
    export MODEL_TAG=$2 # mds_paper_settings-2020-06-12
    export HPARAMS_SET=$3
    export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
    export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
    export RESULTS_DIR=${STORAGE_BUCKET}/results-$MODEL-$MODEL_TAG
    export EVAL_USE_TEST_SET=True

    echo "Process will run the following:"
    echo "TPU_IP_ADDRESS = "$TPU_IP_ADDRESS
    echo "XRT_TPU_CONFIG = "$XRT_TPU_CONFIG
    echo "t2t-eval \\"
    echo "    --problem=$PROBLEM \\"
    echo "    --model=$MODEL \\"
    echo "    --data_dir=$DATA_DIR \\"
    echo "    --output_dir=$TRAIN_DIR \\"
    echo "    --eval_use_test_set=$EVAL_USE_TEST_SET \\"
    echo "    --hparams_set=$HPARAMS_SET \\"
    echo "    --dataset_split=<all_12_of_them> \\"
    echo "    --use_tpu=$USE_TPU \\"
    echo "    --cloud_tpu_name=$CLOUD_TPU_NAME \\"
    echo "    --eval_steps=3 \\"
    echo "    --results_dir=$RESULTS_DIR"

else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <MODEL>                <MODEL_TAG>                     <HPARAMS_SET>\n\
E.g. ./$(basename "$0")  universal_transformer  base_test-loss-0001-2020-06-21  adaptive_universal_transformer_base_tpu\n"
fi
