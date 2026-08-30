# -*- coding: utf-8 -*-
"""Audit webu Cukrarna Pusinka. Generuje 5stranne PDF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

# Fonty se berou ze systemu. Segoe UI je licencovany Microsoftem,
# proto neni soucasti repozitare. Na jinem systemu doplnte vlastni cestu.
FONT_DIRS = [
    os.path.join(BASE, "fonts"),
    r"C:\Windows\Fonts",
    "/usr/share/fonts/truetype/dejavu",
]
FONT_FILES = {
    "UI": ["segoeui.ttf", "DejaVuSans.ttf", "arial.ttf"],
    "UIB": ["segoeuib.ttf", "DejaVuSans-Bold.ttf", "arialbd.ttf"],
    "UISB": ["seguisb.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf", "arialbd.ttf"],
}


def find_font(names):
    for d in FONT_DIRS:
        for n in names:
            f = os.path.join(d, n)
            if os.path.exists(f):
                return f
    raise SystemExit("Nenalezen zadny z fontu: " + ", ".join(names))


for alias, names in FONT_FILES.items():
    pdfmetrics.registerFont(TTFont(alias, find_font(names)))

INK = HexColor("#2B1516")
PINK = HexColor("#EF7E88")
PINKL = HexColor("#FFE3EA")
CREAM = HexColor("#FDF2E7")
CHERRY = HexColor("#960016")
PIST = HexColor("#A8D8C2")
BUTTER = HexColor("#F7C948")
GREY = HexColor("#6B5A55")
LINE = HexColor("#DED0C4")

W, H = A4
M = 20 * mm
CW = W - 2 * M

PAGE_TITLES = {}


def wrap(text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


class Doc:
    def __init__(self, path):
        self.c = rl_canvas.Canvas(path, pagesize=A4)
        self.c.setTitle("Audit webu Cukrarna Pusinka")
        self.c.setAuthor("Tempovis")
        self.c.setSubject("Analyza soucasneho webu a navrh dalsiho postupu")
        self.page = 0
        self.y = H - M

    def para(self, text, size=9.6, font="UI", color=INK, leading=None, gap=3.2, maxw=None):
        leading = leading or size * 1.55
        maxw = maxw or CW
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        for ln in wrap(text, font, size, maxw):
            self.c.drawString(M, self.y, ln)
            self.y -= leading
        self.y -= gap

    def h2(self, text, color=INK, size=15):
        self.c.setFillColor(color)
        self.c.setFont("UIB", size)
        self.c.drawString(M, self.y, text)
        self.y -= size * 0.72
        self.c.setStrokeColor(PINK)
        self.c.setLineWidth(2.4)
        self.c.line(M, self.y, M + 34, self.y)
        self.y -= 12

    def h3(self, text, color=INK, size=10.6):
        self.c.setFillColor(color)
        self.c.setFont("UISB", size)
        self.c.drawString(M, self.y, text)
        self.y -= size * 1.55

    def eyebrow(self, text, color=CHERRY):
        self.c.setFillColor(color)
        self.c.setFont("UISB", 7.6)
        self.c.drawString(M, self.y, text.upper())
        self.y -= 13

    def rule(self, gap=8):
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        self.c.line(M, self.y, W - M, self.y)
        self.y -= gap

    def new_page(self, title=None):
        if self.page:
            self.footer()
            self.c.showPage()
        self.page += 1
        self.y = H - M
        if title:
            PAGE_TITLES[self.page] = title
            self.c.setFillColor(GREY)
            self.c.setFont("UI", 7.6)
            self.c.drawString(M, H - 13 * mm, title)
            self.c.drawRightString(W - M, H - 13 * mm, "Cukrárna Pusinka")
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(0.7)
            self.c.line(M, H - 15 * mm, W - M, H - 15 * mm)
            self.y = H - 22 * mm

    def footer(self):
        if self.page <= 1:
            return
        self.c.setFillColor(GREY)
        self.c.setFont("UI", 7.4)
        self.c.drawString(M, 12 * mm, "Audit webu a návrh dalšího postupu")
        self.c.drawRightString(W - M, 12 * mm, "Strana %d z 5" % self.page)

    def save(self):
        self.footer()
        self.c.save()


def finding(d, num, title, body, impact, sev):
    """Nalez s cislem, popisem a dopadem."""
    sev_col = {"vysoka": CHERRY, "stredni": HexColor("#A96A12"), "nizka": GREY}[sev]
    top = d.y + 4
    d.c.setFillColor(sev_col)
    d.c.circle(M + 5.4, d.y + 1.2, 5.4, stroke=0, fill=1)
    d.c.setFillColor(HexColor("#FFFFFF"))
    d.c.setFont("UIB", 7.6)
    d.c.drawCentredString(M + 5.4, d.y - 1.4, str(num))

    d.c.setFillColor(INK)
    d.c.setFont("UISB", 10.2)
    d.c.drawString(M + 16, d.y, title)

    label = {"vysoka": "vysoká priorita", "stredni": "střední", "nizka": "nízká"}[sev]
    d.c.setFont("UISB", 7.2)
    tw = stringWidth(label.upper(), "UISB", 7.2)
    d.c.setFillColor(sev_col)
    d.c.roundRect(W - M - tw - 12, d.y - 2.6, tw + 12, 12.4, 6.2, stroke=0, fill=1)
    d.c.setFillColor(HexColor("#FFFFFF"))
    d.c.drawCentredString(W - M - tw / 2 - 6, d.y + 1.1, label.upper())

    d.y -= 14
    d.c.setFillColor(GREY)
    d.c.setFont("UI", 9.2)
    for ln in wrap(body, "UI", 9.2, CW - 16):
        d.c.drawString(M + 16, d.y, ln)
        d.y -= 13.2
    d.c.setFillColor(INK)
    d.c.setFont("UISB", 9.2)
    for ln in wrap("Dopad: " + impact, "UISB", 9.2, CW - 16):
        d.c.drawString(M + 16, d.y, ln)
        d.y -= 13.2
    d.y -= 7


def metric_box(d, x, w, big, label, tone=PINKL, bigcol=CHERRY):
    h = 26 * mm
    d.c.setFillColor(tone)
    d.c.roundRect(x, d.y - h, w, h, 5, stroke=0, fill=1)
    d.c.setFillColor(bigcol)
    d.c.setFont("UIB", 21)
    d.c.drawCentredString(x + w / 2, d.y - 12.4 * mm, big)
    d.c.setFillColor(INK)
    d.c.setFont("UI", 7.7)
    lines = wrap(label, "UI", 7.7, w - 10)[:2]
    yy = d.y - 17.4 * mm
    for ln in lines:
        d.c.drawCentredString(x + w / 2, yy, ln)
        yy -= 9.4


# ---------------------------------------------------------------- dokument
out = os.path.join(ROOT, "Audit-webu-Cukrarna-Pusinka.pdf")
d = Doc(out)

# ============================== STRANA 1: titulka + shrnuti
d.new_page()
d.c.setFillColor(PINK)
d.c.rect(0, H - 96 * mm, W, 96 * mm, stroke=0, fill=1)

logo = os.path.join(ROOT, "audit-logo.png")
d.c.setFillColor(CREAM)
d.c.roundRect(M, H - 48 * mm, 52 * mm, 26 * mm, 5, stroke=0, fill=1)
if os.path.exists(logo):
    d.c.drawImage(ImageReader(logo), M + 3 * mm, H - 46 * mm, 46 * mm, 22 * mm,
                  preserveAspectRatio=True, anchor="c", mask="auto")

d.c.setFillColor(INK)
d.c.setFont("UIB", 30)
d.c.drawString(M, H - 62 * mm, "Audit webových stránek")
d.c.setFont("UI", 13.6)
d.c.setFillColor(HexColor("#5A2226"))
d.c.drawString(M, H - 71 * mm, "Cukrářství a perníkářství Pusinka, Brno")
d.c.setFont("UI", 9.6)
d.c.drawString(M, H - 79 * mm, "Analýza současného webu, provedené úpravy a návrh dalšího postupu")
d.c.setFont("UI", 8.6)
d.c.drawString(M, H - 87 * mm, "Srpen 2026")

d.y = H - 112 * mm
d.eyebrow("Shrnutí pro vedení")
d.para(
    "Váš web je obsahově na velmi dobré úrovni. Jsou v něm konkrétní a věrohodné informace, "
    "které vás odlišují: rok 1992, pravé máslo a živočišná šlehačka, ocenění Zlatá chuť jižní Moravy "
    "a rekordní třistakilový dort pro Vaňkovku. Problém není v tom, co web říká. Problém je v tom, "
    "jak to ukazuje.",
    size=9.8)
d.para(
    "Prošli jsme celou úvodní stránku a proměřili ji stejnými nástroji, jaké používá Google. "
    "Našli jsme sedm konkrétních míst, kde web ztrácí návštěvníky, a připravili novou úvodní "
    "stránku, na které si můžete rozdíl prohlédnout. Tento dokument shrnuje, co jsme našli, "
    "co je už hotové a co doporučujeme udělat dál.",
    size=9.8)

d.y -= 4
gap = 5 * mm
bw = (CW - 3 * gap) / 4
metric_box(d, M, bw, "7,5", "obrazovky měří úvodní stránka", PINKL, CHERRY)
metric_box(d, M + bw + gap, bw, "2,7:1", "kontrast textu, norma žádá 4,5:1", PINKL, CHERRY)
metric_box(d, M + 2 * (bw + gap), bw, "42", "prvků je na mobilu příliš malých", PINKL, CHERRY)
metric_box(d, M + 3 * (bw + gap), bw, "25", "obrázků bez užitečného popisku", PINKL, CHERRY)
d.y -= 26 * mm + 8

d.rule(10)
d.c.setFillColor(GREY)
d.c.setFont("UI", 8.4)
d.c.drawString(M, d.y, "Měřeno na adrese cukrarna-pusinka.cz, rozlišení 1280 x 860 bodů, prohlížeč Chrome.")
d.y -= 11
d.c.drawString(M, d.y, "Všechna čísla v dokumentu pocházejí z měření, ne z odhadu.")

# ============================== STRANA 2: nalezy
d.new_page("Co jsme našli")
d.h2("Co na webu brzdí návštěvníky")
d.para(
    "Nálezy řadíme podle toho, jak moc ovlivňují člověka, který u vás chce objednat dort. "
    "Nejde o vkus, ale o věci, které jdou změřit.",
    size=9.4, color=GREY)
d.y -= 2

finding(d, 1, "Text na růžové se špatně čte",
        "Bílý text na růžovém tlačítku Dort ještě dnes má kontrast 2,7:1. Přístupnostní norma "
        "vyžaduje nejméně 4,5:1. Stejný problém mají růžové odkazy na bílém pozadí. Na mobilu "
        "na slunci nebo pro člověka nad padesát let je takový text obtížně čitelný.",
        "nejméně čitelné je právě tlačítko, které vede k rychlé objednávce.", "vysoka")

finding(d, 2, "Úvodní fotka není z vaší cukrárny",
        "Hlavní fotka na úvodní stránce je zakoupená fotobanková fotografie. Návštěvník ji "
        "podvědomě pozná. Vedle textu o poctivém řemesle od roku 1992 působí rozporuplně, "
        "protože slibujete něco vlastního a ukazujete něco cizího.",
        "oslabuje hlavní argument, kterým se odlišujete od konkurence.", "vysoka")

finding(d, 3, "Ovládací prvky jsou na mobilu malé",
        "Našli jsme 42 odkazů a tlačítek nižších než 44 bodů, což je hodnota doporučená "
        "Applem i Googlem. Týká se to i tlačítek Zobrazit u jednotlivých dortů.",
        "na telefonu se lidé netrefují a odcházejí místo objednávky.", "vysoka")

finding(d, 4, "Značka není sjednocená",
        "Web používá tři různé odstíny růžové: jednu v logu, druhou v tlačítcích a odkazech "
        "a třetí v překryvu úvodní fotky. Rozdíly jsou malé, ale oko je zaznamená.",
        "působí to nedbale u firmy, která staví na preciznosti.", "stredni")

finding(d, 5, "Fotky produktů nemají jednotný styl",
        "Vedle sebe stojí tři druhy fotek: růžové studiové, teplé rustikální a starší výřezy "
        "dortů na bílém pozadí. Každá skupina vypadá, jako by patřila na jiný web.",
        "katalog vypadá starší a levněji, než jaké dorty ve skutečnosti pečete.", "stredni")

finding(d, 6, "Web je postavený na zastaralé technice",
        "Stránka načítá knihovny jQuery, jQuery Migrate, Bootstrap, Owl Carousel a GLightbox, "
        "celkem 66 požadavků. Jde o postupy běžné před deseti lety.",
        "pomalejší načítání na mobilních datech a dražší budoucí úpravy.", "stredni")

finding(d, 7, "Drobnosti v textech a popiscích",
        "V české nabídce je anglické slovo Bestsellers. Osm obrázků nemá popisek vůbec "
        "a sedmnáct má popisek typu Úvod: photo nebo icon arrow.",
        "Google těmto obrázkům nerozumí a nevyhledá je.", "nizka")

d.y -= 4
d.rule(11)
d.h3("Co naopak funguje a necháváme být")
d.para(
    "Texty jsou konkrétní a mluví o věcech, které si nikdo nevymyslí: rok založení, jméno "
    "zakladatelky, ocenění, rekordní dort. Struktura nabídky dává smysl a rozdělení na dorty "
    "na počkání, svatby a firmy odpovídá tomu, jak lidé skutečně poptávají. Logo a růžová "
    "barva jsou zapamatovatelné. Web má vyplněné údaje pro vyhledávače včetně otevírací doby.",
    size=9.2, color=GREY)

# ============================== STRANA 3: co je hotove
d.new_page("Co je hotové")
d.h2("Nová úvodní stránka, kterou si můžete projít")
d.para(
    "Připravili jsme novou úvodní stránku jako ukázku. Obsah, ceny i kontakty jsou převzaté "
    "z vašeho webu beze změny. Změnili jsme způsob, jakým se to podává.",
    size=9.4, color=GREY)
d.y -= 3

img_h = 47 * mm
half = (CW - 6 * mm) / 2
old_img = os.path.join(ROOT, "audit-old-hero.png")
new_img = os.path.join(ROOT, "audit-new-hero.png")

d.c.setFillColor(GREY)
d.c.setFont("UISB", 8)
d.c.drawString(M, d.y, "PŮVODNÍ")
d.c.drawString(M + half + 6 * mm, d.y, "NOVÁ")
d.y -= 4

for path, x in ((old_img, M), (new_img, M + half + 6 * mm)):
    if os.path.exists(path):
        d.c.drawImage(ImageReader(path), x, d.y - img_h, half, img_h,
                      preserveAspectRatio=True, anchor="n", mask="auto")
    d.c.setStrokeColor(LINE)
    d.c.setLineWidth(0.8)
    d.c.rect(x, d.y - img_h, half, img_h, stroke=1, fill=0)
d.y -= img_h + 12

rows = [
    ("Čitelnost", "Bílá na růžové, kontrast 2,7:1",
     "Tmavě čokoládová na krémové, kontrast přes 12:1"),
    ("Úvodní fotka", "Fotobanková fotografie",
     "Váš skutečný dort v rámečku, popisek Čerstvě z naší dílny"),
    ("Důvěra", "Hodnocení schované až v patičce",
     "Hodnocení 4,2 a 321 recenzí hned pod tlačítky"),
    ("Ovládání na mobilu", "42 prvků pod doporučenou velikost",
     "10 prvků, zbytek zvětšen na 44 bodů a více"),
    ("Popisky obrázků", "25 chybějících nebo neužitečných",
     "Každý obrázek má popisek, ozdoby jsou skryté před čtečkou"),
    ("Technika", "66 požadavků, pět knihoven",
     "20 požadavků, žádná cizí knihovna kromě animací"),
]

col1, col2 = 34 * mm, 58 * mm
col3 = CW - col1 - col2 - 8 * mm
d.c.setFillColor(INK)
d.c.setFont("UISB", 8.2)
d.c.drawString(M, d.y, "OBLAST")
d.c.drawString(M + col1, d.y, "PŮVODNÍ STAV")
d.c.drawString(M + col1 + col2 + 4 * mm, d.y, "PO ÚPRAVĚ")
d.y -= 5
d.rule(7)

for label, old, new in rows:
    lines_old = wrap(old, "UI", 8.6, col2 - 4 * mm)
    lines_new = wrap(new, "UI", 8.6, col3)
    n = max(len(lines_old), len(lines_new), 1)
    block_h = n * 11.6 + 6
    d.c.setFillColor(INK)
    d.c.setFont("UISB", 8.8)
    d.c.drawString(M, d.y, label)
    d.c.setFont("UI", 8.6)
    d.c.setFillColor(GREY)
    yy = d.y
    for ln in lines_old:
        d.c.drawString(M + col1, yy, ln)
        yy -= 11.6
    yy = d.y
    d.c.setFillColor(HexColor("#2E6B4F"))
    for ln in lines_new:
        d.c.drawString(M + col1 + col2 + 4 * mm, yy, ln)
        yy -= 11.6
    d.y -= block_h
    d.rule(6)

d.y -= 2
d.c.setFillColor(PINKL)
box_h = 22 * mm
d.c.roundRect(M, d.y - box_h, CW, box_h, 5, stroke=0, fill=1)
d.c.setFillColor(INK)
d.c.setFont("UISB", 9.4)
d.c.drawString(M + 8, d.y - 8 * mm, "Co zůstalo beze změny")
d.c.setFont("UI", 8.8)
d.c.setFillColor(GREY)
d.c.drawString(M + 8, d.y - 13.4 * mm,
               "Logo, růžová barva značky, font nadpisů, všechny texty, ceny a kontaktní údaje.")
d.c.drawString(M + 8, d.y - 18 * mm,
               "Recenze jsou skutečné, převzali jsme je z vaší stránky s hodnocením.")

# ============================== STRANA 4: dalsi postup
d.new_page("Návrh dalšího postupu")
d.h2("Co doporučujeme udělat dál")
d.para(
    "Postup dělíme do tří kroků podle toho, co přinese nejvíc užitku za nejmenší úsilí. "
    "Každý krok dává smysl i samostatně.",
    size=9.4, color=GREY)
d.y -= 4

phases = [
    ("Krok 1", "Dokončit web podle nové úvodní stránky", "2 až 3 týdny", PINK, [
        "Převést do nové podoby katalog, stránky Svatby, Pro firmy a Kontakt.",
        "Sjednotit růžovou napříč webem na odstín z loga.",
        "Zvětšit tlačítka a odkazy na mobilu nad 44 bodů.",
        "Opravit popisky obrázků a české názvy sekcí.",
    ]),
    ("Krok 2", "Vyfotit vlastní produkty a provoz", "podle domluvy", BUTTER, [
        "Půldenní focení ve vaší dílně: dorty, zákusky, perníky a vitrína.",
        "Jednotné pozadí a světlo, aby katalog působil jako jeden celek.",
        "Několik fotografií vás a týmu při práci pro sekci o nás.",
        "Tohle je krok s největším dopadem na dojem z celého webu.",
    ]),
    ("Krok 3", "Zjednodušit objednávání", "4 až 6 týdnů", PIST, [
        "Krátký formulář na dort na míru s možností přiložit fotografii.",
        "Přehled dnešní nabídky dortů na počkání, aktualizovaný z mobilu.",
        "Napojení na rezervaci a jasné potvrzení objednávky e-mailem.",
    ]),
]

for tag, title, dur, col, items in phases:
    d.c.setFillColor(col)
    d.c.roundRect(M, d.y - 3, 20 * mm, 13, 6.5, stroke=0, fill=1)
    d.c.setFillColor(INK)
    d.c.setFont("UISB", 8)
    d.c.drawCentredString(M + 10 * mm, d.y + 0.8, tag.upper())
    d.c.setFont("UISB", 11)
    d.c.drawString(M + 24 * mm, d.y + 0.6, title)
    d.c.setFillColor(GREY)
    d.c.setFont("UI", 8.4)
    d.c.drawRightString(W - M, d.y + 0.6, dur)
    d.y -= 17
    d.c.setFont("UI", 9.2)
    for it in items:
        d.c.setFillColor(PINK)
        d.c.circle(M + 4, d.y + 3.2, 1.7, stroke=0, fill=1)
        d.c.setFillColor(GREY)
        for i, ln in enumerate(wrap(it, "UI", 9.2, CW - 14)):
            d.c.drawString(M + 10, d.y, ln)
            d.y -= 12.4
    d.y -= 8

d.rule(10)
d.h3("Co naopak neděláme")
d.para(
    "Nedoporučujeme měnit logo ani růžovou barvu. Obojí je zavedené a lidé si vás podle toho "
    "pamatují. Nedoporučujeme ani plnohodnotný e-shop s platební bránou, dokud nebude jasné, "
    "kolik lidí objednává přes web. Menší krok se dá udělat rychle a změřit.",
    size=9.2, color=GREY)

d.y -= 4
d.h3("Jak měřit, jestli to zabralo")
d.para(
    "Před spuštěním doporučujeme zapnout měření návštěvnosti a sledovat tři čísla: kolik lidí "
    "klikne na tlačítko k objednávce, kolik jich dojde až do formuláře a kolik telefonátů "
    "přijde z webu. Po dvou měsících bude vidět, jestli změny fungují, nebo kde se lidé "
    "zastavují. Bez měření je každá další úprava jen odhad.",
    size=9.2, color=GREY)

# ============================== STRANA 5: zaver
d.new_page("Závěr")
d.h2("Shrnutí")
d.para(
    "Web nemusíte stavět od začátku. Obsah, příběh i důkazy o kvalitě už na něm jsou. "
    "Chybí forma, která by jim odpovídala, a několik technických oprav, které dnes zbytečně "
    "brzdí lidi na mobilu.",
    size=9.8)
d.para(
    "Nová úvodní stránka ukazuje, že se to dá vyřešit bez ztráty toho, co máte. Zůstává logo, "
    "růžová i font nadpisů. Mění se čitelnost, pořadí informací a to, čí fotky návštěvník vidí.",
    size=9.8)

d.y -= 6
d.c.setFillColor(CREAM)
bh = 44 * mm
d.c.roundRect(M, d.y - bh, CW, bh, 6, stroke=0, fill=1)
d.c.setStrokeColor(PINK)
d.c.setLineWidth(1.6)
d.c.roundRect(M, d.y - bh, CW, bh, 6, stroke=1, fill=0)

d.c.setFillColor(CHERRY)
d.c.setFont("UISB", 8)
d.c.drawString(M + 9 * mm, d.y - 9 * mm, "TŘI VĚCI, KTERÉ MAJÍ NEJVĚTŠÍ DOPAD")
d.c.setFillColor(INK)
d.c.setFont("UI", 9.6)
picks = [
    "1.  Opravit čitelnost růžových tlačítek a odkazů. Práce na jeden den.",
    "2.  Vyfotit vlastní dorty a provoz. Nahradí fotobanku a sjednotí katalog.",
    "3.  Zvětšit ovládací prvky na mobilu. Většina návštěv chodí z telefonu.",
]
yy = d.y - 17 * mm
for p in picks:
    d.c.drawString(M + 9 * mm, yy, p)
    yy -= 13

d.y -= bh + 14
d.h3("Další krok")
d.para(
    "Novou úvodní stránku si můžete projít na počítači i na telefonu. Pokud vám bude sedět "
    "směr, domluvíme si schůzku, projdeme kroky podle vašich priorit a upřesníme rozsah "
    "a cenu. Pokud vám něco sedět nebude, řekněte co, a upravíme to.",
    size=9.4, color=GREY)

d.y -= 8
d.rule(12)
d.c.setFillColor(INK)
d.c.setFont("UISB", 9.4)
d.c.drawString(M, d.y, "Zpracoval")
d.c.setFont("UI", 9.4)
d.c.setFillColor(GREY)
d.c.drawString(M + 26 * mm, d.y, "David Jurica")
d.y -= 13
d.c.setFillColor(INK)
d.c.setFont("UISB", 9.4)
d.c.drawString(M, d.y, "Kontakt")
d.c.setFont("UI", 9.4)
d.c.setFillColor(GREY)
d.c.drawString(M + 26 * mm, d.y, "jsme.proste@tempovis.co")
d.y -= 13
d.c.setFillColor(INK)
d.c.setFont("UISB", 9.4)
d.c.drawString(M, d.y, "Ukázka")
d.c.setFont("UI", 9.4)
d.c.setFillColor(GREY)
d.c.drawString(M + 26 * mm, d.y, "odkaz doplníme po nasazení")

d.save()
print("PDF hotovo:", out)
