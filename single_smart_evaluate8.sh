#!/bin/bash

export LIST=(\
    train_easy_add_or_sub \
    train_medium_add_or_sub \
    train_hard_add_or_sub \
    extra_add_or_sub_big \
    train_easy_mul \
    train_medium_mul \
    train_hard_mul \
    extra_mul_big \
    )

if [[ $# -eq 3 ]] ; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)
    export TPU_INFO=$(gcloud compute tpus list --zone=$VM_ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)

    if [[ $VM_ZONE == "us-central1-a" || $VM_ZONE == "us-central1-b" || $VM_ZONE == "us-central1-c" || $VM_ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $VM_ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    else
        echo
        echo
        echo
        echo "ZONE variable is weird... ZONE = "$VM_ZONE
        echo
        echo
        echo
    fi

    # Assumed the VM has a tpu already configured
    export TPU_IP_ADDRESS=$TPU_IP
    export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
    export USE_TPU=True
    export CLOUD_TPU_NAME=$TPU_NAME # jonmcwong-tpu
    export PROBLEM=algorithmic_math_deepmind_all
    export MODEL=$1 # transformer
    export MODEL_TAG=$2 # mds_paper_settings-2020-06-12
    if [[ $MODEL == "transformer" ]] ; then
        export HPARAMS_SET=transformer_tpu
    elif [[ $MODEL == "universal_transformer" ]] ; then
        # check if global is in MODEL_TAG
        if [[ $(echo $MODEL_TAG | grep "global") == "" ]] ; then
            export HPARAMS_SET=adaptive_universal_transformer_base_tpu
        else
            export HPARAMS_SET=adaptive_universal_transformer_global_base_tpu
        fi
    else
        export HPARAMS_SET"???????"
        echo
        echo
        echo "not sure what HPARAMS_SET to assign for this MODEL"
        echo
        echo
    fi
    export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
    export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
    export RESULTS_DIR=${STORAGE_BUCKET}/results-$MODEL-$MODEL_TAG
    export EVAL_USE_TEST_SET=True
    # echo "mkdir eval-results-"$MODEL_TAG
    # mkdir "eval-results-"$MODEL_TAG

    export SPLIT_NUM=$3
    export DATASET_SPLIT=${LIST[$SPLIT_NUM]}



    echo
    echo "Running..."
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
    echo
    echo "Process ran with these settings:"
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

elif [[ $# -eq 4 && $4 == "--dry-run" ]]; then
    export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
    export VM_INFO=$(gcloud compute instances list | grep $VM_IP)
    export VM_NAME=$(echo $VM_INFO | cut -d' ' -f1)
    export VM_ZONE=$(echo $VM_INFO | cut -d' ' -f2)
    export TPU_INFO=$(gcloud compute tpus list --zone=$VM_ZONE | grep $VM_NAME)
    export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
    export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)

    if [[ $VM_ZONE == "us-central1-a" || $VM_ZONE == "us-central1-b" || $VM_ZONE == "us-central1-c" || $VM_ZONE == "us-central1-f" ]] ; then
        export STORAGE_BUCKET=gs://us_bucketbucket
    elif [[ $VM_ZONE == "europe-west4-a" ]] ; then
        export STORAGE_BUCKET=gs://mathsreasoning
    else
        echo
        echo
        echo
        echo "ZONE variable is weird... ZONE = "$VM_ZONE
        echo
        echo
        echo
    fi

    # Assumed the VM has a tpu already configured
    export TPU_IP_ADDRESS=$TPU_IP
    export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
    export USE_TPU=True
    export CLOUD_TPU_NAME=$TPU_NAME # jonmcwong-tpu
    export PROBLEM=algorithmic_math_deepmind_all
    export MODEL=$1 # transformer
    export MODEL_TAG=$2 # mds_paper_settings-2020-06-12
    if [[ $MODEL == "transformer" ]] ; then
        export HPARAMS_SET=transformer_tpu
    elif [[ $MODEL == "universal_transformer" ]] ; then
        export HPARAMS_SET=adaptive_universal_transformer_base_tpu
    else
        export HPARAMS_SET"???????"
        echo
        echo
        echo "not sure what HPARAMS_SET to assign for this MODEL"
        echo
        echo
    fi
    export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
    export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
    export RESULTS_DIR=${STORAGE_BUCKET}/results-$MODEL-$MODEL_TAG
    export EVAL_USE_TEST_SET=True
    # echo "mkdir eval-results-"$MODEL_TAG
    # mkdir "eval-results-"$MODEL_TAG

    export SPLIT_NUM=$3
    export DATASET_SPLIT=${LIST[$SPLIT_NUM]}

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

else
    printf "Invalid arguments provided. Signature is:\n\
     ./$(basename "$0")  <MODEL>                <MODEL_TAG>                    <DATSET_SPLIT_NUM> (--dry-run)\n\
E.g. ./$(basename "$0")  universal_transformer  base_test-loss-0001-2020-06-21 7\n"
fi


