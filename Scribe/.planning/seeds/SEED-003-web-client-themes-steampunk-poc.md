---
id: SEED-003
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Milestone scope includes client theming, theme packs, branded skins, or a first vertical slice of a named aesthetic for the booth UI and composite assets
scope: medium
---

# SEED-003: Web client themes — Steampunk first (PoC)

## Why This Matters

A **theme system** turns one codebase into many looks—critical for events, brands, and seasonal runs. Starting with **Steampunk as the PoC** gives a **strong art-direction constraint** (palette, typography, ornament, background motifs) that stress-tests the pipeline: **theme metadata**, **switching** (runtime or build-time), **compositor-safe assets** (same-origin / CORS-clean), and **UI + print/export cohesion**. Shipping one excellent theme beats five shallow ones; Steampunk is the spike that proves the pattern before scaling to more themes.

## When to Surface

**Trigger:** When a milestone explicitly plans **visual theming for the web client**—chrome, tokens, themed backgrounds/overlays, or “skin” selection—not only core capture without look-and-feel.

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- **Theme pack** or **skin** work (colors, fonts, frame overlays, background sets) for the booth experience.
- **First named aesthetic** or **vertical slice** (here: **Steampunk**) to validate asset and code organization.
- **Operator or guest-facing theme picker** (even if PoC lists one theme + default).
- **Design system hooks** (CSS variables, theme JSON, manifest of assets) shared by UI and compositor.

## Scope Estimate

**Medium** — A focused PoC: one theme (**Steampunk**) end-to-end is **hours to a small number of days** for a thin slice if capture exists; grows if you add many resolutions, animation, or CMS-driven packs. **Does not require** generative AI ([SEED-002](SEED-002-ai-costumes-backgrounds-from-capture.md)); it **does** pair naturally with chroma-key and overlays ([SEED-001](SEED-001-photo-booth-capabilities.md)).

## Breadcrumbs

Related seeds and research:

- [.planning/seeds/SEED-001-photo-booth-capabilities.md](SEED-001-photo-booth-capabilities.md) — compositing and themed layers; assets must not taint canvas.
- [.planning/seeds/SEED-002-ai-costumes-backgrounds-from-capture.md](SEED-002-ai-costumes-backgrounds-from-capture.md) — optional later path for *generated* looks; this seed is **authored** theme packs first.
- [.planning/research/FEATURES.md](../research/FEATURES.md) — theme packs / overlays as differentiators; CORS note.
- [.planning/research/ARCHITECTURE.md](../research/ARCHITECTURE.md) — compositor + CDN/asset pipeline.

## Notes

- **PoC success criteria (suggested):** Steampunk theme applies to **shell UI** + at least **one** composite background (and optional frame overlay) with **export still working** (`toBlob` / share path clean).
- **Steampunk checklist (non-exhaustive):** brass/copper accents, muted sepia or deep slate base, Victorian/industrial display type, gear/bracket **frame** motifs, subtle **noise/paper** or **patina** textures—avoid cliché overload; pick a cohesive **3–5 color** token set.
- **Ordering:** Implement **theme contract** (folder layout, `theme.json`, token names) before art volume; second theme later proves repeatability, not the PoC gate.
