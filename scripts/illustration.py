#!/usr/bin/env python3
"""
Vitablabla branded illustration generator.

Produces inline SVG illustrations in the site's exact palette and aesthetic
(soft top->bottom gradient, a faint highlight circle, simple line+fill motifs).
100% original art — no copyright, perfectly on-brand, tiny file size.

Usage (as a module):
    from illustration import figure_html
    html = figure_html(theme="frozili", color="tb-ice", seed="my-slug",
                       caption="Fig. 01 — Frozili · the cooling finish")

`theme` is one of: frozili, ohcrisp, trend
`color` is one of the tb-* tone classes used across the site.
`seed` (usually the slug) makes the layout deterministic per post.
"""

import hashlib

# tb-* tones -> (gradient top, gradient bottom, ink/foreground, accent)
PALETTE = {
    "tb-ice":    ("#DCEAF0", "#A9CADB", "#1F3A48", "#4A2E1E"),
    "tb-coffee": ("#DEC9AC", "#8B5A3A", "#2A1810", "#E9D9C2"),
    "tb-blush":  ("#F8DDE0", "#E89AA1", "#5A2530", "#5F6E54"),
    "tb-peach":  ("#FAD9BD", "#E89A6F", "#5A2A14", "#5F6E54"),
    "tb-sun":    ("#FAE7A6", "#E8B748", "#5A3A0F", "#5A2530"),
    "tb-sage":   ("#DAE2D0", "#8A9A7B", "#2F3A26", "#4A2E1E"),
    "tb-violet": ("#E6DCEC", "#9F8CB8", "#3A2A4F", "#4A2E1E"),
    "tb-cream":  ("#F4EEDD", "#D8C9A4", "#4A3A1E", "#4A2E1E"),
    "tb-pop":    ("#F4CFD2", "#C76974", "#FBEDEC", "#5A2530"),
}

W, H = 400, 250


def _rng(seed):
    """Tiny deterministic PRNG seeded by string -> yields floats in [0,1)."""
    h = hashlib.sha256(seed.encode()).digest()
    i = 0
    while True:
        for b in h:
            yield b / 255.0
        i += 1
        h = hashlib.sha256(h + bytes([i & 255])).digest()


def _g(rng, lo, hi):
    return lo + next(rng) * (hi - lo)


