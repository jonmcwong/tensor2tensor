#!/bin/bash
cd ..
sudo rm -r tensor2tensor

git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
git config --global user.name jonmcwong
git config --global user.email jonmwong@gmail.com
./setup.sh
./single_smart_evaluate.sh Q8 transformer data-easy-2020-06-24 8
./single_smart_evaluate.sh Q12 transformer base-relu-dp-01-2020-06-25 0
./single_smart_evaluate.sh Q12 transformer base-relu-dp-00-2020-06-25 0


./single_smart_evaluate.sh Q12 \
universal_transformer ut-pres2-2020-06-29 11


c
c


./specific_datagen.sh t2t-data-emheam


git checkout .
git pull
./rebuild.sh



chmod +x single_smart_evaluate.sh

exit
git checkout .
git pull
./single_smart_evaluate.sh Q8 transformer data-easy-2020-06-24 8

./setup.sh


screen
 
./single_smart_evaluate.sh transformer base_test-dropout01-2020-06-24 1

./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 0
./single_smart_evaluate.sh universal_transformer global-lowerlr0-02-2020-06-23 4

git pull

chmod +x single_smart_evaluate.sh

gsutil -m cp -r \
gs://us_bucketbucket/results-transformer-data-easy-2020-06-24 \
$PWD

gs://mathsreasoning/t2t_train/algorithmic_math_deepmind_all/transformer-data-easy-2020-06-24 \

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
font_size=18,
include_model_name=False,
)


# base test dropout 01
plot_against_steps(make_md([
	"combined_transformer-base-dropout01",
    ], [
 "all",
    ]),
xlim=(-10000, 905000),
ylim=(-0.05, 1.05),
title="Accuracies By Question Type During Transformer Base Training",
save_name="Latest_plot.png", 
font_size=20,
include_model_name=False,
multi_model=False,
)


plot_against_difficulty(holder8,
	title="Transformer Accuracy Against Question Difficulty",
	)








plt.clf()
fig, axs = plt.subplots(1, 1, squeeze=False)
plot_against_steps(
axs[0][0],
make_md([
	"universal_transformer-ut-pres-2020-06-28",
	# "universal_transformer-ut-pres2-2020-06-29",
    ], [
"all"
    ]),
xlim=(45000, 225000),
ylim=(-0.05, 1.05),
title="Accuracies By Question Type During Universal Transformer Training",
save_name="Latest_plot.png", 
font_size=20,
include_model_name=True,
multi_model=False,
include_transformer_type=False,
zeroed=False,
)

