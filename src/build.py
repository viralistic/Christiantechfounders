#!/usr/bin/env python3
"""Static site generator for christiantechfounders.com.

Run from the repo root:  python3 src/build.py
Content lives in src/content (Markdown posts) and src/data (JSON).
Output is written to the repo root (index.html, insights/, library/, founders/, nl/...).
Requires: pip install markdown
"""
import html
import json
import math
import random
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DOMAIN = "https://www.christiantechfounders.com"
LUMA = "https://luma.com/rnxcss9v"
LANGS = ["en", "nl"]
PREFIX = {"en": "", "nl": "/nl"}
EVENT_SLUG = "christian-entrepreneurs-coffee-and-calling-amsterdam"
POSTER = "/assets/coffee-and-calling-amsterdam.webp"
YEAR = 2026

esc = html.escape


# ─────────────────────────── Strings ───────────────────────────

T = {
    "en": {
        "nav_insights": "Insights", "nav_library": "Library", "nav_founders": "Founders", "nav_event": "Next event", "nav_about": "About", "nav_partners": "Partners",
        "join": "Join the next event", "menu": "Menu",
        "footer_tag": "A community for Christ-led founders building in tech. Amsterdam.",
        "explore": "Explore", "connect": "Connect", "signup": "Sign up on Luma", "switch": "Nederlands",
        "read_more": "Read more", "min": "min read", "all_insights": "All insights",
        "more_insights": "More insights", "back_insights": "Back to insights",
        "cta_title": "Stop building alone", "cta_text": "Join Christ-led founders for dinner, worship and honest conversation. Next: Coffee & Calling, Sunday 10 January 2027 in Amsterdam. Pay what you want, from €0.50.",
        "home": "Home",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "example": "Example", "projects": "Projects", "stage": "Stage", "looking_for": "Looking for",
        "all_founders": "All founders", "project_count": "{n} project", "project_count_pl": "{n} projects",
        "help_title": "Want to help with a project?", "help_text": "Come to Coffee & Calling and meet the founders in person. Bring your skills, your network or your prayers.",
        "listen": "Listen", "visit": "Visit", "from_notes": "From our notes", "related": "Read the insight",
        "skip": "Skip to content",
    },
    "nl": {
        "nav_insights": "Insights", "nav_library": "Bibliotheek", "nav_founders": "Founders", "nav_event": "Volgende event", "nav_about": "Over ons", "nav_partners": "Partners",
        "join": "Kom naar het volgende event", "menu": "Menu",
        "footer_tag": "Een community voor founders die Christus volgen en bouwen in tech. Amsterdam.",
        "explore": "Ontdek", "connect": "Contact", "signup": "Aanmelden op Luma", "switch": "English",
        "read_more": "Lees meer", "min": "min lezen", "all_insights": "Alle insights",
        "more_insights": "Meer insights", "back_insights": "Terug naar insights",
        "cta_title": "Stop met alleen bouwen", "cta_text": "Kom samen met founders die Christus volgen voor diner, aanbidding en eerlijke gesprekken. Volgende: Coffee & Calling, zondag 10 januari 2027 in Amsterdam. Betaal wat je wilt, vanaf €0,50.",
        "home": "Home",
        "months": ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"],
        "example": "Voorbeeld", "projects": "Projecten", "stage": "Fase", "looking_for": "Zoekt",
        "all_founders": "Alle founders", "project_count": "{n} project", "project_count_pl": "{n} projecten",
        "help_title": "Wil je helpen met een project?", "help_text": "Kom naar Coffee & Calling en ontmoet de founders in het echt. Neem je skills, je netwerk of je gebed mee.",
        "listen": "Luister", "visit": "Bekijk", "from_notes": "Uit onze notities", "related": "Lees de insight",
        "skip": "Naar inhoud",
    },
}

