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
gs://us_bucketbucket/results-universal_transformer-ut-lowerlr0-002-2020-06-23 \
results-universal_transformer-ut-lowerlr0-002-2020-06-23/

git clone https://github.com/jonmcwong/FYP_code.git
git clone https://github.com/jonmcwong/PyTorch-Beam-Search-Decoding.git


plt.clf()
plot_against_steps(make_md([

    "universal_transformer-lowerlr0-02-2020-06-23",

    "universal_transformer-ut-lowerlr0-002-2020-06-23",
    ], [
"all"
    ]), xlim=(-10000, 200000), title="???????????", save_name="Latest_plot.png", font_size=15)
