#!/usr/bin/env python3
"""
Vitablabla Journal build + validation step.

Run from the repo root after adding posts:

    python3 scripts/build-vitablabla.py

What it does:
  1. Validates posts.json (valid JSON, required fields, unique slugs/numbers).
  2. Checks every post has a body file at posts/<slug>.html.
  3. Checks every `related` slug and every internal post.html?slug=... link resolves.
  4. Warns about missing SEO/GEO fields (primaryKeyword, secondaryKeywords, faqs).
  5. Regenerates sitemap.xml from posts.json.

Exit code is non-zero if there are ERRORS (do not push on error).
Warnings do not block.
"""

import json
import os
import re
import sys
from datetime import date

SITE = "https://vitablabla.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON = os.path.join(ROOT, "posts.json")
POSTS_DIR = os.path.join(ROOT, "posts")
SITEMAP = os.path.join(ROOT, "sitemap.xml")

# Static pages that should appear in the sitemap (clean URLs; Cloudflare drops .html).
STATIC_PAGES = [
    ("", "1.0"),            # homepage
    ("blog", "0.9"),
    ("frozili", "0.8"),
    ("ohcrisp", "0.8"),
    ("about", "0.5"),
    ("contact", "0.5"),
]

REQUIRED_FIELDS = ["slug", "number", "title", "excerpt", "date", "categories", "cta"]
SEO_FIELDS = ["primaryKeyword", "secondaryKeywords", "faqs"]

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load():
    if not os.path.exists(POSTS_JSON):
        print("FATAL: posts.json not found at", POSTS_JSON)
        sys.exit(2)
    try:
        with open(POSTS_JSON, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print("FATAL: posts.json is not valid JSON:", e)
        sys.exit(2)


def validate(data):
    posts = data.get("posts", [])
    if not posts:
        err("posts.json has no posts.")
        return posts

    slugs = set(p.get("slug") for p in posts if p.get("slug"))
    seen_slugs = {}
    seen_numbers = {}
    iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    for i, p in enumerate(posts):
        label = p.get("slug") or f"#{i} (no slug)"

        for field in REQUIRED_FIELDS:
            if not p.get(field):
                err(f"[{label}] missing required field: {field}")

        slug = p.get("slug", "")
        if slug:
            if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
                err(f"[{label}] slug is not URL-safe (lowercase, hyphenated).")
            if slug in seen_slugs:
                err(f"[{label}] duplicate slug.")
            seen_slugs[slug] = True
            body = os.path.join(POSTS_DIR, slug + ".html")
            if not os.path.exists(body):
                err(f"[{label}] body file missing: posts/{slug}.html")

        num = p.get("number")
        if num:
            if num in seen_numbers:
                err(f"[{label}] duplicate number: {num}")
            seen_numbers[num] = True

        d = p.get("date", "")
        if d and not iso.match(d):
            err(f"[{label}] date not in YYYY-MM-DD form: {d}")
        dm = p.get("dateModified", "")
        if dm and not iso.match(dm):
            err(f"[{label}] dateModified not in YYYY-MM-DD form: {dm}")

        for rel in p.get("related", []):
            if rel not in slugs:
                err(f"[{label}] related slug does not exist: {rel}")

        # SEO/GEO field warnings
        for field in SEO_FIELDS:
            if not p.get(field):
                warn(f"[{label}] missing SEO/GEO field: {field}")
        chart = p.get("chart")
        if chart:
            if not chart.get("values"):
                err(f"[{label}] chart present but has no 'values'.")
            if not chart.get("source"):
                err(f"[{label}] chart must cite a 'source' (no charts without a real source).")
            if chart.get("labels") and len(chart["labels"]) != len(chart.get("values", [])):
                err(f"[{label}] chart 'labels' and 'values' length mismatch.")

        faqs = p.get("faqs")
        if faqs:
            if not isinstance(faqs, list):
                err(f"[{label}] faqs must be a list of {{q, a}} objects.")
            else:
                for fq in faqs:
                    if not (isinstance(fq, dict) and fq.get("q") and fq.get("a")):
                        err(f"[{label}] each faq needs a 'q' and an 'a'.")

        # Internal link check in the body file
        if slug:
            body = os.path.join(POSTS_DIR, slug + ".html")
            if os.path.exists(body):
                with open(body, encoding="utf-8") as f:
                    html = f.read()
                for m in re.findall(r"post\.html\?slug=([a-z0-9\-]+)", html):
                    if m not in slugs:
                        err(f"[{label}] body links to non-existent post: {m}")

    return posts


def build_sitemap(posts):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, prio in STATIC_PAGES:
        loc = SITE + "/" + path if path else SITE + "/"
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")

    # Newest first
    for p in sorted(posts, key=lambda x: (x.get("date", ""), x.get("number", "")), reverse=True):
        slug = p.get("slug")
        if not slug:
            continue
        loc = f"{SITE}/post.html?slug={slug}"
        lastmod = p.get("dateModified") or p.get("date") or today
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("    <priority>0.7</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(posts)


def main():
    data = load()
    posts = validate(data)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print("  ⚠", w)

    if errors:
        print(f"\n{len(errors)} ERROR(s) — fix before pushing:")
        for e in errors:
            print("  ✗", e)
        print("\nsitemap.xml NOT regenerated due to errors.")
        sys.exit(1)

    n = build_sitemap(posts)
    total_urls = n + len(STATIC_PAGES)
    print(f"\n✓ posts.json valid: {n} posts.")
    print(f"✓ sitemap.xml regenerated: {total_urls} URLs.")
    if warnings:
        print("  (warnings above are non-blocking, but worth fixing for full SEO/GEO coverage.)")


if __name__ == "__main__":
    main()
