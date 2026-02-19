from pathlib import Path
import re

base = Path('docs/worldviews/events')

sgk_anchors = [
"黄巾起义（演义开篇）","何进与十常侍之变","董卓入洛阳与废立","关东诸侯会盟讨董","虎牢关三英战吕布（演义）","王允连环计与诛董（演义）","李傕郭汜乱长安","曹操奉天子都许","吕布据徐州与下邳败亡","宛城之战与典韦战死（演义）",
"白马延津前哨战","官渡乌巢决胜","仓亭与袁氏衰退","曹操平定河北","白狼山破乌桓","刘备依荆州与隆中对","曹操南征荆州","长坂坡救主（演义）","孙刘联盟形成","赤壁之战",
"南郡争夺与荆州分治","刘备入蜀前奏","落凤坡庞统殒命（演义）","刘备据益州","逍遥津之战（演义强化）","荆州借地矛盾","曹操取汉中","定军山斩夏侯渊（演义）","关羽北伐襄樊","吕蒙白衣渡江",
"麦城败亡关羽遇害","曹操卒与魏政交接","刘备称帝","夷陵之战","白帝城托孤","孙权称帝","诸葛亮南征（七擒孟获演义）","第一次北伐与街亭","陈仓攻守","木牛流马叙事（演义）",
"祁山对峙","五丈原诸葛亮病逝","魏政权重心转移","姜维继承北伐","东吴后期内耗","伐蜀前夜部署","剑阁相持阴平奇袭","刘禅出降","钟会姜维之乱","晋灭吴终结三国"
]

def add_anchor_per_event(path, anchor_fn):
    txt = path.read_text(encoding='utf-8')
    parts = re.split(r'(?m)^(### 事件\s+\d+｜.*)$', txt)
    if len(parts) < 3:
        return False
    out = [parts[0]]
    event_index = 0
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1]
        event_index += 1
        anchor_line = f"- **原设锚点**：{anchor_fn(event_index)}\n"
        # already has anchor? replace first occurrence
        if '- **原设锚点**：' in body:
            body = re.sub(r'- \*\*原设锚点\*\*：.*\n', anchor_line, body, count=1)
        else:
            body = anchor_line + body.lstrip('\n')
        out.extend([header, '\n', body])
    path.write_text(''.join(out), encoding='utf-8')
    return True

# 三国精修（逐事件锚点）
sgk = base / '04-three-kingdoms-events.md'
add_anchor_per_event(sgk, lambda i: sgk_anchors[i-1] if i-1 < len(sgk_anchors) else '三国主线补充节点')

# 其他文件锚点规则
rules = {
    '08-harry-potter-events.md': lambda i: (
        '原著1-7卷核心主线' if i <= 9 else ('战后重建与制度修复延展设定' if i <= 45 else '代际传承与社会恢复阶段')
    ),
    '06-legend-of-condor-heroes-events.md': lambda i: (
        '射雕主线：郭靖成长与家国线并进' if i <= 20 else ('射雕中段：江湖势力重排' if i <= 50 else '射雕后段：家国决断与余波')
    ),
    '07-smiling-proud-wanderer-events.md': lambda i: (
        '笑傲主线：福威镖局-华山线' if i <= 15 else ('笑傲中段：五岳并派与黑木崖前后' if i <= 45 else '笑傲后段：秩序重建与评价战')
    ),
    '01-contemporary-china-2020s-events.md': lambda i: '当代中国社会结构变迁锚点（现实向）',
    '02-china-1980s-events.md': lambda i: '改革开放初期社会经济转型锚点（现实向）',
    '03-china-1990s-events.md': lambda i: '90年代市场化与流动社会锚点（现实向）',
    '05-five-dynasties-ten-kingdoms-events.md': lambda i: '五代十国政权更替与地方秩序锚点（历史向）',
}
for fn, rule in rules.items():
    p = base / fn
    if p.exists():
        add_anchor_per_event(p, rule)

# 追加精修说明文档
(Path('docs/worldviews') / 'ROUND3_NOTES.md').write_text('''# 第三轮精修说明（Round 3）

本轮目标：降低事件同质化，增强“原设锚点”可追溯性。

## 已完成
- 为 8 个世界观事件库逐条增加 **原设锚点** 字段。
- 三国事件库采用逐事件专属锚点（50条），对应《三国演义》主线段落。
- 哈利波特/射雕/笑傲补充主线阶段锚点，明确“原著主线”与“延展设定”边界。
- 现实向与历史向文件统一补充时代结构锚点标记。

## 使用建议
1. 选事件时优先查看“原设锚点”；
2. 若要创作角色支线，不改锚点主线胜负；
3. 如需更严谨版本，可继续在每条后增加“章节/史料编号”。
''', encoding='utf-8')

print('round3 refined')
