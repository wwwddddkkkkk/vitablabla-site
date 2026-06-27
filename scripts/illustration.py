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
import os

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


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _src_line(source, ink):
    if not source:
        return ""
    s = source if str(source).lower().startswith("source") else "Source: " + str(source)
    return (f'<text x="{PANEL[0]}" y="234" font-family="JetBrains Mono, monospace" '
            f'font-size="10" fill="{ink}" opacity="0.6">{_esc(s[:64])}</text>')


def chart_from_data(data, ink, accent):
    """Render a REAL chart from supplied data with axis + value labels + source.

    data = {
      "type": "bar" | "line",
      "labels": [...], "values": [...],
      "unit": "%" (optional), "source": "...", "highlight": last index (optional)
    }
    """
    ctype = data.get("type", "bar")
    labels = [str(x) for x in data.get("labels", [])]
    values = [float(v) for v in data.get("values", [])]
    unit = data.get("unit", "")
    src = data.get("source", "")
    n = len(values)
    if n == 0:
        return _panel(ink) + _src_line(src, ink)
    hi = data.get("highlight", n - 1)
    x0, y0, x1, y1 = PANEL
    plot_l, plot_r = x0 + 30, x1 - 18
    plot_t, plot_b = y0 + 24, y1 - 24
    vmax = max(values) or 1.0
    LBL = ('font-family="JetBrains Mono, monospace" font-size="11" '
           f'fill="{ink}" text-anchor="middle"')
    VAL = ('font-family="JetBrains Mono, monospace" font-size="11" '
           f'fill="{accent}" text-anchor="middle" font-weight="500"')
    out = [_panel(ink)]

    def fmt(v):
        t = (f"{v:.0f}" if abs(v - round(v)) < 0.05 else f"{v:.1f}")
        return t + unit

    if ctype == "line":
        xs = [plot_l + (plot_r - plot_l) * i / (n - 1 or 1) for i in range(n)]
        ys = [plot_b - (plot_b - plot_t) * (v / vmax) for v in values]
        out.append(f'<line x1="{plot_l}" y1="{plot_b}" x2="{plot_r}" y2="{plot_b}" stroke="{ink}" stroke-width="1.5" opacity="0.5"/>')
        area = f'M {xs[0]:.0f} {plot_b} ' + " ".join(f"L {x:.0f} {y:.0f}" for x, y in zip(xs, ys)) + f' L {xs[-1]:.0f} {plot_b} Z'
        out.append(f'<path d="{area}" fill="{accent}" opacity="0.14"/>')
        out.append('<path d="M ' + " L ".join(f"{x:.0f} {y:.0f}" for x, y in zip(xs, ys)) + f'" fill="none" stroke="{accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
        for i, (x, y, v) in enumerate(zip(xs, ys, values)):
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{accent}"/>')
            if i == 0 or i == n - 1:
                out.append(f'<text x="{x:.0f}" y="{y-8:.0f}" {VAL}>{fmt(v)}</text>')
            out.append(f'<text x="{x:.0f}" y="{plot_b+16:.0f}" {LBL}>{_esc(labels[i] if i < len(labels) else "")}</text>')
    else:  # bar
        gap = 12
        bw = (plot_r - plot_l - gap * (n - 1)) / n
        out.append(f'<line x1="{plot_l-6}" y1="{plot_b}" x2="{plot_r+6}" y2="{plot_b}" stroke="{ink}" stroke-width="1.5"/>')
        for i, v in enumerate(values):
            bx = plot_l + i * (bw + gap)
            bh = (plot_b - plot_t) * (v / vmax)
            fill = accent if i == hi else ink
            op = "1" if i == hi else "0.32"
            out.append(f'<rect x="{bx:.0f}" y="{plot_b-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="3" fill="{fill}" opacity="{op}"/>')
            out.append(f'<text x="{bx+bw/2:.0f}" y="{plot_b-bh-6:.0f}" {VAL}>{fmt(v)}</text>')
            out.append(f'<text x="{bx+bw/2:.0f}" y="{plot_b+16:.0f}" {LBL}>{_esc(labels[i] if i < len(labels) else "")}</text>')
    out.append(_src_line(src, ink))
    return "".join(out)


# ── Abstract editorial motifs for data-LESS trend pieces (not charts) ──
def _abstract_arcs(ink, accent):
    return (f'<g transform="translate({CX},{CY})">'
            f'<circle r="58" fill="none" stroke="{ink}" stroke-width="2" opacity="0.25"/>'
            f'<circle r="40" fill="none" stroke="{ink}" stroke-width="2" opacity="0.35"/>'
            f'<path d="M-58 0 A58 58 0 0 1 0 -58" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M0 40 A40 40 0 0 1 40 0" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>'
            f'<circle r="14" fill="{accent}" opacity="0.85"/></g>')


def _abstract_grid(ink, accent):
    cells = []
    cols, rows = 6, 4
    gw, gh = 30, 30
    ox = CX - (cols - 1) * gw / 2
    oy = CY - (rows - 1) * gh / 2
    for r in range(rows):
        for c in range(cols):
            on_diag = (c >= r + 2)
            fill = accent if on_diag else ink
            op = "0.9" if on_diag else "0.22"
            cells.append(f'<circle cx="{ox+c*gw:.0f}" cy="{oy+r*gh:.0f}" r="5.5" fill="{fill}" opacity="{op}"/>')
    return "<g>" + "".join(cells) + "</g>"


def _abstract_strata(ink, accent):
    out = ["<g>"]
    widths = [0.45, 0.62, 0.80, 1.0]
    for i, w in enumerate(widths):
        y = CY - 48 + i * 30
        ww = 240 * w
        fill = accent if i == len(widths) - 1 else ink
        op = "0.95" if i == len(widths) - 1 else "0.22"
        out.append(f'<rect x="{CX-ww/2:.0f}" y="{y}" width="{ww:.0f}" height="16" rx="8" fill="{fill}" opacity="{op}"/>')
    out.append("</g>")
    return "".join(out)


THEMES = {
    "frozili": ["iced_cup", "candy", "beans"],
    "ohcrisp": ["strawberry", "orange_wheel", "berries", "bowl"],
    "trend":   ["arcs", "grid", "strata"],
}


CX, CY = 200, 125  # fixed centre -> uniform margins


def _draw_primary(name, ink, accent, s):
    if name == "arcs":
        return _abstract_arcs(ink, accent)
    if name == "grid":
        return _abstract_grid(ink, accent)
    if name == "strata":
        return _abstract_strata(ink, accent)
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


def svg(theme="trend", color="tb-sage", seed="seed", data=None):
    """Render an illustration.

    If `data` is provided (real, sourced figures), render an actual labeled
    chart. Otherwise render the themed motif: product motifs for frozili/ohcrisp,
    and an abstract editorial graphic (NOT a fake chart) for trend.
    """
    top, bottom, ink, accent = PALETTE.get(color, PALETTE["tb-sage"])
    rng = _rng(seed + color + theme)
    motifs = THEMES.get(theme, THEMES["trend"])
    primary = motifs[int(next(rng) * len(motifs)) % len(motifs)]
    is_data_chart = bool(data and data.get("values"))
    s = _g(rng, 0.98, 1.06)

    gid = "g" + hashlib.md5((seed + color).encode()).hexdigest()[:8]

    parts = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Vitablabla illustration" preserveAspectRatio="xMidYMid slice" style="display:block">',
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>',
    ]
    if is_data_chart:
        parts.append(chart_from_data(data, ink, accent))
    else:
        parts.append(f'<circle cx="{W//2}" cy="-20" r="120" fill="#ffffff" opacity="0.18"/>')
        parts.append(_draw_primary(primary, ink, accent, s))
    parts.append('</svg>')
    return "".join(parts)


def figure_html(theme, color, seed, caption, fig_no="FIG. 01", data=None):
    art = svg(theme=theme, color=color, seed=seed, data=data)
    return (
        '<figure>\n'
        f'  <div class="post-illustration">{art}</div>\n'
        f'  <figcaption>{caption}</figcaption>\n'
        '</figure>'
    )


if __name__ == "__main__":
    import sys
    import json as _json
    t = sys.argv[1] if len(sys.argv) > 1 else "frozili"
    c = sys.argv[2] if len(sys.argv) > 2 else "tb-ice"
    s = sys.argv[3] if len(sys.argv) > 3 else "demo"
    # Optional 4th arg: inline JSON or a path to a JSON file with real chart data.
    data = None
    if len(sys.argv) > 4:
        raw = sys.argv[4]
        if os.path.exists(raw):
            raw = open(raw, encoding="utf-8").read()
        data = _json.loads(raw)
    print(figure_html(t, c, s, "Fig. 01 — demo", data=data))
