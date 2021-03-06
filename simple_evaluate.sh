#!/bin/bash
if [ $# -eq 4 ]
then
export STORAGE_BUCKET=gs://mathsreasoning
echo "STORAGE_BUCKET = "$STORAGE_BUCKET

# Assumed the VM has a tpu already configured
export TPU_IP_ADDRESS=$3 # 10.218.218.146
export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
export USE_TPU=True
export CLOUD_TPU_NAME=$4 # jonmcwong-tpu
export PROBLEM=algorithmic_math_deepmind_all
export MODEL=$1 # transformer
export MODEL_TAG=$2 # mds_paper_settings-2020-06-12
export HPARAMS_SET=transformer_tpu
export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
# export RESULTS_DIR=${STORAGE_BUCKET}/evalutation_results
export EVAL_USE_TEST_SET=True

echo "USE_TPU = "$USE_TPU
echo "CLOUD_TPU_NAME = "$CLOUD_TPU_NAME
echo "PROBLEM = "$PROBLEM
echo "MODEL = "$MODEL
echo "MODEL_TAG = "$MODEL_TAG
echo "HPARAMS_SET = "$HPARAMS_SET
echo "DATA_DIR = "$DATA_DIR
echo "TRAIN_DIR = "$TRAIN_DIR
# echo "RESULTS_DIR = "$RESULTS_DIR
echo "EVAL_USE_TEST_SET = "$EVAL_USE_TEST_SET

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
echo "DATASET_SPLIT = "$DATASET_SPLIT
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
--eval_steps=3
# --results_dir=$RESULTS_DIR

done
else
printf "Invalid arguments provided. Signature is:\n\
./$(basename "$0") \
<MODEL> \
<MODEL_TAG> \
<CLOUD_TPU_NAME> \
<TPU_IP_ADDRESS>\n\
E.g. ./$(basename "$0") \
transformer \
mds_paper_settings-2020-06-12 \
10.218.218.146 \
jonmcwong-tpu\n"
fi
