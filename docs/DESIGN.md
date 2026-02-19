# stanley-fantasy 设计文档（草案 v0.1）

## 1. 目标
通过交互式流程创建与演化虚拟人物，沉淀“可持续维护”的角色资产。

## 2. 架构概览

- **数据层（Markdown + Media）**
  - profile.md：角色静态设定
  - memory/short-term.md：近期互动记忆
  - memory/long-term.md：稳定长期记忆
  - media/：图片、音频、视频素材
- **流程层（后续脚本化）**
  - 角色初始化
  - 互动采集
  - 记忆提炼
  - 一致性检查
- **治理层**
  - 命名规范
  - 版本追踪（Git）
  - 变更审阅机制

## 3. 角色目录标准

每个角色目录建议结构：

```text
characters/<character-id>/
├─ profile.md
├─ memory/
│  ├─ short-term.md
│  └─ long-term.md
├─ scenes/
│  └─ dialogue-seeds.md
└─ media/
   ├─ images/
   ├─ audio/
   └─ video/
```

## 4. 交互式建角流程（建议）

1. 收集基础设定（名称、世界观、外观、核心冲突）
2. 生成初版 profile.md
3. 生成 5~10 条对话种子（scenes）
4. 生成初始短期/长期记忆
5. 补充媒体素材（立绘、语音、参考片段）
6. 人工确认并冻结 v1

## 5. 记忆策略

- **短期记忆**：记录近阶段互动事实，定期归档
- **长期记忆**：只保留稳定事实与关键里程碑
- **迁移规则**：短期中重复出现、且稳定不冲突的事实，迁移到长期

## 6. 下一阶段计划（v0.2）

- 提供 `scripts/new_character.sh` 一键建角
- 提供 `scripts/check_consistency.py` 设定一致性检查
- 提供 `docs/INTERVIEW_FLOW.md` 标准访谈提纲
- 提供问卷化流程：`docs/forms/CHARACTER_BACKGROUND_QUESTIONNAIRE_v1.md`
- 提供世界观候选库：`docs/WORLDVIEW_CATALOG.md`


## 7. 问卷流程升级（v2）
- 首题改为“具体世界观单选”
- 第二步根据世界观文档选择角色类型
- 参考：`docs/worldviews/README.md` 与 `docs/forms/CHARACTER_BACKGROUND_QUESTIONNAIRE_v2.md`
