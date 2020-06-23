#!/bin/bash
export ZONE=europe-west4-a
export VM_IP=$(echo $SSH_CONNECTION | sed "s/^.* \([0-9|\.]*\) [0-9]*$/\1/")
export VM_NAME=$(gcloud compute instances list | grep $VM_IP | cut -d' ' -f1)
export TPU_INFO=$(gcloud compute tpus list --zone=$ZONE | grep $VM_NAME)
export TPU_IP=$(echo $TPU_INFO | sed "s/^.*v[0-9].*\s\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\):[0-9]*\s.*$/\1/")
# export TPU_NAME=$(echo $TPU_INFO | sed "s/^\(.*\)\sus-central.*$/\1/")
export TPU_NAME=$(echo $TPU_INFO | cut -d' ' -f1)
echo "VM_IP = "$VM_IP
echo "VM_NAME = "$VM_NAME
# echo "TPU_INFO = "$TPU_INFO
echo "TPU_IP = "$TPU_IP
echo "TPU_NAME = "$TPU_NAME
