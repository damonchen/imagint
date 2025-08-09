# 这是一个进程实现，通过prompt和params参数（通过json方式的stdin传入），通过podrun.io提供的服务（通过配置文件获取参数），实现具体的flux的AI图片生成，图片个数，通过params["_count"]来确定
import json
import sys
import os
import requests
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
    from diffusers import FluxKontextPipeline
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
        model_name = "black-forest-labs/FLUX.1-Kontext-dev"
        # 设备配置
        if torch.cuda.is_available():
            self.torch_dtype = torch.bfloat16
            self.device = "cuda"
        else:
            self.torch_dtype = torch.float32
            self.device = "cpu"

        self.pipe = FluxKontextPipeline.from_pretrained(
            model_name,
            torch_dtype=self.torch_dtype,
            # use_auth_token=os.environ["HF_TOKEN"],
        )

    @modal.enter()
    def move_to_gpu(self):
        self.pipe.to(self.device)

    @modal.method()
    def run(
        self,
        image,
        prompt,
    ):

        image = self.pipe(
            image=image,
            prompt=prompt,
            guidance_scale=3.5,
        ).images[0]

        return image


@app.local_entrypoint()
def main():
    from PIL import Image

    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")
    params = input_data.get("params", {})

    image = params.get("image", "")

    im = Image.open(image)

    image = Inference().run.remote(im, prompt)
    filename = str(uuid.uuid4()) + ".png"
    image.save(filename)

    sys.stdout.write(json.dumps({"images": [filename]}))
    sys.stdout.flush()


# @app.local_entrypoint()
# def main():
#     from PIL import Image

#     im = Image.open("image.png")

#     image = Inference().run.remote(im, "a Add a hat to the girl")
#     filename = str(uuid.uuid4()) + ".png"
#     image.save(filename)

#     sys.stdout.write(json.dumps({"images": [filename]}))
#     sys.stdout.flush()