HOME = {
    "en": {
        "title": "Christian Tech Founders | Community for Christian Entrepreneurs in Tech",
        "desc": "A community for Christian entrepreneurs in tech who put God first. Sunday evenings with worship, sermons on AI, talent alignment and project support in Amsterdam.",
        "hero_label": "Coffee & Calling / Amsterdam",
        "h1": "A community for Christian founders building in tech",
        "lead": "For entrepreneurs who put God first and build with technology. Meet fresh, like-minded people, discover where your talents fit and do good things together with God.",
        "how": "How it works",
        "meta_l": "Next: 10.01.2027", "meta_r": "From €0.50",
        "p_label": "[01] Sound familiar?",
        "p_h2": "Building alone is harder than it should be.",
        "p1": "You love God and you love building. But church friends do not always get startups, and tech peers do not always get your faith. So the big questions stay with you. <strong>Is my company part of my calling? Am I using my gifts where God wants them?</strong>",
        "p2": "Deadlines, metrics and worries keep pulling your eyes to a lower place. Meanwhile a few giants shape the technology the whole world uses, and Christian builders stay scattered.",
        "g_label": "[02] Why we exist",
        "g_h2": "We know the tension. We live it too.",
        "g1": "We know what it feels like to stand between two worlds, deep in faith and deep in technology, as if no one fully understands what you see.",
        "g2": "We believe a calling from God means standing in the place that lines up as closely as possible with your talents. There are thousands of things you could do. But when you stand where your gifts fit, you shine His light like a kaleidoscope, onto as many people as possible, as strongly as possible.",
        "g3": "That is why we started Christian Tech Founders: to bring Christ-led founders, developers and designers together around dinner, worship and honest conversation.",
        "o_label": "[03] What we do",
        "o_h2": "Align your business with God",
        "offer": [
            ("Sunday evenings", "Worship and pray together", "Worship lifts your eyes from the low things that steal your attention. It moves us to compassion, and from there to mission and serving."),
            ("Sermons", "AI, tech and God's real estate", "Honest teaching on AI and technology, how they shape a world that is often dark, and how we claim more space for God's presence in it."),
            ("Talent alignment", "Find where your gifts fit", "In a talent alignment session you discover where your skills and passions have the most impact, so you stop guessing."),
            ("Projects", "Get help to build", "Bring your project. We help you move it forward and publish it on our site, so you can find funding and people to build with."),
        ],
        "s_label": "[04] How it works",
        "s_h2": "From building alone to building together",
        "steps": [
            ("Sign up for an evening", "Pick the next Coffee & Calling and reserve your seat on Luma. You choose what you pay."),
            ("Meet your people", "Share dinner, worship together and talk with founders who understand both your faith and your work."),
            ("Take your next step", "Leave with new friends, fresh perspective and a clearer sense of where your talents belong."),
        ],
        "e_label": "[05] Next event",
        "e_sub": "Aligning Your Business With God",
        "e_text": "An evening with dinner, open worship and a sermon on technology, AI and our role in the world. Open to everyone who feels drawn to it, including people still exploring faith.",
        "facts": [("When", "Sunday 10 January 2027, 18:00 to 22:00"), ("Where", "Amsterdam"), ("Ticket", "Pay what you want, from €0.50"), ("Extra", "Optional coworking from 13:00")],
        "i_label": "[06] Insights", "i_h2": "Read before you come",
        "f_label": "[07] Founders", "f_h2": "Meet Christ-led founders",
        "f_lead": "See what other founders are building and where they need help: funding, co-founders, testers or prayer.",
        "f_btn": "See the founders",
        "c_h2": "Don't carry your calling alone.",
        "c_lead": "Picture a table of founders who pray for your company, challenge your ideas and celebrate your wins. It starts with one evening.",
        "c_btn2": "Read the insights",
        "play_label": "[ CTF / Play ]", "play_hint": "Press any key or tap to play", "score": "Score", "best": "Best",
        "over": "Game over", "over_again": "Press any key or tap to try again",
        "play_aria": "Snake game: a snake of blocks moves across a black grid towards a cross. Press any key to play, use the arrow keys to steer.",
    },
    "nl": {
        "title": "Christian Tech Founders | Community voor christelijke ondernemers in tech",
        "desc": "Een community voor christelijke ondernemers in tech die God op de eerste plek zetten. Zondagavonden met aanbidding, preken over AI en talent alignment.",
        "hero_label": "Coffee & Calling / Amsterdam",
        "h1": "Een community voor christelijke founders die bouwen in tech",
        "lead": "Voor ondernemers die God op de eerste plek zetten en bouwen met technologie. Ontmoet frisse, gelijkgestemde mensen, ontdek waar je talenten passen en bereik samen met God goede dingen.",
        "how": "Zo werkt het",
        "meta_l": "Volgende: 10.01.2027", "meta_r": "Vanaf €0,50",
        "p_label": "[01] Herkenbaar?",
        "p_h2": "Alleen bouwen is zwaarder dan nodig.",
        "p1": "Je houdt van God en je houdt van bouwen. Maar vrienden uit de kerk snappen niet altijd startups, en mensen uit tech snappen niet altijd je geloof. Dus de grote vragen blijven bij jou. <strong>Hoort mijn bedrijf bij mijn roeping? Gebruik ik mijn gaven waar God ze wil hebben?</strong>",
        "p2": "Deadlines, cijfers en zorgen trekken je blik steeds naar een lagere plek. Ondertussen bepalen een paar giganten de technologie die de hele wereld gebruikt, en christelijke bouwers blijven verspreid.",
        "g_label": "[02] Waarom we bestaan",
        "g_h2": "We kennen de spanning. We leven er zelf in.",
        "g1": "We weten hoe het voelt om tussen twee werelden te staan, diep in geloof en diep in technologie, alsof niemand helemaal begrijpt wat jij ziet.",
        "g2": "Wij geloven dat een roeping van God betekent dat je gaat staan op de plek die zo goed mogelijk in lijn is met je talenten. Er zijn duizenden dingen die je kunt doen. Maar als je staat waar je gaven passen, laat je Zijn licht schijnen als een caleidoscoop, op zoveel mogelijk mensen en zo sterk mogelijk.",
        "g3": "Daarom zijn we Christian Tech Founders begonnen: om founders, developers en designers die Christus volgen samen te brengen rond diner, aanbidding en eerlijke gesprekken.",
        "o_label": "[03] Wat we doen",
        "o_h2": "Stem je bedrijf af op God",
        "offer": [
            ("Zondagavonden", "Samen aanbidden en bidden", "Aanbidding tilt je blik op, weg van de lage dingen die je aandacht stelen. Het brengt ons tot compassie, en van daaruit tot missie en dienen."),
            ("Preken", "AI, tech en Gods real estate", "Eerlijk onderwijs over AI en technologie, hoe die een vaak donkere wereld vormen, en hoe we daarin meer ruimte maken voor Gods aanwezigheid."),
            ("Talent alignment", "Vind waar je gaven passen", "In een talent alignment sessie ontdek je waar je skills en passies de meeste impact hebben, zodat je niet meer hoeft te gokken."),
            ("Projecten", "Hulp bij het bouwen", "Neem je project mee. We helpen je verder en publiceren het op onze site, zodat je financiering en mensen vindt om mee te bouwen."),
        ],
        "s_label": "[04] Zo werkt het",
        "s_h2": "Van alleen bouwen naar samen bouwen",
        "steps": [
            ("Meld je aan voor een avond", "Kies de volgende Coffee & Calling en reserveer je plek op Luma. Je bepaalt zelf wat je betaalt."),
            ("Ontmoet je mensen", "Eet samen, aanbid samen en praat met founders die zowel je geloof als je werk begrijpen."),
            ("Zet je volgende stap", "Ga naar huis met nieuwe vrienden, een frisse blik en meer helderheid over waar je talenten thuishoren."),
        ],
        "e_label": "[05] Volgende event",
        "e_sub": "Stem je bedrijf af op God",
        "e_text": "Een avond met diner, open aanbidding en een preek over technologie, AI en onze rol in de wereld. Open voor iedereen die zich aangetrokken voelt, ook als je nog zoekende bent.",
        "facts": [("Wanneer", "Zondag 10 januari 2027, 18:00 tot 22:00"), ("Waar", "Amsterdam"), ("Ticket", "Betaal wat je wilt, vanaf €0,50"), ("Extra", "Optioneel coworken vanaf 13:00")],
        "i_label": "[06] Insights", "i_h2": "Lees alvast",
        "f_label": "[07] Founders", "f_h2": "Ontmoet founders die Christus volgen",
        "f_lead": "Zie wat andere founders bouwen en waar ze hulp bij zoeken: financiering, medeoprichters, testers of gebed.",
        "f_btn": "Bekijk de founders",
        "c_h2": "Draag je roeping niet alleen.",
        "c_lead": "Stel je een tafel voor met founders die bidden voor je bedrijf, je ideeën uitdagen en je successen vieren. Het begint met één avond.",
        "c_btn2": "Lees de insights",
        "play_label": "[ CTF / Play ]", "play_hint": "Druk op een toets of tik om te spelen", "score": "Score", "best": "Best",
        "over": "Game over", "over_again": "Druk op een toets of tik om opnieuw te spelen",
        "play_aria": "Snake spel: een slang van blokjes beweegt over een zwart raster naar een kruis. Druk op een toets om te spelen, stuur met de pijltjestoetsen.",
    },
}

PAGES = {
    "insights": {
        "en": ("Insights for Christian Founders | Christian Tech Founders", "Thinking on faith, calling, worship and technology for Christ-led founders and builders in tech. Plus invitations to meet in person in Amsterdam.",
               "Insights", "Thinking on faith, calling and technology for Christ-led founders. Plus invitations to meet in person."),
        "nl": ("Insights voor christelijke founders | Christian Tech Founders", "Gedachten over geloof, roeping, aanbidding en technologie voor founders die Christus volgen. Plus uitnodigingen om elkaar te ontmoeten in Amsterdam.",
               "Insights", "Gedachten over geloof, roeping en technologie voor founders die Christus volgen. Plus uitnodigingen om elkaar te ontmoeten."),
    },
    "library": {
        "en": ("Library: Findings and Podcasts | Christian Tech Founders", "Findings, podcasts and recordings that help Christ-led founders feel more aligned with God. Curated by Christian Tech Founders.",
               "Library", "Findings, podcasts and recordings to help Christ-led founders feel more aligned with God."),
        "nl": ("Bibliotheek: inzichten en podcasts | Christian Tech Founders", "Inzichten, podcasts en opnames die founders die Christus volgen helpen meer afgestemd te raken op God. Verzameld door Christian Tech Founders.",
               "Bibliotheek", "Inzichten, podcasts en opnames die founders helpen meer afgestemd te raken op God."),
    },
    "founders": {
        "en": ("Founders and Their Projects | Christian Tech Founders", "Meet Christ-led founders building in tech and see the projects they are working on, plus where they need funding, co-founders, testers or prayer.",
               "Founders", "Christ-led founders building in tech. Click a founder to see what they are working on and where they need help."),
        "nl": ("Founders en hun projecten | Christian Tech Founders", "Ontmoet founders die Christus volgen en bouwen in tech. Bekijk hun projecten en waar ze financiering, medeoprichters, testers of gebed zoeken.",
               "Founders", "Founders die Christus volgen en bouwen in tech. Klik op een founder om te zien waar ze aan werken en waar ze hulp zoeken."),
    },
}

LIB = {
    "en": {"f_label": "[01] Findings", "f_lead": "Notes and insights from our evenings and conversations.",
           "l_label": "[02] Listen & watch", "l_lead": "Podcasts and resources we recommend for founders who want to grow in faith and work.",
           "r_label": "[03] From our evenings", "r_title": "Recordings coming soon",
           "r_text": "We will share recordings of our sermons and Sunday evenings here. Want to be there live? Join the next Coffee & Calling."},
    "nl": {"f_label": "[01] Inzichten", "f_lead": "Notities en inzichten uit onze avonden en gesprekken.",
           "l_label": "[02] Luister & kijk", "l_lead": "Podcasts en bronnen die we aanraden voor founders die willen groeien in geloof en werk.",
           "r_label": "[03] Van onze avonden", "r_title": "Opnames volgen binnenkort",
           "r_text": "We delen hier opnames van onze preken en zondagavonden. Wil je er live bij zijn? Kom naar de volgende Coffee & Calling."},
}

