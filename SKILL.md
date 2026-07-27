---
name: ai-promo-video
description: End-to-end AI promo video pipeline — research video generation models, write marketing copy, voiceover scripts, and shot-by-shot video prompts. Use whenever the user wants to make a promotional/brand/marketing video using AI tools like doubao-seedance, Sora, Kling, Runway, or HeyGen — even if they don't explicitly say "promo". Covers scenarios like "帮我做个宣传片"、"用 AI 生成 XX 视频广告"、"写口播稿"、"seedance prompt 怎么写"、"数字人宣传视频"、"品牌片文案". Triggers on mentions of promo video, marketing video, brand video, AI 视频生成, 分镜脚本, 宣传文案, 口播稿.
---

# AI Promo Video Skill

End-to-end pipeline for AI-generated promotional videos. Use when the user wants to plan, write, and produce a marketing/brand/promo video using AI video generation tools.

## What this skill covers

The full 4-phase workflow:

1. **Model research** — survey video generation models (doubao-seedance primary), write capability reports
2. **Marketing copy** — positioning, value props, differentiation, CTAs
3. **Voiceover script** — spoken-style script for digital human or narrator, multiple length versions for different channels
4. **Shot-by-shot prompts** — concrete video generation prompts following the model's official writing conventions

## When to trigger

Trigger when the user wants to:

- Make a promotional/brand/marketing video using AI tools
- Research AI video generation models (seedance, Sora, Kling, Runway, etc.)
- Write voiceover/narration scripts for videos
- Write shot-by-shot prompts for AI video models
- Plan an end-to-end AI video production

Do not trigger for: ordinary video editing tasks, screen-recording tutorials, non-AI video work, or pure copywriting without video context.

## Generality principle (important)

This skill is a **framework**, not a template tied to any specific product, industry, or brand. When working on a project:

- **Examples in reference files are illustrations, not templates to copy.** Adapt the structure to the project's actual audience, voice, and product category.
- **Do not assume B2B, B2C, education, or any specific vertical.** Ask the user about audience and product first if the project context doesn't make it obvious.
- **Default to the project's own brand assets** — pull colors, voice, credentials from the project README and brand folder; never assume specific values.
- **Style rules below (反 AI slop) are defaults, not commandments.** Surface them to the user if the project seems to call for a different voice (e.g., a clickbait ad buy might genuinely want震惊体), but otherwise keep them.

## Core principle: output goes into project docs

All deliverables (research reports, copy, scripts, prompts) should be written as Markdown files under the project's `docs/promo/` directory (or equivalent), so they survive across sessions and can be reviewed/edited by humans. Do not just dump content into the chat.

## Routing by user intent

| User asks | Phase | What to do |
|---|---|---|
| "帮我调研 XX 视频模型" / "seedance 怎么用" | Research | Read `references/research-template.md`, dispatch a research subagent, save report to `docs/promo/00-{model}-调研报告.md` |
| "帮我写宣传文案" / "广告文案" | Copy | Read `assets/copy-template.md`, interview the user briefly (target audience, brand assets, key differentiators), write to `docs/promo/01-宣传文案.md` |
| "写口播稿" / "数字人念稿" | Voiceover | Read `assets/voiceover-template.md`, produce length versions appropriate to the channel, save to `docs/promo/02-口播稿.md` |
| "视频 prompt 怎么写" / "分镜脚本" | Shot prompts | Read `references/shot-prompt-template.md` + the model-specific guide (e.g., `references/seedance-guide.md`), produce per-shot prompts to `docs/promo/03-{model}-视频prompt.md` |
| "从零做一支 AI 宣传片" | All four phases | Run phases in order, save each artifact, link them from `docs/promo/README.md` |

## Phase 1: Model research

Goal: a structured report on the chosen model's capabilities, prompt conventions, API, pricing, and pitfalls.

1. Ask the user which model (default: `doubao-seedance-1-0-pro-250528`; consider pro fast for budget, avoid lite for brand videos). If the user mentions Sora / Kling / Runway / others, dispatch a research subagent for that model — the report structure in `references/research-template.md` is model-agnostic.
2. Read `references/research-template.md` for the survey structure.
3. Dispatch a research subagent (use the `researcher` subagent type) with explicit instructions to cite real URLs and mark "需核实" for unverified claims. Never fabricate prices, API fields, or release dates.
4. Save the report to `docs/promo/00-{model-slug}-调研报告.md`.
5. Highlight 3-5 key constraints that will shape later phases (e.g., "model cannot generate reliable text → all captions must be composited in post").

If the target is doubao-seedance, also read `references/seedance-guide.md` — it contains the pre-validated 5-段式 prompt structure, camera vocabulary, and known pitfalls. For other models, the research report from step 4 is the canonical reference.

## Phase 2: Marketing copy

Goal: a main copy document that downstream voiceover and shot prompts build on.

