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
- 新增Thinking版本：使用Gemini蒸馏1000条带思维链的诊断数据，基于Qwen3-VL-8B-Thinking训练，模型会先进行系统性推理再给出诊断结论。
- 相比前作XrayQwenVL/XrayQwen2VL，升级到Qwen3-VL架构，使用ms-swift v4框架，支持单卡/多卡训练。

## 效果展示

### Instruct 版本

影像诊断：
|X光影像|诊疗报告(医生)|XrayQwen3VL-Instruct|
|:-|:-|:-|
|![](./data/test/1425_2.png)|患者的胸部X光片显示双侧肺部清晰，没有任何合并症、气胸或胸腔积液的迹象。心脏纵隔的轮廓和胸腔的骨质结构都在正常范围内。X光片的印象表明，没有急性心肺功能异常。这表明病人在这个时候有一个健康的呼吸和心血管系统。|X光片显示，心脏大小正常，纵膈不明显。肺部清晰，没有急性疾病的迹象。|
|![](./data/test/2808_1.png)|X光片显示有陈旧性肉芽肿病的后遗症，但肺部清晰，没有任何局灶性固结、胸腔积液或气胸。心脏和纵膈的大小和轮廓正常，表明没有急性心肺功能异常。总的来说，这是一张清晰的胸部X光片。|X光片显示，心脏大小和纵隔轮廓正常。肺部清晰，没有局灶性气隙不透明、胸腔积液或气胸。骨骼结构完整。印象中，没有急性心肺异常。|
|![](./data/test/348_2.png)|研究结果表明，心脏大小和纵隔轮廓正常，肺部清晰，肺血管正常，没有胸腔积液或气孔。此外，观察到胸椎的退行性变化很小。根据印象，没有急性心肺异常的迹象。根据这些结果，病人的整体状况似乎是最佳的。|X光片显示，心脏大小和纵隔轮廓正常，肺部清晰，没有气胸或胸腔积液的迹象。此外，没有急性骨质异常的情况。根据这些发现，没有急性心肺功能异常。|
|![](./data/test/1785_2.png)|胸部X光片显示心脏和纵隔轮廓正常，气管旁区域有肉芽肿性钙化，右上叶有轻度条纹状瘢痕。没有发现活动性肺炎或气胸。骨骼结构完整。根据这些发现，没有大叶性肺炎存在。|X光片显示，心脏大小正常，纵隔轮廓和肺部血管也正常。没有局灶性气隙不透明、胸腔积液或气胸。然而，有证据表明存在慢性变化，如肺气肿和肉芽肿。印象中，没有急性心肺异常，但有肺气肿和肉芽肿的存在。|

### Thinking 版本

Thinking版本会先输出`<think>`推理过程，再给出最终诊断。以下展示最终诊断结果及完整推理过程：

|X光影像|诊疗报告(医生)|XrayQwen3VL-Thinking|
|:-|:-|:-|
|![](./data/test/1425_2.png)|患者的胸部X光片显示双侧肺部清晰，没有任何合并症、气胸或胸腔积液的迹象。心脏纵隔的轮廓和胸腔的骨质结构都在正常范围内。X光片的印象表明，没有急性心肺功能异常。|X光片显示心脏大小正常，肺部清晰，没有局灶性空隙疾病、胸腔积液或气胸的证据。印象中，没有急性心肺功能异常。|
|![](./data/test/2808_1.png)|X光片显示有陈旧性肉芽肿病的后遗症，但肺部清晰，没有任何局灶性固结、胸腔积液或气胸。心脏和纵膈的大小和轮廓正常，表明没有急性心肺功能异常。|X光片显示，心脏大小正常，肺部清晰。然而，肺部血管有轻度的突出，提示轻度肺动脉高压。此外，还观察到右肺上叶的钙化肉芽肿。总的来说，没有急性心肺功能异常。|
|![](./data/test/348_2.png)|研究结果表明，心脏大小和纵隔轮廓正常，肺部清晰，肺血管正常，没有胸腔积液或气孔。此外，观察到胸椎的退行性变化很小。根据印象，没有急性心肺异常的迹象。|X光片显示，心脏大小正常，肺部清晰，没有局灶性空隙疾病、胸腔积液或气胸的证据。然而，胸椎有退行性改变。印象中，没有急性心肺功能异常。|
|![](./data/test/1785_2.png)|胸部X光片显示心脏和纵隔轮廓正常，气管旁区域有肉芽肿性钙化，右上叶有轻度条纹状瘢痕。没有发现活动性肺炎或气胸。骨骼结构完整。|X光片显示心脏大小正常，肺部清晰，没有局灶性空隙疾病、胸腔积液或气胸的证据。然而，胸椎有退行性改变。总的来说，没有急性心肺功能异常。|

