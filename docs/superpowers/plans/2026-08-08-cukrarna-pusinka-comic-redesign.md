# Cukrárna Pusinka Comic Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comic-style demo homepage (+404) for Cukrárna Pusinka Brno as a static Vercel-ready site, per the approved spec.

**Architecture:** Single static page: `index.html` + `css/styles.css` (comic design system on CSS custom properties) + `js/main.js` (menu, ticker helpers, IntersectionObserver reveals) + self-hosted GSAP/ScrollTrigger for scroll motion. Real brand assets (logo SVG, product photos, fonts) downloaded from the client's live site. No build step.

**Tech Stack:** HTML5, hand-written CSS, vanilla JS, GSAP 3 + ScrollTrigger (self-hosted in `vendor/`), self-hosted woff2 fonts (Agbalumo, Raleway).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-08-cukrarna-pusinka-comic-redesign-design.md` — tokens, palette, section table are normative.
- Ink is `#2B1516`; the ONLY pink is `#EF7E88` (logo pink); page base `#FDF2E7`; cherry `#960016`; pistachio `#A8D8C2`; butter `#F7C948`.
- Fonts: Agbalumo (display) + Raleway (body) ONLY, self-hosted woff2 latin+latin-ext, `font-display:swap`.
- All facts/prices/contacts verbatim from cukrarna-pusinka.cz; NO invented reviews; NO AI-generated imagery.
- Every interactive element: ink outline + hard offset shadow (no blur anywhere).
- Accessibility trio in every animated feature: `prefers-reduced-motion:reduce` kill-switch, `@media (hover:none)` persistent fallback, keyboard `:focus-visible`/`:focus-within` equivalents.
- Internal links that have no demo target → `/404`.
- Czech language, Czech diacritics everywhere (latin-ext subsets mandatory).
- Commit after every task with a conventional message.

---

### Task 1: Scaffold + brand assets

**Files:**
- Create: `.gitignore`, `css/`, `js/`, `vendor/`, `fonts/`, `images/` dirs
- Create: `images/logo-pusinka.svg`, product/story photos (webp), `fonts/*.woff2`, `vendor/gsap.min.js`, `vendor/ScrollTrigger.min.js`

**Interfaces:**
- Produces: asset filenames used by all later tasks — `images/logo-pusinka.svg`, `images/cake-cokoladovy.webp`, `images/cake-jahudka.webp`, `images/cake-skluzavka.webp`, `images/cake-makronky.webp`, `images/cake-joggi.webp`, `images/cake-pohadka.webp`, `images/cake-beze.webp`, `images/story-1.webp`, `images/story-2.webp`, `images/promo-svatby.webp`, `images/promo-firmy.webp`, `fonts/agbalumo-latin-ext.woff2` (+latin), `fonts/raleway-*-latin-ext.woff2` (400/700 + latin)

- [ ] **Step 1:** Write `.gitignore` (`node_modules/`, `.vercel/`, `*.log`).
- [ ] **Step 2:** Scrape live homepage HTML for all `data-src`/`data-srcset` webp URLs; download logo SVG, the 7 bestseller product photos, 2 story photos, 2 promo photos into `images/` with the names above (curl, sequential, polite).
- [ ] **Step 3:** Download fonts from `https://www.cukrarna-pusinka.cz/wp-content/themes/propagon/fonts/`: `agbalumo-v6-latin_latin-ext-regular.woff2`, `raleway-v37-latin_latin-ext-regular.woff2`, `raleway-v37-latin_latin-ext-700.woff2` (+500 if present).
- [ ] **Step 4:** Download GSAP: `https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js` and `.../dist/ScrollTrigger.min.js` into `vendor/`.
- [ ] **Step 5:** Verify: `ls` shows every file, each image > 5 kB, fonts > 10 kB, gsap.min.js > 50 kB. Open one image to confirm it is a real photo.
- [ ] **Step 6:** Commit `chore: scaffold project and pull brand assets`.

### Task 2: Real reviews harvest

**Files:**
- Create: `docs/superpowers/notes/reviews.md` (working note, not shipped)

**Interfaces:**
- Produces: 3 short REAL review quotes + first names + rating, copied verbatim from `https://www.cukrarna-pusinka.cz/recenze/` (or Google reviews shown there). Used by Task 7.

