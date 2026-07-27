# Marketing Copy Template

Use this structure when writing the main marketing copy for a promo video. Save output to `docs/promo/01-宣传文案.md` (or equivalent in the project).

## Before writing — gather these inputs

Ask only what isn't already in the project README, brand folder, or prior docs:

1. **Target audience(s)** — who specifically. Could be one segment or several. For B2C: demographic + use case. For B2B: role + industry + decision unit. Do not assume.
2. **Their pain points** — what problem does the audience wake up with. One sentence per audience segment.
3. **Product/brand differentiators** — 3-5 things only this product can claim. Must be concrete (specific feature, real number, named certification), not generic adjectives.
4. **Brand voice and tone** — formal/casual, authoritative/warm, technical/accessible, playful/serious
5. **Brand visual identity** — primary/secondary/accent colors as hex (pull from project brand config or design tokens, do not use placeholders), logo location, existing photo/video assets
6. **Call-to-action** — what should the viewer do after watching. Depends on product type: signup / install / call / visit / partner / subscribe / request demo.
7. **Credentials / proof points** — certifications, awards, real numbers, case studies. Mark anything uncertain as "需核实".

If any input is missing and cannot be inferred, ask the user. Do not invent credentials, numbers, or testimonials.

---

## Document structure

The structure below is the default — adapt to the product. A consumer impulse-buy brand might collapse sections 2 and 4; a B2B enterprise product might expand section 5 with a comparison table.

### 1. 一句话定位 (One-sentence positioning)

A single sentence that captures what the product is and who it's for.

Pattern options:

- `让 X 被 Y，让 Z 有 W。` (parallel structure, good for two-sided products)
- `X 是 Y 自主研发、运营的 Z——把 A、B、C 拉到同一张桌子上，让 D 直接 E。` (good for platforms)
- `X · 一句最锋利的产品承诺。` (good for single-line brand slogans)

Avoid: "行业领先的"、"致力于"、"一站式解决方案"、"赋能".

### 2. 核心价值 (Value propositions)

A table — one row per audience segment. Columns: 对谁 / 痛点 / 答案.

| 对谁 | 痛点 | 答案 |
|---|---|---|
| {受众 1} | {pain} | {answer} |
| {受众 2} | {pain} | {answer} |
| ... | | |

Number of rows = number of distinct audience segments. **One to three rows is typical.** Do not pad to three if there's only one audience; do not cap at three if there are genuinely more.

### 3. 主文案：{主题} (Main narrative)

Long-form prose, 400-600 Chinese characters (or equivalent). Structure:

1. **Open with the human, not the product.** A concrete person with a real skill, habit, or pain. 2-3 sentences. Skip this only for pure product-launch films where the product itself is the protagonist.
2. **Show the matching pain on the other side** (if two-sided) **OR amplify the same pain** (if one-sided). 2-3 sentences.
3. **Bridge to the product.** Introduce the product by name with whatever institutional backing or origin story matters. Keep it short — the product is the answer, not the subject.
4. **Explain how, concretely.** Two to four mechanisms or components, each as a short paragraph or numbered list.
5. **Differentiate.** What this does that existing alternatives (named or implied) cannot.
6. **Close with the slogan.** Two to four short lines, parallel structure. Memorable.

**Style**:

- Plain language. Use one everyday metaphor per concept.
- Show don't claim. Cite the specific credential, number, or feature — "<具体认证名称> beats 行业领先"; "<N> 天无理由退 beats 卓越的客户体验".
- Sentences that survive being spoken. Read every sentence out loud mentally first.

### 4. 差异化卖点 (Differentiators)

Three to five one-line bullets. Each bullet = one concrete thing competitors don't or can't do. Format: `**关键词**：具体说明`.

Order from strongest to weakest. The first bullet is what the viewer remembers.

### 5. 数据/资质背书段 (Credentials)

A blockquote section listing real certifications, licenses, permits, awards, case studies, partner logos, published numbers. Pull from project README or `brand/` folder. Mark anything uncertain as "需核实".

If there are no real credentials, omit this section rather than padding with vague claims.

### 6. CTA (Calls to action)

One CTA per audience segment from section 2. Each CTA:

- Verb-first ("有 X 需求？" / "想 Y？" / "扫码 Z")
- Concrete next step (visit page, scan QR, call number, install link, request demo)
- Friction-removing promise if true (no signup fee, 24h response, free trial, money-back)

If there's only one audience, write one CTA. Do not invent multiple CTAs to fill the section.

### 7. 品牌色与视觉规范 (Brand visual identity)

Table of brand colors with hex values and semantic meaning. Reference paths to logo and photo assets in the project. This section is consumed by the shot-prompt phase to inject color palette into every video prompt.

Pull hex values from the project's actual brand config (`brand/` folder, design tokens file, or `tailwind.config.js`). Do not use placeholder values like `#0E4B3F` unless that's actually the project's brand color.

### 8. 下一步建议 (Next steps)

What the user should do with this copy: split into公众号长文 / 官网页 / 投放短文 / 详情页 / 销售话术 / etc., depending on the project's distribution plan.

---

## Style rules (反 AI slop defaults)

These rules reflect a preference for honest, anti-slop content. They are defaults — surface to the user if the project genuinely calls for a different voice (e.g., a clickbait ad buy), but otherwise keep them.

- **No buzzwords.** Strike each occurrence of "赋能"、"抓手"、"闭环"、"生态"、"一站式"、"行业领先"、"致力于" and rewrite with a concrete verb or specific claim.
- **No fake enthusiasm.** No "太棒了"、"很惊喜"、"竟然". The copy reports facts.
- **No inflated claims.** "行业领先"、"国内首家"、"最佳" — delete unless backed by a cited third-party ranking.
- **Conclusion first, details after.** Every paragraph leads with its point.
- **List over paragraph when the user will act.** Use bullets for actionable items.
- **Match the user's language.** Chinese in, Chinese out; English in, English out.
