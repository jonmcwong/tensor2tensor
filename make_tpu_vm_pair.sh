#!/bin/bash


gcloud config set project mathsreasoning
export PREFIX=smart-eval-frag

for FRAG_NUM in 000
do
    export BIG_NAME=$PREFIX$FRAG_NUM
    echo "Generating VM and TPU "$BIG_NAME"..."

    gcloud compute instances create $BIG_NAME \
    --source-instance-template=train-t2t \
    --zone=us-central1-f

    gcloud compute tpus create $BIG_NAME \
          --accelerator-type=v2-8 \
          --version=1.15.3 \
          --preemptible \
          --zone=us-central1-f

done


#storage for scripts thaty may not be officially saved
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

    # --metadata=startup-script='#! /bin/bash
    # echo "running startup script..."
    # git clone https://github.com/jonmcwong/tensor2tensor.git
    # cd tensor2tensor
    # echo "DONE!"' \
