# AI Video Model Research Template

Use this structure when researching any AI video generation model (seedance, Sora, Kling, Runway, HeyGen, Pika, etc.). Adapt section names to the model; keep the order.

## How to use this template

1. Replace `<MODEL>` with the model name throughout.
2. Dispatch a research subagent (`researcher` type) with this template as the output structure.
3. Require real URLs for every claim. Mark anything unverified as "需核实".
4. Save the report to `docs/promo/00-<model-slug>-调研报告.md`.

---

## Report structure

### 1. 模型基础 (Model basics)

| Dimension | Content |
|---|---|
| 官方全名 | full product name |
| API model ID | exact string for API calls |
| 提供方 | company + platform (e.g., 字节跳动 + 火山引擎方舟) |
| 版本矩阵 | lite / pro / fast variants and their differences |
| 发布时间线 | version release dates |
| 调用方式 | API / web UI; text-to-video / image-to-video / video-to-video support |
| 分辨率 | supported resolutions, defaults |
| 时长 | supported durations, defaults |
| 输出比例 | aspect ratios |
| 音频 | native audio-visual joint generation? |

### 2. Prompt 写法 (Prompt conventions)

- Official recommended prompt structure (e.g., seedance 5-段式)
- Camera vocabulary with both 中文 and English terms where applicable
- Whether `negative_prompt` is supported as a separate field
- Style / lighting / lens vocabulary conventions
- 3-5 real example prompts from official docs or vetted community sources, quoted verbatim with source attribution

### 3. API 参数 (API parameters)

- Endpoint URL
- Required vs optional fields with enums and defaults
- Async flow (POST create → GET poll → fetch result)
- Typical latency per resolution/duration
- Authentication scheme

### 4. 计费 (Pricing)

- Per-token / per-second / per-call pricing
- Token formula if applicable
- Estimated cost per typical shot (e.g., 5s/1080p)
- **Mark "需核实，以官方定价页为准"** with the official pricing URL — prices change quarterly

### 5. 最佳实践 / 避坑 (Best practices / pitfalls)

Known weaknesses with concrete mitigations:

- Complex actions / multi-person interaction
- Text rendering (captions, logos, on-screen text)
- Audio sync
- Identity / character consistency across shots
- Style consistency across shots
- Camera control reliability

### 6. 真实信息源 (Real sources, all actually visited)

Categorize:

- **官方文档** (official docs) — vendor domain
- **官方发布新闻** (official launch news) — vendor blog / press release
- **同源上游 API 聚合** (same-source API aggregators) — for cross-validating fields when official docs are JS-rendered
- **社区 OSS 参考实现** (community OSS) — GitHub prompt libraries
- **第三方评测** (third-party reviews) — blogs, arXiv papers

Every URL must have been actually fetched. No fabrication.

### 7. 注意事项 (Caveats)

- What could not be verified
- What is time-sensitive (pricing, model versions)
- Version generation notes (e.g., "1.0 is now superseded by 1.5 pro / 2.0")

### 8. 可复用结论 (Actionable summary)

5-7 bullets a downstream agent can use directly:

- Which model ID to pick for which scenario
- Which prompt structure to use
- Which constraints to always include
- Which things to never ask the model to do (text, multi-shot, etc.)
- Rough cost per shot
- Where to find the canonical docs

---

## Dispatching the research subagent

When you dispatch the `researcher` subagent, give it:

1. The target model name and any context (use case, budget, region)
2. This template as the output structure
3. Explicit instruction: "find real URLs, mark unverified claims as '需核实', never fabricate prices or API fields"
4. A target word count (typically 1500+ words for a thorough report)
5. The output file path so it can save directly

The subagent's final message will be the full report; relay the key constraints back to the user in chat but save the full report to disk.
