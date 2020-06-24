#!/bin/bash
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor


chmod +x single_smart_evaluate.sh

git checkout .
git pull
chmod +x single_smart_evaluate.sh
./setup.sh
./single_smart_evaluate.sh transformer quick-noam-dropout01-2020-06-21 2


gsutil -m cp -r \
gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/transformer-quick-noam-dropout01-2020-06-21 \
gs://us_bucketbucket/t2t_train/algorithmic_math_deepmind_all/transformer-quick-noam-dropout01-2020-06-21

plt.clf()
plot_against_steps(make_md([
    "transformer-base_test_dropout02-2020-06-19",
    ], [
"all"
    ]), xlim=(-10000, 1200000))
