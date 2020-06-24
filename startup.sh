#!/bin/bash
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com



chmod +x single_smart_evaluate.sh

git checkout .
git pull
chmod +x single_smart_evaluate.sh
./setup.sh
./single_smart_evaluate.sh transformer quick-noam-dropout01-2020-06-21 2


gsutil -m cp -r \
gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/universal_transformer-lowerlr0-02-2020-06-23 \
gs://us_bucketbucket/t2t_train/algorithmic_math_deepmind_all/universal_transformer-lowerlr0-02-2020-06-23

git clone https://github.com/jonmcwong/FYP_code.git
git clone https://github.com/jonmcwong/PyTorch-Beam-Search-Decoding.git


plt.clf()
plot_against_steps(make_md([

    "transformer-base_test_dropout02-2020-06-19",
    ], [
"all"
    ]), xlim=(-10000, 1200000))
