#!/bin/bash



export TPU_IP_ADDRESS=10.218.218.146
export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
export USE_TPU=True
export CLOUD_TPU_NAME=jonmcwong-tpu

export PROBLEM=algorithmic_math_deepmind_all
export MODEL=transformer
# export MODEL_TAG=mds_paper_settings-2020-06-12
export MODEL_TAG=$1
export HPARAMS_SET=transformer_tpu
export STORAGE_BUCKET=gs://mathsreasoning
# export MODEL_TAG=${MODEL_TAG}-$(date +%F)
# export MODEL_TAG=${MODEL_TAG}-2020-06-12
export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
# export TMP_DIR=${STORAGE_BUCKET}/t2t_datagen
export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
# export BEAM_SIZE=4
# export ALPHA=0.6
# export DECODE_FILE=$HOME/test_file.txt
# export DECODE_OUTPUT=$HOME/output.txt
# export DATA_SHARD=$DATA_DIR/algorithmic_math_deepmind_all-train-00000-of-00128
export EVAL_USE_TEST_SET=True


echo "TPU_IP_ADDRESS = "$TPU_IP_ADDRESS
echo "XRT_TPU_CONFIG = "$XRT_TPU_CONFIG
echo "USE_TPU = "$USE_TPU
echo "CLOUD_TPU_NAME = "$CLOUD_TPU_NAME
echo "PROBLEM = "$PROBLEM
echo "MODEL = "$MODEL
echo "HPARAMS_SET = "$HPARAMS_SET
# echo "STORAGE_BUCKET = "$STORAGE_BUCKET
# echo "MODEL_TAG = "$MODEL_TAG
echo "DATA_DIR = "$DATA_DIR
# echo "TMP_DIR = "$TMP_DIR
echo "TRAIN_DIR = "$TRAIN_DIR
# echo "BEAM_SIZE = "$BEAM_SIZE
# echo "ALPHA = "$ALPHA
# echo "DECODE_FILE = "$DECODE_FILE
# echo "DECODE_OUTPUT = "$DECODE_OUTPUT
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
		--eval_steps=4
done
