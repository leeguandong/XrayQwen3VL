#!/bin/bash
# Qwen3-VL-8B LoRA 微调（单卡）
# 使用 ms-swift 框架

MODEL_PATH="/path/to/Qwen3-VL-8B-Instruct"
TRAIN_DATA="data/train.jsonl"
VAL_DATA="data/val.jsonl"

export CUDA_VISIBLE_DEVICES=0
export MAX_PIXELS=1003520
export TRANSFORMERS_NO_TF=1

swift sft \
    --model ${MODEL_PATH} \
    --dataset ${TRAIN_DATA} \
    --val_dataset ${VAL_DATA} \
    --torch_dtype bfloat16 \
    --max_length 2048 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 1e-4 \
    --lr_scheduler_type cosine \
    --warmup_ratio 0.05 \
    --tuner_type lora \
    --lora_rank 8 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --freeze_vit true \
    --freeze_aligner true \
    --gradient_checkpointing true \
    --save_steps 100 \
    --eval_steps 100 \
    --save_total_limit 3 \
    --logging_steps 5 \
    --output_dir output
