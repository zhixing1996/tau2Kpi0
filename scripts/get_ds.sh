#!/usr/bin/env bash

# datasets=(taupair uubar\-1 uubar\-2 uubar\-3 uubar\-4 ddbar ssbar ccbar\-1 ccbar\-2 ccbar\-3 ccbar\-4 charged\-1 charged\-2 mixed\-1 mixed\-2)
datasets=(uubar\-4 ddbar ssbar ccbar\-1 ccbar\-2 ccbar\-3 ccbar\-4 charged\-1 charged\-2 mixed\-1 mixed\-2)

mkdir -p rootfiles
cd rootfiles
for dataset in ${datasets[@]}; do
    echo "Downloading "${dataset}
    gb2_ds_get ${dataset}
done
