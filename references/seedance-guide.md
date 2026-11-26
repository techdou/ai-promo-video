# doubao-seedance Prompt & API Guide

> Verify model access, accepted fields, and pricing for your endpoint before production. Choose from models confirmed to work on the actual account and route; an advertised model is not proof of access.

## Model selection

| Version | Example model ID (Ark) | When to use |
|---|---|---|
| **Seedance 1.5 Pro** | `doubao-seedance-1-5-pro-251215` | Standard text-to-video or image-to-video promo shots; use joint audio/video generation when the endpoint supports it. |
| **Seedance 2.0** | `doubao-seedance-2-0-260128` | Prefer for shots that need multimodal image/video/audio references (e.g., match product appearance, camera motion, and rhythm); also supports text-to-video, frame anchors, and synchronized audio. |

Choose by shot and confirmed access, not by version alone. Check the exact model or inference endpoint ID and supported resolution, duration, and reference mode. Use one prompt per shot by default and cut in post.

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
3. **Multi-shot prompts are harder to control**. Even with Seedance 2.0, prefer one prompt per shot when individual cuts need precise control.
4. **`camera_fixed: true` does not guarantee fixed camera**. The official doc says "效果不保证". For truly fixed shots, write "镜头固定不动，无运镜" explicitly in the prompt.
5. **Audio support is model- and endpoint-dependent**. Seedance 1.5 Pro and 2.0 can generate synchronized audio; keep the final branded voiceover and mix in post when exact timing or wording matters.

## Consistency techniques

- **Character consistency**: use image-to-video with a `first_frame` anchor image (generate the character still first via Seedance text-to-image, SDXL, or 即梦, then reuse that image as `first_frame` for every shot needing that character).
- **Style consistency**: reuse the same "风格前缀 + 镜头规格 + 光照" three-segment template across prompts; fix `seed=42` to improve coherence.
- **Brand consistency**: handle片头片尾, 配色, 字幕模板 entirely in post. AI only generates the picture.

## API fields (方舟 / Volcengine Ark)

Endpoint: `POST /api/v3/contents/generations/tasks`

| Field | Required | Values |
|---|---|---|
| `model` | yes | Enabled model ID or inference endpoint ID; see the selection table. |
| `content` | yes | Text instructions and any media inputs. `image_url` can carry a `first_frame` or `last_frame` role where supported. For 2.0 multimodal reference mode, use `reference_image`, `reference_video`, or `reference_audio` as appropriate; do not mix that mode with frame anchors. |
| `ratio`, `resolution`, `duration` | no | Check allowed values and defaults for the selected model and mode. |
| `generate_audio`, `camera_fixed`, `seed`, `watermark` | no | Send only if the selected model and endpoint support the field. |

### Task polling

After create returns a task ID, query `GET /api/v3/contents/generations/tasks/{id}` every 10–15 seconds. `queued` and `running` are nonterminal. The four terminal states are:

| Status | Action |
|---|---|
| `succeeded` | Read `content.video_url` and download promptly (the URL expires). Missing URL is a delivery error. |
| `failed` | Stop and inspect the task error. |
| `cancelled` | Stop; the task was cancelled. |
| `expired` | Stop; the task expired. |

The example takes a `get_task(task_id)` callable that returns decoded Ark query JSON. It only queries an existing task; it does not submit a generation request.

```python
from time import sleep


def wait_for_video(get_task, task_id, *, max_attempts=60, interval=12):
    for attempt in range(max_attempts):
        task = get_task(task_id)
        status = task.get("status")
        if status == "succeeded":
            url = (task.get("content") or {}).get("video_url")
            if not url:
                raise RuntimeError(f"Task {task_id} succeeded without content.video_url")
            return url
        if status in {"failed", "cancelled", "expired"}:
            raise RuntimeError(f"Task {task_id} ended with status {status}")
        if status not in {"queued", "running"}:
            raise RuntimeError(f"Task {task_id} returned unexpected status {status!r}")
        if attempt + 1 < max_attempts:
            sleep(interval)
    raise TimeoutError(f"Task {task_id} is not terminal; resume polling by task ID")
```

## Pricing and latency (verify before production)

Check [current Ark pricing](https://www.volcengine.com/docs/82379/1544106) for the selected model and mode, including reference inputs and audio. Do not reuse 1.0 price or latency estimates for 1.5 Pro/2.0.

## Official documentation

- [视频生成 API — 火山方舟](https://www.volcengine.com/docs/82379/1520757)
- [查询视频生成任务 — 火山方舟](https://www.volcengine.com/docs/82379/1521309)
- [Seedance 2.0 提示词指南 — 火山方舟](https://www.volcengine.com/docs/82379/2222480)
- [Seedance SDK 示例](https://www.volcengine.com/docs/82379/2298881)
- [模型价格](https://www.volcengine.com/docs/82379/1544106)

## Community reference

- `YouMind-OpenLab/awesome-seedance-2-prompts` (GitHub, Seedance 2.0 prompt examples; verify suitability for your shot and model).
