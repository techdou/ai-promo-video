# Shot-by-Shot Video Prompt Template

Use this when writing per-shot prompts for any AI video generation model. For seedance specifically, also read `seedance-guide.md` for the 5-段式 structure.

## Planning the shot list

Before writing any prompt, plan the whole film:

1. **Map voiceover to shots.** Take the voiceover script (from Phase 3) and break it into shots. Typical cadence: roughly 1 shot per 5-8 seconds of runtime. A 60s film → 8-12 shots; a 30s ad → 4-6 shots; a 15s hook → 3 shots. Adjust based on the actual runtime the user specified.

2. **Per-shot table.** Build this first as a Markdown table in the output doc. Use generic placeholders that match the project's actual content — do not copy the example subjects below verbatim:

   | # | 时长 | 对接口播段 | 画面主题 | 运镜 | 备注 |
   |---|---|---|---|---|---|
   | S1 | 5s | 开场 hook | {主角色特写} | 慢推 | 重音镜头 |
   | S2a-c | 5s×3 | 蒙太奇段 | {三个相关场景} | 跟拍 | 多人物需拆分 |
   | ... | | | | | |

3. **Decide AI vs real vs UI.** Per shot, mark:
   - **AI 空镜**: pure scene, no UI, no text — safe for video model
   - **实拍图生视频**: use real photo as `first_frame` for brand consistency (school gate, office, product)
   - **后期合成**: anything with UI, captions, logos — do NOT pass to video model

   Rule: if the shot needs text, logo, or recognizable UI, AI only generates the background or the empty-handed scene; everything else is post-production compositing.

## Per-shot prompt structure

For seedance, every prompt follows the 5-段式 (see `seedance-guide.md`). For other models, follow that model's official structure — do not invent.

Generic skeleton that adapts to most models:

```
[整体风格与氛围 — film genre, mood, atmosphere]
[主体 — person/product, with identity invariants: age, ethnicity, wardrobe, hair, expression, camera angle]
[场景 — environment, lighting, props, color palette tied to brand]
[时间轴动作 — what happens in 0-N seconds, beat by beat]
[运镜 — camera move in the model's native vocabulary]
[技术参数 — resolution, fps, lens, depth of field, film grain]
[一致性约束 — "无文字、无水印、无 logo、人物五指完整、面部一致"]
```

### Concrete example (filled in)

> This is an illustrative example — replace the subject, wardrobe, scene, and brand colors with the project's actual content. Do not copy verbatim into a new project.
>
> 电影级纪录片风格，沉稳大气。主体：一名 35 岁中国男性电焊工，身穿深绿色（约 `<品牌主色 hex>`）工装，戴深色防护面罩，双手稳握焊枪。场景：明亮现代的工业车间内，焊弧在画面中央迸发出温暖的橙金色光芒，金色火花四溅，背景虚化可见工业设备的深绿色轮廓。0-5 秒：焊工专注地焊接一块钢材，火花从焊点向画面右侧飞溅，人物保持稳定姿态。镜头从远景缓慢推近至焊点特写，浅景深，35mm 变形宽银幕镜头。1080p，24fps，电影级胶片颗粒。画面色调以`<品牌主色>`与`<品牌强调色>`点缀为主。人物面部、服装、发型全程一致，五指完整，无穿模，无文字、无水印、无 logo、无字幕。

## Brand color injection

Always append a color-palette sentence tying the shot to the brand:

> 画面色调以<主色 hex>与<强调色 hex>点缀为主，沉稳大气。

Fix `seed=42` and reuse the same "风格前缀 + 镜头规格 + 光照" three-segment opener across all prompts to keep visual coherence.

## What each shot must include (checklist)

Before finalizing any prompt, verify it has:

- [ ] 整体风格前缀 (e.g., "电影级纪录片风格")
- [ ] 主体描述 with identity invariants (age, ethnicity, wardrobe, hair)
- [ ] 场景 with environment + lighting + props
- [ ] 时间轴 0-N 秒动作描述
- [ ] 运镜 keyword (in the model's preferred language)
- [ ] 技术参数 (resolution, fps, lens, grain)
- [ ] 品牌色注入句
- [ ] 一致性约束尾句 (无文字水印 logo / 五指完整 / 面部一致)
- [ ] API call parameters block (model, ratio, resolution, duration, seed)

## Multi-shot vs single-shot

Default: **one prompt = one shot**. Cut in post.

Exceptions where multi-shot narrative in one prompt is worth trying:

- pro-tier models with documented multi-shot support (seedance 1.0 pro)
- Dialogue scenes where two characters must interact continuously
- When the time-axis structure can be written explicitly (0-4s X, 4-9s Y, 9-15s Z)

Even then, expect higher failure rates and budget extra retry iterations.

## Hand-off to batch execution

After all prompts are written, include in the output doc:

1. A code snippet showing the async task flow (POST → poll → fetch)
2. Common parameters (model, ratio, resolution, duration, seed, watermark)
3. Cost estimate per shot and total budget
4. Retry strategy (抽 2-3 次选优)
5. Acceptance criteria for selecting which retry to keep:
   - Identity consistency with anchor image
   - No frame jumps or model artifacts
   - Camera move matches the prompt
   - Color palette matches brand
   - No stray text or watermarks

Reject and re-roll any shot that fails these criteria; re-rolling a single prompt costs less than ¥1 on seedance pro.