<details>
<summary>1425_2.png 推理过程（点击展开）</summary>

```
作为一名放射科医生，我将对这张胸部侧位X光片进行系统性的分析和诊断：

### 1. 系统性检查与观察表现

*   肺野（Lung Fields）：在侧位片上，观察到下叶后基底段区域存在明显的密度增高影。
    该区域的透亮度明显降低，与周围正常的肺组织形成对比。
*   心脏与纵隔（Heart and Mediastinum）：心影大小在侧位片上观察基本正常。纵隔未见
    明显偏移，气管位置正常。
*   膈肌与肋膈角（Diaphragm and Costophrenic Angles）：后肋膈角变钝，提示存在少量
    胸腔积液。由于下叶的病变，膈肌的后部轮廓变得模糊（Silhouette sign）。
*   骨骼与软组织（Bones and Soft Tissues）：胸椎可见轻度的骨质增生（骨赘形成），
    属于退行性改变。胸壁软组织未见异常。

### 2. 鉴别诊断推理

*   肺炎（Pneumonia）：下叶后基底段的片状高密度影是典型的肺炎表现。
*   胸腔积液（Pleural Effusion）：后肋膈角变钝提示积液，通常与肺炎并发。
*   肺不张（Atelectasis）：下叶的密度增高也可能由肺不张引起，但形态更符合实变。
*   肺部肿块（Lung Mass）：该影的边缘较模糊，更符合炎症浸润的特征。

### 3. 诊断结论

影像学诊断：
1. 左下叶肺炎（Left Lower Lobe Pneumonia）
2. 少量胸腔积液（Small Pleural Effusion）
```

</details>

<details>
<summary>2808_1.png 推理过程（点击展开）</summary>

```
作为一名放射科医生，我将对这张胸部X光片（后前位/正位）进行系统性的分析和诊断：

### 1. 系统性检查描述

*   肺野（Lung Fields）：双肺透亮度正常，未见明显的渗出性病变、实变影、肿块或结节。
    肺纹理走行自然，未见增粗或紊乱。
*   心脏与大血管（Heart and Great Vessels）：心影大小、形态在正常范围内，心胸比（CTR）
    小于0.5。主动脉弓未见明显扩张或钙化。纵隔居中，未见增宽。
*   膈肌与肋膈角（Diaphragm and Costophrenic Angles）：双侧膈肌光滑，位置正常。
    双侧肋膈角锐利，未见胸腔积液征象。
*   骨骼与软组织（Bones and Soft Tissues）：肋骨、锁骨及所见脊椎骨质未见明显骨折
    或破坏征象。

### 2. 异常表现描述

*   最显著的异常：在心影后方、左肺门区域可见一个明显的、边界清晰的圆形高密度影。
*   形态：影像呈典型的"心后三角征（Retrocardiac Triangle Sign）"。

### 3. 鉴别诊断推理

*   心后三角征（Retrocardiac Triangle Sign）：当肺部病变位于心脏后方时，该区域密度
    会显得比实际更高。通常提示病变位于左肺下叶后基底段。
*   左下叶肺炎（Left Lower Lobe Pneumonia）：最常见的原因。
*   左下叶肺不张（Left Lower Lobe Atelectasis）：通常伴有叶间裂移位或膈肌抬高，
    本片中不明显。
*   纵隔肿块：位于如此靠后的位置，可能性较低。

### 4. 诊断结论

影像学诊断：心后三角征，高度提示左下叶肺部实变（Left Lower Lobe Pneumonia）。
建议进行胸部CT扫描以进一步明确病变性质。
```

