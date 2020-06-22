#!/bin/bash

if [[ $# -eq 2 ]]
then
ctpu up \
--disk-size-gb=100 \
--machine-type=n1-standard-1 \
--name=smart-evaluate-tpu$1 \
--preemptible=$2 \
--require-permissions=True \
--zone="us-central1-f" \
--tf-version=1.15.3
else
echo "Invalid argument: needs tpu_num and preemptiple"
fi





git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
./setup.sh
./smart_evaluate.sh \
transformer \
base_test_dropout02-2020-06-19


chmod +x smart_evaluate.sh