- [ ] **Step 1:** Fetch `/recenze/`, extract 3 short positive quotes (≤ 200 chars each) + reviewer first name.
- [ ] **Step 2:** If the page yields no verbatim quotes, fallback rule: reviews section shows ONLY the aggregate rating badge (4,2★ · 321 recenzí) and category chips, no quote bubbles. Record the decision in the note.
- [ ] **Step 3:** Commit `docs: capture real review quotes for reviews section`.

### Task 3: Design system CSS + page skeleton + header/ticker/mobile menu

**Files:**
- Create: `index.html` (skeleton: `<head>` with meta/OG/fonts preload, header, ticker, empty `<main>` section stubs with ids `#uvod #tradice #bestsellery #na-pockani #sluzby #recenze #kontakt`, footer, FAB)
- Create: `css/styles.css` (tokens through component primitives)
- Create: `js/main.js` (mobile menu, header `.scrolled`, ticker duplication)

**Interfaces:**
- Produces CSS primitives every later task uses verbatim:
  - tokens `:root{--ink:#2B1516; --ol:3px solid var(--ink); --shadow:6px 6px 0 var(--ink); --shadow-sm:4px 4px 0 var(--ink); --pink:#EF7E88; --pink-light:#FFE3EA; --cream:#FDF2E7; --cherry:#960016; --pistachio:#A8D8C2; --butter:#F7C948; --agbalumo:'Agbalumo',cursive; --raleway:'Raleway',sans-serif;}`
  - `.btn` / `.btn--cherry` / `.btn--cream` — press-into-shadow: `hover{transform:translate(3px,3px);box-shadow:3px 3px 0 var(--ink)}` `active{transform:translate(6px,6px);box-shadow:none}`
  - `.chip` (pill, r=999px, ink border, shadow-sm), `.badge-circle`, `.sticker`, `.plate` (rotated price)
  - `.polaroid` (with `::before` butter tape), `.bubble` (with `::after` tail: 26px square, matching bg, ink border-right+bottom, `rotate(45deg) skew(8deg,8deg)`)
  - `.divider-cream` scalloped SVG wave (inline SVG, path `M0 26 Q 25 0 50 26 T 100 26 V 0 H 0 Z` repeated, fill = next section color)
  - halftone utility `.dots` (`background-image:radial-gradient(rgba(43,21,22,.07) 1.6px,transparent 1.6px);background-size:26px 26px`)
  - grain: `body::after` fixed feTurbulence data-URI SVG, opacity .05, z-index 2000, pointer-events none
  - `.rev` reveal contract: `opacity:0; transform:translateY(34px) rotate(var(--r,0deg))` → `.in` transitions in with `transition-delay:var(--d,0s)`
- Produces JS: `initMenu()`, `initHeaderShadow()` — plain functions called at bottom of `main.js`.

- [ ] **Step 1:** `@font-face` for Agbalumo + Raleway (400/700), latin-ext, swap. Base: body cream bg, ink text, Raleway; h1–h3 Agbalumo uppercase lh 1.02.
- [ ] **Step 2:** Implement all primitives above in `styles.css`, with a temporary `kitchen.html`-style test block at the end of `index.html` `<main>` (one of each primitive) to eyeball.
- [ ] **Step 3:** Header: cream, `border-bottom:var(--ol)`, logo img 150px w/ hover `rotate(-8deg)` springy `cubic-bezier(.34,1.56,.64,1)`; nav links Raleway 700 uppercase with scaleX underline hover; phone chip `+420 601 587 297` with ring-keyframe SVG icon; cherry CTA „Dort na míru" → `/404`. Sticky; `.scrolled` (scrollY>10) adds `--shadow-sm`.
- [ ] **Step 4:** Ticker: ink bg strip under header, duplicated span marquee `translateX(-50%)` 26s linear infinite, hover pause. Text: „NOVINKY NA LÉTO: Matcha Latté ✦ domácí limonády s novou chutí ✦ Panna Cotta – malina a borůvka ✦" (duplicated).
- [ ] **Step 5:** Mobile menu: burger (ink, 44×44 target) → fullscreen pink overlay, `clip-path:circle(0 at calc(100% - 3rem) 3rem)` → `circle(150%)` .5s; giant Agbalumo links alternately rotated ±2°; Esc closes, focus trapped, `aria-expanded`/`aria-controls`, body scroll-lock.
- [ ] **Step 6:** Verify in browser (preview_start): header/ticker/menu on desktop 1280 and mobile 375 — screenshots. Console: 0 errors. Remove nothing yet (kitchen block stays until Task 8).
- [ ] **Step 7:** Commit `feat: design system, header, ticker, mobile menu`.