</details>

<details>
<summary>348_2.png 推理过程（点击展开）</summary>

```
作为一名放射科医生，我将对这张胸部侧位X光片进行系统性的分析和诊断：

### 1. 系统性检查与观察表现

*   肺野（Lung Fields）：最显著的异常发现位于心后区（Retrocardiac area）。正常情况下
    心后区应该比较透亮，但本影像中该区域可见明显的密度增高影。
*   心脏与纵隔（Heart and Mediastinum）：心脏大小尚属正常范围。纵隔未见明显偏移。
*   膈肌与肋膈角（Diaphragm and Costophrenic Angles）：后肋膈角区密度增高影与膈肌
    重叠，导致后肋膈角变钝。
*   骨骼与软组织：胸椎可见轻度骨质增生，属于退行性改变。

### 2. 异常表现描述

主要异常表现为：心后区及后肋膈角区的密度增高影。这种表现通常被称为"脊柱征
（Spine Sign）"阳性。正常侧位胸片中，胸椎从上往下应该越来越透亮，但本片中
下段胸椎密度反而比中段更高，提示下叶后部存在病变。

### 3. 鉴别诊断推理

1. 下叶肺炎（Lower Lobe Pneumonia）：最常见的原因。
2. 胸腔积液（Pleural Effusion）：后肋膈角模糊提示可能存在少量积液。
3. 肺不张（Atelectasis）：通常伴有叶间裂移位或膈肌抬高，本片中不明显。
4. 肺部肿块（Lung Mass）：密度影形态较为弥漫，更符合炎症浸润。

### 4. 诊断结论

1. 心后区密度增高影：考虑为左下叶或右下叶肺炎（实变影）。
2. 后肋膈角模糊：提示可能存在少量胸腔积液。
3. 胸椎退行性变：老年性骨质增生。
```

</details>

<details>
<summary>1785_2.png 推理过程（点击展开）</summary>

```
作为一名放射科医生，我将对这张胸部侧位X光片进行系统性的分析和诊断：

### 1. 系统性检查与观察表现

*   肺野（Lung Fields）：最显著的异常发现位于下叶后基底段。可以看到一个明显的、
    边缘清晰的楔形（三角形）致密影，其尖端指向肺门，基底朝向后胸壁。
*   心脏与纵隔（Heart and Mediastinum）：心脏大小基本正常。纵隔未见明显偏移。
*   膈肌与肋膈角（Diaphragm and Costophrenic Angles）：后肋膈角变钝，提示存在
    少量胸腔积液。前肋膈角锐利。
*   骨骼与软组织：胸椎可见轻度骨质增生，属于退行性改变。

### 2. 鉴别诊断推理

*   肺不张（Atelectasis）：最可能的诊断。下叶后基底段的楔形致密影是典型表现。
*   肺炎（Pneumonia）：通常表现为斑片状模糊影，边缘不如肺不张锐利。本例边缘
    非常清晰，更符合体积缩小的特征。
*   胸腔积液（Pleural Effusion）：后肋膈角变钝提示有少量积液，但主要致密影位于
    肺实质内。
*   肺部肿块（Lung Mass）：该影形态非常符合肺不张特征。

### 3. 诊断结论

诊断：左下叶肺不张（Left Lower Lobe Atelectasis）
侧位片显示左下叶后基底段体积缩小，表现为典型的楔形致密影。
建议进一步行胸部CT扫描以明确肺不张的原因。
```

</details>

## 训练结果

