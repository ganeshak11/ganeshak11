#!/usr/bin/env python3
"""Frost banner for the profile README: the crimson nebula, a Dynamic Island pill and the name in
Rufscript. Fonts and the background are embedded, so it renders the same everywhere.

  python3 make_banner.py        writes banner.svg
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def b64(path):
    with open(os.path.join(HERE, path), "rb") as f:
        return base64.b64encode(f.read()).decode()


def font_faces(names=("ruf", "jb-regular", "jb-medium")):
    fam = {"ruf": ("Rufscript", 400), "jb-regular": ("Frost Mono", 400), "jb-medium": ("Frost Mono", 500)}
    return "\n".join(
        f'@font-face {{ font-family: "{fam[n][0]}"; font-weight: {fam[n][1]}; '
        f'src: url(data:font/woff;base64,{b64(f"assets/fonts/{n}.woff")}) format("woff"); }}'
        for n in names)


def bars(x0, y0, n=5, w=3, gap=3, h=14):
    """Little beat bars like the island's music activity, bouncing forever."""
    out = []
    for i in range(n):
        lo, hi = 3 + (i * 5) % 4, h - (i * 3) % 6
        dur = 0.7 + 0.13 * i
        vals = f"{lo};{hi};{lo + 2};{hi - 3};{lo}"
        ys = ";".join(str(y0 + h - int(v)) for v in vals.split(";"))
        out.append(
            f'<rect x="{x0 + i * (w + gap)}" y="{y0 + h - lo}" width="{w}" height="{lo}" rx="1.5" fill="#F21D43">'
            f'<animate attributeName="height" values="{vals}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{ys}" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>')
    return "".join(out)


def main():
    W, H = 1200, 300
    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
{font_faces()}
      .name {{ font-family: "Rufscript", cursive; font-size: 68px; fill: #f4f4f6; }}
      .mono {{ font-family: "Frost Mono", "JetBrains Mono", ui-monospace, monospace; }}
      .role {{ font-size: 15px; letter-spacing: 4px; fill: #F21D43; font-weight: 500; }}
      .line {{ font-size: 14px; fill: #b9b9c2; }}
      .chip {{ font-size: 12.5px; fill: #e8e8ee; }}
      .pill {{ font-size: 13px; fill: #f4f4f6; font-weight: 500; }}
      .dim  {{ fill: #8a8a94; }}
    </style>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <linearGradient id="shade" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#050507" stop-opacity="0.92"/>
      <stop offset="0.42" stop-color="#050507" stop-opacity="0.55"/>
      <stop offset="0.7" stop-color="#050507" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.04"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="#050507"/>
    <image x="-100" y="-50" width="1600" height="400" preserveAspectRatio="xMidYMid slice"
      xlink:href="data:image/jpeg;base64,{b64("assets/nebula-strip.jpg")}"/>
    <rect width="{W}" height="{H}" fill="url(#shade)"/>

    <!-- Dynamic Island: music live activity -->
    <g transform="translate({W // 2 - 140}, 14)">
      <rect width="280" height="34" rx="17" fill="#000000"/>
      <rect x="0.5" y="0.5" width="279" height="33" rx="16.5" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
      <circle cx="19" cy="17" r="5" fill="#F21D43"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="33" y="22" class="mono pill">building Fortis · Frost</text>
      {bars(240, 10)}
    </g>

    <text x="56" y="140" class="name">Ganesh Angadi</text>
    <text x="60" y="176" class="mono role">DEVOPS · PLATFORM · SYSTEMS</text>
    <text x="60" y="206" class="mono line">Linux, Rust, Tailscale. Phone and laptop as one machine.</text>

    <g class="mono" transform="translate(60, 232)">
      <rect width="134" height="30" rx="15" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.10"/>
      <circle cx="17" cy="15" r="4" fill="#F21D43"/><text x="29" y="19.5" class="chip">Mysuru, India</text>
      <rect x="146" width="176" height="30" rx="15" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.10"/>
      <circle cx="163" cy="15" r="4" fill="#F21D43"/><text x="175" y="19.5" class="chip">ganeshangadi.online</text>
      <rect x="334" width="150" height="30" rx="15" fill="#F21D43" fill-opacity="0.16" stroke="#F21D43" stroke-opacity="0.55"/>
      <text x="350" y="19.5" class="chip">KDE · Frost <tspan class="dim">#F21D43</tspan></text>
    </g>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="url(#edge)"/>
</svg>
'''
    with open(os.path.join(HERE, "banner.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("banner.svg", len(svg) // 1024, "KiB")


if __name__ == "__main__":
    main()
