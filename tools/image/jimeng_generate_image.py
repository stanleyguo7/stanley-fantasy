#!/usr/bin/env python3
"""
JiMeng (即梦) image generation script (generic REST adapter).

This script is designed to be provider-compatible by configuration, since JiMeng
deployments can differ by endpoint path and response schema.

Environment variables:
  JIMENG_API_BASE_URL   e.g. https://api.jimeng.example.com
  JIMENG_API_KEY        your key

Optional env:
  JIMENG_CREATE_PATH    default: /v1/images/generations
  JIMENG_STATUS_PATH    default: /v1/tasks/{task_id}
  JIMENG_DOWNLOAD_FIELD default: image_url

Usage example:
  python3 tools/image/jimeng_generate_image.py \
    --prompt "cinematic portrait ..." \
    --out assets/images/generated/jimeng-demo.png
"""

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests


def getenv_required(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise RuntimeError(f"{name} is not set")
    return v


def pick(d: Dict[str, Any], *keys, default=None):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def request_json(method: str, url: str, headers: Dict[str, str], payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resp = requests.request(method, url, headers=headers, json=payload, timeout=180)
    if resp.status_code >= 300:
        raise RuntimeError(f"HTTP {resp.status_code} {url}: {resp.text}")
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Non-JSON response from {url}: {resp.text[:300]}")


def download_file(url: str, out_path: Path):
    r = requests.get(url, timeout=180)
    if r.status_code >= 300:
        raise RuntimeError(f"Download failed {r.status_code}: {url}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(r.content)


def main():
    parser = argparse.ArgumentParser(description="Generate image via JiMeng API")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--out", required=True)
    parser.add_argument("--model", default="jimeng-image-v1")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--steps", type=int, default=28)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--timeout-sec", type=int, default=300)
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--meta-out", default="")
    args = parser.parse_args()

    base_url = getenv_required("JIMENG_API_BASE_URL").rstrip("/")
    api_key = getenv_required("JIMENG_API_KEY")

    create_path = os.getenv("JIMENG_CREATE_PATH", "/v1/images/generations")
    status_path_tpl = os.getenv("JIMENG_STATUS_PATH", "/v1/tasks/{task_id}")
    download_field = os.getenv("JIMENG_DOWNLOAD_FIELD", "image_url")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    create_url = f"{base_url}{create_path}"
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt,
        "size": args.size,
        "steps": args.steps,
    }
    if args.seed:
        payload["seed"] = args.seed

    created = request_json("POST", create_url, headers, payload)

    # Compatible extraction for sync/async styles
    image_url = pick(created, download_field)
    task_id = pick(created, "task_id", "id", "job_id")
    status = str(pick(created, "status", default="")).lower()

    # sync: already has URL
    if image_url:
        final = created
    else:
        if not task_id:
            raise RuntimeError(
                "JiMeng response has no direct image URL and no task id. "
                "Please set correct JIMENG_CREATE_PATH / response mapping.\n"
                f"Response: {json.dumps(created, ensure_ascii=False)}"
            )

        deadline = time.time() + args.timeout_sec
        final = created
        while time.time() < deadline:
            status_url = f"{base_url}{status_path_tpl.format(task_id=task_id)}"
            final = request_json("GET", status_url, headers)
            status = str(pick(final, "status", default="")).lower()
            image_url = pick(final, download_field, "url", "result_url")

            if image_url:
                break
            if status in {"failed", "error", "canceled", "cancelled"}:
                raise RuntimeError(f"Task failed: {json.dumps(final, ensure_ascii=False)}")

            time.sleep(args.poll_interval)

        if not image_url:
            raise RuntimeError(f"Timed out waiting image_url. Last response: {json.dumps(final, ensure_ascii=False)}")

    out_path = Path(args.out)
    download_file(image_url, out_path)
    print(f"Saved image: {out_path}")

    if args.meta_out:
        meta_path = Path(args.meta_out)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps({"create": created, "final": final}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved metadata: {meta_path}")


if __name__ == "__main__":
    main()
