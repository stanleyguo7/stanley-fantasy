#!/usr/bin/env python3
import argparse, json, textwrap
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

ROOT = Path(__file__).resolve().parent
PRESET_FILE = ROOT / "worldview_visual_presets.yaml"


def load_presets():
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
    data = yaml.safe_load(PRESET_FILE.read_text(encoding="utf-8"))
    return data["worldviews"]


def join_list(items):
    return "; ".join(items)


def build_prompt(inp, presets):
    wv = inp["worldview"]
    if wv not in presets:
        raise ValueError(f"Unknown worldview: {wv}")
    p = presets[wv]

    name = inp.get("character_name", "Unnamed Character")
    identity = inp.get("identity", "civilian")
    gender_expr = inp.get("gender_expression", "unspecified")
    age = inp.get("age_band", "adult")
    body = inp.get("body", "balanced body proportion")
    face = inp.get("face", "distinct facial features")
    hair = inp.get("hair", "well-defined hairstyle")
    vibe = inp.get("vibe", "calm and layered personality")
    outfit = inp.get("outfit", "worldview-consistent outfit")
    accessories = inp.get("accessories", "minimal meaningful accessories")
    background = inp.get("background", "environment matching role and era")
    pose = inp.get("pose", "natural standing pose")
    camera = inp.get("camera", "medium full-body portrait, 50mm lens")
    quality = inp.get("quality", "ultra-detailed, cinematic, high texture fidelity")
    style = inp.get("style", "elegant, refined, story-rich visual design")

    negative = inp.get("negative_prompt", [
        "lowres", "blurry", "deformed hands", "extra fingers", "bad anatomy",
        "watermark", "text overlay", "logo", "modern anachronism", "oversaturated plastic skin"
    ])

    prompt = textwrap.dedent(f"""
    Character concept art, {quality}, {style}.
    Subject: {name}, {age}, {gender_expr}, identity: {identity}.
    Appearance: {body}; {face}; {hair}; overall vibe: {vibe}.
    Outfit: {outfit}; accessories: {accessories}.
    Worldview: {p['name']}.
    Era and lore cues: {join_list(p['era_keywords'])}.
    Costume constraints: {join_list(p['costume_rules'])}.
    Background scene: {background}; scene constraints: {join_list(p['background_rules'])}.
    Pose and action: {pose}.
    Lighting and atmosphere: {join_list(p['lighting_style'])}.
    Camera and composition: {camera}; shallow depth of field, cinematic composition.
    """).strip()

    return {
        "prompt": " ".join(prompt.split()),
        "negative_prompt": ", ".join(negative),
        "worldview": wv,
        "worldview_name": p["name"],
    }


def main():
    parser = argparse.ArgumentParser(description="Generate polished image prompts from worldview + identity + appearance")
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", default="", help="Optional output JSON path")
    args = parser.parse_args()

    presets = load_presets()
    inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = build_prompt(inp, presets)

    out_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out_text, encoding="utf-8")
    print(out_text)


if __name__ == "__main__":
    main()
