# Feature Landscape

**Domain:** Web-based photo booth / interactive capture kiosk  
**Researched:** 2026-03-30

## Table Stakes

Features users (and event operators) expect. Missing any of these makes the product feel unfinished for a “booth.”

| Feature | Why expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Live camera preview** | Core of a booth | Low–Med | `getUserMedia` + `<video>`; handle aspect ratio and mirroring UX. |
| **Explicit permission + error UX** | Camera failures are common | Med | Denied, in use, HTTPS missing, iframe policy — [MDN lists `NotAllowedError`, `NotFoundError`, etc.](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) |
| **Countdown or “ready” flow** | Prevents blink/missed poses | Low | Pair with audio; respect mute / reduced motion preferences where applicable. |
| **Still capture (photo)** | Primary output | Low–Med | Grab frame from video to canvas or use `ImageCapture` where supported (optional enhancement). |
| **Review / retake** | Social comfort + operator throughput | Med | Simple state machine: idle → countdown → review → export or retake. |
| **Export to file** | Printing / upload | Low | `canvas.toBlob` → download link; [MDN: toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob). |
| **HTTPS / secure context** | Camera simply will not work on modern browsers otherwise | Ops | [MDN secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts); local dev via `localhost` / `file://` exceptions per spec. |
| **Readable UI at arm’s length** | Kiosk viewing distance | Low | Large type, high contrast, minimal steps. |

## Differentiators

Not strictly expected, but strong when executed well.

| Feature | Value proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **WebGL chroma key + themed layers** | “Event grade” look | High | Lighting-sensitive; shader tuning is the moat. |
| **Sound design** (layered cues, spatial or simple stereo) | Emotional beat of the experience | Med | Web Audio scheduling vs. simple `<audio>`. |
| **Theme packs** (backgrounds, overlays, brand) | Repeatable revenue / B2B | Med | Asset pipeline + CDN; watch **CORS** so canvas stays origin-clean. |
| **Optional physical effects sync** | Wow factor at installs | High | Browser path: WebUSB/Web Serial (Chromium); else local bridge. |
| **AI segmentation / virtual background** | No green screen | High | e.g. [MediaPipe Image Segmenter (web)](https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter/web_js) — perf, model load, privacy copy. |
| **Generative backgrounds** | Novelty | High | Usually needs backend, cost controls, safety policy. |
| **PWA / installed mode** | Cleaner shell on tablets | Med | Manifest `fullscreen` / `standalone` — [MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display). |
| **Web Share of finished image** | Mobile-first handoff | Med | [MDN: `navigator.share`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) — feature-detect + fallback. |
| **Operator mode** (PIN, queue, print bridge) | Venue workflows | Med–High | Often overlaps with native print drivers or companion app. |

## Anti-Features

Things that look tempting but commonly hurt this product class.

| Anti-feature | Why avoid | What to do instead |
|--------------|-----------|-------------------|
| **Assuming WebUSB/Web Serial everywhere** | **Safari (incl. iOS) and Firefox do not support them** ([caniuse Web Serial](https://caniuse.com/web-serial), [WebUSB](https://caniuse.com/webusb); Mozilla “harmful”, WebKit “opposed” linked there) | Feature-detect; ship **local bridge** or manual trigger for non-Chromium. |
| **Pixel-loop chroma key on CPU** | Jank at HD | WebGL2 pass; offload to GPU. |
| **Cross-origin background images without CORS** | `SecurityError` on export — [MDN `toBlob` SecurityError](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob) | Host assets same-origin or with proper CORS headers. |
| **Silent failure on permissions** | Users blame hardware | Dedicated screens: “Allow camera”, “Use HTTPS”, “Another app is using the camera.” |
| **Over-automation of share** | `share()` requires user activation — [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) | Clear “Share” / “Save” buttons. |
| **Hard dependency on one browser** without positioning | Locks out iPhone guests or certain venues | Label “best in Chrome/Edge” or support a reduced mode. |

## Feature Dependencies

```
Secure hosting (HTTPS) + manifest (optional PWA)
    → getUserMedia (preview + capture)
        → Canvas / WebGL composite pipeline
            → toBlob / share / print bridge
Audio cues ←→ countdown state machine (parallel, not blocking capture)

Optional: WebUSB / Web Serial ──► physical effects (Chromium desktop/android subset)
    └── falls back to: local companion WebSocket

Optional: AI segmentation ──► replaces or augments chroma key (needs perf budget + model hosting)
```

## MVP Recommendation

Prioritize for a credible first milestone:

1. **HTTPS deploy + getUserMedia** with solid error UX  
2. **Countdown + shutter + review/retake**  
3. **Still export** (download); optional Web Share where supported  
4. **One fixed background** (same-origin asset) via **simple composite** (even 2D) as scaffolding before WebGL polish  

Defer:

- **Physical effects** until core loop and deploy story are stable  
- **AI / generative** until segmentation latency and cost are modeled  
- **Exotic kiosk OS integrations** until target hardware is chosen  

## Sources

- [SEED-001-photo-booth-capabilities.md](../seeds/SEED-001-photo-booth-capabilities.md) (project seed)  
- [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)  
- [MDN: toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)  
- [MDN: Web Share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)  
- [Can I use: Web Serial, WebUSB](https://caniuse.com/)  
- [Google AI Edge: MediaPipe Image Segmenter (web)](https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter/web_js)  
