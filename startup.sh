#!/bin/bash
cd ..
sudo rm -r tensor2tensor

git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com
./setup.sh
./single_smart_evaluate.sh Q8 transformer data-easy-2020-06-24 8



./specific_datagen.sh t2t-data-emheam


./single_smart_evaluate.sh Q8 transformer data-easy-2020-06-24 0



chmod +x single_smart_evaluate.sh

exit
git checkout .
git pull
./setup.sh
./single_smart_evaluate.sh Q8 transformer data-easy-2020-06-24 8



screen
 
./single_smart_evaluate.sh transformer base_test-dropout01-2020-06-24 1

./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 0
./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 4

git pull

chmod +x single_smart_evaluate.sh

gsutil -m cp -r \
gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/transformer-data-easy-2020-06-24 \
gs://us_bucketbucket/t2t_train/algorithmic_math_deepmind_all/transformer-data-easy-2020-06-24

git clone https://github.com/jonmcwong/FYP_code.git
git clone https://github.com/jonmcwong/PyTorch-Beam-Search-Decoding.git

# UT global graph
plt.clf()
plot_against_steps(make_md([
	"universal_transformer-global-lowerlr0-02-2020-06-23",
    ], [
 "all",
    ]),
xlim=(-5000, 105000),
ylim=(0, 1),
title="Accuracies By Question Type During Universal Transformer Training",
save_name="Latest_plot.png", 
font_size=18, col_model=False, include_model_name=False)


# base test dropout 01
plt.clf()
plot_against_steps(make_md([
	"combined_transformer-base-dropout01",
    ], [
 "all",
    ]),
xlim=(-10000, 905000),
ylim=(-0.05, 1.05),
title="Accuracies By Question Type During Universal Transformer Training",
save_name="Latest_plot.png", 
font_size=20, col_model=False, include_model_name=False)
