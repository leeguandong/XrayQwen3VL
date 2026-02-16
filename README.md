# XrayQwen3VL

基于 [Qwen3-VL-8B](https://huggingface.co/Qwen/Qwen3-VL-8B) 的胸部X光智能诊断系统，使用 [ms-swift](https://github.com/modelscope/ms-swift) 框架进行 LoRA 微调。

本项目是 [XrayQwenVL](https://github.com/leeguandong/XrayQwenVL) 和 [XrayQwen2VL](https://github.com/leeguandong/XrayQwen2VL) 的延续。

## 效果展示

| 输入X光片 | 模型诊断 |
|-----------|---------|
| ![xray](data/test/1425_2.png) | 心脏大小正常，纵隔无增宽。双肺纹理清晰，未见明显实质性病变... |

## 训练结果

| 基座模型 | 方法 | 训练集 | 验证集 | Train Loss | Eval Loss | Token Acc |
|---------|------|--------|--------|-----------|-----------|-----------|
| Qwen3-VL-8B-Instruct | LoRA | 6,102 | 321 | 1.382 | 1.250 | 69% / 66% |

## 数据集

使用 [XrayGLM](https://github.com/WangRongsheng/XrayGLM) 提供的 [OpenI](https://openi.nlm.nih.gov/faq#collection) 胸部X光数据集：
- 6,423 张胸部X光图片
- 中文诊断报告标注
- 12 种提示词模板增强多样性

## 模型架构

```
Qwen3-VL-8B-Instruct
├── Vision Encoder (ViT)     ← 冻结
├── Visual-Language Aligner  ← 冻结
└── Language Model (LLM)     ← LoRA 微调
    ├── lora_rank: 8
    ├── lora_alpha: 32
    └── target_modules: all-linear
```

## 环境准备

```bash
# 安装 ms-swift
git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .

# 修复 Keras 兼容性
pip install tf-keras
```

## 快速开始

### 1. 数据准备

```bash
# 转换 XrayGLM 数据集为 ms-swift 格式
python scripts/convert_xray_swift.py \
    --source_json /path/to/XrayGLM/data/openi-zh-prompt.json \
    --images_dir /path/to/XrayGLM/images2 \
    --output_dir data/
```

### 2. LoRA 训练

```bash
# 单卡训练
bash tools/swift/finetune_qwen3vl_lora.sh

# 多卡训练（修改脚本中 CUDA_VISIBLE_DEVICES 和 NPROC_PER_NODE）
bash tools/swift/finetune_qwen3vl_lora_mp.sh
```

### 3. 推理

```bash
# 交互式推理
bash tools/swift/infer_qwen3vl_lora.sh

# 批量推理
python scripts/batch_infer.py \
    --model_path /path/to/Qwen3-VL-8B-Instruct \
    --adapter_path output/checkpoint-573 \
    --test_images data/test/1425_2.png data/test/2808_1.png
```

### 4. 合并 LoRA

```bash
bash tools/swift/merge_qwen3vl_lora.sh
```

## 项目结构

```
XrayQwen3VL/
├── README.md
├── version.py
├── data/                    # 数据集
│   └── test/               # 测试图片
├── doc/                     # 文档和架构图
├── scripts/                 # 数据处理脚本
│   ├── convert_xray_swift.py
│   └── batch_infer.py
├── tools/swift/             # ms-swift 训练脚本
│   ├── finetune_qwen3vl_lora.sh
│   ├── finetune_qwen3vl_lora_mp.sh
│   ├── infer_qwen3vl_lora.sh
│   └── merge_qwen3vl_lora.sh
├── test/                    # 测试脚本
│   └── test_infer.py
├── results/                 # 训练结果
├── weights/                 # 模型权重
└── app/                     # 应用（Gradio）
    └── gradio_app.py
```

## 训练超参数

| 参数 | 值 |
|------|-----|
| 基座模型 | Qwen3-VL-8B-Instruct |
| 微调方法 | LoRA |
| lora_rank | 8 |
| lora_alpha | 32 |
| target_modules | all-linear |
| freeze_vit | true |
| freeze_aligner | true |
| num_epochs | 3 |
| learning_rate | 1e-4 |
| lr_scheduler | cosine |
| warmup_ratio | 0.05 |
| batch_size | 1 |
| gradient_accumulation | 16 |
| max_length | 2048 |
| max_pixels | 1003520 |
| torch_dtype | bfloat16 |
| gradient_checkpointing | true |

## 致谢

- [ms-swift](https://github.com/modelscope/ms-swift) - 训练框架
- [XrayGLM](https://github.com/WangRongsheng/XrayGLM) - 数据集
- [XrayQwenVL](https://github.com/leeguandong/XrayQwenVL) - Qwen-VL 版本
- [XrayQwen2VL](https://github.com/leeguandong/XrayQwen2VL) - Qwen2-VL 版本

## License

CC BY-NC-SA 4.0
