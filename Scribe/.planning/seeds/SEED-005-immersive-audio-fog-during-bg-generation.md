---
id: SEED-005
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Milestone scope includes synchronized sensory feedback during long-running background generation—industrial/steampunk SFX (clank, clang, steam hiss) and optional physical effects via Arduino-attached fog or similar actuators
scope: medium
---

# SEED-005: Immersive audio during background generation + optional Arduino / fog

## Why This Matters

**Background generation** ([SEED-002](SEED-002-ai-costumes-backgrounds-from-capture.md), [SEED-004](SEED-004-generated-background-matches-client-theme.md)) introduces **dead air**: guests wait on the model while staring at a spinner. Layering **thematic audio**—**clank, clang, steam hissing**—turns wait time into **show** and reinforces **Steampunk / industrial** tone ([SEED-003](SEED-003-web-client-themes-steampunk-poc.md)). Optionally **triggering an Arduino** that drives a **fog machine** (relay, remote hack, or safe interface per hardware docs) makes the booth **memorable** for events. This seed ties **timing** (gen lifecycle), **audio mixing** (Web Audio / HTML5, preload, loop vs one-shots), **accessibility** (mute, reduced motion / reduced sensory where applicable), and **hardware reality** (Web Serial on Chromium, **local bridge** elsewhere—see [SEED-001](SEED-001-photo-booth-capabilities.md)).

## When to Surface

**Trigger:** When a milestone ships or extends **async background generation** and should improve **perceived performance** and **atmosphere**, or when **physical effects** are in scope for the same flow.

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- **Progress-synced or staged SFX** while generation runs (idle steam loop, periodic mechanical hits, ramp-up as progress advances).
- **Fog / haze / practical effect** cues aligned with “steam” theme and **safe** operator controls (timeouts, kill switch, venue rules).
- **Arduino (or MCU) serial protocol** from browser **or** companion app: simple line commands (`FOG_ON`, `FOG_OFF`, duration ms) with **fail-safe** defaults.
- **Chromium-first hardware** with documented **Safari/Firefox fallback** (no fog from web, or bridge-only).

## Scope Estimate

**Medium** — **Audio-only** path is bounded (asset sourcing/licensing, mix levels, mute, sync to job state). **Arduino + fog** adds **electrical safety**, **firmware**, **pairing UX**, and **deployment** (kiosk Chrome, dedicated USB port). Treat fog as **optional sub-track** so audio can ship without hardware.

## Breadcrumbs

- [.planning/seeds/SEED-001-photo-booth-capabilities.md](SEED-001-photo-booth-capabilities.md) — audio cues, WebUSB/Web Serial limits, local bridge pattern.
- [.planning/seeds/SEED-002-ai-costumes-backgrounds-from-capture.md](SEED-002-ai-costumes-backgrounds-from-capture.md) — generation latency and backend jobs.
- [.planning/seeds/SEED-003-web-client-themes-steampunk-poc.md](SEED-003-web-client-themes-steampunk-poc.md) — steampunk / steam aesthetic alignment.
- [.planning/seeds/SEED-004-generated-background-matches-client-theme.md](SEED-004-generated-background-matches-client-theme.md) — when generation runs relative to theme.
- [.planning/research/PITFALLS.md](../research/PITFALLS.md) — Web Serial/USB gaps, malicious USB, performance.

## Notes

- **Licensing:** Use royalty-free SFX or commissioned assets; document attribution if required.
- **Arduino:** Typical pattern: **USB serial** (CDC) + **relay module** wired per fog machine manufacturer guidance—**no mains advice in app code**; venue electrician/operator owns wiring.
- **Safety:** Cap fog duration in firmware and UI; **hardware watchdog** if possible; clear **“effects disabled”** toggle for accessibility and indoor air policies.
- **Sync:** On `generation:start` → start steam bed + optional short fog pulse; on `generation:complete` → taper audio, ensure fog off; on **error** → stop all effects.
