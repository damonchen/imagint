# 这是一个进程实现，通过prompt和params参数（通过json方式的stdin传入），通过podrun.io提供的服务（通过配置文件获取参数），实现具体的flux的AI图片生成，图片个数，通过params["_count"]来确定
import json
import sys
import os
import random
import uuid
from typing import Dict, Any

import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "gcc")
    .pip_install(
        "git+https://github.com/huggingface/diffusers",
        "protobuf",
        "transformers[sentencepiece]",
        "torch",
        "torchvision",
        "accelerate",
        "transformers",
    )
    .env({"HALT_AND_CATCH_FIRE": "0"})
    # .run_commands("git clone https://github.com/modal-labs/agi && echo 'ready to go!'")
)

app = modal.App(image=image)


with image.imports():
    from diffusers import DiffusionPipeline
    import torch

CACHE_DIR = "/cache"
cache_vol = modal.Volume.from_name("hf-hub-cache", create_if_missing=True)


@app.cls(
    image=image,
    gpu="H200",
    volumes={CACHE_DIR: cache_vol},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=600,
)
class Inference(object):
    @modal.enter()
    def initialize(self):
        # 模型配置
        model_name = "black-forest-labs/FLUX.1-dev"
        # 设备配置
        if torch.cuda.is_available():
            self.torch_dtype = torch.bfloat16
            self.device = "cuda"
        else:
            self.torch_dtype = torch.float32
            self.device = "cpu"

        self.pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=self.torch_dtype,
            # use_auth_token=os.environ["HF_TOKEN"],
        )

    @modal.enter()
    def move_to_gpu(self):
        self.pipe.to(self.device)

    @modal.method()
    def run(
        self, prompt: str, ratio: str = "16:9", batch_size: int = 4, seed: int = None
    ):
        seed = seed if seed is not None else random.randint(0, 2**32 - 1)

        # 支持多种宽高比
        aspect_ratios = {
            "1:1": (1328, 1328),
            "16:9": (1664, 928),
            "9:16": (928, 1664),
            "4:3": (1472, 1140),
            "3:4": (1140, 1472),
        }

        width, height = aspect_ratios[ratio]

        images = self.pipe(
            prompt=prompt,
            num_images_per_prompt=batch_size,
            width=width,
            height=height,
            guidance_scale=3.5,
            num_inference_steps=50,
            max_sequence_length=512,
            generator=torch.Generator(device=self.device).manual_seed(seed),
        ).images

        return images


# @app.local_entrypoint()
# def main():
#     from PIL import Image

#     input_data = json.load(sys.stdin)
#     prompt = input_data.get("prompt", "")
#     params = input_data.get("params", {})

#     image = params.get("image", "")

#     im = Image.open(image)

#     image = Inference().run.remote(im, prompt)
#     filename = str(uuid.uuid4()) + ".png"
#     image.save(filename)

#     sys.stdout.write(json.dumps({"images": [filename]}))
#     sys.stdout.flush()


@app.local_entrypoint()
def main(prompt, ratio="16:9", batch_size=4, seed=None):
    # ratio = "16:9"
    # batch_size = 4
    # seed = None
    # prompt = "A cat holding a sign that says hello world"

    images = Inference().run.remote(prompt, ratio, batch_size=batch_size, seed=seed)

    file_paths = []
    prefix = str(uuid.uuid4())[:4]
    # output_dir = '.'
    for i, image in enumerate(images):
        v = str(uuid.uuid4())
        output_path = f"images/{prefix}_{i}_{v}.png"
        image.save(output_path)
        # output_path.write_bytes(image_bytes)

        file_paths.append(output_path)

    print(json.dumps(file_paths))
