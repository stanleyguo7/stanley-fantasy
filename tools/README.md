# tools/

与角色视觉生成相关的工具集。

## prompting/
- `generate_image_prompt.py`：根据世界观 + 角色外观生成高质量提示词
- `from_questionnaire_to_prompt.py`：将问卷结果 JSON 映射为可直接生图的提示词
- `worldview_visual_presets.yaml`：各世界观视觉约束与风格预设

## image/
- `openai_generate_image.py`：调用 OpenAI 图片生成 API
- `jimeng_generate_image.py`：调用即梦 API（可配置路径与返回字段）

## 推荐流水线
1. 填写角色问卷（身份+外观）
2. 用 `from_questionnaire_to_prompt.py` 生成 prompt
3. 选择 OpenAI 或 即梦脚本出图
4. 将成图保存到 `assets/images/generated/...`
