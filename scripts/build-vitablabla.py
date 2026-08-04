#!/usr/bin/env python3
"""Validate the journal, pre-render every article, and rebuild sitemap.xml."""

import html
import json
import os
import re
import sys
from datetime import date


SITE = "https://vitablabla.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON = os.path.join(ROOT, "posts.json")
POSTS_DIR = os.path.join(ROOT, "posts")
POST_TEMPLATE = os.path.join(ROOT, "post.html")
ARTICLE_DIR = os.path.join(ROOT, "a")
SITEMAP = os.path.join(ROOT, "sitemap.xml")

STATIC_PAGES = [
    ("", "1.0"),
    ("blog", "0.9"),
    ("frozili", "0.8"),
    ("ohcrisp", "0.8"),
    ("about", "0.5"),
    ("contact", "0.5"),
]

REQUIRED_FIELDS = ["slug", "number", "title", "excerpt", "date", "categories", "cta"]
SEO_FIELDS = ["primaryKeyword", "secondaryKeywords", "faqs"]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OLD_POST_LINK_RE = re.compile(r"(?:/)?post\.html\?slug=([a-z0-9]+(?:-[a-z0-9]+)*)")
CLEAN_POST_LINK_RE = re.compile(r"/a/([a-z0-9]+(?:-[a-z0-9]+)*)/?")

errors = []
warnings = []


def err(message):
    errors.append(message)


def warn(message):
    warnings.append(message)


