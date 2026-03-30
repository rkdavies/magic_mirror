---
id: SEED-002
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Milestone scope includes generative AI on user photos, virtual costumes/wardrobe, AI scene backgrounds, or personalized creative output beyond static chroma-key assets
scope: large
---

# SEED-002: AI generated costumes and backgrounds from captured pictures

## Why This Matters

Static themed backgrounds and overlays (see [SEED-001](SEED-001-photo-booth-capabilities.md)) cap novelty. **Generating costumes and environments from the actual capture** pushes toward differentiation—custom looks per guest, seasonal campaigns, and “you in the movie poster” moments. That upside comes with **non-optional** concerns: **likeness consent**, **safety/moderation**, **latency and cost** (API or self-hosted inference), **quality variance** across devices, and **policy** for minors and commercial use. This seed keeps those constraints attached so roadmap work does not treat “AI button” as a small feature.

## When to Surface

**Trigger:** When planning a milestone that touches **generative or heavily model-driven image editing** built **on top of booth/capture flows**—not merely picking a PNG background.

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- **Virtual costumes / wardrobe** or outfit transfer driven by ML from a guest photo.
- **Generative or strongly personalized backgrounds** (text-to-image, img2img, segmentation + inpaint) using the capture as conditioning.
- **Personalization at scale** (per-event styles, brand-safe templates) where automation replaces hand-authored theme packs.
- Explicit **privacy/consent/moderation** work for **biometric likeness** or user-upload pipelines tied to capture.

## Scope Estimate

**Large** — Spans model selection (client vs. server vs. hybrid), **BFF/API keys**, **queues and SLAs**, **content policy**, **UX for failures and retries**, and **legal/copy** for consent. Often **downstream of** a working capture + export path (depends on [SEED-001](SEED-001-photo-booth-capabilities.md) foundations).

## Breadcrumbs

Related planning and research in this repo:

- [.planning/seeds/SEED-001-photo-booth-capabilities.md](SEED-001-photo-booth-capabilities.md) — capture, chroma key, audio, optional hardware; prerequisite flow.
- [.planning/research/SUMMARY.md](../research/SUMMARY.md) — phase 6 “AI / generative track (optional)”; segmentation vs. server gen.
- [.planning/research/FEATURES.md](../research/FEATURES.md) — differentiators: AI segmentation, generative backgrounds (complexity notes).
- [.planning/research/ARCHITECTURE.md](../research/ARCHITECTURE.md) — optional API client, backend for expensive AI.
- [.planning/research/PITFALLS.md](../research/PITFALLS.md) — AI path FPS collapse, moderation/safety surface area.

No application source files in Scribe yet for this capability.

## Notes

- **Costume** might mean: segmented person + curated asset layers, true generative outfit (higher risk), or hybrid (pose-aware stickers)—scope should be chosen explicitly when this seed activates.
- **Client-side** options (e.g. segmentation) reduce data egress but hit **bundle size and device class**; **server-side** gen simplifies UX but needs **retention policy** and **red-team** prompts.
- Pair with explicit **user-facing consent** (“your photo may be sent to…” / on-device only) before implementation milestones.
