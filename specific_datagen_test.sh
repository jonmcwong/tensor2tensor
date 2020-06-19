#!/bin/bash



# export TPU_IP_ADDRESS=10.218.218.146
# export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
export PROBLEM=algorithmic_math_deepmind_all
# export MODEL=transformer
# export HPARAMS_SET=transformer_tpu
# export TPU_NAME=actualmathstpu  # different for each run
export STORAGE_BUCKET=gs://mathsreasoning
# export MODEL_TAG=mds_paper_settings
# export MODEL_TAG=${MODEL_TAG}-$(date +%F)
# export MODEL_TAG=${MODEL_TAG}-2020-06-12
export DATA_DIR=${STORAGE_BUCKET}/t2t-specific-data
export TMP_DIR=${STORAGE_BUCKET} # /mathematics_dataset-v1.0
# export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
# export BEAM_SIZE=4
# export ALPHA=0.6
# export DECODE_FILE=$HOME/test_file.txt
# export DECODE_OUTPUT=$HOME/output.txt
echo "PROBLEM = "$PROBLEM
# echo "MODEL = "$MODEL
# echo "HPARAMS_SET = "$HPARAMS_SET
# echo "TPU_NAME = "$TPU_NAME
echo "STORAGE_BUCKET = "$STORAGE_BUCKET
# echo "MODEL_TAG = "$MODEL_TAG
# echo "MODEL_TAG = "$MODEL_TAG
echo "DATA_DIR = "$DATA_DIR
echo "TMP_DIR = "$TMP_DIR
# echo "TRAIN_DIR = "$TRAIN_DIR
# echo "BEAM_SIZE = "$BEAM_SIZE
# echo "ALPHA = "$ALPHA
# echo "DECODE_FILE = "$DECODE_FILE
# echo "DECODE_OUTPUT = "$DECODE_OUTPUT



t2t-datagen \
  --problem=$PROBLEM \
  --data_dir=$DATA_DIR \
  --tmp_dir=$TMP_DIR \
  --specific_splits=False