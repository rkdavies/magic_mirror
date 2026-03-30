# Scribe — Requirements (v1)

## Project

**Scribe** (name provisional) is a **web-based photo booth**: guests get a guided capture on a kiosk-class device, optional chroma-key compositing onto **themed** assets, an optional **generative** background path that stays **on-theme**, **immersive wait-time** audio and optional **physical effects**, then **fulfillment** via print and/or **email-gated** digital copy—with non-coercive skip paths. Delivery targets **browser-first** (HTTPS, PWA-style shell); hardware APIs are **Chromium-skewed** with explicit fallbacks per research (see `.planning/research/`).

## v1 requirements

| ID | Requirement |
|----|-------------|
| **FND-01** | Booth runs in a **secure context**; camera/permission failures show **actionable** messaging (denied, insecure, in use, not found). |
| **FND-02** | **Web App Manifest** supports kiosk-style use (`fullscreen` / `standalone`), icons, and documented notes for OS/browser launch (e.g. Chrome `--kiosk`) where relevant. |
| **CAP-01** | **Live camera preview** with kiosk-appropriate layout, mirroring, and aspect handling. |
| **CAP-02** | **Countdown / ready flow** (state machine) before still capture. |
| **AUD-01** | **Audio cues** for countdown/shutter (Web Audio or HTML audio); guest can **mute**; reduced-motion/sensory preferences respected where applicable. |
| **CAP-03** | **Still capture** from the live pipeline (single primary output frame policy as designed). |
| **CAP-04** | **Review** step with **retake** before committing to export/next steps. |
| **EXP-01** | Guest can **download** the final raster (PNG/JPEG/WebP) via origin-clean export (`toBlob` / download). |
| **EXP-02** | **Web Share** used when available and permitted; **download (or equivalent) always remains** if share is unavailable or fails—no silent failure. |
| **CMP-01** | **WebGL2** chroma-key compositing with guest- or operator-visible **tuning** (tolerance/spill) or documented defaults. |
| **CMP-02** | Theme/compositor assets load **without canvas taint** (same-origin or CORS-clean); composite remains **exportable**. |
| **THEME-01** | **Theme contract** (tokens/metadata, asset manifest) drives UI chrome and compositor inputs from one source of truth. |
| **THEME-02** | **Steampunk PoC** theme applies to shell **and** at least one compositor background (and optional frame overlay); guest or operator can **choose theme** when more than one exists. |
| **GEN-01** | **Consent/disclosure** before any capture is sent off-device for AI/generative processing (clear copy; minors/venue policy awareness documented in product). |
| **GEN-02** | **Async background generation** from capture with visible **progress**, **failure handling**, and fallback to a **curated themed** still (no dead-end). |
| **TGEN-01** | **Active theme** informs generation configuration (e.g. server-expanded prompts/params); on failure or weak match, **fall back** to curated themed composite. |
| **SFX-01** | While generation runs, **thematic wait audio** plays (e.g. steampunk/industrial bed); guest can **mute**; licensing-safe assets. |
| **SFX-02** | Wait audio and optional effects **sync to generation lifecycle** (start, complete, error → stop/taper appropriately). |
| **FX-01** | **EffectsPort**: optional **fog/relay** via Web Serial/USB on **supported browsers** OR **local bridge**; unsupported browsers show **clear disabled** state (no silent breakage). |
| **FULF-01** | Guest can **print** the final image via a **browser print** path with a sensible **print layout** (e.g. strip/4×6-oriented CSS). |
| **FULF-02** | Guest can submit **email** for **free digital copy** with **separate** transactional vs marketing/community consent where required; backend or ESP hands **secure delivery** (e.g. signed link), with basic **abuse/rate** safeguards. |
| **FULF-03** | Guest can **complete the flow without email**—download/share/print remains available (non-coercive funnel). |

## Deferred to v2 (explicit)

- **Full generative costumes / wardrobe** and heavy **img2img costume** flows beyond background-focused v1 (see SEED-002 breadth).
- **AI person segmentation / “no green screen”** (e.g. MediaPipe) as primary keying path—optional spike only if v1 green-screen path is insufficient.
- **Enterprise MDM / single-app native wrapper** unless a customer requires it (promote from browser + PWA).
- **Hardware-specific silent print**, cut-sheet accounting, or paid-per-print integrations beyond standard browser print.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FND-01 | 1 | Pending |
| FND-02 | 1 | Pending |
| CAP-01 | 1 | Pending |
| CAP-02 | 1 | Pending |
| AUD-01 | 1 | Pending |
| CAP-03 | 1 | Pending |
| CAP-04 | 1 | Pending |
| EXP-01 | 1 | Pending |
| EXP-02 | 1 | Pending |
| CMP-01 | 2 | Pending |
| CMP-02 | 2 | Pending |
| THEME-01 | 2 | Pending |
| THEME-02 | 2 | Pending |
| GEN-01 | 3 | Pending |
| GEN-02 | 3 | Pending |
| TGEN-01 | 3 | Pending |
| SFX-01 | 4 | Pending |
| SFX-02 | 4 | Pending |
| FX-01 | 4 | Pending |
| FULF-01 | 5 | Pending |
| FULF-02 | 5 | Pending |
| FULF-03 | 5 | Pending |
