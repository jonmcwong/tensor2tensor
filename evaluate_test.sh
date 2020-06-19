#!/bin/bash



export TPU_IP_ADDRESS=10.218.218.146
export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
export PROBLEM=algorithmic_math_deepmind_all
export MODEL=transformer
export HPARAMS_SET=transformer_tpu
export TPU_NAME=actualmathstpu  # different for each run
export STORAGE_BUCKET=gs://mathsreasoning
export MODEL_TAG=mds_paper_settings
# export MODEL_TAG=${MODEL_TAG}-$(date +%F)
export MODEL_TAG=${MODEL_TAG}-2020-06-12
export DATA_DIR=${STORAGE_BUCKET}/t2t-data
export TMP_DIR=${STORAGE_BUCKET}/t2t_datagen
export TRAIN_DIR=${STORAGE_BUCKET}/t2t_train/$PROBLEM/$MODEL-$MODEL_TAG
export BEAM_SIZE=4
export ALPHA=0.6
export DECODE_FILE=$HOME/test_file.txt
export DECODE_OUTPUT=$HOME/output.txt
export DATA_SHARD=$DATA_DIR/algorithmic_math_deepmind_all-train-00000-of-00128
echo "PROBLEM = "$PROBLEM
echo "MODEL = "$MODEL
echo "HPARAMS_SET = "$HPARAMS_SET
echo "TPU_NAME = "$TPU_NAME
echo "STORAGE_BUCKET = "$STORAGE_BUCKET
echo "MODEL_TAG = "$MODEL_TAG
echo "MODEL_TAG = "$MODEL_TAG
echo "DATA_DIR = "$DATA_DIR
echo "TMP_DIR = "$TMP_DIR
echo "TRAIN_DIR = "$TRAIN_DIR
echo "BEAM_SIZE = "$BEAM_SIZE
echo "ALPHA = "$ALPHA
echo "DECODE_FILE = "$DECODE_FILE
echo "DECODE_OUTPUT = "$DECODE_OUTPUT



t2t-eval \
  --problem=$PROBLEM \
  --model=$MODEL \
  --data_dir=$DATA_DIR \
  --output_dir=$TRAIN_DIR \
  --eval_use_test_set=False \
  --hparams_set=$HPARAMS_SET \
  --use_tpu=True \
  --cloud_tpu_name=jonmcwong-tpu
