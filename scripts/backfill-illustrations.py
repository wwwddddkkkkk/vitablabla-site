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
ILLO_RE = re.compile(r'<div class="post-illustration">.*?</div>(?=\s*\n\s*<figcaption|\s*</figure>)', re.S)


def theme_for(post):
    # Theme is driven by CATEGORY, not cta (trend posts still carry a brand cta).
    cats = set(post.get("categories", []))
    if cats & {"OhCrisp", "Freeze-Dried Fruit"}:
        return "ohcrisp"
    if cats & {"Frozili", "Coffee Candy", "Refreshing Snacks"}:
        return "frozili"
    return "trend"


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
        art = illustration.svg(theme=theme_for(p), color=p.get("color", "tb-sage"),
                               seed=slug, data=p.get("chart"))
        new_div = '<div class="post-illustration">' + art + '</div>'
        if "post-illustration" in html:
            # regenerate the existing illustration (e.g. centering / style update)
            html2 = ILLO_RE.sub(new_div, html, count=1)
        elif FIG_RE.search(html):
            html2 = FIG_RE.sub(lambda m: new_div + '\n  ' + m.group(1), html, count=1)
        else:
            skipped.append(slug + " (no figure)")
            continue
        open(path, "w", encoding="utf-8").write(html2)
        changed += 1
    print(f"Illustrated {changed} posts since {SINCE}.")
    if skipped:
        print("Skipped:")
        for s in skipped:
            print("  -", s)


if __name__ == "__main__":
    main()
