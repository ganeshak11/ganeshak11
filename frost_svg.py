"""Shared pieces for the Frost cards: embedded fonts, colours, the glass card frame, chips, wrapping."""
import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))

RED = "#F21D43"
HOT = "#ff5a76"
FG = "#f4f4f6"
TEXT = "#e8e8ee"
SOFT = "#b9b9c2"
DIM = "#8a8a94"
BG = "#0a0a0d"
OK = "#34C759"

_FONTS = {"ruf": ("Rufscript", 400), "jb-regular": ("Frost Mono", 400), "jb-medium": ("Frost Mono", 500)}


def b64(path):
    with open(os.path.join(HERE, path), "rb") as f:
        return base64.b64encode(f.read()).decode()


def font_faces(names=("ruf", "jb-regular", "jb-medium")):
    return "\n".join(
        f'@font-face {{ font-family: "{_FONTS[n][0]}"; font-weight: {_FONTS[n][1]}; '
        f'src: url(data:font/woff;base64,{b64(f"assets/fonts/{n}.woff")}) format("woff"); }}'
        for n in names)


STYLE = f"""
      .mono {{ font-family: "Frost Mono", "JetBrains Mono", ui-monospace, monospace; }}
      .script {{ font-family: "Rufscript", cursive; }}
      .cap {{ font-family: "Frost Mono", "JetBrains Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: 3px; fill: {DIM}; }}
"""


def esc(s):
    return html.escape(str(s), quote=True)


def wrap(text, width_px, size):
    """Greedy wrap for a monospace font (JetBrains Mono advance is 0.6 em)."""
    per = max(8, int(width_px / (0.6 * size)))
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > per:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def text_lines(x, y, lines, size, fill, lh=None, weight=400):
    lh = lh or round(size * 1.55)
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" class="mono" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def chip_w(label, size=11.5):
    return int(len(label) * 0.6 * size + 22)


def chips(x, y, labels, size=11.5, gap=8, max_w=None, accent=False):
    """A row (wrapping when max_w is set) of glass chips. Returns (svg, bottom_y)."""
    out, cx, cy, h = [], x, y, 24
    for lab in labels:
        w = chip_w(lab, size)
        if max_w and cx + w > x + max_w:
            cx, cy = x, cy + h + gap
        fill, stroke, op = (RED, RED, "0.16") if accent else ("#ffffff", "#ffffff", "0.05")
        out.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" rx="12" fill="{fill}" fill-opacity="{op}" '
                   f'stroke="{stroke}" stroke-opacity="{0.5 if accent else 0.1}"/>'
                   f'<text x="{cx + 11}" y="{cy + 16}" class="mono" font-size="{size}" fill="{TEXT}">{esc(lab)}</text>')
        cx += w + gap
    return "".join(out), cy + h


def card(w, h, body, fonts=("ruf", "jb-regular", "jb-medium"), glow=(0.9, 0.0), glow2=None, rx=20, extra_defs="", margin=(0, 0, 0)):
    """A Frost glass card: near-black, a soft red glow in one corner, a light top edge."""
    g2 = ""
    if glow2:
        g2 = (f'<radialGradient id="g2" cx="{glow2[0]}" cy="{glow2[1]}" r="0.6"><stop offset="0" stop-color="{RED}" stop-opacity="0.14"/>'
              f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>')
    ml, mr, mb = margin                      # transparent gutter, so cards in a grid line up with full-width ones
    W, H = w + ml + mr, h + mb
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
{font_faces(fonts)}
{STYLE}
    </style>
    <radialGradient id="g1" cx="{glow[0]}" cy="{glow[1]}" r="0.7"><stop offset="0" stop-color="{RED}" stop-opacity="0.26"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
    {g2}
    <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.04"/></linearGradient>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
    {extra_defs}
  </defs>
  <g transform="translate({ml}, 0)">
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="{BG}"/>
    <rect width="{w}" height="{h}" fill="url(#g1)"/>
    {'<rect width="%d" height="%d" fill="url(#g2)"/>' % (w, h) if glow2 else ''}
  </g>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx - 0.5}" stroke="url(#edge)"/>
  {body}
  </g>
</svg>
'''