FOUNDERS_NOTICE = {
    "en": "Profiles marked Example show how this page works. More founder profiles appear here soon. Want your profile and projects here? Come to a Coffee & Calling evening and tell us what you are building.",
    "nl": "Profielen met het label Voorbeeld laten zien hoe deze pagina werkt. Binnenkort verschijnen hier meer founders. Wil je jouw profiel en projecten hier? Kom naar een Coffee & Calling avond en vertel ons wat je bouwt.",
}


# ─────────────────────────── Helpers ───────────────────────────

def url(lang, path):
    return PREFIX[lang] + path


def abs_url(lang, path):
    return DOMAIN + url(lang, path)


def out_path(lang, path):
    p = ROOT / PREFIX[lang].lstrip("/") / path.strip("/")
    return p / "index.html"


def fmt_date(lang, iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {T[lang]['months'][d.month - 1]} {d.year}"


def logo(size=26, white=False):
    return (f'<img class="logo-mark" src="/assets/brand/icon-{"white" if white else "black"}.svg" '
            f'width="{size}" height="{size}" alt="">')


def wordmark(white=False, h=24, cls="wordmark"):
    w = round(h * (643 / 101 if white else 318 / 48))
    return (f'<img class="{cls}" src="/assets/brand/logo-full-{"white" if white else "black"}.svg" '
            f'width="{w}" height="{h}" alt="Christian Tech Founders">')


def barcode(color="#0B0B0B", cls="barcode"):
    widths = [10, 3, 10, 3, 10, 3, 9, 3, 6, 3, 4, 3, 2, 3, 2, 2, 1]
    x, rects = 0, []
    for i, w in enumerate(widths):
        if i % 2 == 0:
            rects.append(f'<rect x="{x}" width="{w}" height="40"/>')
        x += w
    return f'<svg class="{cls}" viewBox="0 0 {x} 40" fill="{color}" aria-hidden="true">{"".join(rects)}</svg>'


def cross_icon():
    return '<svg viewBox="0 0 14 18" aria-hidden="true"><path d="M5 0h4v5h5v4H9v9H5V9H0V5h5z" fill="#fff"/></svg>'


def label(text):
    return f'<span class="label">{esc(text)}</span>'


def ticket_head(title="Christian Tech Founders", bar=True):
    mark = wordmark(h=26) if title == "Christian Tech Founders" else f'{logo()}<span class="brand">{esc(title)}</span>'
    return f'<div class="ticket-head">{mark}{barcode() if bar else ""}</div>'


def ld(graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"


ORG = {"@type": "Organization", "@id": DOMAIN + "/#organization", "name": "Christian Tech Founders", "url": DOMAIN + "/",
       "logo": DOMAIN + "/assets/brand/logo-full-black.svg",
       "description": "A community for Christian entrepreneurs and builders in tech who put God first. Sunday evenings with worship and prayer, sermons on AI and technology, talent alignment sessions and project support."}
SITE = {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "Christian Tech Founders",
        "publisher": {"@id": DOMAIN + "/#organization"}, "inLanguage": ["en", "nl"]}


def breadcrumb(lang, items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(lang, p)} for i, (n, p) in enumerate(items)]}


# ─────────────────────────── Layout ───────────────────────────

def page(lang, path, title, desc, main, active=None, schema=None, og_image=POSTER, og_type="website", scripts=""):
    t = T[lang]
    other = "nl" if lang == "en" else "en"
    nav = [("about", "/about/"), ("founders", "/founders/"), ("partners", "/partners/"), ("insights", "/insights/"), ("library", "/library/")]
    links = "".join(
        f'<a href="{url(lang, p)}"{" aria-current=\"page\"" if active == k else ""}>{t["nav_" + k]}</a>' for k, p in nav)
    lang_sw = (f'<span class="lang"><a href="{url("en", path)}" class="{"on" if lang == "en" else ""}" hreflang="en" lang="en">EN</a>'
               f'<a href="{url("nl", path)}" class="{"on" if lang == "nl" else ""}" hreflang="nl" lang="nl">NL</a></span>')
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(l, path)}">' for l in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{abs_url("en", path)}">'
    footer_links = "".join(f'<li><a href="{url(lang, p)}">{t["nav_" + k]}</a></li>' for k, p in nav)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{abs_url(lang, path)}">
{alt}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{abs_url(lang, path)}">
<meta property="og:image" content="{DOMAIN}{og_image}">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'nl_NL'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#D3D3D3">
<link rel="icon" href="/assets/brand/icon-black.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Silkscreen:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{ld(schema) if schema else ""}
</head>
<body>
<a class="skip" href="#main" style="position:absolute;left:-9999px">{t["skip"]}</a>
<header class="site-header">
  <div class="wrap hdr">
    <a class="hdr-brand" href="{url(lang, '/')}" aria-label="Christian Tech Founders">{wordmark(h=24)}</a>
    <button class="menu-btn" aria-label="{t['menu']}" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="hdr-nav" id="nav">
      {links}
      {lang_sw}
      <a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t["join"]}</a>
    </nav>
    {barcode()}
  </div>
</header>
<main id="main">
{main}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="ftr">
      <div>
        <div class="ftr-brand">{wordmark(white=True, h=30)}</div>
        <p class="muted" style="color:rgba(255,255,255,.65);max-width:360px;font-size:14px">{t["footer_tag"]}</p>
      </div>
      <div><h4>{t["explore"]}</h4><ul>{footer_links}<li><a href="{url(lang, '/')}#event">{t["nav_event"]}</a></li></ul></div>
      <div><h4>{t["connect"]}</h4><ul><li><a href="{LUMA}" target="_blank" rel="noopener">{t["signup"]}</a></li><li><a href="{url(other, path)}" hreflang="{other}">{t["switch"]}</a></li></ul></div>
    </div>
    <div class="ftr-bottom"><span>&copy; {YEAR} Christian Tech Founders</span>{barcode("#fff")}</div>
  </div>
</footer>
<script>
(function(){{var b=document.querySelector('.menu-btn'),n=document.getElementById('nav');if(!b)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});}})();
</script>
{scripts}
</body>
</html>
"""


def write(lang, path, doc):
    p = out_path(lang, path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")


# ─────────────────────────── Content loading ───────────────────────────

def parse_post(file):
    text = file.read_text(encoding="utf-8")
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    m = re.search(r"^# (.+)$", body, re.M)
    meta["h1"] = m.group(1).strip()
    body = body[:m.start()] + body[m.end():]
    words = len(re.findall(r"\w+", body))
    meta["minutes"] = max(1, math.ceil(words / 220))
    meta["words"] = words
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"])
    h = md.convert(body.strip())
    h = h.replace("<p>", '<p class="lead-p">', 1)
    h = h.replace("<img ", '<img loading="lazy" ', )
    h = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', h)
    meta["html"] = h
    return meta


def load_posts(lang):
    posts = [parse_post(f) for f in sorted((SRC / "content" / "insights" / lang).glob("*.md"))]
    posts.sort(key=lambda p: (p["slug"] != EVENT_SLUG, p["date"]), reverse=False)
    event = [p for p in posts if p["slug"] == EVENT_SLUG]
    rest = sorted([p for p in posts if p["slug"] != EVENT_SLUG], key=lambda p: p["date"], reverse=True)
    return event + rest


# ─────────────────────────── Components ───────────────────────────

def post_card(lang, p, big=False):
    t = T[lang]
    img = ""
    if big and p.get("image"):
        img = f'<img src="{p["image"]}" alt="{esc(p.get("image_alt", ""))}" width="1581" height="1263" loading="lazy" style="border-bottom:var(--line);background:var(--paper)">'
    return f"""<a class="ticket" href="{url(lang, '/insights/' + p['slug'] + '/')}">
  <div class="card-head"><span>{esc(p['category'])}</span>{barcode()}</div>
  {img}
  <div class="card-body">
    <span class="muted" style="font-size:12px">{fmt_date(lang, p['date'])} / {p['minutes']} {t['min']}</span>
    <h3 class="h3">{esc(p['h1'])}</h3>
    <p>{esc(p['description'])}</p>
    <span class="more">{t['read_more']} <span class="arrow">&rarr;</span></span>
  </div>
</a>"""


def cta_ticket(lang):
    t = T[lang]
    return f"""<div class="ticket cta-ticket">
  {ticket_head("Coffee & Calling")}
  <div class="ticket-body">
    <h2 class="h2" style="font-size:clamp(26px,3.4vw,40px)">{t['cta_title']}</h2>
    <p class="lead">{esc(t['cta_text'])}</p>
    <div class="btn-row"><a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t['signup']} <span class="arrow">&rarr;</span></a></div>
  </div>
