#!/usr/bin/env python3
"""Check cover variety in real views and parity between browser/static output."""
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
from cover_theme import arrange_covers

ROOT = Path(__file__).resolve().parent.parent
registry = json.loads((ROOT / "posts.json").read_text())
posts = sorted(registry["posts"], key=lambda post: (post["date"], post["number"]), reverse=True)
views = [posts]
views.extend([post for post in posts if category in post["categories"]] for category in registry["categories"])
for query in ("coffee", "yogurt", "fruit", "freeze", "summer", "travel", "chocolate", "strawberry", "snack"):
    views.append([post for post in posts if query in " ".join(str(post.get(field, "")) for field in ("title", "cardTitle", "excerpt", "categories")).lower()])
by_slug = {post["slug"]: post for post in posts}
views.extend([by_slug[slug] for slug in post.get("related", [])[:3] if slug in by_slug] for post in posts)
expected = []
for view in views:
    themes = [post["coverTheme"] for post in arrange_covers(view)]
    assert themes == [post["coverTheme"] for post in arrange_covers(view)], "Non-deterministic cover mix"
    for index, theme in enumerate(themes):
        _, color, pattern = theme.split()
        for neighbor in themes[max(0, index - 3):index]:
            _, neighbor_color, neighbor_pattern = neighbor.split()
            assert color != neighbor_color, f"Repeated visible palette near {view[index]['slug']}"
            assert pattern != neighbor_pattern, f"Repeated print near {view[index]['slug']}"
    expected.append(themes)

browser = subprocess.run(["node", "-e", """
const fs = require('node:fs'), vm = require('node:vm');
const context = {window:{}};
vm.runInNewContext(fs.readFileSync('site.js','utf8'), context);
const views = JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(views.map(posts => context.window.VB.arrangeCovers(posts).map(post => post.coverTheme))));
"""], input=json.dumps(views), text=True, capture_output=True, cwd=ROOT, check=True)
assert json.loads(browser.stdout) == expected, "Browser and static cover selections diverged"

# Inspect the actual archive, not just isolated recipe output. The featured
# cover participates in the same ordered list as all subsequent grid cards.
class ArchiveCovers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.themes = []
        self.slugs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "content-cover" in classes:
            self.themes.append(" ".join(value for value in classes if value == "content-cover" or value.startswith(("tb-", "pattern-"))))
        href = attrs.get("href", "")
        if tag == "a" and href.startswith("/a/"):
            self.slugs.append(href.removeprefix("/a/").strip("/"))

archive = ArchiveCovers()
archive.feed((ROOT / "blog.html").read_text())
assert archive.slugs == [post["slug"] for post in posts], "Static Journal order differs from the displayed registry list"
assert archive.themes == expected[0], "Static Journal cover mix differs from browser selection"
print(f"✓ cover variety and browser/static parity: {len(views)} views, including all categories, searches and related cards.")
print(f"✓ actual Journal HTML: {len(archive.slugs)} links and cover themes match the browser list.")
