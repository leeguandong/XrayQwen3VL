#!/usr/bin/env python3
"""
XrayGLM 数据集转换为 ms-swift messages 格式
将 openi-zh-prompt.json 转为 JSONL，增加 prompt 多样性，切分 train/val
"""
import argparse
import json
import os
import random

PROMPT_TEMPLATES = [
    "通过这张胸部X光影像可以诊断出什么？",
    "请分析这张胸部X光片。",
    "这张X光影像显示了什么？",
    "请对这张胸部X光进行诊断分析。",
    "根据这张X光片，患者的情况如何？",
    "请描述这张胸部X光片的诊断结果。",
    "这张胸部X光影像有什么异常发现吗？",
    "请根据这张X光影像给出诊断意见。",
    "分析这张胸部X光片并给出诊断报告。",
    "请解读这张胸部X光影像的检查结果。",
    "这张X光片反映了哪些临床发现？",
    "请对这张胸部影像进行专业分析。",
]


def convert_dataset(source_json, images_dir, output_dir, split_ratio=0.05, seed=42):
    random.seed(seed)

    with open(source_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    samples = []
    skipped = 0
    for item in data:
        img_filename = os.path.basename(item['img'])
        img_path = os.path.join(images_dir, img_filename)

        if not os.path.exists(img_path):
            skipped += 1
            continue

        prompt = random.choice(PROMPT_TEMPLATES)
        sample = {
            "messages": [
                {"role": "user", "content": f"<image>{prompt}"},
                {"role": "assistant", "content": item['label']}
            ],
            "images": [img_path]
        }
        samples.append(sample)

    random.shuffle(samples)

    val_size = max(1, int(len(samples) * split_ratio))
    val_samples = samples[:val_size]
    train_samples = samples[val_size:]

    os.makedirs(output_dir, exist_ok=True)
    train_path = os.path.join(output_dir, 'train.jsonl')
    val_path = os.path.join(output_dir, 'val.jsonl')

    for path, subset in [(train_path, train_samples), (val_path, val_samples)]:
        with open(path, 'w', encoding='utf-8') as f:
            for s in subset:
                f.write(json.dumps(s, ensure_ascii=False) + '\n')

    print(f"转换完成:")
    print(f"  训练集: {len(train_samples)} 条 -> {train_path}")
    print(f"  验证集: {len(val_samples)} 条 -> {val_path}")
    if skipped:
        print(f"  跳过（图片不存在）: {skipped} 条")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='转换 XrayGLM 数据集为 ms-swift 格式')
    parser.add_argument('--source_json', required=True, help='原始 JSON 文件路径')
    parser.add_argument('--images_dir', required=True, help='图片目录路径')
    parser.add_argument('--output_dir', required=True, help='输出目录')
    parser.add_argument('--split_ratio', type=float, default=0.05, help='验证集比例')
    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    args = parser.parse_args()

    convert_dataset(args.source_json, args.images_dir, args.output_dir, args.split_ratio, args.seed)
