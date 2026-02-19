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


## JiMeng（即梦）脚本（新增）

文件：`tools/image/jimeng_generate_image.py`

> 说明：即梦不同渠道接口路径可能不同，本脚本支持通过环境变量配置接口路径和返回字段。

### 环境变量
```bash
export JIMENG_API_BASE_URL="https://your-jimeng-api-base"
export JIMENG_API_KEY="your_key"
# 可选：
# export JIMENG_CREATE_PATH="/v1/images/generations"
# export JIMENG_STATUS_PATH="/v1/tasks/{task_id}"
# export JIMENG_DOWNLOAD_FIELD="image_url"
```

### 调用示例
```bash
python3 tools/image/jimeng_generate_image.py   --prompt "A refined portrait in Three Kingdoms style..."   --out assets/images/generated/three-kingdoms/shen-he/jimeng-v1.png   --size 1024x1536   --steps 30   --meta-out examples/results/jimeng-meta-shen-he.json
```
