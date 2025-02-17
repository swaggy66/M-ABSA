# M-ABSA

This repo contains the data and code for our paper 《M-ABSA: A Multilingual Dataset for Aspect-Based Sentiment Analysis》.

## Requirements

We recommend you to install the specified version of the following packages:

- transformers==4.0.0
-  sentencepiece==0.1.91
-  pytorch_lightning==0.8.1

## Quick Start

- Set up the environment as described in the above section.
- Download the pre-trained mT5-base model from [https://huggingface.co/google/mt5-base](https://huggingface.co/google/mt5-base) and place it under the folder mT5-base/ .
- Run command bash run.sh, which train the model on source language under UABSA/TASD task.
- Run command bash evaluate.sh, which test the model on target language under UABSA/TASD task.

## Detailed Usage
We conduct experiments on two ABSA subtasks with M-ABSA dataset in the paper, you can change the parameters in run.sh to try them:

```
python main.py --task tasd \
            --dataset hotel \
            --model_name_or_path mt5-base \
            --paradigm extraction \
            --n_gpu 0 \
            --do_train \
            --do_direct_eval \
            --train_batch_size 16 \
            --gradient_accumulation_steps 2 \
            --eval_batch_size 16 \
            --learning_rate 3e-4 \
            --num_train_epochs 5
```

- $task refers to one of the ABSA task in [uabsa, tasd]
- $dataset refers to one of the seven datasets in [food, restaurant, coursera, laptop, sight, phone, hotel]


## Citation

If the code is used in your research, please star our repo and cite our paper as follows:
```
```

