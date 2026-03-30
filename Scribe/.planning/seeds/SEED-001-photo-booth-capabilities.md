---
id: SEED-001
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Planning a milestone for interactive capture, kiosk/event UX, media-heavy web features, or hardware-adjacent experiences
scope: large
---

# SEED-001: Photo booth capabilities

## Why This Matters

A self-contained **photo booth** flow combines several high-impact UX pieces: live camera capture with **audio cues**, optional **chroma-key** compositing onto **themed backgrounds**, and optionally **synchronized physical effects** (e.g. fog) via **USB/serial** or a local bridge. Together they solve “event-grade” capture without a native app, while keeping room for polish (lighting, edge quality, permissions). Capturing this as a seed preserves the **full stack picture** (browser limits, hardware indirection, HTTPS/permission model) so it resurfaces when the right product milestone appears—not as a vague “do a camera thing” line item.

## When to Surface

**Trigger:** When the roadmap or a new milestone touches **interactive capture**, **kiosk/event experiences**, **media pipelines in the browser**, or **optional local hardware integration** (WebUSB, Web Serial, or companion service).

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- Building or extending **web-based capture** (getUserMedia, still export, countdown UX).
- Adding **real-time or post-capture effects** (canvas/WebGL chroma key, themed layers).
- Shipping **event or installation** features where **sound design** and **timed cues** matter.
- Exploring **USB/serial/HID** or a **small local daemon** to drive **relays, DMX, or other actuators** alongside the page.

## Scope Estimate

**Large** — Multiple subsystems: media permissions, capture pipeline, compositing (quality vs. performance), asset/theming strategy, audio, and optionally hardware protocol + cross-browser reality (Chrome vs. Safari/Firefox). Likely a dedicated milestone or multi-phase effort, not a single afternoon.

## Breadcrumbs

Related code and decisions found in the current codebase:

- No `photo`, `booth`, `camera`, or chroma-key references under the Scribe workspace yet (`grep` across `*.ts`, `*.js`, `*.md`).
- No `.planning/STATE.md` or `ROADMAP.md` present at seed planting time—relink here when those exist.

**Session context (for future you):** Prior discussion covered feasibility of **getUserMedia**, **Web Audio / HTML audio** for cues, **canvas/WebGL** green-screen compositing vs. **AI-generated** backgrounds (often via backend), and **WebUSB / Web Serial** for triggering an intermediary device (relay, MCU) rather than a “USB fog machine” directly.

## Notes

- Prefer **WebGL** for live keying if resolution and frame rate matter; naive per-pixel JS is simpler but heavier.
- For broad deployment (especially iOS) or blocked browser APIs, plan B is a **thin local service** (WebSocket/HTTP) that owns USB and exposes “fog on / fog off” to the page.
- Themed backgrounds: distinguish **curated assets** vs. **generative/AI**—only the latter needs server-side or API spend.
