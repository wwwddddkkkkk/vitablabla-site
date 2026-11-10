#!/usr/bin/env python3
"""Validate generated article SEO and crawlability without executing JavaScript."""

import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, deque
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit


SITE = "https://vitablabla.com"
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ARTICLE_DIR = os.path.join(ROOT, "a")
ARTICLE_PATH = re.compile(r"^/a/([a-z0-9]+(?:-[a-z0-9]+)*)/$")


class AnchorParser(HTMLParser):
    """Read actual anchors, including archive scope, without executing scripts."""

    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.links = []
        self.archive_links = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        archive = attrs.get("id") in {"featuredSlot", "articleGrid"} or any(item[1] for item in self.stack)
        inert = tag == "template" or "hidden" in attrs or any(item[2] for item in self.stack)
        if tag == "a" and "href" in attrs and not inert:
            self.links.append(attrs["href"])
            if archive:
                self.archive_links.append(attrs["href"])
        if tag not in self.VOID_TAGS:
            self.stack.append((tag, archive, inert))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)


def clean_link_path(href, current_path):
    """Resolve same-origin anchors only; query aliases do not prove clean reachability."""
    try:
        target = urlsplit(urljoin(SITE + current_path, href))
    except ValueError:
        return None
    if target.scheme != "https" or target.netloc != "vitablabla.com" or target.query:
        return None
    path = target.path or "/"
    if "\\" in path or "%" in path or any(part in {".", ".."} for part in path.split("/")):
        return None
    return path


def validate_discovery(slugs, errors):
    expected = {f"/a/{slug}/" for slug in slugs}
    cache = {}

    def read_page(path):
        if path in cache:
            return cache[path]
        relative = "index.html" if path == "/" else path.lstrip("/")
        if path != "/" and path.endswith("/"):
            relative += "index.html"
        elif not os.path.splitext(relative)[1]:
            relative += ".html"
        filename = os.path.realpath(os.path.join(ROOT, relative))
        if os.path.commonpath((ROOT, filename)) != ROOT or not filename.endswith(".html") or not os.path.isfile(filename):
            cache[path] = None
        else:
            with open(filename, encoding="utf-8") as file:
                cache[path] = AnchorParser(file.read())
        return cache[path]

    archive = read_page("/blog")
    counts = Counter()
    for href in archive.archive_links if archive else []:
        path = clean_link_path(href, "/blog")
        if path is None or not ARTICLE_PATH.fullmatch(path):
            fail(errors, f"[blog] archive contains a non-clean article link: {href}")
        else:
            counts[path] += 1
    missing = sorted(expected - counts.keys())
    unknown = sorted(counts.keys() - expected)
    duplicates = sorted(path for path, count in counts.items() if count != 1)
    if missing:
        fail(errors, f"[blog] static archive missing {len(missing)} registered articles: " + ", ".join(missing[:10]))
    if unknown:
        fail(errors, "[blog] static archive links to unknown articles: " + ", ".join(unknown))
    if duplicates:
        fail(errors, "[blog] static archive must link each article exactly once: " + ", ".join(duplicates))

    depths = {"/": 0}
    pending = deque(["/"])
    while pending:
        current = pending.popleft()
        if depths[current] == 3:
            continue
        page = read_page(current)
        for href in page.links if page else []:
            target = clean_link_path(href, current)
            if target is not None and target not in depths and read_page(target) is not None:
                depths[target] = depths[current] + 1
                pending.append(target)
    unreachable = sorted(expected - depths.keys())
    if unreachable:
        fail(errors, f"{len(unreachable)} articles unreachable within three homepage HTML anchor hops: " + ", ".join(unreachable[:10]))
    return max((depths[path] for path in expected if path in depths), default=0)


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
        if post.get("image"):
            image = post["image"]
            image_url = SITE + image["src"]
            if f'<meta property="og:image" content="{image_url}"' not in markup:
                fail(errors, f"[{slug}] missing social image")
            article_schema = next((schema for schema in schemas if schema.get("@type") == "Article"), {})
            if article_schema.get("image", {}).get("url") != image_url:
                fail(errors, f"[{slug}] Article image does not match the editorial asset")
            if not body_match or image["src"] not in body_match[1]:
                fail(errors, f"[{slug}] editorial image is missing from the visible article")

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

    # Brand browsing is direct; company introductions share one story page.
    with open(os.path.join(ROOT, "about.html"), encoding="utf-8") as file:
        about = file.read()
    with open(os.path.join(ROOT, "_redirects"), encoding="utf-8") as file:
        redirects = file.read().splitlines()
    for brand in ("ohcrisp", "ohsip", "ohviva", "frozili"):
        if f'id="{brand}"' not in about:
            fail(errors, f"[about] missing {brand} introduction")
    for brand in ("ohcrisp", "frozili"):
        for old_path in (f"/{brand}", f"/{brand}/", f"/{brand}.html"):
            if f"{old_path} /about#{brand} 301" not in redirects:
                fail(errors, f"missing redirect for {old_path}")
        if SITE + "/" + brand in locations:
            fail(errors, f"retired brand page is still in the sitemap: {brand}")
    expected_brands = {"https://www.ohcrisp.com", "https://getohsip.com", "https://drinkohviva.com", "https://www.frozili.com"}
    paths = [os.path.join(ROOT, filename) for filename in static_pages]
    paths += [os.path.join(ARTICLE_DIR, slug, "index.html") for slug in slugs]
    for path in paths:
        with open(path, encoding="utf-8") as file:
            markup = file.read()
        footer = re.search(r'<footer class="house-footer">(.*?)</footer>', markup, re.S)
        if not footer or not expected_brands.issubset(set(re.findall(r'href="([^"]+)"', footer.group(1)))):
            fail(errors, f"[{os.path.relpath(path, ROOT)}] footer must link to all four official brands")

    maximum_hops = validate_discovery(slugs, errors)

    if errors:
        print(f"{len(errors)} static SEO error(s):")
        for message in errors:
            print("  ✗", message)
        sys.exit(1)

    print(f"✓ static SEO valid: {len(posts)} article pages.")
    print(f"✓ clean canonicals and sitemap URLs: {len(expected_articles)}.")
    print("✓ Article/Breadcrumb/FAQ structured data and internal links validated.")
    print("✓ static page descriptions and canonicals validated.")
    print(f"✓ complete static Journal archive: {len(slugs)} unique article links; all articles within {maximum_hops} homepage HTML anchor hops.")


if __name__ == "__main__":
    main()
