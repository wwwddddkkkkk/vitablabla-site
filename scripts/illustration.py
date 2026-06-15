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


# ── Trend / analysis charts (editorial "PPT" style, not cute) ─────────
# All charts are drawn inside a fixed inset panel so the margins are uniform.
PANEL = (44, 50, 356, 200)  # x0, y0, x1, y1


def _panel(ink):
    x0, y0, x1, y1 = PANEL
    return (f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="10" '
            f'fill="#FBF7EE" opacity="0.72" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.5"/>')


def _chart_bars(ink, accent):
    x0, y0, x1, y1 = PANEL
    base = y1 - 22
    left = x0 + 26
    right = x1 - 26
    n = 5
    gap = 14
    bw = (right - left - gap * (n - 1)) / n
    heights = [0.30, 0.44, 0.55, 0.72, 0.95]
    out = [f'<line x1="{left-8}" y1="{base}" x2="{right+8}" y2="{base}" stroke="{ink}" stroke-width="1.5"/>']
    for i, h in enumerate(heights):
        bx = left + i * (bw + gap)
        bh = (base - (y0 + 26)) * h
        fill = accent if i == n - 1 else ink
        op = "1" if i == n - 1 else "0.30"
        out.append(f'<rect x="{bx:.0f}" y="{base-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="3" fill="{fill}" opacity="{op}"/>')
    # rising trend arrow across the tops
    y_for = lambda h: base - (base - (y0 + 26)) * h - 8
    pts = " ".join(f"{left + i*(bw+gap) + bw/2:.0f},{y_for(h):.0f}" for i, h in enumerate(heights))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 5"/>')
    return "".join(out)


def _chart_line(ink, accent):
    x0, y0, x1, y1 = PANEL
    bx0, by0, bx1, by1 = x0 + 24, y0 + 22, x1 - 22, y1 - 24
    out = [f'<line x1="{bx0}" y1="{by0}" x2="{bx0}" y2="{by1}" stroke="{ink}" stroke-width="1.5" opacity="0.6"/>',
           f'<line x1="{bx0}" y1="{by1}" x2="{bx1}" y2="{by1}" stroke="{ink}" stroke-width="1.5" opacity="0.6"/>']
    ys = [0.25, 0.20, 0.42, 0.38, 0.62, 0.80, 0.96]
    n = len(ys)
    xs = [bx0 + (bx1 - bx0) * i / (n - 1) for i in range(n)]
    pys = [by1 - (by1 - by0) * v for v in ys]
    area = f'M {xs[0]:.0f} {by1} ' + " ".join(f"L {x:.0f} {y:.0f}" for x, y in zip(xs, pys)) + f' L {xs[-1]:.0f} {by1} Z'
    out.append(f'<path d="{area}" fill="{accent}" opacity="0.16"/>')
    line = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in zip(xs, pys))
    out.append(f'<path d="{line}" fill="none" stroke="{accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{xs[-1]:.0f}" cy="{pys[-1]:.0f}" r="5.5" fill="{accent}" stroke="#FBF7EE" stroke-width="2"/>')
    return "".join(out)


def _chart_quadrant(ink, accent):
    x0, y0, x1, y1 = PANEL
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    out = [f'<line x1="{x0+22}" y1="{cy:.0f}" x2="{x1-22}" y2="{cy:.0f}" stroke="{ink}" stroke-width="1.5" opacity="0.55"/>',
           f'<line x1="{cx:.0f}" y1="{y0+18}" x2="{cx:.0f}" y2="{y1-18}" stroke="{ink}" stroke-width="1.5" opacity="0.55"/>']
    dots = [(-0.5, 0.45, 0.30, 6), (0.45, 0.40, 0.30, 6), (-0.4, -0.4, 0.30, 6), (0.55, -0.5, 1.0, 10)]
    for dx, dy, op, r in dots:
        px = cx + dx * (x1 - x0) / 2 * 0.7
        py = cy - dy * (y1 - y0) / 2 * 0.7
        out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="{accent}" opacity="{op}"/>')
    return "".join(out)


def _chart_donut(ink, accent):
    x0, y0, x1, y1 = PANEL
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    r = 52
    import math
    frac = 0.62
    a = -90 + 360 * frac
    rad = math.radians(a)
    ex = cx + r * math.cos(math.radians(-90)) + 0
    # base ring
    out = [f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="none" stroke="{ink}" stroke-width="16" opacity="0.22"/>']
    x_start = cx + r * math.cos(math.radians(-90))
    y_start = cy + r * math.sin(math.radians(-90))
    x_end = cx + r * math.cos(rad)
    y_end = cy + r * math.sin(rad)
    large = 1 if frac > 0.5 else 0
    out.append(f'<path d="M {x_start:.1f} {y_start:.1f} A {r} {r} 0 {large} 1 {x_end:.1f} {y_end:.1f}" fill="none" stroke="{accent}" stroke-width="16" stroke-linecap="butt"/>')
    out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r-26}" fill="#FBF7EE" opacity="0.5"/>')
    return "".join(out)


def _trend_chart(name, ink, accent):
    body = {"bars": _chart_bars, "line": _chart_line,
            "quadrant": _chart_quadrant, "donut": _chart_donut}[name](ink, accent)
    return _panel(ink) + body


THEMES = {
    "frozili": ["iced_cup", "candy", "beans"],
    "ohcrisp": ["strawberry", "orange_wheel", "berries", "bowl"],
    "trend":   ["bars", "line", "quadrant", "donut"],
}


CX, CY = 200, 125  # fixed centre -> uniform margins


def _draw_primary(name, ink, accent, s):
    if name in ("bars", "line", "quadrant", "donut"):
        return _trend_chart(name, ink, accent)
    if name == "iced_cup":
        return _iced_cup(CX, CY, ink, accent, s)
    if name == "candy":
        return _candy(CX, CY, ink, accent, s)
    if name == "beans":
        return _beans(CX - 22, CY - 10, ink, accent, s)
    if name == "strawberry":
        return _strawberry(CX, CY - 6, ink, s)
    if name == "orange_wheel":
        return _orange_wheel(CX, CY, ink, accent, s)
    if name == "berries":
        return _berries(CX, CY, ink, s)
    if name == "bowl":
        return _bowl(CX, CY - 6, ink, accent, s)
    return ""


def svg(theme="trend", color="tb-sage", seed="seed"):
    top, bottom, ink, accent = PALETTE.get(color, PALETTE["tb-sage"])
    rng = _rng(seed + color + theme)
    motifs = THEMES.get(theme, THEMES["trend"])
    primary = motifs[int(next(rng) * len(motifs)) % len(motifs)]
    is_chart = primary in ("bars", "line", "quadrant", "donut")
    s = _g(rng, 0.98, 1.06)

    gid = "g" + hashlib.md5((seed + color).encode()).hexdigest()[:8]

    parts = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Vitablabla illustration" preserveAspectRatio="xMidYMid slice" style="display:block">',
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>',
    ]
    # Product motifs sit on a soft gradient with one symmetric highlight.
    # Charts sit directly on the gradient inside their own panel (cleaner).
    if not is_chart:
        parts.append(f'<circle cx="{W//2}" cy="-20" r="120" fill="#ffffff" opacity="0.18"/>')
    parts.append(_draw_primary(primary, ink, accent, s))
    parts.append('</svg>')
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