| 基座模型 | 方法 | 训练集 | 验证集 | Train Loss | Eval Loss | Token Acc |
|---------|------|--------|--------|-----------|-----------|-----------|
| Qwen3-VL-8B-Instruct | LoRA | 6,102 | 321 | 1.382 | 1.250 | 69% / 66% |
| Qwen3-VL-8B-Thinking | LoRA | 950 | 50 | 0.865 | 0.893 | 76% / 75% |

Thinking版本使用Gemini蒸馏的思维链数据训练，数据格式为`<think>推理过程</think>最终诊断`。

## 数据集

- [OpenI](https://openi.nlm.nih.gov/faq#collection)是一个来自印第安纳大学医院的胸部X光片数据集，包括6,459张图像和3,955个报告。

借助ChatGPT的能力，将英文报告进行了中文翻译，并最终形成了可用于训练的数据集。训练时使用12种提示词模板增强多样性。

|数据集|数量|下载链接|
|:-|:-|:-|
|OpenI-zh|6,423|[诊疗报告(英文)](https://github.com/leeguandong/XrayQwenVL/blob/master/data/openi-en.json)、[诊疗报告(中文)](https://github.com/leeguandong/XrayQwenVL/blob/master/data/Xray/openi-zh.json)、[X光影像](https://pan.baidu.com/s/13GBsDMKf6xBZBSHpoWH_EA?pwd=k9sh)|
|OpenI-zh-thinking|1,000|从OpenI-zh中采样1000条，使用Gemini蒸馏生成思维链推理过程|

## 模型架构

```
Qwen3-VL-8B-Instruct / Qwen3-VL-8B-Thinking
├── Vision Encoder (ViT)     ← 冻结
├── Visual-Language Aligner  ← 冻结
└── Language Model (LLM)     ← LoRA 微调
    ├── lora_rank: 8
    ├── lora_alpha: 32
    └── target_modules: all-linear
```

Thinking版本的数据流：
```
输入X光图片 → ViT编码 → Aligner → LLM → <think>系统性推理过程</think> → 最终诊断结论
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

|模型权重|基座模型|下载链接|微调方法|
|:-|:-|:-|:-|
|checkpoint-573|Qwen3-VL-8B-Instruct|[results/checkpoint-573](https://github.com/leeguandong/XrayQwen3VL/tree/main/results/checkpoint-573)|LoRA|
|checkpoint-90-thinking|Qwen3-VL-8B-Thinking|[results/checkpoint-90-thinking](https://github.com/leeguandong/XrayQwen3VL/tree/main/results/checkpoint-90-thinking)|LoRA + 思维链蒸馏|

#### CLI推理

```bash
# Instruct 版本
CUDA_VISIBLE_DEVICES=0 MAX_PIXELS=1003520 swift infer \
    --model /path/to/Qwen3-VL-8B-Instruct \
    --adapters results/checkpoint-573 \
    --torch_dtype bfloat16 \
    --infer_backend pt

# Thinking 版本（输出包含 <think>推理过程</think> + 诊断结论）
CUDA_VISIBLE_DEVICES=0 MAX_PIXELS=1003520 swift infer \
    --model /path/to/Qwen3-VL-8B-Thinking \
    --adapters results/checkpoint-90-thinking \
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
├── results/                 # LoRA 权重
│   ├── checkpoint-573/             # Instruct 版本
│   └── checkpoint-90-thinking/     # Thinking 版本
└── app/                     # 应用（Gradio）
    └── gradio_app.py
```

## 训练超参数

### Instruct 版本

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

### Thinking 版本

| 参数 | 值 |
|------|-----|
| 基座模型 | Qwen3-VL-8B-Thinking |
| 微调方法 | LoRA |
| 蒸馏数据 | Gemini蒸馏1000条思维链 |
| 数据格式 | `<think>推理过程</think>最终诊断` |
| lora_rank | 8 |
| lora_alpha | 32 |
| target_modules | all-linear |
| freeze_vit | true |
| freeze_aligner | true |
| num_epochs | 3 |
| learning_rate | 1e-4 |
| max_length | 4096 |
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