</div>"""


def page_hero(lang, kicker, h1, lead_text, pixel_word):
    return f"""<section class="hero">
  <div class="wrap">
    <div class="ticket">
      {ticket_head()}
      <div class="ticket-body hero-grid" style="grid-template-columns:1.5fr 1fr">
        <div>
          {label(kicker)}
          <h1 class="h1">{esc(h1)}</h1>
          <p class="lead">{esc(lead_text)}</p>
        </div>
        <div class="cosmos cosmos-panel" style="aspect-ratio:4/3"><span class="pixel">{esc(pixel_word)}</span></div>
      </div>
    </div>
  </div>
</section>"""


# ─────────────────────────── Pages ───────────────────────────

def build_home(lang, posts):
    h, t = HOME[lang], T[lang]
    offer = "".join(f"""<div class="ticket"><div class="card-head"><span>{esc(a)}</span>{barcode()}</div>
      <div class="card-body"><h3 class="h3">{esc(b)}</h3><p>{esc(c)}</p></div></div>""" for a, b, c in h["offer"])
    steps = "".join(f"""<div class="ticket"><div class="card-head"><span>Step 0{i + 1}</span>{barcode()}</div>
      <div class="card-body"><span class="pixel ink step-num">0{i + 1}</span><h3 class="h3">{esc(a)}</h3><p>{esc(b)}</p></div></div>""" for i, (a, b) in enumerate(h["steps"]))
    if lang == "nl":
        steps = steps.replace(">Step 0", ">Stap 0")
    facts = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in h["facts"])
    cards = "".join(post_card(lang, p) for p in [q for q in posts if q["slug"] != EVENT_SLUG][:3])
    main = f"""
<section class="hero">
  <div class="wrap">
    <div class="ticket">
      {ticket_head()}
      <div class="ticket-body hero-grid">
        <div>
          {label(h['hero_label'])}
          <h1 class="h1">{esc(h['h1'])}</h1>
          <p class="lead">{esc(h['lead'])}</p>
          <div class="btn-row">
            <a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t['join']} <span class="arrow">&rarr;</span></a>
            <a class="btn alt" href="#how">{h['how']}</a>
          </div>
        </div>
        <div>
          <div class="cosmos cosmos-panel"><span class="pixel">Amsterdam</span></div>
          <div class="hero-meta"><span>{esc(h['meta_l'])}</span><span>{esc(h['meta_r'])}</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band on-dark snake-sec" id="problem" data-snake aria-label="{esc(h['play_aria'])}">
  <canvas role="img" aria-label="{esc(h['play_aria'])}"></canvas>
  <div class="play-hud">
    <span>{esc(h['play_label'])}</span>
    <span class="score" aria-live="polite">{cross_icon()}<span>{h['score']} <span data-score>0</span></span><span style="opacity:.6">{h['best']} <span data-best>0</span></span></span>
  </div>
  <div class="wrap narrow snake-copy" style="margin:0 auto">
    <div class="sec-head">{label(h['p_label'])}<h2 class="h2">{esc(h['p_h2'])}</h2></div>
    <p class="lead" style="max-width:none;margin-bottom:18px">{h['p1']}</p>
    <p class="lead" style="max-width:none">{esc(h['p2'])}</p>
  </div>
  <div class="play-hint">{esc(h['play_hint'])}</div>
  <div class="play-over"><div><span class="pixel">{esc(h['over'])}</span><p style="font-weight:700;text-transform:uppercase;letter-spacing:.08em">{h['score']}: <span data-over-score>0</span></p><p style="margin-top:10px;font-size:12px;opacity:.8">{esc(h['over_again'])}</p></div></div>
</section>

<section id="why">
  <div class="wrap">
    <div class="ticket">
      {ticket_head()}
      <div class="ticket-body" style="max-width:860px">
        <div class="sec-head" style="margin-bottom:22px">{label(h['g_label'])}<h2 class="h2">{esc(h['g_h2'])}</h2></div>
        <p class="lead" style="max-width:none;margin-bottom:16px">{esc(h['g1'])}</p>
        <p class="lead" style="max-width:none;margin-bottom:16px">{esc(h['g2'])}</p>
        <p class="lead" style="max-width:none">{esc(h['g3'])}</p>
      </div>
    </div>
  </div>
</section>

<section id="offer" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(h['o_label'])}<h2 class="h2">{esc(h['o_h2'])}</h2></div>
    <div class="grid g4">{offer}</div>
  </div>
</section>

<section id="how" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(h['s_label'])}<h2 class="h2">{esc(h['s_h2'])}</h2></div>
    <div class="grid g3">{steps}</div>
  </div>
</section>

<section id="event" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(h['e_label'])}</div>
    <div class="ticket">
      {ticket_head("Coffee & Calling")}
      <div class="event-grid">
        <div class="poster"><img src="{POSTER}" alt="Coffee &amp; Calling Amsterdam poster" width="1581" height="1263" loading="lazy"></div>
        <div class="ticket-body">
          <h2 class="h2">Coffee &amp; Calling</h2>
          <p class="pixel ink" style="font-size:clamp(18px,2.2vw,26px);margin:14px 0 18px">{esc(h['e_sub'])}</p>
          <p class="muted">{esc(h['e_text'])}</p>
          <ul class="facts">{facts}</ul>
          <div class="btn-row">
            <a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t['signup']} <span class="arrow">&rarr;</span></a>
            <a class="btn alt" href="{url(lang, '/insights/' + EVENT_SLUG + '/')}">{t['read_more']}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head" style="grid-template-columns:1fr auto;align-items:end">
      <div style="display:grid;gap:16px">{label(h['i_label'])}<h2 class="h2">{esc(h['i_h2'])}</h2></div>
      <a class="btn alt" href="{url(lang, '/insights/')}">{t['all_insights']} <span class="arrow">&rarr;</span></a>
    </div>
    <div class="grid g3">{cards}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="ticket">
      {ticket_head()}
      <div class="ticket-body hero-grid" style="grid-template-columns:1.4fr 1fr">
        <div>
          {label(h['f_label'])}
          <h2 class="h2" style="margin:16px 0 18px">{esc(h['f_h2'])}</h2>
          <p class="lead" style="margin-bottom:26px">{esc(h['f_lead'])}</p>
          <a class="btn" href="{url(lang, '/founders/')}">{h['f_btn']} <span class="arrow">&rarr;</span></a>
        </div>
        <div class="grid g2" style="gap:14px">
          {"".join(f'<div class="cosmos" style="aspect-ratio:1;border:var(--line);display:flex;align-items:flex-end;padding:12px"><span class="pixel" style="font-size:34px">{x}</span></div>' for x in ["EA", "EB", "EC", "+"])}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cosmos dim band on-dark cta-band">
  <div class="wrap">
    {label("Coffee & Calling")}
    <h2 class="h2">{esc(h['c_h2'])}</h2>
    <p class="lead">{esc(h['c_lead'])}</p>
    <div class="btn-row">
      <a class="btn light" href="{LUMA}" target="_blank" rel="noopener">{t['join']} <span class="arrow">&rarr;</span></a>
      <a class="btn" href="{url(lang, '/insights/')}">{h['c_btn2']}</a>
    </div>
  </div>
</section>

"""
    schema = [ORG, SITE]
    write(lang, "/", page(lang, "/", h["title"], h["desc"], main, schema=schema,
                          scripts='<script src="/assets/js/snake.js" defer></script>'))


def build_insights(lang, posts):
    title, desc, h1, lead_text = PAGES["insights"][lang]
    t = T[lang]
    featured = posts[0]
    rest = "".join(post_card(lang, p) for p in posts[1:])
    main = page_hero(lang, "Christian Tech Founders / " + h1, h1, lead_text, "Insights") + f"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="grid" style="grid-template-columns:1fr">{post_card(lang, featured, big=False).replace('<div class="card-body">', '<div class="card-body" style="padding:28px 26px 30px">', 1)}</div>
    <div class="grid g3" style="margin-top:22px">{rest}</div>
  </div>
</section>"""
    schema = [ORG, {"@type": "CollectionPage", "@id": abs_url(lang, "/insights/") + "#page", "url": abs_url(lang, "/insights/"),
                    "name": title, "inLanguage": lang, "isPartOf": {"@id": DOMAIN + "/#website"}},
              breadcrumb(lang, [(t["home"], "/"), (h1, "/insights/")])]
    write(lang, "/insights/", page(lang, "/insights/", title, desc, main, active="insights", schema=schema))


