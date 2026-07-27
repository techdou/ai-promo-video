# Voiceover Script Template

Use this when writing voiceover scripts for a digital human or human narrator. Output goes to `docs/promo/02-口播稿.md`.

## Source

The script is derived from the Phase 2 marketing copy. Do not invent new messaging. If the copy lacks a piece of information needed for the script, go back to Phase 2 and ask the user — do not fill gaps with assumptions.

## Length versions — channel-driven, not fixed

Ask the user about the distribution channel first. Channel determines the length versions needed.

| Channel | Typical length | Notes |
|---|---|---|
| 抖音/快手信息流 | 15-30s | 前 3 秒必须有钩子，否则划走 |
| 视频号广告 | 30-60s | 节奏可以稍慢 |
| 朋友圈广告 | 10-15s | 单一信息点 |
| B站 | 60s-3min | 可讲完整故事 |
| 公众号嵌入 | 60s+ | 配合长文阅读 |
| 官网置顶 | 60-90s | 品牌片，节奏稳 |
| 开屏广告 | 3-15s | 单 hook + logo |
| 销售演示 | 2-5min | 可详细 |

The template below provides **three default versions** (长片 60s, 中片 30s, 短片 15s) — produce whichever subset matches the channel. If the user wants a 45s or 90s version, adapt the structure accordingly; do not force-fit into 60/30/15.

## Three default length versions

| Version | Length | Word count (Chinese) | Default use |
|---|---|---|---|
| 长片 | 60s | ≈230 字 | 官网置顶、公众号长文嵌入、品牌发布会 |
| 中片 | 30s | ≈125 字 | 信息流投放、视频号广告 |
| 短片 | 15s | ≈60 字 | 开屏广告、信息流前 3 秒钩子 |

## Reading conventions (annotate every script)

These markers drive both TTS prosody and video editing beat. Document them at the top of every script file:

- **语速**: characters per minute (品牌片 200-220, 转化广告 220-240, 钩子 240+)
- **断句**: end-of-line pause 0.3-0.5s; end-of-paragraph pause 0.8-1s
- **重音**: `▲` before a stress word, `▼` before a soft word, `…` for a held beat (0.5s)
- **数字念法**: Chinese reading by default ("两千四" not "二千四百"; "3 到 5 名" reads "三到五名")
- **品牌念法**: brand name pronounced how — document specific pronunciation for non-obvious names

## Per-version structure

### 长片 (60s+) — 8-beat structure

| Beat | Time | Content |
|---|---|---|
| 1. Hook | 0-4s | A short, weighted opening line |
| 2. Pain A | 4-12s | The audience's world before the product |
| 3. Pain B (if two-sided) | 12-22s | The other side's matching pain |
| 4. Bridge | 22-30s | "我们做的事，就是…" + product name + backing |
| 5. Value | 30-45s | Two to four mechanisms, each one short |
| 6. Differentiation | 45-55s | What alternatives cannot do |
| 7. Slogan | 55-60s | Two to four parallel lines, brand close |

For 90s+ films, expand beats 5 and 6; do not pad other sections.

### 中片 (30s) — 4-beat structure

| Beat | Time | Content |
|---|---|---|
| 1. Problem hook | 0-5s | Direct pain question or scene |
| 2. Solution intro | 5-15s | Brand + compressed mechanisms |
| 3. Differentiation | 15-25s | One concrete differentiator with proof |
| 4. CTA | 25-30s | Brand name + slogan + action |

### 短片 (15s) — 3-beat structure

| Beat | Time | Content |
|---|---|---|
| 1. Question | 0-3s | Two parallel pain questions or scenes |
| 2. Solution | 3-12s | Brand + one or two mechanisms |
| 3. Tag | 12-15s | Brand name + slogan |

## Style rules (non-negotiable for spoken content)

- **Short sentences.** One idea per line. If a sentence has more than two commas, break it.
- **Conversational, not written.** "我们做的事，就是把这两边拉到一起" beats "本平台致力于实现人才与企业的精准对接".
- **Read every line aloud mentally.** If it sounds like a press release, rewrite.
- **Numbers in numerals, but pronounced in Chinese.** Write "20 个焊工" — TTS reads "二十个焊工". (Replace "焊工" with the project's actual subject.)
- **Stress markers are load-bearing.** ▲ and ▼ are not decorative; they tell TTS where to push and tell the editor where to cut.

## Shot-by-shot mapping table

After every version, include a table mapping each voiceover segment to a visual:

| 时间 | 口播段 | 画面建议 | 备注 |
|---|---|---|---|
| 0-4s | {hook line} | {visual concept} | {production note} |
| 4-12s | {pain A line} | {visual concept} | {production note} |
| ... | | | |

The "画面建议" column should describe the visual in plain terms (realistic enough that the editor or the next phase can act on it), not generic placeholders.

This table is what Phase 4 (shot prompts) consumes to plan the shot list.

## Digital human production notes

Include a section with:

- **形象建议**: demographic (age range, ethnicity, gender presentation), wardrobe aligned with brand colors (cite specific hex from the project's brand config)
- **音色建议**: specific TTS voice name. Common options: mimo "冰糖"/"茉莉"/"晓秋" (Chinese female), boson "chloe"/"eleanor"/"oliver" (multilingual). Pick based on brand voice.
- **字幕样式**: font family, weight, size relative to frame, color (main text + emphasis color tied to brand), background treatment
- **背景音乐**: BPM range, genre, instrumentation, what to avoid

## SSML hints (for TTS)

If the script will feed a TTS engine that supports SSML, include an example. Notation varies by engine:

**SSML (Azure / 豆包 TTS / mimo)**:

```xml
<speak>
  <prosody rate="1.0" pitch="0">
    {opening line}…
    <emphasis level="strong">{stress word}。</emphasis>
  </prosody>
  <break time="500ms"/>
  {next line}
</speak>
```

**Inline tags (boson higgs-tts-3)**:

```
<|emotion:enthusiasm|>{excited line} <|sfx:laughter|>{more}
<|prosody:speed_slow|>{slow line}<|prosody:pause|> {next}
```

Common SSML elements:

- `<emphasis level="strong">` for stress
- `<break time="300ms"/>` for pauses
- `<phoneme>` for brand-name pronunciation
- `<say-as interpret-as="characters">` for spelled-out strings

Boson inline tag categories: emotion / style / sfx / prosody (see `boson-ai-skill/docs/tts_tags.md` for the full list).

Check the target TTS skill's docs before assuming a notation is supported.
