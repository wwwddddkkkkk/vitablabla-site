#!/usr/bin/env python3
"""
One-off: replace the typographic title-block figure in recent posts with a
branded SVG illustration, preserving each post's <figcaption>.

Usage:
    python3 scripts/backfill-illustrations.py [SINCE_DATE]
SINCE_DATE defaults to 2026-06-01 (the recent ~2 weeks).
"""
import json
import os
import re
import sys

import illustration

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINCE = sys.argv[1] if len(sys.argv) > 1 else "2026-06-01"

FIG_RE = re.compile(r'<div class="title-block.*?</div>\s*(<figcaption)', re.S)


def theme_for(post):
    cta = post.get("cta", "")
    cats = " ".join(post.get("categories", [])).lower()
    if "freeze" in cats or cta == "ohcrisp":
        return "ohcrisp"
    return "frozili"


def main():
    data = json.load(open(os.path.join(ROOT, "posts.json"), encoding="utf-8"))
    recent = [p for p in data["posts"] if p.get("date", "") >= SINCE]
    changed, skipped = 0, []
    for p in recent:
        slug = p["slug"]
        path = os.path.join(ROOT, "posts", slug + ".html")
        if not os.path.exists(path):
            skipped.append(slug + " (no file)")
            continue
        html = open(path, encoding="utf-8").read()
        if "post-illustration" in html:
            skipped.append(slug + " (already done)")
            continue
        if not FIG_RE.search(html):
            skipped.append(slug + " (no title-block figure)")
            continue
        art = illustration.svg(theme=theme_for(p), color=p.get("color", "tb-sage"), seed=slug)
        new_div = '<div class="post-illustration">' + art + '</div>\n  '
        html2 = FIG_RE.sub(lambda m: new_div + m.group(1), html, count=1)
        open(path, "w", encoding="utf-8").write(html2)
        changed += 1
    print(f"Illustrated {changed} posts since {SINCE}.")
    if skipped:
        print("Skipped:")
        for s in skipped:
            print("  -", s)


if __name__ == "__main__":
    main()