def build_post(lang, p, posts):
    t = T[lang]
    path = f"/insights/{p['slug']}/"
    others = [o for o in posts if o["slug"] != p["slug"]][:2]
    more = "".join(post_card(lang, o) for o in others)
    main = f"""
<section class="post-hero" style="padding-bottom:0">
  <div class="wrap">
    <a class="more" href="{url(lang, '/insights/')}" style="text-decoration:none"><span class="arrow">&larr;</span> {t['back_insights']}</a>
    <div class="ticket" style="margin-top:18px">
      {ticket_head()}
      <div class="ticket-body">
        {label(p['category'])}
        <h1 class="h1">{esc(p['h1'])}</h1>
        <div class="post-meta"><span class="chip">{fmt_date(lang, p['date'])}</span><span class="chip">{p['minutes']} {t['min']}</span><span class="chip grad">Christian Tech Founders</span></div>
      </div>
    </div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <article class="article-wrap">
      <div class="prose">
{p['html']}
      </div>
    </article>
    {cta_ticket(lang)}
    <div class="sec-head" style="margin-top:72px">{label(t['more_insights'])}</div>
    <div class="grid g2">{more}</div>
  </div>
</section>"""
    page_url = abs_url(lang, path)
    img = DOMAIN + (p.get("image") or POSTER)
    graph = [ORG, SITE,
             {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": p["title"], "inLanguage": lang,
              "isPartOf": {"@id": DOMAIN + "/#website"}, "breadcrumb": {"@id": page_url + "#breadcrumb"},
              "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".lead-p"]}},
             dict(breadcrumb(lang, [(t["home"], "/"), ("Insights", "/insights/"), (p["h1"], path)]), **{"@id": page_url + "#breadcrumb"}),
             {"@type": "BlogPosting", "@id": page_url + "#article", "headline": p["h1"], "description": p["description"],
              "url": page_url, "image": img, "datePublished": p["date"], "dateModified": p["date"], "inLanguage": lang,
              "author": {"@id": DOMAIN + "/#organization"}, "publisher": {"@id": DOMAIN + "/#organization"},
              "mainEntityOfPage": {"@id": page_url + "#webpage"}, "keywords": p.get("keyword", ""),
              "wordCount": p["words"], "timeRequired": f"PT{p['minutes']}M"}]
    if p["slug"] == EVENT_SLUG:
        graph[-1]["about"] = {"@id": page_url + "#event"}
        graph.append({"@type": "Event", "@id": page_url + "#event",
                      "name": "Aligning Your Business With God: Coffee & Calling Amsterdam",
                      "description": "An evening for Christian entrepreneurs and builders in tech with dinner, open worship, a sermon on technology, AI and our role in the world, discussion and networking. Optional coworking from 13:00.",
                      "startDate": "2027-01-10T18:00:00+01:00", "endDate": "2027-01-10T22:00:00+01:00",
                      "eventStatus": "https://schema.org/EventScheduled",
                      "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                      "location": {"@type": "Place", "name": "Amsterdam", "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressCountry": "NL"}},
                      "image": DOMAIN + POSTER, "url": LUMA, "isAccessibleForFree": False,
                      "offers": {"@type": "Offer", "url": LUMA, "priceCurrency": "EUR", "price": "0.50",
                                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": "0.50", "priceCurrency": "EUR", "description": "Pay what you want, from 0.50 euro"}},
                      "organizer": {"@id": DOMAIN + "/#organization"}})
    write(lang, path, page(lang, path, p["title"], p["description"], main, active="insights", schema=graph,
                           og_image=p.get("image") or POSTER, og_type="article"))


def build_library(lang, lib):
    title, desc, h1, lead_text = PAGES["library"][lang]
    t, L = T[lang], LIB[lang]
    findings = "".join(f"""<div class="ticket"><div class="card-head"><span>{t['from_notes']} / {fmt_date(lang, f['date'])}</span>{barcode()}</div>
      <div class="card-body"><h3 class="h3">{esc(f['title'][lang])}</h3><p>{esc(f['body'][lang])}</p>
      <a class="more" href="{url(lang, f['link'])}">{t['related']} <span class="arrow">&rarr;</span></a></div></div>""" for f in lib["findings"])
    listen = "".join(f"""<a class="ticket" href="{esc(r['url'])}" target="_blank" rel="noopener"><div class="card-head"><span>{esc(r['type'][lang])}</span>{barcode()}</div>
      <div class="card-body"><h3 class="h3">{esc(r['title'])}</h3><span class="muted" style="font-size:12px">{esc(r['by'])}</span><p>{esc(r['desc'][lang])}</p>
      <span class="more">{t['listen'] if r['type']['en'] == 'Podcast' else t['visit']} <span class="arrow">&nearr;</span></span></div></a>""" for r in lib["listen"])
    main = page_hero(lang, "Christian Tech Founders / " + h1, h1, lead_text, "Align") + f"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(L['f_label'])}<p class="lead">{esc(L['f_lead'])}</p></div>
    <div class="grid g3">{findings}</div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(L['l_label'])}<p class="lead">{esc(L['l_lead'])}</p></div>
    <div class="grid g4">{listen}</div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(L['r_label'])}</div>
    <div class="ticket">
      {ticket_head("Coffee & Calling / Recordings")}
      <div class="ticket-body hero-grid" style="grid-template-columns:1.4fr 1fr">
        <div><h2 class="h2" style="font-size:clamp(26px,3.4vw,40px);margin-bottom:16px">{esc(L['r_title'])}</h2>
        <p class="lead" style="margin-bottom:24px">{esc(L['r_text'])}</p>
        <a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t['signup']} <span class="arrow">&rarr;</span></a></div>
        <div class="cosmos cosmos-panel" style="aspect-ratio:16/10"><span class="pixel" style="font-size:clamp(26px,4vw,48px)">Soon</span></div>
      </div>
    </div>
  </div>
</section>"""
    schema = [ORG, breadcrumb(lang, [(t["home"], "/"), (h1, "/library/")])]
    write(lang, "/library/", page(lang, "/library/", title, desc, main, active="library", schema=schema))


def avatar(initials, photo=None, name=""):
    if photo:
        return (f'<div class="cosmos avatar photo"><img src="{photo}" alt="{esc(name)}" width="616" height="876" loading="lazy">'
                f'</div>')
    return f'<div class="cosmos avatar"><span class="pixel">{esc(initials)}</span></div>'


def build_founders(lang, founders):
    title, desc, h1, lead_text = PAGES["founders"][lang]
    t = T[lang]
    cards = ""
    for f in founders:
        n = len(f["projects"])
        count = (t["project_count"] if n == 1 else t["project_count_pl"]).format(n=n)
        badge = f'<span class="badge">{t["example"]}</span>' if f.get("example") else ""
        cards += f"""<a class="ticket" href="{url(lang, '/founders/' + f['slug'] + '/')}">
  <div class="card-head"><span>{esc(f['location'])}</span>{badge}</div>
  {avatar(f['initials'], f.get('photo'), f['name'])}
  <div class="card-body"><h3 class="h3">{esc(f['name'])}</h3><span class="muted" style="font-size:13px">{esc(f['role'][lang])}</span>
  <div class="chips">{"".join(f'<span class="chip">{esc(x)}</span>' for x in f['tags'])}</div>
  <span class="more">{count} <span class="arrow">&rarr;</span></span></div>
</a>"""
    main = page_hero(lang, "Christian Tech Founders / " + h1, h1, lead_text, "Builders") + f"""
<section style="padding-top:0">
  <div class="wrap">
    <p class="notice" style="margin-bottom:28px">{esc(FOUNDERS_NOTICE[lang])}</p>
    <div class="grid g3">{cards}</div>
  </div>