### Task 4: Hero

**Files:**
- Modify: `index.html` (`#uvod`), `css/styles.css`, `js/main.js`

**Interfaces:**
- Consumes: `.btn--cherry`, `.btn--cream`, `.chip`, `.sticker`, `.badge-circle`, `.dots`
- Produces: `#uvod.hero` markup pattern; GSAP is NOT yet loaded (Task 8 wires motion) — hero ships with CSS-only spin/bob.

- [ ] **Step 1:** Pink `.dots` section. Left column: chip „Brno-Královo Pole • od roku 1992"; H1 `POCTIVÁ BRNĚNSKÁ<br><span class="outline-word">CUKRAŘINA</span>` — outline-word: cream fill, `-webkit-text-stroke:2px var(--ink)`, `text-shadow:4px 4px 0 var(--ink)`, `display:inline-block; transform:rotate(-1.2deg)`; sub-paragraph verbatim: „Od roku 1992. Pečeme z pravého másla, živočišné šlehačky a s láskou k řemeslu. Objednejte si dort na oslavu, nebo se zastavte na kávu v Králově Poli."; CTAs „VYBRAT DORT" (cherry) + „DORT JEŠTĚ DNES" (cream) → `/404`; trust chip „★ 4,2 · 321 recenzí na Google".
- [ ] **Step 2:** Right column: `.hero-cake` — circular photo (`images/cake-beze.webp`), `border:7px solid var(--ink)`, inset cream ring `box-shadow: inset 0 0 0 6px var(--cream), 10px 12px 0 rgba(43,21,22,.28)`, `animation:spin 22s linear infinite` on the img, hover `animation-duration:6s`. Stickers: butter `.badge-circle` „Z PRAVÉHO MÁSLA!" rotate(9deg) + cherry pill „DENNĚ ČERSTVÉ" rotate(-7deg), both `animation:bob 5s ease-in-out infinite` (second reverse). 2–3 ✦ sparks + hand-drawn SVG cherry doodle, hidden below 768px.
- [ ] **Step 3:** Keyframes `spin`, `bob`; reduced-motion kill.
- [ ] **Step 4:** Browser verify desktop+mobile screenshots: headline wraps ≤ 3 lines at 1280, CTAs above fold at 375×812.
- [ ] **Step 5:** Commit `feat: comic hero with spinning cake and stickers`.

### Task 5: Story/Tradice + Bestsellery

**Files:**
- Modify: `index.html` (`#tradice`, `#bestsellery`), `css/styles.css`

**Interfaces:**
- Consumes: `.polaroid`, `.chip`, `.plate`, `.bubble`, `.divider-cream`, `.btn--cream`
- Produces: `.card-cake` component (cream card, circular photo protruding via `margin-top:-72px`, Agbalumo name, Raleway desc, rotated `.plate` price, BESTSELLER sticker)

