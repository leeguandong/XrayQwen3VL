#!/usr/bin/env python3
"""
XrayQwen3VL 推理测试
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_infer():
    """测试单张图片推理"""
    os.environ.setdefault('MAX_PIXELS', '1003520')

    from swift.infer_engine import InferRequest, RequestConfig, TransformersEngine
    from swift.pipelines.utils import prepare_model_template
    from swift.arguments import InferArguments

    model_path = os.environ.get('MODEL_PATH', '/path/to/Qwen3-VL-8B-Instruct')
    adapter_path = os.environ.get('ADAPTER_PATH', 'output/checkpoint-573')
    test_image = os.environ.get('TEST_IMAGE', 'data/test/1425_2.png')

    infer_args = InferArguments(
        model=model_path,
        adapters=[adapter_path],
        torch_dtype='bfloat16',
        infer_backend='transformers',
    )
    model, template = prepare_model_template(infer_args)
    engine = TransformersEngine(model, template=template)

    request_config = RequestConfig(max_tokens=512, temperature=0.0)
    infer_request = InferRequest(
        messages=[{'role': 'user', 'content': '<image>通过这张胸部X光影像可以诊断出什么？'}],
        images=[test_image],
    )
    response = engine.infer([infer_request], request_config=request_config)
    text = response[0].choices[0].message.content
    print(f'诊断结果:\n{text}')
    assert len(text) > 0, '推理结果为空'
    print('\n测试通过!')


if __name__ == '__main__':
    test_infer()
