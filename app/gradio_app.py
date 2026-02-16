#!/usr/bin/env python3
"""
XrayQwen3VL Gradio 推理界面
用法: python app/gradio_app.py --model_path MODEL --adapter_path ADAPTER [--port 7860]
"""
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='XrayQwen3VL Gradio 推理界面')
    parser.add_argument('--model_path', required=True, help='基座模型路径')
    parser.add_argument('--adapter_path', required=True, help='LoRA adapter 路径')
    parser.add_argument('--port', type=int, default=7860, help='服务端口')
    parser.add_argument('--share', action='store_true', help='创建公网链接')
    parser.add_argument('--max_tokens', type=int, default=512)
    args = parser.parse_args()

    print(f'模型: {args.model_path}')
    print(f'LoRA: {args.adapter_path}')
    print('正在加载模型...')

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

    print('模型加载完成，启动 Gradio...')

    import gradio as gr

    def predict(image, prompt, max_tokens, temperature):
        if image is None:
            return '请上传一张胸部X光图片'
        request_config = RequestConfig(
            max_tokens=int(max_tokens), temperature=float(temperature))
        infer_request = InferRequest(
            messages=[{'role': 'user', 'content': f'<image>{prompt}'}],
            images=[image])
        response = engine.infer([infer_request], request_config=request_config)
        return response[0].choices[0].message.content

    with gr.Blocks(title='XrayQwen3VL 胸部X光诊断') as demo:
        gr.Markdown('# XrayQwen3VL 胸部X光智能诊断')
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type='pil', label='上传胸部X光图片')
                prompt_input = gr.Textbox(
                    value='通过这张胸部X光影像可以诊断出什么？',
                    label='提示词', lines=2)
                with gr.Row():
                    max_tokens_slider = gr.Slider(
                        64, 1024, value=args.max_tokens, step=64, label='最大生成长度')
                    temperature_slider = gr.Slider(
                        0.0, 1.0, value=0.1, step=0.05, label='Temperature')
                submit_btn = gr.Button('开始诊断', variant='primary')
            with gr.Column(scale=1):
                output_text = gr.Textbox(label='诊断结果', lines=15)

        submit_btn.click(
            fn=predict,
            inputs=[image_input, prompt_input, max_tokens_slider, temperature_slider],
            outputs=output_text)

    demo.launch(server_name='0.0.0.0', server_port=args.port, share=args.share)


if __name__ == '__main__':
    main()