- [ ] **Step 1:** `#tradice` (cream): left = two overlapping `.polaroid`s (story photos, rotations -4°/+3°, hover straighten), captions „Naše dílna v Králově Poli" / „Poctivé řemeslo od roku 1992". Right: h2 „TRADIČNÍ PŘÍSTUP", copy (shortened, facts kept: čerstvá vejce z lokálních chovů, živočišná smetana, 30+ let, žádné polotovary), 4 chips: „100% POCTIVÉ SUROVINY" „VLASTNÍ VÝROBA V BRNĚ" „ZLATÁ CHUŤ JIŽNÍ MORAVY" „300KG DORT PRO VAŇKOVKU".
- [ ] **Step 2:** Scallop divider cream→cherry. `#bestsellery` (cherry bg): h2 „NEJPRODÁVANĚJŠÍ" cream/outline style + sub „Bestsellery, které mizí z vitríny první."; grid of 7 `.card-cake` (auto-fit minmax(240px,1fr)): Čokoládový dort od 570 Kč · Jahůdka dort od 590 Kč · Skluzavka 930 Kč · Makronky 55 Kč (+chip „BEZ MOUKY") · Joggi dort od 590 Kč · Pohádka dort od 550 Kč · Bezé dort 990 Kč. Per-card `--tilt` rotations; hover lift -8px + photo rotate 14° scale, back-out easing. Pohádka card: hidden `.bubble` „Přes léto na dotaz! ☎ 601 587 297" scales in on hover (persistent under `hover:none`). All „ZOBRAZIT" buttons → `/404`. CTA row: cream btn „VŠECHNY PRODUKTY" → `/404`.
- [ ] **Step 3:** Browser verify: divider seam pixel-clean at 3 widths (375/768/1280), cards wrap 1/2/3-4 columns. Screenshots.
- [ ] **Step 4:** Commit `feat: story section and bestseller cake cards`.

### Task 6: Na počkání + Svatby/Firmy promos

**Files:**
- Modify: `index.html` (`#na-pockani`, `#sluzby`), `css/styles.css`

**Interfaces:**
- Consumes: `.divider-*`, `.chip`, `.btn--cherry`, `.badge-circle`
- Produces: `.pbanner` (promo card with oversized half-clipped spinning photo disc, 120s)

- [ ] **Step 1:** Scallop cherry→cream. `#na-pockani`: big cream banner card (ink border, shadow): h2 „ZAPOMNĚLI JSTE? ZACHRÁNÍME VÁS." + copy (vitrína v Králově Poli, dozdobíme na místě) + 3 step chips: „① DO 15 MINUT" „② AŽ 20 DRUHŮ DENNĚ" „③ DOZDOBÍME NA MÍSTĚ" + courier chips „BOLT · FOODORA · WOLT" + cherry CTA „DORTY NA POČKÁNÍ" → `/404`.
- [ ] **Step 2:** `#sluzby`: two `.pbanner` cards side by side — pistachio „SVATEBNÍ DORTY & SWEET BARY" („Dokonalá sladká tečka pro váš velký den.") photo `promo-svatby.webp`; pink „CATERING PRO VAŠI FIRMU" („Zvládli jsme i rekordní 300kg dort pro Vaňkovku.") photo `promo-firmy.webp`. Half-clipped 19rem discs, `spin 120s`, CTAs → `/404`.
- [ ] **Step 3:** Browser verify + screenshots (discs clip correctly, no horizontal scroll at 375).
- [ ] **Step 4:** Commit `feat: express cakes banner and weddings/corporate promos`.

### Task 7: Recenze + Kontakt + Footer + FAB

**Files:**
- Modify: `index.html` (`#recenze`, `#kontakt`, footer, FAB), `css/styles.css`, `js/main.js`