</section>"""
    schema = [ORG, breadcrumb(lang, [(t["home"], "/"), (h1, "/founders/")])]
    write(lang, "/founders/", page(lang, "/founders/", title, desc, main, active="founders", schema=schema))

    for f in founders:
        path = f"/founders/{f['slug']}/"
        badge = f'<span class="badge">{t["example"]}</span>' if f.get("example") else ""
        projects = "".join(f"""<div class="ticket"><div class="card-head"><span>{t['stage']}: {esc(p['stage'][lang])}</span>{barcode()}</div>
  <div class="card-body"><h3 class="h3">{esc(p['name'])}</h3><p>{esc(p['summary'][lang])}</p>
  {(f'<span class="label" style="margin-top:4px">{t["looking_for"]}</span><div class="chips">' + "".join(f'<span class="chip grad">{esc(x)}</span>' for x in p['looking_for'][lang]) + '</div>') if p['looking_for'][lang] else ""}
  {f'<a class="more" href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["url"].split("//")[1])} <span class="arrow">&nearr;</span></a>' if p.get("url") else ""}</div></div>""" for p in f["projects"])
        main = f"""
<section class="post-hero" style="padding-bottom:0">
  <div class="wrap">
    <a class="more" href="{url(lang, '/founders/')}" style="text-decoration:none"><span class="arrow">&larr;</span> {t['all_founders']}</a>
    <div class="ticket" style="margin-top:18px">
      {ticket_head()}
      <div class="founder-top">
        {avatar(f['initials'], f.get('photo'), f['name'])}
        <div class="ticket-body">
          <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">{label(f['location'])}{badge}</div>
          <h1 class="h1" style="font-size:clamp(32px,5vw,60px);margin:16px 0 10px">{esc(f['name'])}</h1>
          <p style="font-weight:700;margin-bottom:14px">{esc(f['role'][lang])}</p>
          <p class="lead">{esc(f['bio'][lang])}</p>
          <div class="chips" style="margin-top:18px">{"".join(f'<span class="chip">{esc(x)}</span>' for x in f['tags'])}</div>
          {('<div class="btn-row" style="margin-top:22px">' + "".join(f'<a class="btn alt" href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])} <span class="arrow">&nearr;</span></a>' for l in f["links"]) + '</div>') if f.get("links") else ""}
        </div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head">{label(t['projects'])}</div>
    <div class="grid g2">{projects}</div>
    <div class="ticket cta-ticket">
      {ticket_head("Coffee & Calling")}
      <div class="ticket-body">
        <h2 class="h2" style="font-size:clamp(26px,3.4vw,40px)">{esc(t['help_title'])}</h2>
        <p class="lead">{esc(t['help_text'])}</p>
        <div class="btn-row"><a class="btn" href="{LUMA}" target="_blank" rel="noopener">{t['signup']} <span class="arrow">&rarr;</span></a></div>
      </div>
    </div>
  </div>
