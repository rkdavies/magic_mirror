---
id: SEED-006
status: dormant
planted: 2026-03-30
planted_during: ad-hoc session (no STATE.md in repo)
trigger_when: Milestone scope includes post-generation fulfillment—physical print from the booth, and/or email capture offering a free digital copy in exchange for joining a digital community (newsletter, membership, CRM list)
scope: medium
---

# SEED-006: Print after generation + free digital copy for email / community signup

## Why This Matters

After a guest gets a **final image** ([SEED-001](SEED-001-photo-booth-capabilities.md) export path; possibly post [SEED-002](SEED-002-ai-costumes-backgrounds-from-capture.md)/[SEED-004](SEED-004-generated-background-matches-client-theme.md)), the product still owes **delivery**: **print** for the venue experience and **digital** for shareability. Offering a **free digital copy when the user supplies email** builds a **community / marketing list**—but only if **consent copy**, **double opt-in** (where required), **unsubscribe**, and **data retention** are designed intentionally. **Print** is deceptively varied: browser print dialog, **OS printer queue**, **dedicated kiosk printer**, or **cloud print**—each with different reliability and support burden. This seed keeps **print + email growth loop** explicit so they are not bolted on without compliance and UX for “skip,” **wrong email**, and **printer offline**.

## When to Surface

**Trigger:** When a milestone adds **fulfillment** after the composite or generated asset is ready—not only on-device download.

This seed should be presented during `/gsd:new-milestone` when the milestone scope matches any of these conditions:

- **“Print this photo”** (or operator-assisted print) on a **review** screen after generation completes.
- **Email field** with value prop: **free digital copy** + **join digital community** (define: newsletter, Discord invite, member portal, etc.).
- **Backend or ESP integration** (SendGrid, Mailchimp, Customer.io, etc.) or **BFF** that stores consent metadata and triggers **transactional** “here’s your image” email.
- **Privacy policy / terms** updates, **CAN-SPAM**, **GDPR** (if EU), **COPPA** awareness for minors at events.

## Scope Estimate

**Medium** — **Email + secure link or attachment flow** is a standard web problem with **policy** overhead. **Print** can stay **M** (browser `print()` + CSS `@media print`) or become **L** if you integrate **hardware-specific drivers**, **cut sheets**, or **paid per-print** accounting. Split phases if needed: **digital fulfillment first**, **print second**.

## Breadcrumbs

- [.planning/seeds/SEED-001-photo-booth-capabilities.md](SEED-001-photo-booth-capabilities.md) — `toBlob`, Web Share, download path; secure context.
- [.planning/research/FEATURES.md](../research/FEATURES.md) — Web Share + fallback; operator flows.
- [.planning/research/ARCHITECTURE.md](../research/ARCHITECTURE.md) — optional backend, BFF, API keys.

## Notes

- **Clear offer:** Separate **transactional** “here is your file” from **marketing** community emails unless legally combined with explicit consent checkboxes where required.
- **Abuse:** Rate-limit email sends per IP/session; **magic link** or **time-limited signed URL** for downloads instead of huge attachments when possible.
- **Print UX:** High-contrast preview, **2×3 / 4×6** layout templates, **bleed** if venue cares; test **silent print** policies on locked-down kiosks (often needs OS-level config, not SPA-only).
- **No email path:** Always offer **paid or free download on device** or **QR to personal device** so the funnel is not coercive.
