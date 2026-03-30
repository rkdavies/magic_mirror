# Architecture Patterns

**Domain:** Web-based photo booth / interactive capture kiosk  
**Researched:** 2026-03-30

## Deployment models (choose explicitly)

### A. Browser-only (static + optional lightweight API)

**What:** SPA hosted on HTTPS; all capture, audio, and compositing in the tab; optional backend only for assets, auth, or AI.

**Best when:** Green screen quality is acceptable, hardware effects are out of scope, and targets are **Chromium-based kiosks** and/or **mobile Safari** in “save/share only” mode.

**Limits:** No WebUSB/Web Serial on Safari/Firefox ([caniuse Web Serial](https://caniuse.com/web-serial), [WebUSB](https://caniuse.com/webusb)); generative/expensive AI usually needs server.

### B. Browser + local companion (“bridge”)

**What:** Same SPA; a small **localhost** service owns serial/USB/HID and exposes a narrow API (e.g. WebSocket: `{ "cmd": "fog", "ms": 800 }`).

**Best when:** Physical effects matter, or you must support **Safari/iOS** alongside Chrome without dropping effects entirely.

**Limits:** Install/signing story for the companion; firewall/OS prompts; two release artifacts (web + native).

### C. Full native wrapper (Electron, Tauri, WebView2, Capacitor)

**What:** Embedded webview loads the booth UI; native layer handles devices, autostart, and sometimes printing.

**Best when:** Single-vendor deploy, strict kiosk lockdown, or deep OS integration (single-app mode, USB permissions).

**Limits:** Build/sign per platform; larger operational surface than static hosting.

**Recommendation for Scribe roadmap:** Start with **A** for core capture/composite/export; design **B** behind a `HardwarePort` interface so effects can land without rewriting the UI. Promote to **C** only if a customer profile demands OS-level kiosk management.

## Recommended logical architecture (browser-centric)

```
┌─────────────────────────────────────────────────────────────┐
│                     Booth SPA (Vite + TS)                  │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Media layer  │ Composite    │ Export       │ Effects        │
│ getUserMedia │ WebGL2 /     │ toBlob,      │ Web Serial /   │
│ Web Audio    │ shader pass  │ share, print │ WebUSB OR      │
│              │              │ fallback     │ bridge WS      │
└──────────────┴──────────────┴──────────────┴────────────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
   Camera/Mic     GPU (canvas)    Files / OS      USB / Serial /
                                   share sheet      localhost
```

### Component boundaries

| Component | Responsibility | Communicates with |
|-----------|----------------|-------------------|
| **Session / state** | Step machine, selected theme, timers | All UI panels |
| **Media service** | Acquire/release `MediaStream`, device change | Preview view, capture pipeline |
| **Audio service** | Cue scheduling, volume, mute | Session |
| **Compositor** | Video frame → keyed + background + overlays | Export service (read pixels from same canvas or double-buffer) |
| **Export service** | `toBlob`, filenames, `navigator.share`, download | Session, storage (optional) |
| **Effects port** (interface) | Abstract over Web Serial/USB vs bridge | Hardware module |
| **Asset loader** | Themes, images, fonts | Compositor; must preserve canvas origin-clean rules |
| **Optional API client** | AI or signed theme fetch | Backend |

## Data flow: capture → composite → export/share

1. **Acquire stream:** `getUserMedia({ video: …, audio: optional })` → attach to `<video>` for preview.  
2. **Run loop:** `requestAnimationFrame` (or worker + `OffscreenCanvas` if you move GL later) reads video into compositor.  
3. **Composite:** Draw background (texture) → draw keyed video (shader replaces chroma) → draw foreground stickers/text.  
4. **Capture moment:** Copy current frame to export buffer **or** freeze last N frames policy (anti-blink — product choice).  
5. **Export:** `canvas.toBlob(type, quality)` → `File` → `navigator.share({ files })` if allowed, else `<a download>`.  

**Critical constraint:** Any `drawImage` from cross-origin media without CORS taints the canvas — [MDN `toBlob` SecurityError](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob).

## Patterns to follow

### Pattern: Capability detection at runtime

Gate `navigator.usb`, `navigator.serial`, `navigator.share` behind presence checks; surface “unsupported” UX rather than throwing.

### Pattern: User activation for hardware and share

Web Serial/USB typically need **gesture**-gated permission flows; Web Share requires [transient activation](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share). Design UI so the same tap connects port and arms share.

### Pattern: Single compositor owner

One module owns the WebGL context and texture uploads; avoid multiple canvases fighting for GPU memory on low-end tablets.

## Anti-patterns to avoid

| Anti-pattern | Consequence | Instead |
|--------------|-------------|---------|
| Capturing in an iframe without Permissions Policy | `getUserMedia` never prompts — [MDN](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) | Top-level or delegated policy |
| Loading theme images from random CDNs without CORS | Broken export | Same-origin proxy or proper `Access-Control-Allow-Origin` |
| Blocking main thread with segmentation | Missed countdown sync | Throttle AI path or run in worker if feasible |

## Scalability considerations

| Concern | Single kiosk | Many venues | Many concurrent users (web traffic) |
|---------|--------------|-------------|-------------------------------------|
| GPU memory | One context, few textures | Same | N/A unless server-render |
| Asset updates | Manual refresh | CDN versioning + cache bust | CDN + auth for premium themes |
| AI / gen | Optional local or API | Per-venue API keys via BFF | Queueing, rate limits, caching |

## Sources

- [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)  
- [MDN: Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)  
- [MDN: HTMLCanvasElement.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)  
- [MDN: WebUSB](https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API), [Web Serial](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API)  
- [Can I use: WebUSB, Web Serial](https://caniuse.com/)  
- [Chrome: display_override](https://developer.chrome.com/docs/capabilities/display-override)  
- [SEED-001](../seeds/SEED-001-photo-booth-capabilities.md)  
