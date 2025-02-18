# M-ABSA

This repo contains the data and code for our paper ****M-ABSA: A Multilingual Dataset for Aspect-Based Sentiment Analysis****.

[![arXiv](https://img.shields.io/badge/arXiv-2502.11824-b31b1b.svg)](https://arxiv.org/abs/2502.11824)


# Data Description:

All datasets are stored in the data/ folder:

- All dataset contains 7 domains. 

 ```
domains = ["coursera", "hotel", "laptop", "restaurant", "phone", "sight", "food"]
``` 
- Each dataset contains 21 languages.
```
langs = ["ar", "da", "de", "en", "es", "fr", "hi", "hr", "id", "ja", "ko", "nl", "pt", "ru", "sk", "sv", "sw", "th", "tr", "vi", "zh"]
```
- Each dataset is divided into training, validation, and test sets. Each sentence is separated by __"####"__, with the first part being the sentence and the second part being the corresponding triplet. Here is an example, where the triplet includes __[aspect, category, sentiment]__.

```
This coffee brews up a nice medium roast with exotic floral and berry notes .####[['coffee', 'food quality', 'positive', 'nice']]
```

## Requirements

We recommend you to install the specified version of the following packages:

- transformers==4.0.0
-  sentencepiece==0.1.91
-  pytorch_lightning==0.8.1

## Quick Start for the Baseline

- Set up the environment as described in the above section.
- Download the pre-trained mT5-base model from [https://huggingface.co/google/mt5-base](https://huggingface.co/google/mt5-base) and place it under the folder mT5-base/ .
- Run command bash run.sh, which train the model on source language under UABSA/TASD task.
- Run command bash evaluate.sh, which test the model on target language under UABSA/TASD task.

****Detailed Usage****

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

If the code or dataset is used in your research, please star our repo and cite our paper as follows:
```
@misc{wu2025mabsa,
      title={M-ABSA: A Multilingual Dataset for Aspect-Based Sentiment Analysis}, 
      author={Chengyan Wu and Bolei Ma and Yihong Liu and Zheyu Zhang and Ningyuan Deng and Yanshu Li and Baolan Chen and Yi Zhang and Barbara Plank and Yun Xue},
      year={2025},
      eprint={2502.11824},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.11824}, 
}
```

