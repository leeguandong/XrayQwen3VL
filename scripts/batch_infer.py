#!/usr/bin/env python3
"""
XrayQwen3VL 批量推理脚本
用法: python scripts/batch_infer.py --model_path MODEL --adapter_path ADAPTER [--test_images ...]
"""
import argparse
import json
import os


def main():
    parser = argparse.ArgumentParser(description='XrayQwen3VL 批量推理')
    parser.add_argument('--model_path', required=True, help='基座模型路径')
    parser.add_argument('--adapter_path', required=True, help='LoRA adapter 路径')
    parser.add_argument('--test_images', nargs='+', default=None, help='测试图片路径')
    parser.add_argument('--images_dir', default=None, help='图片目录（随机选取测试图片）')
    parser.add_argument('--num_samples', type=int, default=5, help='随机选取图片数量')
    parser.add_argument('--prompt', default='通过这张胸部X光影像可以诊断出什么？')
    parser.add_argument('--max_tokens', type=int, default=512)
    parser.add_argument('--output_file', default='infer_results.json')
    args = parser.parse_args()

    if args.test_images is None:
        if args.images_dir is None:
            print('错误: 请指定 --test_images 或 --images_dir')
            return
        import random
        random.seed(42)
        all_imgs = [f for f in os.listdir(args.images_dir) if f.endswith('.png')]
        selected = random.sample(all_imgs, min(args.num_samples, len(all_imgs)))
        args.test_images = [os.path.join(args.images_dir, f) for f in selected]

    print(f'模型: {args.model_path}')
    print(f'LoRA: {args.adapter_path}')
    print(f'测试图片: {len(args.test_images)} 张')
    print()

    os.environ.setdefault('MAX_PIXELS', '1003520')

    from swift.infer_engine import InferRequest, RequestConfig, TransformersEngine
    from swift.pipelines.utils import prepare_model_template
    from swift.arguments import InferArguments

    infer_args = InferArguments(
        model=args.model_path,
        adapters=[args.adapter_path],
        torch_dtype='bfloat16',
        infer_backend='transformers',
    )
    model, template = prepare_model_template(infer_args)
    engine = TransformersEngine(model, template=template)
    request_config = RequestConfig(max_tokens=args.max_tokens, temperature=0.0)

    results = []
    for img_path in args.test_images:
        print(f'--- {os.path.basename(img_path)} ---')
        infer_request = InferRequest(
            messages=[{'role': 'user', 'content': f'<image>{args.prompt}'}],
            images=[img_path],
        )
        response = engine.infer([infer_request], request_config=request_config)
        text = response[0].choices[0].message.content
        print(text)
        print()
        results.append({'image': img_path, 'prompt': args.prompt, 'response': text})

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'结果已保存至: {args.output_file}')


if __name__ == '__main__':
    main()
