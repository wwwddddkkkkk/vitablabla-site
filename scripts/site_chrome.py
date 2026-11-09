"""Keep the crawlable header and footer aligned with the homepage."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def chrome_header(active=""):
    home = (ROOT / "index.html").read_text()
    header = re.search(r'<header class="house-header">.*?</header>', home, re.S).group()
    header = header.replace('class="house-header"', 'class="house-header" id="top"', 1)
    for anchor, target in (("brands", "/#brands"), ("technology", "/#technology"), ("story", "/about"), ("journal", "/blog")):
        header = header.replace(f'href="#{anchor}"', f'href="{target}"')
    header = re.sub(r' data-chapter="[^"]+"| aria-current="location"', '', header)
    header = header.replace('Our house', 'Our story')
    if active:
        header = header.replace(f'href="/{active}"', f'href="/{active}" aria-current="page"')
    return '<a class="skip-link" href="#main">Skip to content</a>\n' + header


def chrome_footer():
    home = (ROOT / "index.html").read_text()
    footer = re.search(r'<footer class="house-footer">.*?</footer>', home, re.S).group()
    return footer.replace('href="#technology"', 'href="/#technology"').replace('href="#main"', 'href="#top"')


def head(title, description, path):
    import html
    t, d = html.escape(title, quote=True), html.escape(description, quote=True)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{t}</title><meta name="description" content="{d}"/>
<link rel="canonical" href="https://vitablabla.com/{path}"/>
<meta property="og:type" content="website"/><meta property="og:site_name" content="Vitablabla"/>
<meta property="og:title" content="{t}"/><meta property="og:description" content="{d}"/><meta property="og:url" content="https://vitablabla.com/{path}"/>
<meta name="twitter:card" content="summary"/><meta name="theme-color" content="#DFC8E7"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="stylesheet" href="/styles.css"/><link rel="stylesheet" href="/home.css"/><link rel="stylesheet" href="/pages.css"/><link rel="stylesheet" href="/covers.css"/>
<noscript><style>.interior-page .menu-toggle{{display:none}}@media(max-width:680px){{.interior-page .mobile-menu[hidden]{{display:block!important}}}}</style></noscript>
</head><body class="brand-house science-house interior-page">'''
