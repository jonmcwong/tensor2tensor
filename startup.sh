#!/bin/bash
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com



chmod +x single_smart_evaluate.sh

git checkout .
git pull
./setup.sh
screen
 
./single_smart_evaluate.sh transformer base_test-dropout01-2020-06-24 1

./single_smart_evaluate.sh transformer quick-noam-dropout01-2020-06-21 2

chmod +x single_smart_evaluate.sh

gsutil -m cp -r \
gs://us_bucketbucket/results-universal_transformer-ut-lowerlr0-002-2020-06-23 \
results-universal_transformer-ut-lowerlr0-002-2020-06-23/

git clone https://github.com/jonmcwong/FYP_code.git
git clone https://github.com/jonmcwong/PyTorch-Beam-Search-Decoding.git


plt.clf()
plot_against_steps(make_md([

    "transformer-noam-dropout01-2020-06-20",
    ], [
    "extra_add_or_sub_big",
    "extra_mul_big",

    "inter_mul",

    "inter_add_or_sub",

    ]), xlim=(0, 1200000), title="???????????", save_name="Latest_plot.png", font_size=12)
