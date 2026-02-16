# XrayQwen3VL

Xray Large Multi-model Model，基于Qwen3-VL-8B微调Xray的多模态大模型，在2张A800上基于Qwen3-VL-8B-Instruct模型使用[ms-swift](https://github.com/modelscope/ms-swift)框架进行LoRA微调。

本项目是 [XrayQwenVL](https://github.com/leeguandong/XrayQwenVL) 和 [XrayQwen2VL](https://github.com/leeguandong/XrayQwen2VL) 的延续。

 <p align="center">
      <a href='https://github.com/leeguandong/XrayQwen3VL'>
            <img src='https://img.shields.io/badge/Project-Page-Green'>
      </a>
      </br>
      <a href="https://github.com/leeguandong/XrayQwen3VL/graphs/contributors">
        <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/leeguandong/XrayQwen3VL" />
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/leeguandong/XrayQwen3VL?color=0088ff" />
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/leeguandong/XrayQwen3VL?color=0088ff" />
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL/stargazers">
        <img src="https://img.shields.io/github/stars/leeguandong/XrayQwen3VL?color=ccf">
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL">
        <img src="https://img.shields.io/github/repo-size/leeguandong/XrayQwen3VL.svg?style=flat-square">
      </a>
      </br>
      <a href="https://github.com/leeguandong/XrayQwen3VL">
        <img src="https://visitor-badge.laobi.icu/badge?page_id=https://github.com/leeguandong/XrayQwen3VL">
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL">
        <img src="https://img.shields.io/github/last-commit/leeguandong/XrayQwen3VL">
      </a>
      <a href="https://github.com/leeguandong/XrayQwen3VL/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" />
      </a>
  </p>

## 本文贡献

- 借助Xray开源数据集，基于Qwen3-VL-8B-Instruct训练微调，并开放了用于学术研究的训练LoRA权重（`results/checkpoint-573/`），推理时需要自行加载原始的Qwen3-VL-8B-Instruct权重。
- 相比前作XrayQwenVL/XrayQwen2VL，升级到Qwen3-VL架构，使用ms-swift v4框架，支持单卡/多卡训练。

## 效果展示

影像诊断：
|X光影像|诊疗报告(医生)|XrayQwen3VL|
|:-|:-|:-|
|![](./data/test/1425_2.png)|患者的胸部X光片显示双侧肺部清晰，没有任何合并症、气胸或胸腔积液的迹象。心脏纵隔的轮廓和胸腔的骨质结构都在正常范围内。X光片的印象表明，没有急性心肺功能异常。这表明病人在这个时候有一个健康的呼吸和心血管系统。|X光片显示，心脏大小正常，纵膈不明显。肺部清晰，没有急性疾病的迹象。|
|![](./data/test/2808_1.png)|X光片显示有陈旧性肉芽肿病的后遗症，但肺部清晰，没有任何局灶性固结、胸腔积液或气胸。心脏和纵膈的大小和轮廓正常，表明没有急性心肺功能异常。总的来说，这是一张清晰的胸部X光片。|X光片显示，心脏大小和纵隔轮廓正常。肺部清晰，没有局灶性气隙不透明、胸腔积液或气胸。骨骼结构完整。印象中，没有急性心肺异常。|
|![](./data/test/348_2.png)|研究结果表明，心脏大小和纵隔轮廓正常，肺部清晰，肺血管正常，没有胸腔积液或气孔。此外，观察到胸椎的退行性变化很小。根据印象，没有急性心肺异常的迹象。根据这些结果，病人的整体状况似乎是最佳的。|X光片显示，心脏大小和纵隔轮廓正常，肺部清晰，没有气胸或胸腔积液的迹象。此外，没有急性骨质异常的情况。根据这些发现，没有急性心肺功能异常。|
|![](./data/test/1785_2.png)|胸部X光片显示心脏和纵隔轮廓正常，气管旁区域有肉芽肿性钙化，右上叶有轻度条纹状瘢痕。没有发现活动性肺炎或气胸。骨骼结构完整。根据这些发现，没有大叶性肺炎存在。|X光片显示，心脏大小正常，纵隔轮廓和肺部血管也正常。没有局灶性气隙不透明、胸腔积液或气胸。然而，有证据表明存在慢性变化，如肺气肿和肉芽肿。印象中，没有急性心肺异常，但有肺气肿和肉芽肿的存在。|

## 训练结果

| 基座模型 | 方法 | 训练集 | 验证集 | Train Loss | Eval Loss | Token Acc |
|---------|------|--------|--------|-----------|-----------|-----------|
| Qwen3-VL-8B-Instruct | LoRA | 6,102 | 321 | 1.382 | 1.250 | 69% / 66% |

## 数据集

- [OpenI](https://openi.nlm.nih.gov/faq#collection)是一个来自印第安纳大学医院的胸部X光片数据集，包括6,459张图像和3,955个报告。

借助ChatGPT的能力，将英文报告进行了中文翻译，并最终形成了可用于训练的数据集。训练时使用12种提示词模板增强多样性。

|数据集|数量|下载链接|
|:-|:-|:-|
|OpenI-zh|6,423|[诊疗报告(英文)](https://github.com/leeguandong/XrayQwenVL/blob/master/data/openi-en.json)、[诊疗报告(中文)](https://github.com/leeguandong/XrayQwenVL/blob/master/data/Xray/openi-zh.json)、[X光影像](https://pan.baidu.com/s/13GBsDMKf6xBZBSHpoWH_EA?pwd=k9sh)|

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

## 快速上手

### 1.安装环境

```bash
# 安装 ms-swift（从源码）
git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .

# 修复 Keras 兼容性
pip install tf-keras
```

### 2.模型推理

|模型权重|下载链接|微调方法|
|:-|:-|:-|
|checkpoint-573|[XrayQwen3VL/results/checkpoint-573](https://github.com/leeguandong/XrayQwen3VL/tree/main/results/checkpoint-573)|LoRA|

#### CLI推理

```bash
CUDA_VISIBLE_DEVICES=0 MAX_PIXELS=1003520 swift infer \
    --model /path/to/Qwen3-VL-8B-Instruct \
    --adapters results/checkpoint-573 \
    --torch_dtype bfloat16 \
    --infer_backend pt
```

#### 批量推理

```bash
python scripts/batch_infer.py \
    --model_path /path/to/Qwen3-VL-8B-Instruct \
    --adapter_path results/checkpoint-573 \
    --test_images data/test/1425_2.png data/test/2808_1.png
```

#### Gradio 推理界面

```bash
python app/gradio_app.py \
    --model_path /path/to/Qwen3-VL-8B-Instruct \
    --adapter_path results/checkpoint-573
```

### 3.模型训练（复现XrayQwen3VL）

<details>
  <summary>硬件资源</summary>
  <p>* 实验在A800 (2X, 80GB)上进行</p>
</details>

- （1）准备[诊疗报告(中文)](https://github.com/leeguandong/XrayQwenVL/blob/master/data/Xray/openi-zh.json)和[X光影像](https://pan.baidu.com/s/13GBsDMKf6xBZBSHpoWH_EA?pwd=k9sh)；
- （2）转换数据格式：
```bash
python scripts/convert_xray_swift.py \
    --source_json /path/to/openi-zh-prompt.json \
    --images_dir /path/to/images2 \
    --output_dir data/
```
- （3）开始训练：
```bash
# 单卡训练
bash tools/swift/finetune_qwen3vl_lora.sh

# 多卡训练
bash tools/swift/finetune_qwen3vl_lora_mp.sh
```

### 4.合并LoRA

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

## 项目致谢

1. [XrayGLM](https://github.com/WangRongsheng/XrayGLM)为我们提供了数据集；
1. [ms-swift](https://github.com/modelscope/ms-swift)为我们提供了训练框架；

## 相关项目

1. [XrayQwenVL](https://github.com/leeguandong/XrayQwenVL)
2. [XrayQwen2VL](https://github.com/leeguandong/XrayQwen2VL)
3. [XrayLLaVA](https://github.com/leeguandong/XrayLLaVA)
4. [XrayLLama3.2Vision](https://github.com/leeguandong/XrayLLama3.2Vision)

## 免责声明

本项目相关资源仅供学术研究之用，严禁用于商业用途。使用涉及第三方代码的部分时，请严格遵循相应的开源协议。模型生成的内容受模型计算、随机性和量化精度损失等因素影响，本项目无法对其准确性作出保证。即使本项目模型输出符合医学事实，也不能被用作实际医学诊断的依据。对于模型输出的任何内容，本项目不承担任何法律责任，亦不对因使用相关资源和输出结果而可能产生的任何损失承担责任。

## 使用许可

此存储库遵循[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/) ，请参阅许可条款。
