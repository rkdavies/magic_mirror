# Research Summary: Scribe (provisional)

**Domain:** Web-based photo booth / interactive capture kiosk  
**Researched:** 2026-03-30  
**Overall confidence:** **MEDIUM–HIGH** for browser APIs and cross-browser hardware gaps; **MEDIUM** for exact npm patch pins and some kiosk/OS behaviors; **LOW** for anecdotal iOS Lockdown / ChromeOS offline+kiosk reports without primary repro.

## Executive Summary

Scribe sits at the intersection of **mature** web media APIs (`getUserMedia`, Web Audio, canvas export) and **intentionally constrained** hardware access (WebUSB, Web Serial). MDN classifies `getUserMedia` as Baseline widely available but requires a **secure context** and careful permission handling; `toBlob` is Baseline for turning composites into shareable files. **WebUSB and Web Serial are not viable on Safari (including iOS) or Firefox** according to [caniuse](https://caniuse.com/web-serial) tables and MDN’s experimental/limited-availability labeling, with Mozilla/WebKit positions cited there as negative. Any product promise of “USB fog machine from the browser everywhere” fails without a **local companion** or a **Chromium-only** deployment story.

For **chroma-key compositing**, the seed’s guidance holds: prefer **WebGL 2** (MDN notes Baseline widely available with possible sub-feature variance) over naive Canvas2D per-pixel work. A small library such as **`gl-chromakey`** can accelerate integration but should be vetted for WebGL2 assumptions and maintenance. **AI segmentation** (e.g. MediaPipe Tasks Vision on the web) is a credible differentiator for “no green screen” but adds **latency, binary size, and device variance**—best treated as an optional track with a performance budget.

**Kiosk delivery** combines PWA manifest display modes (`fullscreen` / `standalone`, per MDN) with **OS-level** browser launch (e.g. Chrome `--kiosk`) for true chromeless operation. The SPA alone cannot fully enforce kiosk security; architecture should separate **product UX** from **device hardening**.

## Key Findings

**Stack:** Vite 8.x + TypeScript + React 19.2.x (verify at lock) for the shell; platform APIs for capture/audio/export; WebGL2 for compositing; optional `gl-chromakey` or MediaPipe for specialized paths — see [STACK.md](./STACK.md).

**Architecture:** Default **browser-only** MVP; **`EffectsPort` abstraction** so Web Serial/USB and a **localhost bridge** coexist; promote to native wrapper only for strict enterprise kiosk needs — see [ARCHITECTURE.md](./ARCHITECTURE.md).

**Critical pitfall:** **Hardware APIs are Chromium-skewed**; Safari/Firefox require fallback — see [PITFALLS.md](./PITFALLS.md).

## Implications for Roadmap

Suggested phase structure (ordering follows dependencies and risk reduction):

1. **Foundation: secure deploy + media spine**  
   - Addresses: HTTPS/hosting, `getUserMedia`, preview, permission UX, basic still capture, download export.  
   - Avoids: building compositor on sand (insecure context, unclear device matrix).

2. **Booth flow + audio**  
   - Addresses: countdown state machine, Web Audio or HTML audio cues, review/retake, optional Web Share with fallback ([MDN `share`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)).  
   - Avoids: silent `share()` failures without download path.

3. **Compositing v1 (themed backgrounds)**  
   - Addresses: asset pipeline with **CORS**, WebGL2 chroma key, tuning controls for spill/tolerance.  
   - Avoids: canvas taint `SecurityError` on export ([MDN `toBlob`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)).

4. **PWA / kiosk packaging**  
   - Addresses: manifest `display`, icons, offline assets (where valuable), documented Chrome `--kiosk` / platform notes ([MDN display](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display), [Chrome display_override](https://developer.chrome.com/docs/capabilities/display-override)).  
   - Avoids: assuming installed PWA equals fully offline on all kiosk OSes without validation.

5. **Physical effects (optional)**  
   - Addresses: Web Serial/USB on Chromium + **bridge service** for gaps; protocol design (IDs, timeouts, fail-safe).  
   - Avoids: Safari show-stopper per [caniuse Web Serial](https://caniuse.com/web-serial).

6. **AI / generative track (optional)**  
   - Addresses: MediaPipe segmentation or server-side gen; cost, privacy, and FPS guardrails.  
   - Avoids: shipping ML on the critical path before profiling.

**Phase ordering rationale:** Media + export correctness must precede visual effects; compositing depends on clean asset rules; hardware and AI are expanders that should not block a working booth.

**Research flags for phases:**

| Phase | Flag |
|-------|------|
| Compositing | Shader tuning + venue lighting — may need on-site research |
| Kiosk/PWA | Validate target OS (ChromeOS, Windows, iPad) — anecdotal offline issues **LOW confidence** |
| Hardware | Legal/USB safety review for operator-triggered devices |
| AI | Model licensing, size on wire, WASM performance |

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **MEDIUM** | Vite 8.0.3 verified on npm; React patch from secondary sources — confirm with `npm view` |
| Features | **HIGH** | Grounded in MDN + seed; AI details MEDIUM (official Google AI Edge docs) |
| Architecture | **HIGH** | Patterns follow documented API constraints |
| Pitfalls | **HIGH** for HTTPS/USB/Safari; **LOW–MEDIUM** for niche iOS security mode edge cases |

## Gaps to Address

- **Context7** not wired in this workspace — library APIs should be re-queried during implementation.  
- **Exact React patch** and **gl-chromakey** maintenance status at implementation time.  
- **Target hardware list** (tablet model, GPU, lighting kit) for compositor QA.  
- **Enterprise kiosk** requirements (MDM, single-app mode) if customers need them — OS vendor docs per platform.

## Sources (summary)

Primary: MDN (getUserMedia, Web Audio, WebGL2, WebUSB, Web Serial, Secure Contexts, toBlob, Web Share, manifest `display`), Can I use (WebUSB, Web Serial), Chrome Developers (display_override), Google AI Edge (MediaPipe web segmenter), npm (vite), GitHub/npm (gl-chromakey).
