#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from generate_image_prompt import build_prompt, load_presets


def map_questionnaire_to_input(q):
    worldview = q["worldview"]
    identity = q["identity"]

    appearance = q.get("appearance", {})
    narrative = q.get("narrative", {})

    mapped = {
        "worldview": worldview,
        "character_name": q.get("character_name", "Unnamed Character"),
        "identity": identity,
        "gender_expression": q.get("gender_expression", "unspecified"),
        "age_band": appearance.get("age_band", "adult"),
        "body": appearance.get("body", "balanced body proportion"),
        "face": appearance.get("face", "clear facial structure"),
        "hair": appearance.get("hair", "well-groomed hairstyle"),
        "vibe": appearance.get("vibe", "layered, believable personality"),
        "outfit": appearance.get("outfit", "worldview-consistent outfit"),
        "accessories": appearance.get("accessories", "minimal meaningful props"),
        "background": appearance.get("background", "worldview-consistent scene"),
        "pose": appearance.get("pose", "natural portrait pose"),
        "camera": appearance.get("camera", "3/4 portrait, 50mm lens"),
        "quality": q.get("quality", "ultra-detailed, cinematic, high texture fidelity"),
        "style": q.get("style", "refined, elegant, story-rich visual design"),
        "negative_prompt": q.get("negative_prompt", [])
    }

    return mapped, {
        "first_impression": narrative.get("first_impression", ""),
        "closeup_desc": narrative.get("closeup_desc", ""),
        "fullbody_desc": narrative.get("fullbody_desc", ""),
        "prop_story": narrative.get("prop_story", "")
    }


def main():
    parser = argparse.ArgumentParser(description="Bridge questionnaire answers to polished image prompt")
    parser.add_argument("--input", required=True, help="Questionnaire result JSON")
    parser.add_argument("--output", required=True, help="Output JSON with mapped selection and prompt")
    args = parser.parse_args()

    q = json.loads(Path(args.input).read_text(encoding="utf-8"))
    mapped, desc = map_questionnaire_to_input(q)
    presets = load_presets()
    prompt_result = build_prompt(mapped, presets)

    result = {
        "questionnaire_selection": q,
        "mapped_prompt_input": mapped,
        "narrative_notes": desc,
        "generated_prompt": prompt_result
    }

    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "output": args.output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
