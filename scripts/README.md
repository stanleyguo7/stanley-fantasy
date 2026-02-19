# scripts/

项目维护与批量生成脚本。

## 世界观事件库相关
- `generate_worldview_events.py`：初版批量生成事件库
- `rebuild_remaining_worldview_events.py`：重写其余世界观事件库
- `round3_refine_annotations.py`：补充原设锚点
- `round4_add_reference_ranges.py`：补充参考范围
- `round5_full_polish.py`：全量结构化 QA 巡检

## 建议
- 这些脚本主要用于“内容工程维护”，非运行时必需。
- 在大规模改动前建议先创建分支或打 tag。
