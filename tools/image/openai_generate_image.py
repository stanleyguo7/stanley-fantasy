#!/usr/bin/env python3
"""
Generate images with OpenAI Images API.

Requirements:
  export OPENAI_API_KEY=...

Example:
  python3 tools/image/openai_generate_image.py \
    --prompt "A cinematic portrait of ..." \
    --out assets/images/generated/test.png
"""

import argparse
import base64
import json
import os
from pathlib import Path

import requests

API_URL = "https://api.openai.com/v1/images/generations"


def generate_image(
    api_key: str,
    prompt: str,
    model: str = "gpt-image-1",
    size: str = "1024x1024",
    quality: str = "high",
    background: str = "auto",
    output_format: str = "png",
):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "background": background,
        "output_format": output_format,
    }

    resp = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=180)
    if resp.status_code >= 300:
        raise RuntimeError(f"OpenAI API error {resp.status_code}: {resp.text}")

    data = resp.json()
    if not data.get("data"):
        raise RuntimeError(f"Unexpected response: {data}")

    item = data["data"][0]
    b64 = item.get("b64_json")
    if not b64:
        raise RuntimeError(f"No b64_json in response: {item}")

    image_bytes = base64.b64decode(b64)
    return image_bytes, data


def main():
    parser = argparse.ArgumentParser(description="Generate image via OpenAI Images API")
    parser.add_argument("--prompt", required=True, help="Image prompt")
    parser.add_argument("--out", required=True, help="Output image path")
    parser.add_argument("--model", default="gpt-image-1")
    parser.add_argument("--size", default="1024x1024", choices=["1024x1024", "1024x1536", "1536x1024", "auto"])
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high", "auto"])
    parser.add_argument("--background", default="auto", choices=["transparent", "opaque", "auto"])
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"])
    parser.add_argument("--meta-out", default="", help="Optional path to save full JSON response")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    image_bytes, raw = generate_image(
        api_key=api_key,
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        quality=args.quality,
        background=args.background,
        output_format=args.output_format,
    )

    out_path.write_bytes(image_bytes)
    print(f"Saved image: {out_path}")

    if args.meta_out:
        meta_path = Path(args.meta_out)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved metadata: {meta_path}")


if __name__ == "__main__":
    main()