**Interfaces:**
- Consumes: `.bubble`, `.badge-circle`, `.chip`; reviews data from Task 2 note
- Produces: `initToday()` (highlights today's opening row), `initFab()` (IntersectionObserver on `#uvod`)

- [ ] **Step 1:** `#recenze` (pistachio, ink top border): h2 „ŘÍKAJÍ O NÁS"; rotated badge-circle „GOOGLE 4,2★ · 321 RECENZÍ"; 3 `.bubble` quotes from Task 2 (real only; else aggregate-only fallback), each with cherry ★ row + first name, per-bubble `--r` rotation.
- [ ] **Step 2:** `#kontakt` (ink bg, cream text): grid 2 cols. Left: h2 „ZASTAVTE SE V KRÁLOVĚ POLI"; opening hours list PO–NE 9.00–18.00 as 7 rows w/ `border-bottom:2px dashed rgba(253,242,231,.25)`, JS `initToday()` adds butter „DNES" chip to current day. Right: address rows w/ SVG icons (Palackého tř. 1379/97, 612 00 Brno-Královo Pole · „2 parkovací místa, Riegrova 1 (vlevo)"), big butter phone link `tel:+420601587297`, mail `objednavky@cukrarna-pusinka.cz`, Google Maps iframe (`https://maps.google.com/maps?q=Palack%C3%A9ho%20t%C5%99.%201379%2F97%20Brno&output=embed`) in ink-border frame with static fallback text behind it.
- [ ] **Step 3:** Footer (ink, `border-top:2px dashed rgba(253,242,231,.25)`): logo (cream-tinted or on cream chip), „© 2026 Cukrárna Pusinka", „Demo redesign — není oficiální web". FAB: fixed bottom-right, cherry, „🍰 Dort ještě dnes" → `/404`, mobile only, `.show` when `#uvod` leaves viewport.
- [ ] **Step 4:** Delete the kitchen test block from `index.html`.
- [ ] **Step 5:** Browser verify + screenshots; check `initToday()` highlights correct row.
- [ ] **Step 6:** Commit `feat: reviews, contact, footer, mobile FAB`.

### Task 8: Motion pass (GSAP + ScrollTrigger)

**Files:**
- Modify: `index.html` (script tags before `</body>`: `vendor/gsap.min.js`, `vendor/ScrollTrigger.min.js`, `js/main.js` last), `js/main.js`, `css/styles.css`

**Interfaces:**
- Consumes: `.rev` contract from Task 3; section ids.
- Produces: `initMotion()` — all GSAP code lives in this one function, guarded by `if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;` and `if (!window.gsap) return;`.

- [ ] **Step 1:** Tag reveal elements: every section head, card, chip-row, polaroid, bubble gets `class="rev"` + inline `style="--d:.08s;--r:-2deg"` staggers.
- [ ] **Step 2:** `initMotion()`: `gsap.registerPlugin(ScrollTrigger)`; batch reveals via `ScrollTrigger.batch('.rev', {onEnter: b => b.forEach((el,i)=>el.classList.add('in'))})` (CSS does the transition — GSAP only orchestrates); hero parallax: cake disc `y:-40`, stickers `y:-70`, doodles `y:-100` scrubbed over hero; bestseller grid: slight `y` drift per column; scallop dividers: subtle `xPercent` drift scrub. NO pinning (page is short), no scroll-jacking.
- [ ] **Step 3:** Fallback: `.no-js`/`no-gsap` path — plain IntersectionObserver adds `.in` (already the Task 3 contract), so page works with vendor scripts blocked.
- [ ] **Step 4:** Browser verify: scroll through, console 0 errors; toggle reduced-motion emulation → everything visible instantly, no infinite animations.
- [ ] **Step 5:** Commit `feat: scroll motion pass with GSAP ScrollTrigger`.

### Task 9: 404 page

**Files:**
- Create: `404.html` (self-contained: reuses `css/styles.css`)

- [ ] **Step 1:** Pink `.dots` full-viewport center: big Agbalumo „JEJDA!", outline-word „TAHLE STRÁNKA SE JEŠTĚ PEČE.", spinning cake disc (reuse hero pattern, `cake-cokoladovy.webp`), copy „Tohle je demo — funguje zatím jen úvodní stránka.", cherry btn „ZPĚT DO CUKRÁRNY" → `/`. Header-less, minimal.
- [ ] **Step 2:** Verify `/404.html` in browser + screenshot; check every internal link on index points to `/404` (grep `href` audit — external links: maps, tel, mailto allowed).
- [ ] **Step 3:** Commit `feat: comic 404 demo page`.

### Task 10: Favicon + OG assets

**Files:**
- Create: `images/favicon.svg` (+ png fallbacks), `images/og.png`; modify `index.html`/`404.html` `<head>`

- [ ] **Step 1:** Use web-asset-generator skill: favicon from logo „P"/pusinka mark on pink, OG image 1200×630 (logo + „Poctivá brněnská cukrařina" on cream comic bg with ink border) — composed from real assets, no AI imagery.
- [ ] **Step 2:** Wire `<link rel="icon">` + OG/Twitter meta (title „Cukrárna Pusinka Brno — poctivá cukrařina od roku 1992", desc, og:image), verify with browser tab icon.
- [ ] **Step 3:** Commit `feat: favicon and social meta assets`.

### Task 11: Audits + polish + final verification

**Files:**
- Modify: any (fixes only)

- [ ] **Step 1:** Run web-design-guidelines review on `index.html`+`css/styles.css`+`js/main.js`; fix findings.
- [ ] **Step 2:** Run design:accessibility-review (WCAG 2.1 AA): contrast of every text/bg pair (esp. pink bg + ink, cherry btn + cream text, butter on ink), touch targets ≥ 44px, focus visible everywhere, alt texts, landmark roles, heading order. Fix findings.
- [ ] **Step 3:** impeccable live pass in browser: spacing rhythm, alignment, rotation balance (not more than ~1 rotated element per viewport cluster), shadow consistency; iterate until it looks hand-placed, not templated.
- [ ] **Step 4:** verification-before-completion: screenshots desktop 1280 / tablet 768 / mobile 375 full page; console 0 errors/warnings; no horizontal scroll at any width; Lighthouse-style sanity (images sized, fonts swap, lazy loading below fold).
- [ ] **Step 5:** Commit `polish: audit fixes and final visual pass`.
