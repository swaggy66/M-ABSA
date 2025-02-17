# M-ABSA

This repo contains the data and code for our paper 《M-ABSA: A Multilingual Dataset for Aspect-Based Sentiment Analysis》.

## Requirements

We recommend you to install the specified version of the following packages:

- transformers==4.0.0
-  sentencepiece==0.1.91
-  pytorch_lightning==0.8.1

## Quick Start

- Set up the environment as described in the above section
- Download the pre-trained mT5-base model from [https://huggingface.co/google/mt5-base](https://huggingface.co/google/mt5-base)
- Run command bash run.sh, which train the model on source language under UABSA/TASD task.
- Run command bash evaluate.sh, which test the model on target language under UABSA/TASD task.

## Detailed Usage
We conduct experiments on two ABSA subtasks with M-ABSA dataset in the paper, you can change the parameters in run.sh to try them:

```

```

