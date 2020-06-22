#!/bin/bash

# if [[ $# -eq 2 ]]
# then
# ctpu up \
# --disk-size-gb=100 \
# --machine-type=n1-standard-1 \
# --name=smart-evaluate-tpu-$1 \
# --preemptible=$2 \
# --require-permissions=True \
# --zone="us-central1-f" \
# --tf-version=1.15.3
# else
# echo "Invalid argument: needs tpu_num and preemptiple"
# fi





# git clone https://github.com/jonmcwong/tensor2tensor.git
# cd tensor2tensor
# ./setup.sh
# chmod +x smart_evaluate.sh
export BIG_NAME=smart-eval-007
gcloud compute instances create $BIG_NAME \
--metadata=startup-script='#! /bin/bash
echo "running startup script..."
git clone https://github.com/jonmcwong/tensor2tensor.git
cd tensor2tensor
echo "DONE!"' \
--source-instance-template=train-t2t \
--zone=us-central1-f

# --machine-type=n1-standard-1 \
# --scopes=storage-full,cloud-platform,compute-rw \

# --scopes=storage-ro \

gcloud compute tpus create $BIG_NAME \
      --zone=us-central1-f \
      --accelerator-type=v2-8 \
      --version=1.15.3 \
      --preemptible
