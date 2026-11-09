"""Content-led cover selection; keep in sync with VB.arrangeCovers in site.js."""
import re

PATTERNS = ("checker", "gingham", "pinstripe", "diagonal", "dots", "stars", "citrus", "berry-ribbon", "cherry-check", "heart-gingham", "patchwork", "wavy-check", "cocoa-dots", "stripes")
COLORS = ("tb-ice", "tb-coffee", "tb-blush", "tb-peach", "tb-sun", "tb-sage", "tb-violet", "tb-cream", "tb-pop")
# Illustrated prints have their own colors: count the visible palette, not a
# class that would leave the illustrated colors unchanged.
FIXED_COLORS = {"stars": "tb-sun", "citrus": "tb-sun", "berry-ribbon": "tb-blush", "cherry-check": "tb-ice", "wavy-check": "tb-ice", "patchwork": "tb-pop", "cocoa-dots": "tb-coffee"}


def cover_options(post):
    slug = post.get("slug", "")
    seed = sum((index + 1) * ord(char) for index, char in enumerate(slug))
    patterns, colors = PATTERNS, COLORS
    if re.search(r"rehydrat|sublimat|freeze-drying|how-ohcrisp-is-made", slug):
        patterns = ("wavy-check", "checker", "diagonal", "pinstripe", "dots", "gingham")
        colors = ("tb-ice", "tb-sage", "tb-violet", "tb-cream")
    elif re.search(r"strawberry|berry|acai|yogurt", slug):
        patterns = ("berry-ribbon", "cherry-check", "heart-gingham", "gingham", "pinstripe", "checker")
        colors = ("tb-blush", "tb-ice", "tb-violet", "tb-cream", "tb-peach")
    elif re.search(r"mango|pineapple|citrus|tropical|lemonade", slug):
        patterns = ("citrus", "gingham", "stripes", "checker", "pinstripe", "dots")
        colors = ("tb-sun", "tb-peach", "tb-sage", "tb-ice", "tb-cream")
    elif re.search(r"(^|-)(tea|ohviva)(-|$)", slug):
        patterns = ("citrus", "gingham", "pinstripe", "wavy-check", "dots", "checker")
        colors = ("tb-sage", "tb-ice", "tb-sun", "tb-peach", "tb-cream")
    elif re.search(r"coffee|espresso|ohsip|frozili|slow-melt", slug):
        patterns = ("cocoa-dots", "pinstripe", "heart-gingham", "diagonal", "gingham", "dots")
        colors = ("tb-coffee", "tb-cream", "tb-ice", "tb-violet", "tb-peach")
    elif re.search(r"freeze-dried-fruit|fruit-crunch|fruit-snack", slug):
        patterns = ("gingham", "cherry-check", "checker", "citrus", "berry-ribbon", "heart-gingham", "pinstripe", "diagonal", "dots", "wavy-check")
        colors = ("tb-peach", "tb-blush", "tb-sun", "tb-sage", "tb-ice", "tb-cream")

    # Occasion accents distinguish articles about the same product.
    if re.search(r"red-eye|night|stargaz|evening|movie|theatre|theater", slug):
        patterns = ("stars", "dots", "pinstripe", "checker", "diagonal", "gingham")
        colors = ("tb-violet", "tb-ice", "tb-cream", "tb-coffee", "tb-blush")
    elif re.search(r"airplane|airport|road-trip|travel|hotel|flight|train|commute", slug):
        patterns = ("patchwork", "stars", "wavy-check", "stripes", "dots", "pinstripe", "gingham")
        colors = ("tb-ice", "tb-sun", "tb-sage", "tb-cream", "tb-violet")
    elif re.search(r"beach|pool|summer|picnic|outdoor|camp|hiking|lake|heatwave", slug):
        patterns = ("stripes", "gingham", "dots", "checker", "pinstripe", "wavy-check")
        colors = ("tb-sun", "tb-ice", "tb-sage", "tb-peach", "tb-cream")
    elif re.search(r"chocolate|smores|hot-chocolate", slug):
        patterns = ("cocoa-dots", "diagonal", "heart-gingham", "pinstripe", "gingham", "checker")
        colors = ("tb-coffee", "tb-cream", "tb-peach", "tb-blush", "tb-violet")

    elif re.search(r"bagel|toast|pancake|waffle|oat|cereal|grain-bowl|muffin|crepe|scone|bread", slug):
        patterns = ("gingham", "checker", "heart-gingham", "cherry-check", "pinstripe", "berry-ribbon")
        colors = ("tb-peach", "tb-blush", "tb-ice", "tb-cream", "tb-sage")

    preferred = post.get("color")
    if preferred in colors:
        colors = (preferred,) + tuple(color for color in colors if color != preferred)
    offset = seed % len(patterns)
    patterns = patterns[offset:] + patterns[:offset]
    offset = (seed // 7) % len(colors)
    colors = colors[offset:] + colors[:offset]
    options = []
    for pattern_rank, pattern in enumerate(patterns):
        for color_rank, color in enumerate(colors):
            color = FIXED_COLORS.get(pattern, color)
            item = {"pattern": pattern, "color": color, "rank": pattern_rank * 3 + color_rank}
            if not any(p["pattern"] == pattern and p["color"] == color for p in options):
                options.append(item)
    return options


def theme_class(theme):
    return f'content-cover {theme["color"]} pattern-{theme["pattern"]}'


def cover_class(post):
    return post.get("coverTheme") or theme_class(cover_options(post)[0])


def arrange_covers(posts):
    """Avoid repeated prints AND visible palettes at distances 1, 2 and 3.

    Covers neighboring cards in one-, two- and three-column layouts.
    Run on the displayed list, including after a category/search change.
    """
    chosen, result = [], []
    for post in posts:
        def score(option):
            penalty = option["rank"]
            for distance, neighbor in enumerate(reversed(chosen[-3:]), 1):
                weight = 4 - distance
                penalty += weight * (200 * (option["pattern"] == neighbor["pattern"]) + 160 * (option["color"] == neighbor["color"]))
            return penalty

        theme = min(cover_options(post), key=score)
        chosen.append(theme)
        result.append({**post, "coverTheme": theme_class(theme)})
    return result