1. Read `assets/copy-template.md`.
2. Gather inputs (ask only what's missing; pull from project README, brand folder, prior docs first):
   - Target audience(s) and their pain points — could be one segment or several; do not assume
   - Product/brand differentiators (3-5)
   - Brand voice and tone
   - Brand visual identity (colors, logos, existing assets) — pull hex values from the project's actual brand config, do not use placeholders
   - Call-to-action (could be enterprise / consumer / partner / install / signup — depends on product)
3. Write the copy following the template's structure: one-sentence positioning → value props → main narrative → differentiators → data/credentials → CTAs.
4. Save to `docs/promo/01-宣传文案.md`.

**Style rules (defaults — surface to user if the project calls for something different)**:

- Plain language over buzzwords. Use everyday metaphors; keep technical terms only when they teach the reader something.
- Show, don't claim. Cite real credentials, rankings, numbers — never inflate.
- Sentences that survive being spoken aloud. Read every sentence out loud mentally; if it sounds like a press release, rewrite.

## Phase 3: Voiceover script

Goal: a spoken-style script for a digital human or human narrator, structured for TTS and video editing.

1. Read `assets/voiceover-template.md`.
2. Base it on the main copy from Phase 2 — do not invent new messaging.
3. Ask the user about the distribution channel (抖音/视频号/公众号/官网/B站/朋友圈/开屏 etc.) — channel determines the length versions needed. The template lists typical versions (长片 60s+, 中片 30s, 短片 15s) as defaults, not fixed requirements.
4. Annotate with reading conventions: speech rate, pauses, emphasis markers (▲ for stress, ▼ for soft, … for held), numbers in Chinese reading.
5. Provide a shot-by-shot mapping table (time → voiceover segment → visual suggestion).
6. Save to `docs/promo/02-口播稿.md`.

**Style rules**:

- Short sentences. One idea per line, breakable into independent clauses.
- Conversational, not written. "我们做的事，就是把这两边拉到一起" beats "本平台致力于实现人才与企业的精准对接".
- Stress and pause markers matter — they drive TTS rhythm and video editing beat.

If the user will feed the script into mimo TTS or similar, also produce a `segments.json` following `assets/segments-template.json` — one segment per shot, with per-segment style instructions.

## Phase 4: Shot-by-shot video prompts

Goal: concrete, copy-pasteable prompts for the chosen video model, one per shot, ready for batch API calls.

1. Read `references/shot-prompt-template.md` and the model-specific guide (`references/seedance-guide.md` for seedance; for other models, the research report from Phase 1).
2. Map the voiceover script into shots (typically 5-10s each; total shot count scales with total runtime, roughly 1 shot per 5-8 seconds).
3. For each shot, write a complete prompt following the model's official structure. For seedance, that's the **5-段式**:
   - 整体风格与氛围
   - 主体（含一致性约束）
   - 场景（环境/光照/道具）
   - 时间轴动作（0-N 秒）
   - 运镜 + 技术参数
   - 一致性约束（无文字水印 logo、五指完整）
4. Include API call parameters (model, resolution, ratio, duration, seed) and a code snippet for batch submission.
5. Save to `docs/promo/03-{model}-视频prompt.md`.

**Hard rules for seedance** (these came from real failures):

- 字幕、品牌名、Logo 一律后期合成 — seedance 1.0 text rendering is weak.
- No independent `negative_prompt` field — fold negations into positive constraints ("无文字" not "不要文字").
- One prompt = one shot. Don't try multi-shot narratives in a single prompt; cut in post.
- For character consistency across shots, use image-to-video with a first-frame anchor image rather than text-to-video.
- Always append explicit "无文字、无水印、无 logo、人物五指完整" at the end.

For other models, follow that model's official prompt structure and constraints as documented in the Phase 1 research report.

## Pitfalls from real production runs

Things this skill has seen go wrong (all are general, not project-specific):

- **Boson `higgs-avatar` preview-version watermark** — videos ship with "This digital avatar is generated by AI" at the bottom. Crop with ffmpeg in post: `ffmpeg -i in.mp4 -vf "crop=W:H-30:0:30,scale=W:H" out.mp4`. The watermark is added at video generation time, not by the source image.
- **Parameter confusion between skills** — `--skip-check` exists in mimo-lecture-audio-skill but NOT in boson-ai-skill. Always check the skill's own `--help` before assuming flags transfer.
- **Audio length caps on avatar services** — boson caps single audio at 60s. Split longer scripts into ≤60s segments and merge videos in post.
- **Image API relay occasionally disconnects** on high-quality large batches (RemoteProtocolError). Use `--count 1` per call and loop, or drop to `--quality medium`.
- **Video model task queue** — longer videos (10s) take 3-5x longer than shorter (5s) on the same model. Budget for retries when iterating.
- **Image-to-video is more consistent than text-to-video** — for any character that must look the same across shots, generate a still first and reuse it as the first frame.

## Hand-off to execution skills

This skill produces plans and prompts; it does not execute the API calls itself. After Phase 4, point the user to execution:

- Image generation (avatar/product shots) → `image2-api` skill
- Voiceover TTS → `mimo-lecture-audio-skill` (Chinese) or `boson-ai-skill` (multilingual)
- Digital human video → `boson-ai-skill` (`higgs-avatar`, audio-to-video mode)
- B-roll / scene shots → call the video model API directly (no wrapper skill yet for seedance/Sora/Kling)

## Output index file

After all four phases, maintain `docs/promo/README.md` as the index — list every artifact, the execution order, budget estimate, and the open decisions. This is what the user opens next session to resume.

## Style across all outputs (反 AI slop defaults)

These rules reflect a preference for honest, anti-slop content. They are defaults — surface them to the user if the project seems to call for a different voice, but otherwise keep them.

- Headlines plain, not clickbait. No "震惊！" or "竟然发现...!".
- Conclusions first, details after. Lists over paragraphs when the user will act on items.
- Honest about uncertainty. Mark "需核实" for unverified facts; never fabricate URLs, prices, or features.
- Strike AI-slop words by default: "赋能"、"抓手"、"闭环"、"生态"、"一站式"、"行业领先"、"致力于". Replace each with a concrete verb or specific claim.
- No fake enthusiasm in reports. No "太棒了"、"很惊喜". The deliverable reports facts.
- Match the user's language — Chinese in, Chinese out.
