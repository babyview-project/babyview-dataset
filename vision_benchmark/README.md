# BabyView Vision Benchmark

This directory contains instructions on how to train DINOv2 on the BabyView (BV-Home) dataset and evaluate on downstream tasks for ImageNet classification, NYUv2 depth estimation and COCOStuff segmentation

## Preprocessing the dataset

The first step is to convert the video dataset into an image dataset and to create a `.txt` file of relative path/filenames that is needed for the DINOv2 data loader. The code for this is in the `preproc` directory.

## Training DINOv2

To train DINOv2 after processing the dataset refer to our modified [DINOv2 fork](https://github.com/sstojanov/dinov2) of the original code. ImageNet object category recognition is also done using the code from this fork (WIP).

## Downstream Evaluation on COCOStuff Segmentation

To evaluate DINOv2 trained on BabyView on COCOStuff segmentation refer to our [mmsegmentation fork](https://github.com/sstojanov/mmsegmentation) (WIP).

## Downstream Evaluation on NYUv2 Depth Estimation

To evaluate DINOv2 trained on BabyView on NYUv2 depth estimation refer to our [monocular depth estimation toolbox fork](https://github.com/sstojanov/Monocular-Depth-Estimation-Toolbox) (WIP).
