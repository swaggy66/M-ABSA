#!/usr/bin/env bash


# single_run

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


