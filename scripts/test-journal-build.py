#!/usr/bin/env python3
"""Regression: future registry entries must join the static archive automatically."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("build", ROOT / "scripts/build-vitablabla.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class JournalBuildTests(unittest.TestCase):
    def test_new_registry_entry_and_repeat_build(self):
        posts = json.loads((ROOT / "posts.json").read_text())["posts"]
        future = dict(posts[0], slug="future-archive-regression", number="999", date="2099-01-01", title="Future archive regression")
        with tempfile.TemporaryDirectory() as directory, patch.object(build, "ROOT", directory):
            output = Path(directory) / "blog.html"
            output.write_text((ROOT / "blog.html").read_text())
            build.build_journal([*reversed(posts), future])
            first = output.read_text()
            links = build.re.findall(r'href="/a/([^/]+)/"', first)
            expected = sorted([*posts, future], key=lambda post: (post["date"], post["number"]), reverse=True)
            self.assertEqual(links, [post["slug"] for post in expected])
            self.assertIn(f'{len(expected)} ARTICLES', first)
            build.build_journal([*posts, future])
            self.assertEqual(first, output.read_text())


if __name__ == "__main__":
    unittest.main()
