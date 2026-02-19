# OpenAI Image Generator

使用 OpenAI 官方图片生成接口（`/v1/images/generations`）生成角色图。

## 前置

```bash
export OPENAI_API_KEY=your_key
pip install requests
```

## 用法

```bash
python3 tools/image/openai_generate_image.py \
  --prompt "A cinematic portrait of a Three Kingdoms ferry accountant..." \
  --out assets/images/generated/three-kingdoms/shen-he/openai-v1.png \
  --size 1024x1536 \
  --quality high \
  --output-format png \
  --meta-out examples/results/openai-image-meta-shen-he.json
```

## 参数
- `--model` 默认 `gpt-image-1`
- `--size` `1024x1024 | 1024x1536 | 1536x1024 | auto`
- `--quality` `low | medium | high | auto`
- `--background` `transparent | opaque | auto`
- `--output-format` `png | jpeg | webp`

## 与现有提示词工具联动
可先用：
- `tools/prompting/from_questionnaire_to_prompt.py`

拿到 `generated_prompt.prompt` 后再传给本脚本的 `--prompt`。
