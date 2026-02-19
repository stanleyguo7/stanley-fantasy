# stanley-fantasy

一个用于“交互式创建虚拟人物”的项目。

目标：
- 通过对话/互动逐步生成角色
- 每个角色拥有完整档案（设定、关系、外观、语气、世界观锚点）
- 每个角色拥有独立记忆（可长期演化）
- 角色资料可由 Markdown + 多媒体素材共同构成

## 核心理念

1. **角色即目录**：每个虚拟人物一个独立目录，包含完整资料与素材。
2. **文档即状态**：角色状态尽量通过 Markdown 明确记录，便于追踪与版本控制。
3. **记忆分层**：短期记忆与长期记忆分开，避免污染、便于维护。
4. **可演进**：后续可以接入自动化脚本、生成模型、检索系统。

## 目录结构

```text
stanley-fantasy/
├─ docs/                     # 项目文档（设计、规范、流程）
├─ templates/                # 角色模板
├─ assets/                   # 通用素材（非角色专属）
│  ├─ images/
│  ├─ audio/
│  └─ video/
├─ characters/               # 角色总目录
│  ├─ .index/                # 角色索引与状态表
│  └─ <character-id>/        # 单个角色资料目录
└─ scripts/                  # 自动化脚本（后续）
```

## 快速开始

1. 复制 `templates/character-template/` 到 `characters/<character-id>/`
2. 填写 `profile.md` 与 `memory/` 下文档
3. 将图片/音频/视频放入 `media/`
4. 更新 `characters/.index/characters.md`

## 状态

当前为 v0 基础骨架，后续将补充：
- 交互式建角流程
- 角色一致性检查
- 记忆更新策略
- 多媒体素材规范


## 目录导航（已整理）

- `docs/worldviews/`：世界观设定与事件库
- `docs/forms/`：背景与外观问卷
- `docs/character-design/`：身份/家庭/关系模板与外观系统
- `tools/`：提示词与生图工具（见 `tools/README.md`）
- `scripts/`：内容批量生成与精修脚本（见 `scripts/README.md`）
- `assets/images/generated/`：生成图片素材归档

## 视觉生成最短流程

1. 准备问卷结果 JSON（示例在 `examples/`）
2. 运行问卷桥接：
   - `python3 tools/prompting/from_questionnaire_to_prompt.py --input ... --output ...`
3. 选择生图引擎：
   - OpenAI：`python3 tools/image/openai_generate_image.py ...`
   - 即梦：`python3 tools/image/jimeng_generate_image.py ...`
4. 结果入库到 `assets/images/generated/<worldview>/<character>/`
