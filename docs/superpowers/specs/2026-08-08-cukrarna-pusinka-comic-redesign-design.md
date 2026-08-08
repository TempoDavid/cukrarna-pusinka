# Cukrárna Pusinka — komiksový redesign homepage (demo)

**Datum:** 2026-08-08 · **Status:** schváleno Davidem · **Rozsah:** demo úvodní stránka + 404, statická, Vercel-ready

## Cíl

Grafický facelift homepage www.cukrarna-pusinka.cz v plném komiksovém stylu (à la Pizza Bolka — pizzabolka-web.vercel.app), přebarvený do cukrárnového světa. Veškerá fakta, ceny a kontakty 1:1 z původního webu; headliny a mikrotexty přepsané do úderného komiksového tónu. Všechny prokliky vedou na komiksovou 404. Zachovat: SVG logo lettering „Pusinka" (#EF7E88) a font Agbalumo.

## Design systém

### Tokeny

```css
--ink:        #2B1516;              /* tmavá čokoláda — všechny obrysy a stíny */
--ol:         3px solid var(--ink);
--shadow:     6px 6px 0 var(--ink);
--shadow-sm:  4px 4px 0 var(--ink);
--pink:       #EF7E88;  /* růžová z loga = hlavní brand barva */
--pink-light: #FFE3EA;  /* světlé plochy, karty */
--cream:      #FDF2E7;  /* vanilkový základ stránky */
--cherry:     #960016;  /* primární tlačítka, akcenty (NE barva všeho textu) */
--pistachio:  #A8D8C2;  /* recenze, kontrastní sekce */
--butter:     #F7C948;  /* samolepky, ceny, páska polaroidů */
```