</section>"""
        ftitle = f"{f['name']} | Christian Tech Founders"
        fdesc = f"{f['role'][lang]}. {f['bio'][lang]}"[:158]
        doc = page(lang, path, ftitle, fdesc, main, active="founders",
                   schema=[ORG, breadcrumb(lang, [(t["home"], "/"), ("Founders", "/founders/"), (f["name"], path)])])
        if f.get("example"):
            doc = doc.replace("<meta charset=\"UTF-8\">", "<meta charset=\"UTF-8\">\n<meta name=\"robots\" content=\"noindex\">", 1)
        write(lang, path, doc)


# ─────────────────────────── About, Partners, Thanks ───────────────────────────

ABOUT = {
    "en": {
        "title": "About Christian Tech Founders | Builders Who Put God First",
        "desc": "Christian Tech Founders brings Christ-led founders and builders in tech together in Amsterdam. Read our story, what we believe and who is behind it.",
        "h1": "Builders who put God first",
        "lead": "Christian Tech Founders brings Christ-led founders and builders in tech together, so nobody has to carry their calling alone.",
        "s_label": "[01] How it started", "s_h2": "Two worlds that did not understand each other.",
        "story": [
            "The idea for CTF came from a simple observation. In church, the entrepreneurial and technical side of people was not really understood. In the tech world, deeper meaning was not valued.",
            "The first gathering in 2025 drew around forty people. Too many, too mixed in level and too shallow to go deep. That was the lesson learned.",
            "Since April 2026 we work in smaller groups around real projects, next to evenings like Coffee & Calling that are open to everyone who feels drawn to them.",
        ],
        "b_label": "[02] What we believe", "b_h2": "What drives us",
        "beliefs": ["Excellence and meaning belong together", "What we build shapes people and culture", "Responsibility comes with power", "The right people in one place speed each other up"],
        "b_text": "We believe a calling from God means standing where your talents fit best. There, like a kaleidoscope, you shine His light onto as many people as possible, as strongly as possible.",
        "f_label": "[03] Who is behind it", "f_profile": "View founder profile",
        "c_h2": "Sound like your people?",
    },
    "nl": {
        "title": "Over Christian Tech Founders | Bouwers die God op één zetten",
        "desc": "Christian Tech Founders brengt founders en bouwers in tech die Christus volgen samen in Amsterdam. Lees ons verhaal, wat we geloven en wie erachter zit.",
        "h1": "Bouwers die God op één zetten",
        "lead": "Christian Tech Founders brengt founders en bouwers in tech die Christus volgen samen, zodat niemand zijn roeping alleen hoeft te dragen.",
        "s_label": "[01] Hoe het begon", "s_h2": "Twee werelden die elkaar niet begrepen.",
        "story": [
            "Het idee voor CTF ontstond uit een eenvoudige observatie. In de kerk werden de ondernemende en technische kanten van mensen niet begrepen. In de tech-wereld werd diepere zingeving niet gewaardeerd.",
            "De eerste gathering in 2025 trok zo'n veertig mensen. Te veel, te divers in niveau en te oppervlakkig om diep te kunnen gaan. Dat was de lesson learned.",
            "Sinds april 2026 werken we in kleinere groepen rond echte projecten, naast avonden zoals Coffee & Calling die open zijn voor iedereen die zich aangetrokken voelt.",
        ],
        "b_label": "[02] Wat we geloven", "b_h2": "Wat ons drijft",
        "beliefs": ["Excellentie en betekenis horen samen", "Wat we bouwen vormt mensen en cultuur", "Verantwoordelijkheid hoort bij macht", "De juiste mensen op één plek versnellen elkaar"],
        "b_text": "Wij geloven dat een roeping van God betekent dat je staat waar je talenten het beste passen. Daar laat je, als een caleidoscoop, Zijn licht schijnen op zoveel mogelijk mensen en zo sterk mogelijk.",
        "f_label": "[03] Wie erachter zit", "f_profile": "Bekijk founderprofiel",
        "c_h2": "Klinkt dit als jouw mensen?",
    },
}

PARTNERS = {
    "en": {
        "title": "Partners | Christian Tech Founders",
        "desc": "Partners of Christian Tech Founders. Join as a partner, or submit your project if your Christian company needs developers, designers or other technical people.",
        "h1": "Partners",
        "lead": "Companies and initiatives that help Christ-led founders build. Want to partner with us, or does your Christian company need technical people? Let us know.",
        "p_label": "[01] Our partners", "visit": "Visit",
        "j_label": "[02] Become a partner", "j_h2": "Partner with us",
        "j_lead": "Do you want to support Christ-led founders with space, services, sponsoring or expertise? Tell us about your company.",
        "s_label": "[03] Submit a project", "s_h2": "Need technical people?",
        "s_lead": "Are you a Christian company, church or ministry looking for developers, designers or other technical people? Submit your project. With or without a budget, we look for the right fit in our community.",
        "company": "Company", "org": "Organisation", "website": "Website", "contact": "Your name", "email": "Email", "message": "Message",
        "ptype": "How would you like to partner?", "ptypes": ["Sponsor events", "Host a space", "Offer services or expertise", "Other"],
        "ptitle": "Project title", "pdesc": "What do you need help with?", "skills": "Which skills are you looking for?",
        "skill_opts": ["Development", "Design", "AI & data", "Product", "Marketing", "Other"],
        "budget": "Budget", "budget_opts": ["No budget (volunteers or pro bono)", "Budget available", "Not sure yet"],
        "range": "Budget range", "range_opts": ["Under €1,000", "€1,000 to €5,000", "€5,000 to €20,000", "More than €20,000"],
        "timeline": "Timeline", "timeline_opts": ["As soon as possible", "Within 3 months", "Later this year", "Flexible"],
        "consent": "I agree that Christian Tech Founders shares this project with suitable people in the community.",
        "choose": "Choose...", "send_partner": "Send partner request", "send_project": "Submit project",
        "note": "We read every submission and get back to you.", "required": "required",
    },
    "nl": {
        "title": "Partners | Christian Tech Founders",
        "desc": "Partners van Christian Tech Founders. Word partner, of dien je project in als je christelijke bedrijf developers, designers of andere technische mensen zoekt.",
        "h1": "Partners",
        "lead": "Bedrijven en initiatieven die founders die Christus volgen helpen bouwen. Wil je partner worden, of zoekt je christelijke bedrijf technische mensen? Laat het ons weten.",
        "p_label": "[01] Onze partners", "visit": "Bekijk",
        "j_label": "[02] Word partner", "j_h2": "Word partner",
        "j_lead": "Wil je founders die Christus volgen steunen met ruimte, diensten, sponsoring of expertise? Vertel ons over je bedrijf.",
        "s_label": "[03] Dien een project in", "s_h2": "Technische mensen nodig?",
        "s_lead": "Ben je een christelijk bedrijf, kerk of bediening en zoek je developers, designers of andere technische mensen? Dien je project in. Met of zonder budget, wij zoeken de juiste match in onze community.",
        "company": "Bedrijf", "org": "Organisatie", "website": "Website", "contact": "Je naam", "email": "E-mail", "message": "Bericht",
        "ptype": "Hoe wil je partner zijn?", "ptypes": ["Events sponsoren", "Een ruimte aanbieden", "Diensten of expertise aanbieden", "Anders"],
        "ptitle": "Projectnaam", "pdesc": "Waar heb je hulp bij nodig?", "skills": "Welke skills zoek je?",
        "skill_opts": ["Development", "Design", "AI & data", "Product", "Marketing", "Anders"],
        "budget": "Budget", "budget_opts": ["Geen budget (vrijwilligers of pro bono)", "Budget beschikbaar", "Weet ik nog niet"],
        "range": "Indicatie budget", "range_opts": ["Minder dan €1.000", "€1.000 tot €5.000", "€5.000 tot €20.000", "Meer dan €20.000"],
        "timeline": "Planning", "timeline_opts": ["Zo snel mogelijk", "Binnen 3 maanden", "Later dit jaar", "Flexibel"],
        "consent": "Ik ga ermee akkoord dat Christian Tech Founders dit project deelt met geschikte mensen in de community.",
        "choose": "Kies...", "send_partner": "Verstuur partneraanvraag", "send_project": "Project indienen",
        "note": "We lezen elke inzending en nemen contact met je op.", "required": "verplicht",
    },
}

THANKS = {
    "en": ("Thank you | Christian Tech Founders", "Thank you", "We received your message and will get back to you soon. In the meantime, read our insights or join the next Coffee & Calling.", "Back to home", "Read the insights"),
    "nl": ("Bedankt | Christian Tech Founders", "Bedankt", "We hebben je bericht ontvangen en nemen snel contact met je op. Lees in de tussentijd onze insights of kom naar de volgende Coffee & Calling.", "Terug naar home", "Lees de insights"),
}


def build_about(lang, me):
    a, t = ABOUT[lang], T[lang]
    story = "".join(f'<p class="lead" style="max-width:none;margin-bottom:16px">{esc(x)}</p>' for x in a["story"])
    beliefs = "".join(f'<li><span class="pixel ink">0{i + 1}</span><span>{esc(x)}</span></li>' for i, x in enumerate(a["beliefs"]))
    links = "".join(f'<a class="btn alt" href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])} <span class="arrow">&nearr;</span></a>' for l in me["links"])
    main = page_hero(lang, "Christian Tech Founders / " + t["nav_about"], a["h1"], a["lead"], "2025") + f"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="ticket">
      {ticket_head()}
      <div class="ticket-body" style="max-width:860px">
        <div class="sec-head" style="margin-bottom:22px">{label(a['s_label'])}<h2 class="h2">{esc(a['s_h2'])}</h2></div>
        {story}
      </div>
    </div>
  </div>
</section>
<section class="cosmos dim band on-dark">
  <div class="wrap narrow" style="margin:0 auto">
    <div class="sec-head">{label(a['b_label'])}<h2 class="h2">{esc(a['b_h2'])}</h2></div>
    <ul class="belief-list">{beliefs}</ul>
    <p class="lead" style="max-width:none;margin-top:28px">{esc(a['b_text'])}</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head">{label(a['f_label'])}</div>
    <div class="ticket">
      {ticket_head()}
      <div class="founder-top">
        {avatar(me['initials'], me.get('photo'), me['name'])}
        <div class="ticket-body">
          {label(me['location'])}
          <h2 class="h1" style="font-size:clamp(32px,5vw,60px);margin:16px 0 10px">{esc(me['name'])}</h2>
          <p style="font-weight:700;margin-bottom:14px">{esc(me['role'][lang])}</p>
          <p class="lead">{esc(me['bio'][lang])}</p>
          <div class="btn-row" style="margin-top:24px">{links}</div>
          <a class="more" style="display:inline-block;margin-top:22px" href="{url(lang, '/founders/' + me['slug'] + '/')}">{a['f_profile']} <span class="arrow">&rarr;</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="cosmos dim band on-dark cta-band">
  <div class="wrap">
    {label("Coffee & Calling")}
    <h2 class="h2">{esc(a['c_h2'])}</h2>
    <div class="btn-row" style="margin-top:28px">
      <a class="btn light" href="{LUMA}" target="_blank" rel="noopener">{t['join']} <span class="arrow">&rarr;</span></a>
      <a class="btn" href="{url(lang, '/partners/')}">{t['nav_partners']}</a>
    </div>
  </div>
</section>"""
    page_url = abs_url(lang, "/about/")
    person = {"@type": "Person", "@id": DOMAIN + "/#founder", "name": me["name"], "jobTitle": "Founder",
              "image": DOMAIN + me["photo"], "worksFor": {"@id": DOMAIN + "/#organization"},
              "sameAs": [l["url"] for l in me["links"] if "viralistic" in l["url"]]}
    org = dict(ORG, founder={"@id": DOMAIN + "/#founder"})
    schema = [org, person, {"@type": "AboutPage", "@id": page_url + "#page", "url": page_url, "name": a["title"], "inLanguage": lang,
                            "about": {"@id": DOMAIN + "/#organization"}},
              breadcrumb(lang, [(t["home"], "/"), (t["nav_about"], "/about/")])]
    write(lang, "/about/", page(lang, "/about/", a["title"], a["desc"], main, active="about", schema=schema))


def field(label_text, inner, full=False, req=False, rq=""):
    star = f' <abbr title="{rq}">*</abbr>' if req else ""
    return f'<label class="field{" full" if full else ""}"><span>{esc(label_text)}{star}</span>{inner}</label>'


