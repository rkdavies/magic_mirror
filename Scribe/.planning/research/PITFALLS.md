# Domain Pitfalls

**Domain:** Web-based photo booth / interactive capture kiosk  
**Researched:** 2026-03-30

## Critical pitfalls

### Pitfall: Treating WebUSB / Web Serial as cross-browser

**What goes wrong:** Feature works in Chrome; **Safari and Firefox do not implement** WebUSB/Web Serial per [caniuse WebUSB](https://caniuse.com/webusb) and [Web Serial](https://caniuse.com/web-serial); MDN marks both experimental with secure-context requirements ([WebUSB](https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API), [Web Serial](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API)).

**Why it happens:** Docs and demos target Chromium; product owner tests on one laptop.

**Consequences:** “Effects broken on iPad” in the field; impossible demos without a bridge.

**Prevention:** Abstract `EffectsPort`; ship **local companion** or documented **Chromium-only** hardware path.

**Detection:** `if (!('usb' in navigator))` / `serial` checks; explicit QA matrix row for Safari.

---

### Pitfall: Insecure context (no HTTPS)

**What goes wrong:** `navigator.mediaDevices` is `undefined` or calls reject — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

**Why it happens:** LAN IP over HTTP, mixed-content embed, wrong tunnel.

**Consequences:** Booth appears “dead” on first load.

**Prevention:** Enforce HTTPS in prod; use `localhost` / documented exceptions for dev per [MDN Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts).

**Detection:** `window.isSecureContext` banner in dev builds.

---

### Pitfall: Canvas taint from backgrounds

**What goes wrong:** `toBlob` throws `SecurityError` — [MDN toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob).

**Why it happens:** Themed image from CDN without CORS; user loads arbitrary URL.

**Consequences:** No save/print; silent failure if uncaught.

**Prevention:** Same-origin assets or CORS-enabled CDN + `crossOrigin = "anonymous"` on `Image`.

---

### Pitfall: Ignoring lighting for chroma key

**What goes wrong:** Green spill, hair halos, “cheap” composite despite good code.

**Why it happens:** Software can’t fully fix bad uniform lighting or wrong screen color.

**Consequences:** Rework perceived as “buggy app.”

**Prevention:** Operator checklist (even, soft light, distance to screen); shader params (tolerance, spill suppression); optional “calibrate key color” step.

**Detection:** QA in venue-like lighting, not only desk lamps.

---

## Moderate pitfalls

### Pitfall: Permission and iframe policy

**What goes wrong:** `NotAllowedError` or no prompt — Permissions Policy can block camera — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

**Prevention:** Run booth top-level or set `Permissions-Policy` correctly for embeds.

---

### Pitfall: `getUserMedia` hang

**What goes wrong:** Promise never settles — [MDN notes](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) user may ignore prompt.

**Prevention:** Timeout + cancellable UI; educate “click Allow.”

---

### Pitfall: Web Share assumptions

**What goes wrong:** `share()` rejects — not Baseline, file type limits, no transient activation — [MDN share()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share).

**Prevention:** `canShare` check; always offer download; gate behind button click.

---

### Pitfall: Performance on low-end tablets

**What goes wrong:** AI segmentation + HD video + GL stalls countdown.

**Prevention:** Resolution caps; optional “quality” preset; worker/OffscreenCanvas (phase research).

---

### Pitfall: iOS / Safari edge cases (Lockdown Mode, etc.)

**What goes wrong:** Community reports of `MediaDevices` unavailable under heightened security modes even on HTTPS — **LOW confidence** for exact iOS version matrix; treat as support FAQ.

**Prevention:** Detect absence of `mediaDevices`; show human-readable recovery steps.

---

## Minor pitfalls

### Pitfall: Mirroring confusion

Users expect selfie mirror; developers flip inconsistently. Pick one product rule and stick to it.

### Pitfall: Autoplay audio blocked

Browsers gate audio; cue first sound off explicit tap or use Web Audio after gesture.

---

## Security and kiosk mode

| Topic | Risk | Mitigation |
|-------|------|------------|
| **Open URL bar** | Guests navigate away | PWA `fullscreen`/`standalone`, or OS `--kiosk` launch (vendor-specific) |
| **DevTools / escape** | Tampering | OS-level kiosk profile; not solvable by SPA alone |
| **Malicious USB** | WebUSB connects arbitrary devices | Pair only known VID/PID; operator pairing step; prefer dedicated MCU |
| **Session recording** | Privacy | On-device processing; clear signage; data retention policy |

**Note:** True “kiosk hardening” is **OS + browser + app**. The SPA can only do its part (fullscreen manifest, no sensitive data in URLs).

---

## Phase-specific warnings

| Phase topic | Likely pitfall | Mitigation |
|-------------|----------------|------------|
| Media capture | HTTPS / permissions | Ship diagnostic screen first |
| Compositing | CPU keying | WebGL2 path early |
| Export | CORS taint | Asset pipeline review |
| Hardware | Safari gap | Bridge interface from day one |
| AI background | FPS collapse | Profiling milestone before promising |

## Sources

- [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)  
- [MDN: Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)  
- [MDN: HTMLCanvasElement.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)  
- [MDN: WebUSB](https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API)  
- [MDN: Web Serial](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API)  
- [MDN: Navigator.share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)  
- [Can I use: WebUSB, Web Serial](https://caniuse.com/)  
- [Mozilla standards positions](https://mozilla.github.io/standards-positions/) (linked from caniuse for WebUSB/Web Serial)  
- [WebKit tracking prevention / positions](https://webkit.org/) (referenced from caniuse resources for Web Serial)  
