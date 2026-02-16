#!/bin/bash
# Qwen3-VL-8B LoRA 推理

MODEL_PATH="/path/to/Qwen3-VL-8B-Instruct"
ADAPTER_PATH="output/checkpoint-573"

export CUDA_VISIBLE_DEVICES=0
export MAX_PIXELS=1003520

swift infer \
    --model ${MODEL_PATH} \
    --adapters ${ADAPTER_PATH} \
    --torch_dtype bfloat16 \
    --infer_backend pt
