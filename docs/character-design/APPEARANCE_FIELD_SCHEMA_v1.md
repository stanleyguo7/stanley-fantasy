# 外观字段 Schema（v1）

用于把问卷答案落地为结构化记录（可写入 profile.md 或独立 appearance.md）。

```yaml
appearance:
  age_band: "青年"
  body:
    height_band: "中等"
    build: "匀称"
    skin_tone: "小麦色"
    skin_state: ["常年日晒", "轻微疤痕"]
  face:
    face_shape: "椭圆"
    eyes: "细长眼"
    brows: "平直"
    nose: "挺直"
    lips: "常抿嘴"
    marks: ["左颊浅痣"]
  hair:
    length: "中长"
    texture: "微卷"
    density: "适中"
    color: "黑色"
    style: "束发"
  posture:
    stand: "警觉型"
    walk: "平稳"
    gestures: ["背手", "摸下巴"]
    vibe: ["冷静", "机敏"]
  outfit:
    style: "朴素实用"
    palette: "深色系"
    materials: ["棉麻", "皮革"]
    wear_level: "轻度磨损"
  accessories:
    main: "护腕"
    carry: ["药包", "小刀", "信物"]
  variants:
    default: "整洁"
    stress: ["沉默寡言", "衣装失序"]
    scene_versions: ["正式场合", "旅行"]
  narrative:
    first_impression: "..."
    portrait_closeup: "..."
    fullbody_desc: "..."
    accessory_story: "..."
    contrast: "..."
```

