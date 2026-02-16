#!/bin/bash
# 合并 LoRA 权重到基座模型

MODEL_PATH="/path/to/Qwen3-VL-8B-Instruct"
ADAPTER_PATH="output/checkpoint-573"

swift merge-lora \
    --model ${MODEL_PATH} \
    --adapters ${ADAPTER_PATH} \
    --torch_dtype bfloat16 \
    --merge_lora_output merged_model