def build_partners(lang, partners):
    P, t = PARTNERS[lang], T[lang]
    thanks = url(lang, "/thanks/")
    rq = P["required"]
    cards = "".join(f"""<a class="ticket" href="{esc(p['url'])}" target="_blank" rel="noopener">
  <div class="card-head"><span>{esc(p['domain'])}</span>{barcode()}</div>
  <div class="cosmos partner-mark"><span class="pixel">{esc(p['name'])}</span></div>
  <div class="card-body"><h3 class="h3">{esc(p['name'])}</h3><p>{esc(p['desc'][lang])}</p>
  <span class="more">{P['visit']} {esc(p['domain'])} <span class="arrow">&nearr;</span></span></div></a>""" for p in partners)

    def opts(items):
        return f'<option value="">{P["choose"]}</option>' + "".join(f'<option>{esc(x)}</option>' for x in items)

    hp = '<p class="hp" aria-hidden="true"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'
    partner_form = f"""<form class="form" name="partner" method="POST" action="{thanks}" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="partner"><input type="hidden" name="language" value="{lang}">{hp}
  {field(P['company'], '<input name="company" required autocomplete="organization">', req=True, rq=rq)}
  {field(P['website'], '<input name="website" type="url" placeholder="https://" autocomplete="url">')}
  {field(P['contact'], '<input name="name" required autocomplete="name">', req=True, rq=rq)}
  {field(P['email'], '<input name="email" type="email" required autocomplete="email">', req=True, rq=rq)}
  {field(P['ptype'], f'<select name="partner_type" required>{opts(P["ptypes"])}</select>', full=True, req=True, rq=rq)}
  {field(P['message'], '<textarea name="message" rows="4"></textarea>', full=True)}
  <div class="full form-foot"><button class="btn" type="submit">{P['send_partner']} <span class="arrow">&rarr;</span></button><span class="muted">{P['note']}</span></div>
</form>"""
    skills = "".join(f'<label class="check"><input type="checkbox" name="skills" value="{esc(x)}"><span>{esc(x)}</span></label>' for x in P["skill_opts"])
    budgets = "".join(f'<label class="check"><input type="radio" name="budget" value="{esc(x)}" required{" data-has-budget" if i == 1 else ""}><span>{esc(x)}</span></label>' for i, x in enumerate(P["budget_opts"]))
    project_form = f"""<form class="form" name="project" method="POST" action="{thanks}" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="project"><input type="hidden" name="language" value="{lang}">{hp}
  {field(P['org'], '<input name="organisation" required autocomplete="organization">', req=True, rq=rq)}
  {field(P['website'], '<input name="website" type="url" placeholder="https://" autocomplete="url">')}
  {field(P['contact'], '<input name="name" required autocomplete="name">', req=True, rq=rq)}
  {field(P['email'], '<input name="email" type="email" required autocomplete="email">', req=True, rq=rq)}
  {field(P['ptitle'], '<input name="project_title" required>', full=True, req=True, rq=rq)}
  {field(P['pdesc'], '<textarea name="project_description" rows="5" required></textarea>', full=True, req=True, rq=rq)}
  <fieldset class="field full"><legend>{esc(P['skills'])}</legend><div class="checks">{skills}</div></fieldset>
  <fieldset class="field full"><legend>{esc(P['budget'])} <abbr title="{rq}">*</abbr></legend><div class="checks">{budgets}</div></fieldset>
  <div class="field budget-range" hidden>{field(P['range'], f'<select name="budget_range">{opts(P["range_opts"])}</select>')}</div>
  {field(P['timeline'], f'<select name="timeline">{opts(P["timeline_opts"])}</select>')}
  <label class="check full"><input type="checkbox" name="consent" value="yes" required><span>{esc(P['consent'])}</span></label>
  <div class="full form-foot"><button class="btn" type="submit">{P['send_project']} <span class="arrow">&rarr;</span></button><span class="muted">{P['note']}</span></div>
</form>"""
    main = page_hero(lang, "Christian Tech Founders / " + P["h1"], P["h1"], P["lead"], "Together") + f"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">{label(P['p_label'])}</div>
    <div class="grid g4">{cards}</div>
  </div>
</section>
<section style="padding-top:0" id="join">
  <div class="wrap">
    <div class="ticket">
      {ticket_head("Partners / Join")}
      <div class="ticket-body form-grid">
        <div>{label(P['j_label'])}<h2 class="h2" style="margin:16px 0 18px">{esc(P['j_h2'])}</h2><p class="lead">{esc(P['j_lead'])}</p></div>
        {partner_form}
      </div>
    </div>
  </div>
</section>
<section style="padding-top:0" id="project">
  <div class="wrap">
    <div class="ticket">
      {ticket_head("Projects / Submit")}
      <div class="ticket-body form-grid">
        <div>{label(P['s_label'])}<h2 class="h2" style="margin:16px 0 18px">{esc(P['s_h2'])}</h2><p class="lead">{esc(P['s_lead'])}</p></div>
        {project_form}
      </div>
    </div>
  </div>
</section>"""
    js = """<script>
document.querySelectorAll('form[name="project"]').forEach(function(f){
  var box=f.querySelector('.budget-range');
  f.querySelectorAll('input[name="budget"]').forEach(function(r){r.addEventListener('change',function(){box.hidden=!f.querySelector('input[data-has-budget]').checked;});});
});
</script>"""
    schema = [ORG, breadcrumb(lang, [(t["home"], "/"), ("Partners", "/partners/")])]
    write(lang, "/partners/", page(lang, "/partners/", P["title"], P["desc"], main, active="partners", schema=schema, scripts=js))


def build_thanks(lang):
    title, h1, text, b1, b2 = THANKS[lang]
    main = page_hero(lang, "Christian Tech Founders", h1, text, "Amen") + f"""
<section style="padding-top:0"><div class="wrap"><div class="btn-row">
  <a class="btn" href="{url(lang, '/')}">{b1}</a><a class="btn alt" href="{url(lang, '/insights/')}">{b2}</a>
</div></div></section>"""
    doc = page(lang, "/thanks/", title, text, main)
    doc = doc.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex">', 1)
    write(lang, "/thanks/", doc)


def build_404():
    main = page_hero("en", "Error 404", "Page not found", "This page does not exist (anymore). Go back home or read our insights.", "404") + """
<section style="padding-top:0"><div class="wrap"><div class="btn-row">
  <a class="btn" href="/">Home</a><a class="btn alt" href="/insights/">Insights</a><a class="btn alt" href="/nl/">Nederlands</a>
</div></div></section>"""
    doc = page("en", "/404/", "Page not found | Christian Tech Founders", "Page not found.", main)
    doc = doc.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex">', 1)
    (ROOT / "404.html").write_text(doc, encoding="utf-8")


# ─────────────────────────── Assets ───────────────────────────

def build_cosmos():
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.uniform(0, 800):.1f}" cy="{rnd.uniform(0, 800):.1f}" r="{rnd.uniform(0.4, 1.3):.2f}" opacity="{rnd.uniform(0.25, 0.95):.2f}"/>'
        for _ in range(520))
    cx, cy = 690, 980
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for r in range(130, 1500, 78))
    spokes = ""
    for i in range(-6, 7):
        tx = cx + i * 150
        spokes += f'<path d="M{cx} {cy} Q {cx + i * 60} {cy - 520} {tx} -40"/>'
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice">
<rect width="800" height="800" fill="#000"/>
<g fill="#fff">{stars}</g>
<g fill="none" stroke="#fff" stroke-opacity="0.62" stroke-width="1.6">{rings}{spokes}</g>
</svg>"""
    (ROOT / "assets" / "img" / "cosmos.svg").write_text(svg, encoding="utf-8")


def build_redirects():
    target = "/insights/" + EVENT_SLUG + "/"
    for rel, dest in [("blog/index.html", "/insights/"), ("blog/" + EVENT_SLUG + ".html", target)]:
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Moved</title>
<link rel="canonical" href="{DOMAIN}{dest}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={dest}"></head>
<body><p>This page moved to <a href="{dest}">{DOMAIN}{dest}</a>.</p></body></html>
""", encoding="utf-8")


def build_sitemap(paths):
    items = []
    for p in paths:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(l, p)}"/>' for l in LANGS)
        for l in LANGS:
            items.append(f"<url><loc>{abs_url(l, p)}</loc>{alts}</url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(items) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


def main():
    build_cosmos()
    founders = json.loads((SRC / "data" / "founders.json").read_text(encoding="utf-8"))
    lib = json.loads((SRC / "data" / "library.json").read_text(encoding="utf-8"))
    partners = json.loads((SRC / "data" / "partners.json").read_text(encoding="utf-8"))["partners"]
    paths = ["/", "/about/", "/partners/", "/insights/", "/library/", "/founders/"]
    for lang in LANGS:
        posts = load_posts(lang)
        build_home(lang, posts)
        build_insights(lang, posts)
        for p in posts:
            build_post(lang, p, posts)
        build_library(lang, lib)
        build_founders(lang, founders)
        build_about(lang, founders[0])
        build_partners(lang, partners)
        build_thanks(lang)
    build_404()
    paths += ["/insights/" + p["slug"] + "/" for p in load_posts("en")]
    build_redirects()
    build_sitemap(paths)
    print("Built", len(paths) * len(LANGS), "pages + founder profiles")


if __name__ == "__main__":
    main()