# ── Motifs ───────────────────────────────────────────────────────────
def _iced_cup(cx, cy, ink, accent, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <path d="M-36 -52 H36 L29 70 Q28 82 16 82 H-16 Q-28 82 -29 70 Z" fill="{accent}" stroke="{ink}" stroke-width="3"/>
  <path d="M-29 8 H29 L23 70 Q22 82 11 82 H-11 Q-22 82 -23 70 Z" fill="{ink}" opacity="0.9"/>
  <rect x="-20" y="-40" width="18" height="18" rx="3" fill="#ffffff" opacity="0.85" transform="rotate(-12)"/>
  <rect x="2" y="-26" width="16" height="16" rx="3" fill="#ffffff" opacity="0.7" transform="rotate(10)"/>
  <rect x="-12" y="-18" width="14" height="14" rx="3" fill="#ffffff" opacity="0.55" transform="rotate(18)"/>
  <line x1="6" y1="-64" x2="18" y2="-86" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>
</g>'''


def _candy(cx, cy, ink, accent, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <rect x="-34" y="-34" width="68" height="68" rx="22" fill="{accent}" stroke="{ink}" stroke-width="3"/>
  <ellipse cx="-10" cy="-10" rx="16" ry="10" fill="#ffffff" opacity="0.45" transform="rotate(-20 -10 -10)"/>
  <path d="M-34 0 h68 M0 -34 v68" stroke="{ink}" stroke-width="1.5" opacity="0.25"/>
</g>'''


def _beans(cx, cy, ink, accent, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <ellipse cx="0" cy="0" rx="22" ry="30" fill="{accent}" stroke="{ink}" stroke-width="3" transform="rotate(-18)"/>
  <path d="M0 -26 Q-8 0 0 26" fill="none" stroke="{ink}" stroke-width="3" transform="rotate(-18)"/>
  <ellipse cx="40" cy="20" rx="18" ry="25" fill="{accent}" stroke="{ink}" stroke-width="3" transform="rotate(22 40 20)"/>
  <path d="M40 -2 Q33 20 40 42" fill="none" stroke="{ink}" stroke-width="3" transform="rotate(22 40 20)"/>
</g>'''


def _strawberry(cx, cy, ink, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <path d="M-30 -20 Q0 -42 30 -20 Q24 40 0 60 Q-24 40 -30 -20 Z" fill="#ECA08A" stroke="{ink}" stroke-width="3"/>
  <circle cx="-10" cy="2" r="3" fill="{ink}"/><circle cx="8" cy="-2" r="3" fill="{ink}"/>
  <circle cx="-1" cy="20" r="3" fill="{ink}"/><circle cx="-15" cy="30" r="3" fill="{ink}"/><circle cx="12" cy="26" r="3" fill="{ink}"/>
  <path d="M0 -40 q-9 -15 7 -22" fill="none" stroke="#5F6E54" stroke-width="3" stroke-linecap="round"/>
</g>'''


def _orange_wheel(cx, cy, ink, accent, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <circle r="42" fill="#F2D26A" stroke="{ink}" stroke-width="3"/>
  <circle r="33" fill="none" stroke="{ink}" stroke-width="2" opacity="0.6"/>
  <path d="M0 0 L0 -33 M0 0 L29 16 M0 0 L29 -16 M0 0 L-29 16 M0 0 L-29 -16 M0 0 L0 33" stroke="{ink}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
</g>'''


def _berries(cx, cy, ink, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <circle cx="-18" cy="0" r="18" fill="#9F8CB8" stroke="{ink}" stroke-width="3"/>
  <circle cx="16" cy="-8" r="15" fill="#C76974" stroke="{ink}" stroke-width="3"/>
  <circle cx="6" cy="22" r="16" fill="#E89AA1" stroke="{ink}" stroke-width="3"/>
  <circle cx="-20" cy="-3" r="3" fill="#ffffff" opacity="0.6"/>
</g>'''


def _bowl(cx, cy, ink, accent, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <path d="M-50 0 A50 50 0 0 0 50 0 Z" fill="{accent}" stroke="{ink}" stroke-width="3"/>
  <ellipse cx="0" cy="0" rx="50" ry="12" fill="{accent}" stroke="{ink}" stroke-width="3"/>
  <circle cx="-20" cy="-4" r="7" fill="#ECA08A"/><circle cx="0" cy="-6" r="7" fill="#F2D26A"/><circle cx="20" cy="-4" r="7" fill="#9F8CB8"/>
</g>'''


def _sensory_arc(cx, cy, ink, accent, s=1.0):
    """Abstract motif for trend/analysis/broad pieces."""
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <circle r="46" fill="none" stroke="{ink}" stroke-width="3" opacity="0.85"/>
  <path d="M-46 0 A46 46 0 0 1 46 0" fill="{accent}" opacity="0.55"/>
  <circle r="20" fill="#ffffff" opacity="0.5"/>
  <circle r="20" fill="none" stroke="{ink}" stroke-width="2.5"/>
  <line x1="0" y1="-70" x2="0" y2="-54" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>
  <line x1="62" y1="0" x2="78" y2="0" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>
  <line x1="-62" y1="0" x2="-78" y2="0" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>
</g>'''


THEMES = {
    "frozili": ["iced_cup", "candy", "beans"],
    "ohcrisp": ["strawberry", "orange_wheel", "berries", "bowl"],
    "trend":   ["sensory_arc", "candy", "berries"],
}


def _draw_primary(name, ink, accent, rng):
    cx = _g(rng, 175, 225)
    cy = _g(rng, 120, 140)
    s = _g(rng, 0.95, 1.15)
    if name == "iced_cup":
        return _iced_cup(cx, cy, ink, accent, s)
    if name == "candy":
        return _candy(cx, cy, ink, accent, s)
    if name == "beans":
        return _beans(cx - 20, cy - 10, ink, accent, s)
    if name == "strawberry":
        return _strawberry(cx, cy, ink, s)
    if name == "orange_wheel":
        return _orange_wheel(cx, cy, ink, accent, s)
    if name == "berries":
        return _berries(cx, cy, ink, s)
    if name == "bowl":
        return _bowl(cx, cy, ink, accent, s)
    if name == "sensory_arc":
        return _sensory_arc(cx, cy, ink, accent, s)
    return ""


def svg(theme="trend", color="tb-sage", seed="seed"):
    top, bottom, ink, accent = PALETTE.get(color, PALETTE["tb-sage"])
    rng = _rng(seed + color + theme)
    motifs = THEMES.get(theme, THEMES["trend"])
    primary = motifs[int(next(rng) * len(motifs)) % len(motifs)]

    gid = "g" + hashlib.md5((seed + color).encode()).hexdigest()[:8]
    hi_cx = _g(rng, 280, 340)
    hi_cy = _g(rng, 40, 70)

    parts = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Vitablabla illustration" preserveAspectRatio="xMidYMid slice" style="display:block">',
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>',
        f'<circle cx="{hi_cx:.0f}" cy="{hi_cy:.0f}" r="62" fill="#ffffff" opacity="0.28"/>',
        f'<circle cx="40" cy="{H-34}" r="46" fill="#000000" opacity="0.05"/>',
        _draw_primary(primary, ink, accent, rng),
        '</svg>',
    ]
    return "".join(parts)


def figure_html(theme, color, seed, caption, fig_no="FIG. 01"):
    art = svg(theme=theme, color=color, seed=seed)
    return (
        '<figure>\n'
        f'  <div class="post-illustration">{art}</div>\n'
        f'  <figcaption>{caption}</figcaption>\n'
        '</figure>'
    )


if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "frozili"
    c = sys.argv[2] if len(sys.argv) > 2 else "tb-ice"
    s = sys.argv[3] if len(sys.argv) > 3 else "demo"
    print(figure_html(t, c, s, "Fig. 01 — demo"))
