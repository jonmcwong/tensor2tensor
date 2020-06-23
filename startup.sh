#!/bin/bash
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
export ZONE=us-central1-f
chmod +x single_smart_evaluate.sh

git pull
chmod +x single_smart_evaluate.sh

./setup.sh
./single_smart_evaluate.sh transformer quick-noam-dropout01-2020-06-21 2


gsutil -m cp -r \
gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/transformer-quick-noam-dropout01-2020-06-21 \
gs://us_bucketbucket/t2t_train/algorithmic_math_deepmind_all/transformer-quick-noam-dropout01-2020-06-21


