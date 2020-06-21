#!/bin/bash
if [ $# -eq 0 ]
	then echo "No MODEL_TAG provided, e.g. './$(basename "$0") mds_paper_settings-2020-06-12'"
else
	# Get the VM_NAME and INTERNAL_IP
	export INTERNAL_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
	export VM_NAME=$(gcloud compute instances list | grep $INTERNAL_IP | cut -d' ' -f1)
	export STORAGE_BUCKET=gs://mathsreasoning
	echo "VM_NAME = "$VM_NAME
	echo "INTERNAL_IP = "$INTERNAL_IP
	echo "STORAGE_BUCKET = "$STORAGE_BUCKET

	# Assumed the VM has a tpu already configured
	export TPU_IP_ADDRESS=10.218.218.146
	export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
	export USE_TPU=True
	export CLOUD_TPU_NAME=$VM_NAME
	export PROBLEM=algorithmic_math_deepmind_all
	export MODEL=transformer
	export MODEL_TAG=$1 # mds_paper_settings-2020-06-12
	export HPARAMS_SET=transformer_tpu
	export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
	export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
	export EVAL_USE_TEST_SET=True

	echo "USE_TPU = "$USE_TPU
	echo "CLOUD_TPU_NAME = "$CLOUD_TPU_NAME
	echo "PROBLEM = "$PROBLEM
	echo "MODEL = "$MODEL
	echo "MODEL_TAG = "$MODEL_TAG
	echo "HPARAMS_SET = "$HPARAMS_SET
	echo "DATA_DIR = "$DATA_DIR
	echo "TRAIN_DIR = "$TRAIN_DIR
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
fi