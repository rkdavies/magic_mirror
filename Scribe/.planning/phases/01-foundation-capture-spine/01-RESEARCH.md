# Phase 01 research — Foundation & capture spine

**Researched:** 2026-03-30  
**Confidence:** HIGH for web platform APIs (MDN Baseline / widely available); MEDIUM for kiosk OS matrix.

## Sources already in-repo

- `.planning/research/SUMMARY.md`, `STACK.md`, `FEATURES.md`, `PITFALLS.md`, `ARCHITECTURE.md` — stack (Vite + React + TS), `getUserMedia`, Web Audio, `toBlob`, Web Share + fallback, secure context, canvas taint (preview for later phases).

## Phase-specific notes

### Secure context (FND-01)

- `getUserMedia` and many media APIs require a **secure context** (HTTPS or `http://localhost`). Non-secure: show explicit copy (“Use HTTPS or localhost”) and avoid silent failure.
- MDN documents `NotAllowedError`, `NotFoundError`, `NotReadableError`, `OverconstrainedError`, `SecurityError` — map each to a guest-visible message + recovery hint where possible.

### Web App Manifest (FND-02)

- `display: standalone` or `fullscreen` improves kiosk feel; icons required for install prompts; `theme_color` / `background_color` for splash. Document Chrome `--kiosk` / edge cases separately from SPA code.

### Capture pipeline (CAP / EXP)

- Still frame: draw current video frame to `canvas` (same-origin video only for taint — camera stream is fine), `canvas.toBlob('image/jpeg'|'image/png')`.
- `navigator.share({ files: [...] })` needs `canShare` check, user gesture, and **HTTPS**; always keep **download** path.

### Audio (AUD-01)

- Web Audio: decode buffers once, schedule beeps to countdown; respect **muted** tab / user mute toggle (gain node at 0 or suspend context).
- `prefers-reduced-motion`: optional visual substitute for motion-heavy countdown (larger numerals, no shake).

## Open items for execution

- Exact **aspect ratio** (4:3 vs 16:9 vs square) — pick one in 01-02 unless product says otherwise.
- **Mirror** preview horizontally for selfie UX (common booth expectation).

## Verdict

No additional external research required before planning; implement against MDN + existing `.planning/research/`.