def load():
    if not os.path.exists(POSTS_JSON):
        print("FATAL: posts.json not found at", POSTS_JSON)
        sys.exit(2)
    try:
        with open(POSTS_JSON, encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        print("FATAL: posts.json is not valid JSON:", exc)
        sys.exit(2)


def plain(value):
    without_tags = re.sub(r"<[^>]+>", "", value or "")
    return html.unescape(without_tags).strip()


def normalized_text(value):
    return re.sub(r"\s+", " ", plain(value)).strip().casefold()


def article_path(slug):
    return f"/a/{slug}/"


def article_url(slug):
    return SITE + article_path(slug)


def rewrite_internal_links(body_html):
    body_html = OLD_POST_LINK_RE.sub(lambda match: article_path(match.group(1)), body_html)
    body_html = re.sub(
        r'href=(["\'])(?!/)(index|blog|frozili|ohcrisp|about|contact)\.html([^"\']*)\1',
        lambda match: f'href={match.group(1)}/{match.group(2)}{match.group(3)}{match.group(1)}',
        body_html,
    )
    return body_html


def validate(data):
    posts = data.get("posts", [])
    if not posts:
        err("posts.json has no posts.")
        return posts

    slugs = {post.get("slug") for post in posts if post.get("slug")}
    seen_slugs = set()
    seen_numbers = set()
    seen_primary_keywords = {}
    iso_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    for index, post in enumerate(posts):
        label = post.get("slug") or f"#{index} (no slug)"

        for field in REQUIRED_FIELDS:
            if not post.get(field):
                err(f"[{label}] missing required field: {field}")

        slug = post.get("slug", "")
        if slug:
            if not SLUG_RE.fullmatch(slug):
                err(f"[{label}] slug is not URL-safe (lowercase, hyphenated).")
            if slug in seen_slugs:
                err(f"[{label}] duplicate slug.")
            seen_slugs.add(slug)
            body_file = os.path.join(POSTS_DIR, slug + ".html")
            if not os.path.exists(body_file):
                err(f"[{label}] body file missing: posts/{slug}.html")

        number = post.get("number")
        if number:
            if number in seen_numbers:
                err(f"[{label}] duplicate number: {number}")
            seen_numbers.add(number)

        published = post.get("date", "")
        modified = post.get("dateModified", "")
        if published and not iso_date.fullmatch(published):
            err(f"[{label}] date not in YYYY-MM-DD form: {published}")
        if modified and not iso_date.fullmatch(modified):
            err(f"[{label}] dateModified not in YYYY-MM-DD form: {modified}")

        for related_slug in post.get("related", []):
            if related_slug not in slugs:
                err(f"[{label}] related slug does not exist: {related_slug}")

        for field in SEO_FIELDS:
            if not post.get(field):
                warn(f"[{label}] missing SEO/GEO field: {field}")

        primary_keyword = normalized_text(post.get("primaryKeyword", ""))
        if primary_keyword:
            duplicate = seen_primary_keywords.get(primary_keyword)
            if duplicate:
                warn(f"[{label}] primary keyword duplicates [{duplicate}]: {post.get('primaryKeyword')}")
            else:
                seen_primary_keywords[primary_keyword] = label

        chart = post.get("chart")
        if chart:
            if not chart.get("values"):
                err(f"[{label}] chart present but has no 'values'.")
            if not chart.get("source"):
                err(f"[{label}] chart must cite a source.")
            if chart.get("labels") and len(chart["labels"]) != len(chart.get("values", [])):
                err(f"[{label}] chart labels and values length mismatch.")

        faqs = post.get("faqs")
        if faqs:
            if not isinstance(faqs, list):
                err(f"[{label}] faqs must be a list of q/a objects.")
            else:
                for faq in faqs:
                    if not (isinstance(faq, dict) and faq.get("q") and faq.get("a")):
                        err(f"[{label}] each faq needs a q and an a.")

        if slug:
            body_file = os.path.join(POSTS_DIR, slug + ".html")
            if os.path.exists(body_file):
                with open(body_file, encoding="utf-8") as file:
                    body_html = file.read()
                referenced_slugs = set(OLD_POST_LINK_RE.findall(body_html))
                referenced_slugs.update(CLEAN_POST_LINK_RE.findall(body_html))
                for linked_slug in referenced_slugs:
                    if linked_slug not in slugs:
                        err(f"[{label}] body links to non-existent post: {linked_slug}")

    return posts


def extract_post_css():
    with open(POST_TEMPLATE, encoding="utf-8") as file:
        template = file.read()
    match = re.search(r"<style>(.*?)</style>", template, re.DOTALL)
    if not match:
        raise RuntimeError("post.html has no inline article styles")
    return match.group(1).strip()


def category_tags(post):
    tag_classes = {
        "Frozili": "frozili",
        "OhCrisp": "ohcrisp",
        "Coffee Candy": "coffee",
        "Freeze-Dried Fruit": "fruit",
        "Refreshing Snacks": "refresh",
        "Travel & Work": "travel",
        "Travel & Work Snacks": "travel",
        "Workday Snacks": "work",
        "Taste Notes": "work",
        "Notes": "work",
        "Better-for-You": "bfu",
        "Snack Ideas": "work",
    }
    return " ".join(
        f'<span class="tag {tag_classes.get(category, "work")}">{html.escape(category)}</span>'
        for category in post.get("categories", [])
    )


def format_date_long(iso_date):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    year, month, day = [int(part) for part in iso_date.split("-")]
    return f"{months[month - 1]} {day}, {year}"


def render_card(post):
    title = post.get("cardTitle") or post.get("title") or ""
    title = title.replace("<em>", '<span class="ital">').replace("</em>", "</span>")
    primary_category = (post.get("categories") or [""])[0]
    return f'''<a class="article" href="{article_path(post['slug'])}">
  <div class="title-block {html.escape(post.get('color') or 'tb-sage')}">
    <div class="tb-top"><span class="tb-num">No. {html.escape(str(post.get('number', '')))}</span><span class="tb-num">{html.escape(post.get('readTime', ''))}</span></div>
    <h3 class="tb-title">{title}</h3>
    <div class="tb-bottom"><span>{html.escape(primary_category)}</span><span>{html.escape(post.get('date', ''))}</span></div>
  </div>
  <p>{html.escape(post.get('excerpt', ''))}</p>
</a>'''


def extract_visible_faqs(body_html):
    headings = list(re.finditer(r"<h2\b[^>]*>(.*?)</h2>", body_html, re.IGNORECASE | re.DOTALL))
    faq_heading = None
    for heading in reversed(headings):
        heading_text = normalized_text(heading.group(1))
        if "quick question" in heading_text or "frequently asked" in heading_text or heading_text == "faq":
            faq_heading = heading
            break
    if faq_heading is None:
        return []

    faq_section = body_html[faq_heading.end():]
    pairs = re.findall(
        r"<h3\b[^>]*>(.*?)</h3>\s*<p\b[^>]*>(.*?)</p>",
        faq_section,
        re.IGNORECASE | re.DOTALL,
    )
    return [{"q": plain(question), "a": plain(answer)} for question, answer in pairs if plain(question) and plain(answer)]


def ensure_visible_faq(body_html, post):
    faqs = post.get("faqs") or []
    if not faqs:
        return body_html, []

    visible_faqs = extract_visible_faqs(body_html)
    if visible_faqs:
        metadata_pairs = [(normalized_text(item["q"]), normalized_text(item["a"])) for item in faqs]
        visible_pairs = [(normalized_text(item["q"]), normalized_text(item["a"])) for item in visible_faqs]
        if metadata_pairs != visible_pairs:
            warn(f"[{post['slug']}] FAQ metadata differs from visible copy; structured data uses visible copy.")
        return body_html, visible_faqs

    body_text = normalized_text(body_html)
    all_visible = all(
        normalized_text(faq.get("q", "")) in body_text
        and normalized_text(faq.get("a", "")) in body_text
        for faq in faqs
    )
    if all_visible:
        return body_html, faqs

    faq_items = []
    for faq in faqs:
        faq_items.append(
            f'<h3>{html.escape(faq["q"])}</h3>\n<p>{html.escape(faq["a"])}</p>'
        )
    warn(f"[{post['slug']}] rendered visible FAQ from metadata to match structured data.")
    rendered_body = body_html.rstrip() + '\n<section class="post-faq" aria-labelledby="faq-heading">\n' + \
        '<h2 id="faq-heading">Quick questions</h2>\n' + "\n".join(faq_items) + "\n</section>\n"
    return rendered_body, faqs


def json_ld(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_article(post, posts_by_slug, post_css):
    slug = post["slug"]
    with open(os.path.join(POSTS_DIR, slug + ".html"), encoding="utf-8") as file:
        body_html = rewrite_internal_links(file.read())
    body_html, schema_faqs = ensure_visible_faq(body_html, post)

    title = plain(post.get("title", ""))
    description = plain(post.get("excerpt", ""))
    canonical = article_url(slug)
    published = post.get("date", "")
    modified = post.get("dateModified") or published
    categories = post.get("categories") or []
    keywords = ([post["primaryKeyword"]] if post.get("primaryKeyword") else []) + (post.get("secondaryKeywords") or [])

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": published,
        "dateModified": modified,
        "url": canonical,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "articleSection": categories,
        "author": {"@type": "Organization", "name": "Vitablabla", "url": SITE},
        "publisher": {
            "@type": "Organization",
            "name": "Vitablabla",
            "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"},
        },
    }
    if keywords:
        article_schema["keywords"] = keywords

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "/blog"},
            {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
        ],
    }

    schema_scripts = [article_schema, breadcrumb_schema]
    faqs = [faq for faq in schema_faqs if faq.get("q") and faq.get("a")]
    if faqs:
        schema_scripts.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
                }
                for faq in faqs
            ],
        })

    related_slugs = post.get("related") or [item["slug"] for item in posts_by_slug.values() if item["slug"] != slug][:3]
    related_posts = [posts_by_slug[item] for item in related_slugs if item in posts_by_slug][:3]
    related_html = "\n".join(render_card(item) for item in related_posts)

    crumbs = ['<a href="/blog">Journal</a>']
    crumbs.extend(html.escape(item) for item in post.get("crumbs", []))
    crumbs_html = " &nbsp;/&nbsp; ".join(crumbs)

    if post.get("cta") == "ohcrisp":
        cta_class = "ohcrisp"
        cta_title = "Try a pouch for <em>yourself.</em>"
        cta_href = "https://www.ohcrisp.com"
        cta_attrs = ' target="_blank" rel="noopener" style="background:#5A2530;color:#FBEDEC"'
        cta_label = "Visit ohcrisp.com"
    else:
        cta_class = "frozili"
        cta_title = "Try a slow-melt for <em>yourself.</em>"
        cta_href = "/frozili"
        cta_attrs = ' style="background:var(--frozili-coffee);color:var(--ivory)"'
        cta_label = "Visit Frozili"

    schema_html = "\n".join(
        f'<script type="application/ld+json">{json_ld(schema)}</script>' for schema in schema_scripts
    )

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{html.escape(title)} — Vitablabla Journal</title>
<meta name="description" content="{html.escape(description, quote=True)}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Vitablabla Journal" />
<meta property="og:title" content="{html.escape(title, quote=True)}" />
<meta property="og:description" content="{html.escape(description, quote=True)}" />
<meta property="og:url" content="{canonical}" />
<meta property="article:published_time" content="{html.escape(published)}" />
<meta property="article:modified_time" content="{html.escape(modified)}" />
<meta name="twitter:card" content="summary" />
<meta name="twitter:title" content="{html.escape(title, quote=True)}" />
<meta name="twitter:description" content="{html.escape(description, quote=True)}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="stylesheet" href="/styles.css" />
{schema_html}
<style>{post_css}</style>
</head>
<body>
<div class="progress"><div class="bar" id="bar"></div></div>
<div class="topstrip">The Vitablabla Journal &middot; Product stories &amp; taste ideas &middot; <a href="/blog">Back to all articles</a></div>
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-left"><a class="nav-link" href="/">Home</a><a class="nav-link" href="/#brands">Brands</a><a class="nav-link" href="/about">About</a></div>
    <a class="logo" href="/">vitablabla<span class="dot">.</span></a>
    <div class="nav-right"><a class="nav-link" href="/contact">Contact</a><a class="cta-pill active" href="/blog">Read Blog <span class="arrow">↗</span></a></div>
  </div>
