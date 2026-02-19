from pathlib import Path
import re

base = Path('docs/worldviews/events')

# 三国按《三国演义》大致回目区间
sgk_ranges = [
"回目1-3","4-6","4-6","5-6","5-6","8-9","9-10","14-16","18-19","16-17",
"25-26","30-31","31-33","33-34","33-35","35-38","42-43","41-42","43-44","43-50",
"50-53","60-63","63-64","65-66","67-68","73-74","71-72","71-73","74-76","75-77",
"77-78","78-80","80-82","82-84","85","90","87-90","95","96-97","102",
"102-103","103-104","106-107","107-111","111-114","115","116","117-118","118","119-120"
]

files = {
    '04-three-kingdoms-events.md': lambda i: f"《三国演义》{sgk_ranges[i-1] if i-1 < len(sgk_ranges) else '相关回目'}（近似锚定）",
    '08-harry-potter-events.md': lambda i: (
        '《哈利·波特》1-7卷主线' if i <= 9 else ('战后重建期（同人延展设定）' if i <= 45 else '新世代阶段（延展设定）')
    ),
    '06-legend-of-condor-heroes-events.md': lambda i: '《射雕英雄传》主线段（近似锚定）',
    '07-smiling-proud-wanderer-events.md': lambda i: '《笑傲江湖》主线段（近似锚定）',
    '01-contemporary-china-2020s-events.md': lambda i: '现实向：2018-至今阶段锚点',
    '02-china-1980s-events.md': lambda i: '现实向：1978-1989阶段锚点',
    '03-china-1990s-events.md': lambda i: '现实向：1990-1999阶段锚点',
    '05-five-dynasties-ten-kingdoms-events.md': lambda i: '历史向：907-979阶段锚点',
}

def patch(path, fn):
    txt = path.read_text(encoding='utf-8')
    blocks = re.split(r'(?m)^(### 事件\s+\d+｜.*)$', txt)
    if len(blocks) < 3:
        return False
    out=[blocks[0]]
    idx=0
    for i in range(1,len(blocks),2):
        head=blocks[i]
        body=blocks[i+1]
        idx+=1
        ref_line=f"- **参考范围**：{fn(idx)}\n"
        if '- **参考范围**：' in body:
            body = re.sub(r'- \*\*参考范围\*\*：.*\n', ref_line, body, count=1)
        else:
            # insert after 原设锚点 if exists
            if '- **原设锚点**：' in body:
                body = re.sub(r'(- \*\*原设锚点\*\*：.*\n)', r'\1'+ref_line, body, count=1)
            else:
                body = ref_line + body.lstrip('\n')
        out.extend([head,'\n',body])
    path.write_text(''.join(out), encoding='utf-8')
    return True

for fn, rule in files.items():
    p = base / fn
    if p.exists():
        patch(p, rule)

notes = Path('docs/worldviews/ROUND4_NOTES.md')
notes.write_text('''# 第四轮精修说明（Round 4）

## 本轮动作
- 为全部事件库新增字段：**参考范围**。
- 三国事件按《三国演义》回目提供近似区间锚定，便于校对与再精修。
- 其他世界观补充作品卷/阶段或现实时间段锚点。

## 结果
- 事件选择时可同时参考：
  1) 原设锚点
  2) 参考范围
- 后续可继续升级到“逐事件章节级精确引用”。
''', encoding='utf-8')
print('round4 done')
