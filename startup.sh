#!/bin/bash
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com

git checkout split8
git branch --set-upstream-to origin split8

chmod +x single_smart_evaluate.sh

cd ..
sudo rm -r tensor2tensor
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com
git checkout split8
git branch -u origin/split8
./setup.sh


screen -r

exit
git checkout .
git pull
./setup.sh
screen
 
./single_smart_evaluate.sh transformer base_test-dropout01-2020-06-24 1

./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 0
./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 4
./single_smart_evaluate8.sh transformer data-easy-2020-06-24 0

chmod +x single_smart_evaluate.sh

gsutil -m cp -r \
gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/transformer-data-easy-2020-06-24 \
gs://us_bucketbucket/t2t_train/algorithmic_math_deepmind_all/transformer-data-easy-2020-06-24

git clone https://github.com/jonmcwong/FYP_code.git
git clone https://github.com/jonmcwong/PyTorch-Beam-Search-Decoding.git


plt.clf()
plot_against_steps(make_md([

    "combined_transformer-base-dropout01",


    ], [
 "all",
    ]), xlim=(-10000, 1000000), xlabel="Accuracy", title="Accuracy for each question type", save_name="Latest_plot.png", font_size=12)