</nav>
<main id="postRoot" data-state="ready">
  <header class="post-hero"><div class="container">
    <div class="crumbs">{crumbs_html}</div>
    <h1>{post.get('title', '')}</h1>
    <div class="post-meta">
      <div class="item"><span class="lbl">Category</span><span class="val">{category_tags(post)}</span></div>
      <div class="item"><span class="lbl">Published</span><time class="val" datetime="{html.escape(published)}">{format_date_long(published)}</time></div>
      <div class="item"><span class="lbl">Read time</span><span class="val">{html.escape(post.get('readTime', ''))}</span></div>
    </div>
  </div></header>
  <article class="post-body">{body_html}</article>
  <section><div class="post-cta {cta_class}"><h2>{cta_title}</h2><a class="cta-pill" href="{cta_href}"{cta_attrs}>{cta_label} <span class="arrow">↗</span></a></div></section>
  <section class="related"><div class="container">
    <div class="related-head"><h2>Keep <span style="font-style:italic;color:var(--sage-deep)">reading.</span></h2><span class="meta">Three more from the journal</span></div>
    <div class="related-grid">{related_html}</div>
  </div></section>
</main>
<footer class="footer"><div class="container">
  <div class="footer-grid">
    <div><div class="footer-brand"><span class="italic">vita<br/>blabla.</span></div><p class="footer-tag">Made for specific tastes and little daily joys.</p></div>
    <div><h4>Brands</h4><ul><li><a href="/frozili">Frozili</a></li><li><a href="/ohcrisp">OhCrisp</a></li><li><span style="color:var(--ink-mute)">More coming</span></li></ul></div>
    <div><h4>Company</h4><ul><li><a href="/about">About</a></li><li><a href="/blog">Journal</a></li><li><a href="/contact">Contact</a></li></ul></div>
    <div><h4>Elsewhere</h4><ul><li><a href="https://www.instagram.com/vitablabla" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.tiktok.com/@froziliofficial" target="_blank" rel="noopener">TikTok</a></li><li><a href="https://www.pinterest.com/vitablabla/" target="_blank" rel="noopener">Pinterest</a></li><li><a href="mailto:info@vitablabla.com">info@vitablabla.com</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 Vitablabla, Inc.</span><span>Made with care, for specific tastes.</span></div>
