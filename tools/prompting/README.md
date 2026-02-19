# Image Prompt Generator (Character Visual)

根据**世界观 + 身份 + 外观描述**生成高质量图片提示词。

## 输入
JSON 文件，关键字段：
- worldview（必填）
- identity（必填）
- appearance fields（body/face/hair/vibe/outfit/accessories）
- background（建议）

## 支持世界观
- three_kingdoms
- contemporary_china
- china_1980s
- china_1990s
- five_dynasties_ten_kingdoms
- condor_heroes
- smiling_proud_wanderer
- harry_potter

## 用法
```bash
python3 tools/prompting/generate_image_prompt.py \
  --input examples/image_prompt_input_three_kingdoms.json
```

可选输出到文件：
```bash
python3 tools/prompting/generate_image_prompt.py \
  --input examples/image_prompt_input_three_kingdoms.json \
  --output /tmp/prompt.json
```

## 输出
- prompt（正向提示词）
- negative_prompt（负向提示词）
- worldview metadata


## 问卷桥接（新增）

将问卷结果直接转换为可用提示词：

```bash
python3 tools/prompting/from_questionnaire_to_prompt.py \
  --input examples/questionnaire_result_three_kingdoms_female_accountant.json \
  --output examples/results/three_kingdoms_female_accountant_prompt_result.json
```

输出包含：
- questionnaire_selection（模拟用户选择结果）
- mapped_prompt_input（标准化后的提示词输入）
- generated_prompt（最终 prompt + negative_prompt）