Sjednocujeme tři rozjeté růžové originálu (#EF7E88 logo / #e0848a theme / #d7a59f overlay) na jedinou: **#EF7E88 z loga**.

### Typografie

- **Agbalumo** (display, weight 400) — všechny h1/h2/h3, uppercase, line-height ~1.02. Self-hosted woff2, latin + latin-ext, font-display:swap.
- **Raleway** (400/500/700) — tělo, labely (uppercase 700 + letter-spacing), tlačítka. Self-hosted woff2, latin-ext.
- Headline recept: zvýrazněné slovo v jiné barvě s `-webkit-text-stroke: 2px var(--ink)` + `text-shadow: 4px 4px 0 var(--ink)` + rotate(-1.2deg).
- Logo: `logo-pusinka.svg` z jejich webu, beze změn.

### Komiksové techniky (kompletní DNA z Bolky)

1. Ink obrys `--ol` + tvrdý stín `--shadow`/`--shadow-sm` na každé kartě, chipu, tlačítku, badge.
2. Press-into-shadow tlačítka: hover `translate(3px,3px)` + stín 3px; active `translate(6px,6px)` + stín 0.
3. Rotace všeho o ±1–9° (per-element `--r`/`--tilt` custom properties), hover často narovná.
4. Halftone tečky na hero (`radial-gradient` 1.6px / 26px grid, ink 7 %).
5. feTurbulence papírový grain přes celou stránku (`body::after`, data-URI SVG, opacity .05, fixed, pointer-events:none).
6. Polaroidy s máslovou páskou (`::before` pásek rgba(--butter,.85), rotate(-3deg)), překryté dvojice s protichůdnou rotací.
7. Speech bubbles s ocáskem (`::after` čtverec, rotate(45deg) skew(8,8)).
8. Kruhové badge (4–7px ink border) + pill chips (r=999px) + bob float animace.
9. **Šlehačková vlnka** — scalloped SVG divider mezi color-blocked sekcemi (fill = barva další sekce, wrapper bg = předchozí). U cukrárny čte jako poleva/šlehačka.
10. Marquee ticker (duplikovaný span, translateX(-50%), hover pauza).
11. Kruhové fotky produktů vykukující nad kartou (negative margin), pomalá rotace hero dortu (22 s, hover zrychlí na 6 s), půlené obří disky v promo kartách (120 s).
12. Rozeseté SVG doodles: třešničky, posypky, ✦ hvězdičky (display font, rotované, hidden na mobilu).

## Struktura stránky (color-blocked rytmus)

| # | Sekce | Pozadí | Obsah |
|---|-------|--------|-------|
| 1 | Sticky header | cream, ink border-bottom | logo (hover wiggle), nav: Na počkání · Katalog · O nás · Svatby · Pro firmy · Kontakt, telefon chip (zvonící ikona, +420 601 587 297), CTA „Dort na míru" (cherry). Mobil: clip-path circle menu (pink) s obřími rotovanými odkazy. `.scrolled` přidá tvrdý stín. |
| 2 | Ticker | ink | „NOVINKY NA LÉTO: Matcha Latté ✦ domácí limonády s novou chutí ✦ Panna Cotta – malina a borůvka" |
| 3 | Hero | pink + halftone | pill „Brno-Královo Pole • od roku 1992", H1 „POCTIVÁ BRNĚNSKÁ CUKRAŘINA" (CUKRAŘINA cream + stroke, rotovaná), podtext (pravé máslo, živočišná šlehačka), CTA „Vybrat dort" (cherry) + „Dort ještě dnes" (cream), Google badge 4,2★ / 321 recenzí. Vpravo točící se dort (reálná fotka, kruh, 7px obrys) + samolepky „Z pravého másla!" (kruh, butter) a „Denně čerstvé" (pill, cherry), doodles, GSAP parallax. |
| 4 | Příběh/Tradice | cream | 2 polaroidy s páskou (reálné fotky), copy: 1992, Ing. Jarmila Křížová, žádné náhražky/polotovary. Chips: 100% poctivé suroviny · Vlastní výroba v Brně · Zlatá chuť jižní Moravy · 300kg dort pro Vaňkovku. |
| 5 | Bestsellery | cherry (vstup šlehačkovou vlnkou) | cream karty: kruhová fotka nad kartou, název, krátký popis, rotovaná cenovka, štítek BESTSELLER; Makronky navíc „BEZ MOUKY". Easter egg: hover na Pohádce → bublina „Přes léto na dotaz! ☎". Produkty + ceny: Čokoládový od 570 · Jahůdka od 590 · Skluzavka 930 · Makronky 55 · Joggi od 590 · Pohádka od 550 · Bezé 990 Kč. CTA „Všechny produkty". |
| 6 | Dorty na počkání | cream | banner „ZAPOMNĚLI JSTE? ZACHRÁNÍME VÁS." + 3 kroky: Do 15 minut · Až 20 druhů denně · Dozdobíme na místě. Chips kurýrů: Bolt · Foodora · Wolt. CTA „Dorty na počkání". |
| 7 | Svatby + Firmy | pistachio + pink karty | 2 promo bannery s půlenými točícími fotkami: „Svatební dorty & sweet bary" / „Firemní catering — zvládli jsme i 300kg dort". CTAs. |
| 8 | Recenze | pistachio | 3 speech bubbles s ★★★★★ — POUZE reálné texty z /recenze/ nebo Google (žádné vymyšlené recenze). Rotovaný badge Google 4,2 / 321 recenzí. |
| 9 | Kontakt | ink, cream text | Otevírací doba PO–NE 9.00–18.00 (dashed řádky, JS zvýrazní „dnes"), adresa Palackého tř. 1379/97, Brno-Královo Pole + „2 parkovací místa, Riegrova 1 (vlevo)", velký butter telefon, e-mail objednavky@cukrarna-pusinka.cz, mapa v ink rámu (iframe + offline fallback). |
| 10 | Footer | ink, dashed top | logo, © 2026 Cukrárna Pusinka, poznámka „Demo redesign". |
| 11 | FAB (mobil) | — | „🍰 Dort ještě dnes", vyskočí po odscrollování hera (IntersectionObserver). |

**404.html** — komiksová stránka „JEJDA! Tahle stránka se ještě peče." + dort + CTA zpět na homepage. Cíl všech interních prokliků (Vercel ji servíruje pro neexistující cesty automaticky; interní odkazy vedou přímo na `/404`).

## Motion

- **GSAP + ScrollTrigger self-hosted ve `vendor/`** — scroll reveals (stagger, rotace z `--r`), hero parallax vrstvy, pin/scrub efekty kde dávají smysl.
- CSS keyframes: spin (22 s/120 s), bob float, ring (telefon), tick (marquee).
- Přístupnost od začátku: `prefers-reduced-motion: reduce` vypne reveals i nekonečné animace; `@media (hover:none)` zviditelní hover-only obsah trvale; `:focus-within` ekvivalenty pro klávesnici.

## Soubory

```
index.html  404.html  vercel.json (jen pokud potřeba)
css/styles.css   js/main.js
vendor/gsap.min.js  vendor/ScrollTrigger.min.js
fonts/  (Agbalumo + Raleway woff2, latin-ext)
images/ (logo-pusinka.svg + produktové/story fotky .webp z jejich webu)
```

Bez build stepu. Deploy: složku nahrát na Vercel. Favicon + OG obrázek přes web-asset-generator.

## Mimo rozsah

Podstránky, objednávkový systém, CMS, SEO migrace, nasazení na produkční doménu.

## Kvalita / ověření

- Skilly při implementaci: frontend-design, high-end-visual-design, redesign-existing-projects, gsap-framer-scroll-animation, scroll-experience.
- Po buildu: web-design-guidelines audit + design:accessibility-review (kontrast! — původní web má WCAG faily), impeccable polish živě v prohlížeči, verification-before-completion (screenshoty desktop/mobil, konzole bez chyb).
- Žádný AI slop: žádné AI generované obrázky, žádné fabrikované recenze, texty faktově 1:1 z originálu.
