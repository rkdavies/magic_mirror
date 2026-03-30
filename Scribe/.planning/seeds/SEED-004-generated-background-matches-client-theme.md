---
id: SEED-004
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Milestone scope includes AI or procedural background generation that must stay visually consistent with the active web client theme (e.g. Steampunk tokens, style prompts, or reference assets)
scope: large
---

# SEED-004: Generated background matches theme set in web client

## Why This Matters

**Themes** ([SEED-003](SEED-003-web-client-themes-steampunk-poc.md)) and **generative backgrounds** ([SEED-002](SEED-002-ai-costumes-backgrounds-from-capture.md)) are separate until you **bind them**: the guest picks (or the venue locks) **Steampunk** in the UI, but the model returns a **generic sci-fi hallway**—the product feels broken. This seed captures the **integration contract**: the active theme must drive **prompts, LoRA/style refs, negative prompts, palette clamps, or post color-grade** so generated output **reads as the same world** as buttons, frames, and overlays. Without that, “themed booth + AI” ships as two unrelated features.

## When to Surface

**Trigger:** When a milestone combines **(a)** runtime **theme selection** or **theme manifest** with **(b)** **server- or client-side generation** of backgrounds (or strong img2img) from the capture pipeline.

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- **Theme-aware prompting** — inject theme id, style bible text, or reference thumbnails into the generation API.
- **Per-theme model or adapter** — different checkpoint/LoRA per theme (e.g. Steampunk vs. neon cyber).
- **Post-process alignment** — LUT, palette mapping, or small refiner pass so output matches **design tokens** (primary/secondary/accent).
- **QA / acceptance** — defining “on-theme” for generated frames (human review rubric or automated embedding distance to reference set).

## Scope Estimate

**Large** — Touches **product** (what “match” means), **prompt engineering** or **training assets**, **API payloads** (theme → gen params), **latency/cost** (extra refiner step), and **failure modes** (fallback to curated theme background if gen drifts). Depends on both **working themes** and **working generation path**; typically **after** PoC theme ([SEED-003](SEED-003-web-client-themes-steampunk-poc.md)) and **alongside or after** gen MVP ([SEED-002](SEED-002-ai-costumes-backgrounds-from-capture.md)).

## Breadcrumbs

- [.planning/seeds/SEED-002-ai-costumes-backgrounds-from-capture.md](SEED-002-ai-costumes-backgrounds-from-capture.md) — generative track, consent, server/client split.
- [.planning/seeds/SEED-003-web-client-themes-steampunk-poc.md](SEED-003-web-client-themes-steampunk-poc.md) — theme manifest, tokens, Steampunk PoC.
- [.planning/research/SUMMARY.md](../research/SUMMARY.md) — optional AI phase; cost and safety guardrails.
- [.planning/research/ARCHITECTURE.md](../research/ARCHITECTURE.md) — optional API client, BFF, compositor.

## Notes

- **Single source of truth:** Prefer theme id → **server-side expansion** into full gen config (secrets, long prompts) rather than sending opaque prompt blobs from the browser.
- **Steampunk PoC hook:** First vertical slice = `theme: steampunk` maps to a **frozen prompt prefix + negative list + palette hints**; measure subjective match before tuning per-venue.
- **Fallback:** If generation fails or scores low on theme classifier (if used), **composite curated Steampunk plate** so the booth never shows a mismatched gen.
