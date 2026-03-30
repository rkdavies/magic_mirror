# Technology Stack

**Project:** Scribe (provisional)  
**Domain:** Web-based photo booth / interactive capture kiosk  
**Researched:** 2026-03-30

## Recommended Stack

### Core application shell

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Vite** | **8.0.x** (npm shows 8.0.3 as of 2026-03-26) | Dev server, production build, native ESM | Fast HMR, small config, static hosting friendly for kiosk deploys. Verified via [npm `vite` package page](https://www.npmjs.com/package/vite). |
| **TypeScript** | **5.x** (pin at init) | Type safety across media/hardware code | Reduces mistakes in async permission flows and WebGL resource lifecycle. |
| **React** | **19.2.x** (verify `npm view react version` at lock time) | UI state: countdown, themes, error surfaces | Ecosystem depth for kiosk UIs; optional alternatives below. **Exact patch:** MEDIUM confidence — npm fetch timed out; secondary sources cite 19.2.x family. |

**Opinionated default:** Vite + React + TypeScript. **When to prefer vanilla:** a single full-screen canvas with almost no DOM chrome; still use Vite for build and TS for safety.

### Capture, audio, and export (platform APIs — no mandatory libs)

| Layer | Technology | Purpose | Notes |
|-------|------------|---------|-------|
| Camera | `navigator.mediaDevices.getUserMedia()` | Live preview + capture source | [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) — secure context, permissions, Baseline widely available. |
| Audio cues | **Web Audio API** (`AudioContext`, buffers) or **HTML `<audio>`** | Countdown beeps, shutter, voiceover | Web Audio for precise scheduling; HTML audio for simplicity. [MDN: Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API). |
| Still export | `HTMLCanvasElement.toBlob()` / `toDataURL()` | PNG/JPEG/WebP output | [MDN: toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob) — Baseline widely available; mind **origin-clean** / `SecurityError` if compositing cross-origin assets without CORS. |
| Share / save | **Web Share API** (`navigator.share`) + download fallback | Mobile-friendly share | [MDN: share()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) — secure context, not Baseline; requires user activation and `canShare` checks. |

### Compositing (chroma key / backgrounds)

| Approach | Library / API | Purpose | Why / when |
|----------|---------------|---------|------------|
| **Primary (live keying)** | **Custom fragment shader on WebGL 2** or thin wrapper | Green/blue screen, spill suppression, performance | Full control; matches seed guidance. [MDN: WebGL2RenderingContext](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext) — Baseline widely available (MDN notes some sub-features may vary). |
| **Accelerated integration** | **`gl-chromakey`** (npm; community reports **2.x**, WebGL2) | Drop-in GPU chroma key from `HTMLVideoElement` | Fewer lines than raw GL; **verify** bundle size, license, and WebGL2 requirement against target hardware. [GitHub: bhj/gl-chromakey](https://github.com/bhj/gl-chromakey), [npm registry](https://www.npmjs.com/package/gl-chromakey). |
| **Heavier 3D** | **Three.js** / **Babylon.js** | Themed 3D scenes + video textures | Use if the product is scene-driven; otherwise overhead for a flat booth. Ecosystem moves fast — pin major version at implementation. |
| **AI / segmentation (optional)** | **MediaPipe Tasks Vision** (`@mediapipe/tasks-vision`) | Person segmentation / virtual background without physical green screen | Runs client-side with WASM/models; higher CPU/GPU cost and integration complexity. [Google AI Edge: Image Segmenter (web)](https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter/web_js). |

### Kiosk / PWA shell

| Technology | Purpose | Why |
|------------|---------|-----|
| **Web App Manifest** (`display`: `fullscreen` or `standalone`) | Installed / minimal-chrome experience | [MDN: display](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display); fallback chain documented on MDN. |
| **`display_override`** (Chrome) | Finer control before legacy `display` fallback | [Chrome: display-override](https://developer.chrome.com/docs/capabilities/display-override) — use for edge cases; MDN notes limited Baseline for manifest display overall. |
| **Service Worker** (optional) | Offline assets, faster repeat visits | Valuable for fixed installs; test against real kiosk offline behavior (known ChromeOS+kiosk reports of online-only behavior — **LOW confidence** without repro; treat as risk). |
| **OS launch** | Chrome/Edge **`--kiosk URL`** (or platform kiosk suites) | True fullscreen, no browser UI | Documented in vendor/community guides; not a W3C spec — validate on target OS. |

### Optional backend (themes, AI, analytics)

| Component | Options | When |
|-----------|---------|------|
| **Static asset CDN** | Any CDN + versioned theme packs | Default for themed backgrounds/stickers; keep CORS headers correct for canvas **taint**. |
| **Signed URL / BFF** | Small Node/Deno/Go service | License keys, rate limits, hiding API keys for third-party AI. |
| **AI background gen** | Partner APIs (image gen / segmentation) | Only if product promises generative themes; budget for latency, cost, and moderation. |

### Hardware bridge (when WebUSB / Web Serial are insufficient)

| Component | Purpose |
|-----------|---------|
| **Local companion** (Node, Python, Go) + **WebSocket** or **HTTP** on `localhost` | Owns serial/USB where the browser cannot; exposes `effectOn` / `effectOff` to the page. Aligns with SEED-001 plan B. |

## Alternatives Considered

| Category | Recommended | Alternative | Why not |
|----------|-------------|-------------|---------|
| UI framework | React + Vite | Vue / Svelte / vanilla | All viable; React chosen for hiring/docs depth — not a technical requirement. |
| Compositing | WebGL2 shader | Pure **Canvas 2D** per-pixel | Simpler but poor FPS at HD; seed explicitly warns against naive JS loops for live keying. |
| Compositing | Custom GL | **Babylon** / **Three** | Justified for 3D booths, not for flat overlay compositing only. |
| Hardware | In-browser WebUSB/Web Serial | Local daemon | **Required** for Safari/iOS and Firefox users; see PITFALLS and ARCHITECTURE. |

## Installation (illustrative — pin versions at project init)

```bash
npm create vite@latest scribe -- --template react-ts
cd scribe
npm install
# Optional compositing helper (evaluate need first):
# npm install gl-chromakey
```

## Sources

- [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- [MDN: Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [MDN: HTMLCanvasElement.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
- [MDN: WebGL2RenderingContext](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext)
- [MDN: Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)
- [MDN: WebUSB API](https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API)
- [MDN: Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API)
- [MDN: Navigator.share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)
- [MDN: Manifest `display`](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display)
- [Can I use: Web Serial](https://caniuse.com/web-serial), [WebUSB](https://caniuse.com/webusb)
- [Chrome: display_override](https://developer.chrome.com/docs/capabilities/display-override)
- [npm: vite](https://www.npmjs.com/package/vite)
- [Google AI Edge: MediaPipe Image Segmenter (web)](https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter/web_js)
- [GitHub: gl-chromakey](https://github.com/bhj/gl-chromakey)

**Context7:** Not available in this workspace’s MCP configuration; library APIs were not resolved via Context7 for this research pass.
