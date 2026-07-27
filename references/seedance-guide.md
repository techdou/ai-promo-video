# doubao-seedance Prompt & API Guide

> Snapshot: 2026-07-25. Verify pricing and field defaults against the official doc links at the bottom before production runs.

## Model selection

| Version | model ID | When to use |
|---|---|---|
| **pro** (recommended) | `doubao-seedance-1-0-pro-250528` | Brand films, multi-shot narratives, 1080p required |
| **pro fast** | `doubao-seedance-1-0-pro-fast-251015` | Budget-sensitive, 3x speed, 72% cheaper than pro |
| lite | `doubao-seedance-1-0-lite-*` | Avoid for brand films — single-shot, lower quality |

For promo videos, default to **pro 1080p**. Drop to pro fast only if iteration speed matters more than peak quality.

## The 5-段式 prompt structure (官方推荐)

Every prompt should follow this template, in this order:

```
[整体风格与氛围]
+ [主体（人物/产品，含一致性约束）]
+ [场景（环境/光照/道具）]
+ [时间轴分镜动作（0-N 秒）]
+ [运镜]
+ [技术参数（分辨率/帧率/景深/镜头规格）]
+ [一致性约束（无文字水印 logo、人物五指完整、面部一致）]
```

Example (illustrative — replace subject, wardrobe, scene, and brand colors with the project's actual content):

> 电影级纪录片风格，沉稳大气。主体：一名 35 岁中国男性电焊工，身穿深绿色（约 #0E4B3F）工装，戴深色防护面罩，双手稳握焊枪。场景：明亮现代的工业车间内，焊弧在画面中央迸发出温暖的橙金色光芒，金色火花四溅，背景虚化可见工业设备的深绿色轮廓。0-5 秒：焊工专注地焊接一块钢材，火花从焊点向画面右侧飞溅，人物保持稳定姿态。镜头从远景缓慢推近至焊点特写，浅景深，35mm 变形宽银幕镜头。1080p，24fps，电影级胶片颗粒。画面色调以深绿与暖金点缀为主。人物面部、服装、发型全程一致，五指完整，无穿模，无文字、无水印、无 logo、无字幕。

## Camera vocabulary

Mix Chinese-with-Chinese or English-with-English; do not mix within one prompt (causes drift).

| Type | 中文 | English |
|---|---|---|
| Push/Pull | 推近、缓慢推镜、拉远 | Push-in / dolly in, Pull out |
| Pan | 水平横摇、垂直纵摇 | Pan left/right, Tilt up/down |
| Track | 平移跟拍、侧移 | Truck left/right, Tracking shot |
| Follow | 跟拍、肩后视角、低机位贴地 | Tracking, Over-the-shoulder |
| Orbit | 360 度环绕、半圆环绕 | Orbit, Bullet-time orbit |
| FPV/Aerial | FPV 无人机穿越、低空 FPV 追拍、航拍俯瞰 | FPV drone dive, Aerial, Bird's-eye |
| Special | 子弹时间、希区柯克变焦、变速 | Bullet time, Dolly zoom, Speed ramp |

## Hard constraints (these caused real failures)

1. **No independent `negative_prompt` field**. Fold negations into positive constraints: write "干净画面" not "无水印" alone, or append "无文字、无水印、无 logo、人物五指完整" at the end.
2. **Text rendering is weak**. Captions, brand names, logos, on-screen text — composite all in post. Never ask the model to render the project's brand name or any slogan.
3. **Multi-shot narratives in one prompt are fragile**. Pro supports it but failure rate is high. Default to one prompt = one shot, cut in post.
4. **`camera_fixed: true` does not guarantee fixed camera**. The official doc says "效果不保证". For truly fixed shots, write "镜头固定不动，无运镜" explicitly in the prompt.
5. **No audio in 1.0 series**. 1.5 pro added audio-visual joint generation; 1.0 needs post-production voiceover.

## Consistency techniques

- **Character consistency**: use image-to-video with a `first_frame` anchor image (generate the character still first via Seedance text-to-image, SDXL, or 即梦, then reuse that image as `first_frame` for every shot needing that character).
- **Style consistency**: reuse the same "风格前缀 + 镜头规格 + 光照" three-segment template across prompts; fix `seed=42` to improve coherence.
- **Brand consistency**: handle片头片尾, 配色, 字幕模板 entirely in post. AI only generates the picture.

## API fields (方舟 / Volcengine Ark)

Endpoint: `POST /api/v3/contents/generations/tasks`

| Field | Required | Values |
|---|---|---|
| `model` | yes | `doubao-seedance-1-0-pro-250528` |
| `content` | yes | `[{type:"text", text:"..."}]` + optional `[{type:"image_url", image_url:{url}, role:"first_frame"\|"last_frame"}]` |
| `ratio` | no | `1:1`/`3:4`/`4:3`/`16:9`/`9:16`/`21:9`/`adaptive`, default `16:9` |
| `resolution` | no | `480p`/`720p`/`1080p`, default `1080p` |
| `duration` | no | `5`/`10`, default `5` |
| `camera_fixed` | no | default `false` |
| `seed` | no | fix for coherence |
| `watermark` | no | default `false` |

Async flow: POST create → GET poll every 10-15s → on `completed`, fetch `content.video_url` (TOS URL, time-limited, download promptly).

Typical latency: 5s/720p ≈ 40-50s on pro; pro fast ≈ 10s.

## Pricing (verify before production)

- 720p: **¥1.73 / million tokens**
- 1080p: **¥3.89 / million tokens**
- Token formula: `tokens = (height × width × FPS × duration) / 1024`
- Per-shot reference: 1080p/5s ≈ ¥0.94

Source: <https://www.volcengine.com/docs/82379/1544106> (re-check; pricing adjusts quarterly).

## Official documentation

- [Seedance 1.0 提示词指南 — 火山方舟](https://www.volcengine.com/docs/82379/1631633) (中文, JS-rendered, may need login)
- [Seedance-1.0-pro & pro-fast Prompt Guide — BytePlus ModelArk](https://docs.byteplus.com/en/docs/ModelArk/1631633) (English mirror, same fields)
- [Seedance SDK 示例](https://www.volcengine.com/docs/82379/2298881)
- [模型价格](https://www.volcengine.com/docs/82379/1544106)
- [Seedance 1.0 pro fast 模型页 — BytePlus](https://docs.byteplus.com/en/docs/ModelArk/1901652)

## Community reference

- `YouMind-OpenLab/awesome-seedance-2-prompts` (GitHub, 5000+ vetted prompts; naming says 2.0 but the 5-段式 structure and camera vocabulary apply to 1.0 pro)
