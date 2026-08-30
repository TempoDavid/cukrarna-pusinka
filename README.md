# Cukrárna Pusinka — demo úvodní stránky

Grafický návrh nové úvodní stránky pro [Cukrářství a perníkářství Pusinka](https://www.cukrarna-pusinka.cz/)
v Brně-Králově Poli. Statická stránka bez build kroku, připravená k nasazení na Vercel.

Jde o **ukázku, ne o oficiální web klienta**. Všechny prokliky vedou na komiksovou stránku 404.

## Co to je

Obsah, ceny, recenze i kontakty jsou převzaté z původního webu beze změny. Změnila se podoba:
komiksový vizuální styl navázaný na stávající značku. Logo, růžová barva i font nadpisů zůstávají.

## Struktura

```
index.html        úvodní stránka
404.html          komiksová 404, cíl všech prokliků
css/styles.css    design systém a všechny sekce
js/main.js        menu, animace textu a scroll efekty
vendor/           GSAP a ScrollTrigger, self-hosted
fonts/            Agbalumo a Raleway ve formátu woff2
images/           logo, fotky produktů, favicony, OG obrázek
assets-src/       zdrojové HTML pro generování OG obrázku a ikon
audit/            generátor klientského auditu v PDF
docs/             specifikace a plán implementace
```

## Spuštění lokálně

```bash
npx serve -l 3000 .
```

Otevřete `http://localhost:3000`.

## Nasazení

Repozitář se importuje do Vercelu bez konfigurace. `vercel.json` zapíná `cleanUrls`,
aby odkazy na `/404` fungovaly.

## Použité technologie

Ruční HTML a CSS, vanilla JavaScript, GSAP se ScrollTriggerem pro animace.
Žádný framework ani build krok.

## Audit

Pětistránkový audit původního webu v PDF se generuje takto:

```bash
python audit/build_audit.py
```

Skript hledá fonty v systému. Segoe UI je licencované Microsoftem, proto není součástí repozitáře.

## Autorská práva

Fotografie produktů, logo a texty patří Cukrářství a perníkářství Pusinka a jsou zde
použité pro účely návrhu.
