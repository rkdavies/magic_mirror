# Roadmap: Scribe (booth)

## Overview

Ship a **browser-first** event photo booth: secure **capture and export** first, then **Steampunk-themed WebGL compositing**, then an optional **generative background** path **bound to the active theme**, **wait-time audio** and optional **fog/effects** via an abstracted port, and finally **print plus email-gated digital copy** with ethical skip paths. Phases follow vertical slices and API risk order from `.planning/research/SUMMARY.md` (media spine before heavy GL, GL before server gen, gen before wait SFX, fulfillment last).

## Phases

- [ ] **Phase 1: Foundation & capture spine** — Secure deploy, manifest, live preview, countdown, audio cues, review/retake, download and share-with-fallback.
- [ ] **Phase 2: Themes & compositing** — Theme contract, Steampunk PoC, WebGL2 chroma key, CORS-safe assets, export still clean.
- [ ] **Phase 3: Generative backgrounds + theme binding** — Consent, async gen with progress/fallback, theme-driven gen config and mismatch fallback.
- [ ] **Phase 4: Wait experience & physical effects** — Generation-synced SFX/mute; EffectsPort for fog/bridge with unsupported-browser UX.
- [ ] **Phase 5: Fulfillment** — Print layout, email + digital delivery with consent and abuse basics; always a no-email path.

## Phase Details

### Phase 1: Foundation & capture spine

**Goal:** Guests can run a credible booth loop—preview, timed capture with sound, review, and reliable save/share—on HTTPS without compositing or AI.

**Depends on:** Nothing (first phase)

**Requirements:** FND-01, FND-02, CAP-01, CAP-02, AUD-01, CAP-03, CAP-04, EXP-01, EXP-02

**Success Criteria** (what must be TRUE):

1. Opening the app over non-secure HTTP (where applicable) or with camera blocked shows a **clear next step**, not a blank screen.
2. Guest sees **live video** from the chosen camera before capture.
3. Guest experiences a **countdown or ready sequence** and hears (or sees, if muted) cues aligned with capture timing.
4. Guest can **retake** after review instead of being forced forward.
5. Guest always gets a **saved file** (download); if **Share** exists and works, it is offered without removing download.

**Plans:** 4 (see `.planning/phases/01-foundation-capture-spine/*-PLAN.md`)

Plans:

- [ ] 01-01: Secure context, manifest, and hosting/dev notes
- [ ] 01-02: Media acquisition, preview, and permission error surfaces
- [ ] 01-03: Countdown/review state machine + audio cues + mute
- [ ] 01-04: Still capture + export (blob, download, share + fallback)

### Phase 2: Themes & compositing

**Goal:** The same booth delivers a **Steampunk** look in UI and composite, with **GPU chroma key** and exports that never hit canvas **SecurityError** from bad assets.

**Depends on:** Phase 1

**Requirements:** CMP-01, CMP-02, THEME-01, THEME-02

**Success Criteria** (what must be TRUE):

1. Guest or operator can **select Steampunk** (and default/minimal baseline if applicable) and the **chrome and backgrounds** reflect it.
2. With a standard green-screen setup, the guest sees themselves **composited** over the themed plate in real time or at capture time per product choice.
3. Guest can adjust (or operator can lock) **key tuning** and see **meaningful** edge/spill change.
4. **Download/share** of the composite still succeeds with **theme assets** loaded the intended way (no taint surprises).

**Plans:** TBD

Plans:

- [ ] 02-01: Theme manifest, tokens, and asset loading (CORS-safe)
- [ ] 02-02: WebGL2 chroma pipeline wired to preview/capture
- [ ] 02-03: Steampunk asset pack + UI skin + export integration

### Phase 3: Generative backgrounds + theme binding

**Goal:** Guests who opt in can get an **AI-generated** background that **reads as the same world** as the active theme, with safe **fallback**.

**Depends on:** Phase 2

**Requirements:** GEN-01, GEN-02, TGEN-01

**Success Criteria** (what must be TRUE):

1. Before any server/gen processing, the guest sees **explicit consent** matching the actual data path.
2. During generation, the guest sees **progress** (not an unexplained hang) and receives a **final image** even when the job fails (fallback plate).
3. With **Steampunk** selected, generated output **uses theme-derived parameters** (visible in behavior: style matches steampunk brief—not a random unrelated scene).
4. If generation is off-theme or errors, the guest still receives a **cohesive Steampunk curated** composite.

**Plans:** TBD

Plans:

- [ ] 03-01: BFF/API client, keys, job model, and consent UX
- [ ] 03-02: Theme id → server-side gen config + fallback policy
- [ ] 03-03: End-to-end gen flow from capture to final composite

### Phase 4: Wait experience & physical effects

**Goal:** Generation wait feels **intentional** (audio + optional fog) and **safe** to skip or disable; hardware stays behind a **port** with honest browser support messaging.

**Depends on:** Phase 3

**Requirements:** SFX-01, SFX-02, FX-01

**Success Criteria** (what must be TRUE):

1. While generation runs, **thematic audio** plays unless the guest has muted or opted for reduced sensory (per product rules).
2. Audio **starts and stops** in sync with generation state (including errors).
3. On a **supported** configuration, an operator-approved **fog pulse** (or similar) can fire; on **unsupported** browsers, the UI states that **hardware effects are unavailable**—rest of the booth still works.

**Plans:** TBD

Plans:

- [ ] 04-01: Wait SFX assets, mixing, mute, lifecycle hooks
- [ ] 04-02: EffectsPort + Web Serial/bridge + fail-safe timeouts

### Phase 5: Fulfillment

**Goal:** Guests leave with **paper and/or inbox**, with **consent-respecting** email capture and **no forced** marketing funnel.

**Depends on:** Phase 2 (minimum final image); **full story** assumes Phase 3–4 complete for gen+drama path

**Requirements:** FULF-01, FULF-02, FULF-03

**Success Criteria** (what must be TRUE):

1. Guest can **print** from a dedicated action with a **print-styled** preview/layout.
2. Guest can enter **email** and receive a **digital copy** under terms shown at collection time; transactional vs community signup is **not misleading**.
3. Guest can **finish** with only **on-device download/share/print**—no email required.

**Plans:** TBD

Plans:

- [ ] 05-01: Print CSS/layout + user flow from final image
- [ ] 05-02: Email capture, consent copy, backend/ESP, signed link delivery
- [ ] 05-03: Rate limits, validation, and skip-path QA

## Progress

**Execution order:** 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & capture spine | 0/4 | Planned | - |
| 2. Themes & compositing | 0/TBD | Not started | - |
| 3. Generative + theme binding | 0/TBD | Not started | - |
| 4. Wait experience & effects | 0/TBD | Not started | - |
| 5. Fulfillment | 0/TBD | Not started | - |
