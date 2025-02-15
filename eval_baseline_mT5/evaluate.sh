#!/usr/bin/env bash

languages=('zh' 'de' 'ja' 'ko' 'th' 'hi' 'vi' 'nl' 'sw' 'ar' 'ru' 'tr' 'fr' 'pt' 'es' 'id' 'sv' 'hr' 'sk' 'da')


for lang in "${languages[@]}"; do
    echo "Running for language: $lang"

    python main.py --task tasd \
                --dataset hotel/$lang \
                --model_name_or_path mt5-base \
                --paradigm extraction \
                --n_gpu 0 \
                --do_eval \
                --train_batch_size 16 \
                --gradient_accumulation_steps 2 \
                --eval_batch_size 16 \
                --learning_rate 3e-4 \
                --num_train_epochs 30 \
                --evaluate_checkpoint_dir model \
                --lang $lang
    echo "Finished running for language: $lang"
done

