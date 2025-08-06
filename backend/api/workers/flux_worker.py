# 这是一个进程实现，通过prompt和params参数（通过json方式的stdin传入），通过podrun.io提供的服务（通过配置文件获取参数），实现具体的flux的AI图片生成，图片个数，通过params["_count"]来确定
import json
import sys
import os
import requests
from typing import Dict, Any

def generate_flux_images(prompt: str, params: Dict[str, Any]) -> None:
    """
    Generate AI images using Flux service based on prompt and parameters
    
    Args:
        prompt (str): The text prompt for image generation
        params (Dict[str, Any]): Parameters including image count in params["_count"]
    """
    # Read podrun.io configuration
    config_path = os.getenv("PODRUN_CONFIG", "config.json")
    with open(config_path) as f:
        config = json.load(f)
    
    # Get Flux API credentials from config
    flux_api_key = config.get("flux_api_key")
    flux_endpoint = config.get("flux_endpoint", "https://api.flux.ai/v1/generate")
    
    # Prepare request payload
    payload = {
        "prompt": prompt,
        "num_images": params.get("_count", 1),
        **params  # Include any additional parameters
    }
    
    headers = {
        "Authorization": f"Bearer {flux_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make request to Flux API
        response = requests.post(
            flux_endpoint,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        # Process and return generated images
        result = response.json()
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")
    params = input_data.get("params", {})
    
    # Generate images
    generate_flux_images(prompt, params)

if __name__ == "__main__":
    main()