</div></footer>
<script>
(() => {{
  const bar = document.getElementById('bar');
  const article = document.querySelector('.post-body');
  const update = () => {{
    const rect = article.getBoundingClientRect();
    const top = window.scrollY + rect.top;
    const scrolled = window.scrollY - top + window.innerHeight * 0.4;
    bar.style.width = (Math.max(0, Math.min(1, scrolled / rect.height)) * 100) + '%';
  }};
  document.addEventListener('scroll', update, {{ passive: true }});
  update();
}})();
</script>
</body>
</html>
'''


def build_articles(posts):
    os.makedirs(ARTICLE_DIR, exist_ok=True)
    post_css = extract_post_css()
    posts_by_slug = {post["slug"]: post for post in posts if post.get("slug")}
    expected_slugs = set(posts_by_slug)

    for slug, post in posts_by_slug.items():
        output_dir = os.path.join(ARTICLE_DIR, slug)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
            file.write(render_article(post, posts_by_slug, post_css))

    for entry in os.scandir(ARTICLE_DIR):
        if not entry.is_dir() or entry.name in expected_slugs or not SLUG_RE.fullmatch(entry.name):
            continue
        stale_file = os.path.join(entry.path, "index.html")
        if os.path.isfile(stale_file):
            os.remove(stale_file)
        try:
            os.rmdir(entry.path)
        except OSError:
            warn(f"[{entry.name}] stale generated directory contains extra files; left in place.")

    return len(posts_by_slug)


def build_sitemap(posts):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority in STATIC_PAGES:
        location = SITE + "/" + path if path else SITE + "/"
        lines.extend([
            "  <url>",
            f"    <loc>{location}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ])

    for post in sorted(posts, key=lambda item: (item.get("date", ""), item.get("number", "")), reverse=True):
        slug = post.get("slug")
        if not slug:
            continue
        lines.extend([
            "  <url>",
            f"    <loc>{article_url(slug)}</loc>",
            f"    <lastmod>{post.get('dateModified') or post.get('date') or today}</lastmod>",
            "    <priority>0.7</priority>",
            "  </url>",
        ])

    lines.append("</urlset>")
    with open(SITEMAP, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return len(posts)


def main():
    data = load()
    posts = validate(data)

    if errors:
        print(f"\n{len(errors)} ERROR(s) — fix before publishing:")
        for message in errors:
            print("  ✗", message)
        print("\nStatic articles and sitemap were not regenerated.")
        sys.exit(1)

    rendered_count = build_articles(posts)
    sitemap_count = build_sitemap(posts)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for message in warnings:
            print("  ⚠", message)

    print(f"\n✓ posts.json valid: {len(posts)} posts.")
    print(f"✓ static articles rendered: {rendered_count} pages under a/<slug>/.")
    print(f"✓ sitemap.xml regenerated: {sitemap_count + len(STATIC_PAGES)} URLs.")
    if warnings:
        print("  (Warnings are non-blocking; legacy metadata can be improved incrementally.)")


if __name__ == "__main__":
    main()
