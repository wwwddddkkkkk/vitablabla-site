#!/usr/bin/env python3
"""Validate generated article SEO and crawlability without executing JavaScript."""

import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET


SITE = "https://vitablabla.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE_DIR = os.path.join(ROOT, "a")


def fail(errors, message):
    errors.append(message)


def plain(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def main():
    errors = []
    with open(os.path.join(ROOT, "posts.json"), encoding="utf-8") as file:
        registry = json.load(file)

    posts = registry.get("posts", [])
    slugs = {post["slug"] for post in posts}
    canonicals = set()

    generated = {
        entry.name
        for entry in os.scandir(ARTICLE_DIR)
        if entry.is_dir() and os.path.isfile(os.path.join(entry.path, "index.html"))
    }
    missing = sorted(slugs - generated)
    extra = sorted(generated - slugs)
    if missing:
        fail(errors, "missing generated articles: " + ", ".join(missing))
    if extra:
        fail(errors, "generated articles without registry entries: " + ", ".join(extra))

    for post in posts:
        slug = post["slug"]
        path = os.path.join(ARTICLE_DIR, slug, "index.html")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as file:
            markup = file.read()

        expected_canonical = f"{SITE}/a/{slug}/"
        title_match = re.search(r"<title>(.*?)</title>", markup, re.DOTALL | re.IGNORECASE)
        description_match = re.search(
            r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>', markup, re.IGNORECASE
        )
        canonical_match = re.search(
            r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>', markup, re.IGNORECASE
        )
        body_match = re.search(
            r'<article\s+class="post-body">(.*?)</article>', markup, re.DOTALL | re.IGNORECASE
        )

        if not title_match or not plain(title_match.group(1)) or "Loading" in title_match.group(1):
            fail(errors, f"[{slug}] missing static title")
        if not description_match or not html.unescape(description_match.group(1)).strip():
            fail(errors, f"[{slug}] missing meta description")
        if not canonical_match or canonical_match.group(1) != expected_canonical:
            fail(errors, f"[{slug}] canonical mismatch")
        elif expected_canonical in canonicals:
            fail(errors, f"[{slug}] duplicate canonical")
        else:
            canonicals.add(expected_canonical)
        if not body_match or len(plain(body_match.group(1)).split()) < 80:
            fail(errors, f"[{slug}] static body is missing or too short")
        if "post.html?slug=" in markup:
            fail(errors, f"[{slug}] generated page contains a legacy article link")

        schemas = []
        for script in re.findall(
            r'<script\s+type="application/ld\+json">(.*?)</script>', markup, re.DOTALL | re.IGNORECASE
        ):
            try:
                schemas.append(json.loads(script))
            except json.JSONDecodeError as exc:
                fail(errors, f"[{slug}] invalid JSON-LD: {exc}")

        schema_types = {schema.get("@type") for schema in schemas if isinstance(schema, dict)}
        if "Article" not in schema_types:
            fail(errors, f"[{slug}] missing Article JSON-LD")
        if "BreadcrumbList" not in schema_types:
            fail(errors, f"[{slug}] missing BreadcrumbList JSON-LD")
        if post.get("faqs") and "FAQPage" not in schema_types:
            fail(errors, f"[{slug}] has FAQ metadata but no visible FAQ JSON-LD")

        for linked_slug in re.findall(r'href="/a/([a-z0-9]+(?:-[a-z0-9]+)*)/"', markup):
            if linked_slug not in slugs:
                fail(errors, f"[{slug}] links to unknown clean article: {linked_slug}")

    sitemap = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = {node.text for node in sitemap.findall("sm:url/sm:loc", namespace)}
    expected_articles = {f"{SITE}/a/{slug}/" for slug in slugs}
    missing_sitemap = sorted(expected_articles - locations)
    old_sitemap = sorted(location for location in locations if "post.html?slug=" in location)
    if missing_sitemap:
        fail(errors, "sitemap missing clean article URLs: " + ", ".join(missing_sitemap[:10]))
    if old_sitemap:
        fail(errors, "sitemap still contains legacy article URLs")

    static_pages = {
        "index.html": SITE + "/",
        "blog.html": SITE + "/blog",
        "frozili.html": SITE + "/frozili",
        "ohcrisp.html": SITE + "/ohcrisp",
        "about.html": SITE + "/about",
        "contact.html": SITE + "/contact",
    }
    for filename, expected_canonical in static_pages.items():
        with open(os.path.join(ROOT, filename), encoding="utf-8") as file:
            markup = file.read()
        if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', markup, re.IGNORECASE):
            fail(errors, f"[{filename}] missing meta description")
        if f'<link rel="canonical" href="{expected_canonical}"' not in markup:
            fail(errors, f"[{filename}] canonical mismatch")

    if errors:
        print(f"{len(errors)} static SEO error(s):")
        for message in errors:
            print("  ✗", message)
        sys.exit(1)

    print(f"✓ static SEO valid: {len(posts)} article pages.")
    print(f"✓ clean canonicals and sitemap URLs: {len(expected_articles)}.")
    print("✓ Article/Breadcrumb/FAQ structured data and internal links validated.")
    print("✓ static page descriptions and canonicals validated.")


if __name__ == "__main__":
    main()
