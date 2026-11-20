#!/usr/bin/env python3
"""Every Frost card on the profile: the banner, section headers, Fortis, experience, projects, stack
and the footer. Fonts are embedded, so they render the same everywhere.

  python3 make_cards.py        writes banner.svg and assets/cards/*.svg

The terminal card (terminal.svg) is written by update_profile.py every six hours.
"""
import os

from frost_svg import (BG, DIM, FG, HOT, OK, RED, SOFT, STYLE, TEXT, b64, card, chip_w, chips, esc,
                       font_faces, text_lines, wrap)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "cards")


def save(name, svg):
    path = os.path.join(HERE, name) if name.endswith("banner.svg") else os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{name:28s} {len(svg) // 1024} KiB")


# ------------------------------------------------------------------ banner

def bars(x0, y0, n=5, w=3, gap=3, h=14):
    out = []
    for i in range(n):
        lo, hi = 3 + (i * 5) % 4, h - (i * 3) % 6
        dur = 0.7 + 0.13 * i
        vals = f"{lo};{hi};{lo + 2};{hi - 3};{lo}"
        ys = ";".join(str(y0 + h - int(v)) for v in vals.split(";"))
        out.append(
            f'<rect x="{x0 + i * (w + gap)}" y="{y0 + h - lo}" width="{w}" height="{lo}" rx="1.5" fill="{RED}">'
            f'<animate attributeName="height" values="{vals}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{ys}" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>')
    return "".join(out)


def banner():
    W, H = 1200, 300
    pill = "building Fortis"
    pw = int(len(pill) * 7.8) + 96
    chip_svg, _ = chips(60, 232, ["Mysuru, India", "ganeshangadi.online", "Rust · Kotlin · Linux"], size=12.5)
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
{font_faces()}
{STYLE}
    </style>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <linearGradient id="shade" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#050507" stop-opacity="0.92"/>
      <stop offset="0.45" stop-color="#050507" stop-opacity="0.55"/>
      <stop offset="0.72" stop-color="#050507" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.04"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="#050507"/>
    <image x="-100" y="-50" width="1600" height="400" preserveAspectRatio="xMidYMid slice"
      xlink:href="data:image/jpeg;base64,{b64("assets/nebula-strip.jpg")}"/>
    <rect width="{W}" height="{H}" fill="url(#shade)"/>
    <g transform="translate({(W - pw) // 2}, 14)">
      <rect width="{pw}" height="34" rx="17" fill="#000"/>
      <rect x="0.5" y="0.5" width="{pw - 1}" height="33" rx="16.5" fill="none" stroke="#fff" stroke-opacity="0.08"/>
      <circle cx="19" cy="17" r="5" fill="{RED}"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="33" y="22" class="mono" font-size="13" font-weight="500" fill="{FG}">{pill}</text>
      {bars(pw - 44, 10)}
    </g>
    <text x="56" y="140" class="script" font-size="68" fill="{FG}">Ganesh Angadi</text>
    <text x="60" y="176" class="mono" font-size="15" font-weight="500" letter-spacing="4" fill="{RED}">SYSTEMS ENGINEER · CLOUD · DEVOPS</text>
    <text x="60" y="206" class="mono" font-size="14" fill="{SOFT}">One user, many machines: my phone and laptops as one system, no cloud.</text>
    {chip_svg}
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="url(#edge)"/>
</svg>
'''


# ------------------------------------------------------------------ section headers

def header(index, cmd, title):
    W, H = 1000, 64
    body = f'''
  <circle cx="30" cy="32" r="5" fill="{RED}"/>
  <text x="48" y="37" class="mono" font-size="13" fill="{DIM}">{index} <tspan fill="{RED}">$</tspan> {esc(cmd)}</text>
  <text x="{48 + len(f"{index} $ {cmd}") * 7.8 + 22:.0f}" y="42" class="script" font-size="30" fill="{FG}">{esc(title)}</text>
  <line x1="{W - 300}" y1="32" x2="{W - 30}" y2="32" stroke="url(#fade)" stroke-width="1.5"/>'''
    fade = (f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{RED}" stop-opacity="0.7"/></linearGradient>')
    return card(W, H, body, glow=(1.0, 0.5), rx=16, extra_defs=fade)


HEADERS = [
    ("01", "whoami", "About me"),
    ("02", "cat fortis/README.md", "Fortis Ecosystem"),
    ("03", "experience", "Experience"),
    ("04", "ls ~/dev", "Projects"),
    ("05", "cat stack.conf", "Stack"),
    ("06", "ls blog/", "Writing"),
    ("07", "gh stats", "On GitHub"),
    ("08", "contact", "Get in touch"),
]


# ------------------------------------------------------------------ Fortis

def fortis():
    W, P = 1000, 44                       # width, padding on every side
    b = []
    b.append(f'<text x="{P}" y="{P + 6}" class="cap">FLAGSHIP · SINCE JULY 2026 · OPEN SOURCE</text>')
    b.append(f'<text x="{W - P}" y="{P + 6}" class="mono" font-size="12" fill="{DIM}" text-anchor="end">Fortis-OS/fortis-ecosystem</text>')
    b.append(f'<text x="{W - P}" y="{P + 26}" class="mono" font-size="12" fill="{DIM}" text-anchor="end">~13k Rust · ~9.7k Kotlin · 9 components</text>')
    b.append(f'<text x="{P}" y="{P + 62}" class="script" font-size="44" fill="{FG}">Fortis Ecosystem</text>')
    lede = ("A password vault, autofill, fingerprint sudo and laptop remote for my Android phone and Linux laptops. "
            "Over Tailscale, no cloud. The docs are the specification: the code has to follow them, and a broken MUST rule blocks a release.")
    ll = wrap(lede, W - 2 * P, 14)
    y = P + 106
    b.append(text_lines(P, y, ll, 14, SOFT, lh=23))
    y += 23 * (len(ll) - 1) + 32

    # architecture band: three nodes, equal gaps, inset from the band like the band is from the card
    band_h, inset, node_h = 124, 22, 80
    b.append(f'<rect x="{P}" y="{y}" width="{W - 2 * P}" height="{band_h}" rx="18" fill="#fff" fill-opacity="0.03" stroke="#fff" stroke-opacity="0.07"/>')
    widths = [236, 244, 212]
    inner = W - 2 * P - 2 * inset
    gap = (inner - sum(widths)) // 2
    xs = [P + inset, P + inset + widths[0] + gap, P + inset + widths[0] + widths[1] + 2 * gap]
    ny = y + (band_h - node_h) // 2

    def node(x, w, name, sub, hub=False):
        stroke = f'stroke="{RED}" stroke-opacity="0.8"' if hub else 'stroke="#fff" stroke-opacity="0.12"'
        fill = f'fill="{RED}" fill-opacity="0.12"' if hub else 'fill="#fff" fill-opacity="0.04"'
        sub_l = wrap(sub, w - 36, 11)[:2]
        return (f'<rect x="{x}" y="{ny}" width="{w}" height="{node_h}" rx="14" {fill} {stroke}/>'
                f'<text x="{x + 18}" y="{ny + 30}" class="mono" font-size="14" font-weight="500" fill="{FG}">{esc(name)}</text>'
                + text_lines(x + 18, ny + 52, sub_l, 11, DIM, lh=16))

    b.append(node(xs[0], widths[0], "fortis-mobile", "Kotlin · Compose: vault, autofill, sudo, remote, webcam"))
    b.append(node(xs[1], widths[1], "fortis-agent", "Rust daemon: REST on 127.0.0.1 and the tailnet, IPC socket", hub=True))
    b.append(node(xs[2], widths[2], "desktop · cli", "Tauri app and a terminal client"))
    mid = ny + node_h // 2
    for (x1, x2), lab in (((xs[0] + widths[0], xs[1]), "Tailscale"), ((xs[1] + widths[1], xs[2]), "IPC")):
        b.append(f'<line x1="{x1 + 8}" y1="{mid}" x2="{x2 - 8}" y2="{mid}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 5">'
                 f'<animate attributeName="stroke-dashoffset" values="18;0" dur="1.2s" repeatCount="indefinite"/></line>')
        b.append(f'<text x="{(x1 + x2) // 2}" y="{mid - 10}" class="mono" font-size="10" fill="{DIM}" text-anchor="middle">{lab}</text>')
    y += band_h + 44

    feats = [
        ("Encrypted vault + autofill", "SQLCipher vault on the laptop, an encrypted copy on the phone, autofill on both."),
        ("Fingerprint-approved sudo", "A Rust PAM module asks the phone and checks its signature against a root-owned key."),
        ("TOTP codes", "2FA codes on both devices, generated from the same encrypted vault."),
        ("Laptop remote", "Files, actions, notifications and keyboard/mouse from the phone, behind a fresh fingerprint."),
        ("Phone as webcam", "Streams only on the phone's Tailscale address, to the paired laptop."),
        ("Encrypted backups", "Hard-linked snapshots on a systemd timer, with an off-site copy on the phone."),
    ]
    cgap = 40
    colw = (W - 2 * P - cgap) // 2
    row_h = 84
    for i, (t, d) in enumerate(feats):
        x = P + (i % 2) * (colw + cgap)
        yy = y + (i // 2) * row_h
        b.append(f'<rect x="{x}" y="{yy - 15}" width="3" height="56" rx="1.5" fill="{RED}"/>')
        b.append(f'<text x="{x + 18}" y="{yy}" class="mono" font-size="14" font-weight="500" fill="{FG}">{esc(t)}</text>')
        b.append(text_lines(x + 18, yy + 22, wrap(d, colw - 24, 12)[:2], 12, DIM, lh=18))
    y += 3 * row_h - 18 + 32

    b.append(f'<text x="{P}" y="{y}" class="cap">ONLY THESE PRIMITIVES</text>')
    c, bottom = chips(P, y + 14, ["Argon2id", "HKDF-SHA-256", "SQLCipher 4", "XChaCha20-Poly1305", "ECDSA P-256", "RFC 6238 TOTP"], accent=True, gap=10)
    b.append(c)
    return card(W, bottom + P, "\n  ".join(b), glow=(0.95, 0.0), glow2=(0.0, 1.0))


# ------------------------------------------------------------------ experience

def experience():
    W = 1000
    items = [
        ("FOUNDING SDE", "Founding Software Engineer (Intern) · Vaniger", "Kridtech Corp. · Jul – Oct 2026",
         "Kept a live conversational sales and telephony SaaS deployed for 2+ months across a GCP VM (Node.js, Nginx, PM2) and Vercel. "
         "Built the GitHub Actions pipelines with zero-downtime restarts, browser WebRTC calling over a Telnyx SIP bridge, live AI coaching "
         "on Deepgram dual-channel streams and an atomic PostgreSQL billing ledger.",
         ["WebRTC", "Telnyx", "Deepgram", "Node.js", "PostgreSQL", "CI/CD", "GCP", "Next.js"],
         ("If circumstances permitted, I would gladly retain Ganesh as a full-time member of our engineering team.",
          "Rananjay Kandamwar, Co-Founder & CEO, Kridtech")),
        ("1ST PLACE", "MCP-Based Systems Engineering Hackathon", "Open Innovation · Apr 2026",
         "Built an MCP server around an Indian Sign Language translator so AI assistants can use it. Focused on the integration layer, not on reinventing the tool.",
         ["MCP", "Python", "Protocol design"], None),
        ("INTERNSHIP", "AI & Machine Learning Intern", "Artsy Technologies · May – Jun 2026",
         "Python machine-learning projects with the engineering team, turning models into deployable components.",
         ["Python", "AI/ML"], None),
    ]
    b, y = [], 60
    for i, (badge, title, org, desc, tags, quote) in enumerate(items):
        top = y
        bw = chip_w(badge, 10.5) + len(badge)
        solid = i < 2
        b.append(f'<rect x="76" y="{y - 16}" width="{bw}" height="22" rx="11" fill="{RED}" fill-opacity="{0.9 if solid else 0.15}" stroke="{RED}" stroke-opacity="0.6"/>'
                 f'<text x="{76 + 11}" y="{y - 1}" class="mono" font-size="10.5" letter-spacing="1" font-weight="500" fill="{FG}">{badge}</text>')
        b.append(f'<text x="{76 + bw + 12}" y="{y - 0}" class="mono" font-size="12" fill="{DIM}">{esc(org)}</text>')
        y += 32
        b.append(f'<text x="76" y="{y}" class="mono" font-size="17" font-weight="500" fill="{FG}">{esc(title)}</text>')
        y += 26
        lines = wrap(desc, W - 120, 12.5)
        b.append(text_lines(76, y, lines, 12.5, SOFT, lh=19))
        y += 19 * (len(lines) - 1) + 22
        if quote:
            ql = wrap(f"“{quote[0]}”", W - 150, 15)
            b.append(f'<rect x="76" y="{y}" width="3" height="{len(ql) * 22 + 22}" rx="1.5" fill="{RED}"/>')
            b.append(f'<text x="94" y="{y + 18}" class="script" font-size="17" fill="{TEXT}">' +
                     "".join(f'<tspan x="94" dy="{0 if k == 0 else 22}">{esc(l)}</tspan>' for k, l in enumerate(ql)) + '</text>')
            b.append(f'<text x="94" y="{y + 18 + len(ql) * 22}" class="mono" font-size="11.5" fill="{DIM}">— {esc(quote[1])}</text>')
            y += len(ql) * 22 + 42
        c, y2 = chips(76, y, tags, size=11)
        b.append(c)
        y = y2 + 56
        # timeline
        b.append(f'<circle cx="44" cy="{top - 5}" r="7" fill="{BG}" stroke="{RED}" stroke-width="2"/>'
                 f'<circle cx="44" cy="{top - 5}" r="3" fill="{RED}"/>')
        if i < len(items) - 1:
            b.append(f'<line x1="44" y1="{top + 4}" x2="44" y2="{y - 30}" stroke="{RED}" stroke-opacity="0.35" stroke-width="1.5"/>')
    H = y - 12
    return card(W, H, "\n  ".join(b), glow=(1.0, 0.0))


# ------------------------------------------------------------------ projects

PROJECTS = [
    ("frost", "Frost", "Daily driver", OK,
     "A dark glass KDE Plasma 6 desktop and an Android launcher that work as one machine.",
     ["Generated theme, boot to editor: GRUB to VS Code", "Island, Spotlight, widgets; phone synced over Tailscale"],
     ["Plasma 6", "QML", "Python", "Kotlin"]),
    ("fortisos", "FortisOS", "In design", HOT,
     "One user, many machines: a personal distributed OS layer.",
     ["Op-log metadata engine, encrypted chunk store", "Deterministic fault simulator, power-cut crash tests"],
     ["Rust", "Distributed systems"]),
    ("fortis-tools", "Fortis-Tools", "On npm", OK,
     "Small CLIs: fortis-share (AirDrop for Linux to Android) and healthcheck.",
     ["Files, screenshots, clipboard to the phone; QR fallback", "DNS, SSL, HTTP/2, headers, SPF/DMARC; JSON for CI"],
     ["TypeScript", "Node.js", "Tailscale"]),
    ("mysurubus", "MY(suru) BUS", "Tested", HOT,
     "Real-time bus tracking and fleet management: four apps, one backend.",
     ["Socket.io rooms per bus; offline-first driver app", "Geofenced stops; trigram route search"],
     ["Node.js", "PostgreSQL", "React Native", "Next.js"]),
    ("mechkeys", "mechkeys", "Hobby", RED,
     "Mechanical keyboard sounds for any keyboard, with no lag.",
     ["Samples decoded once, mixed in memory", "Daemon over a Unix socket, per-key packs"],
     ["Rust", "evdev", "rodio"]),
    ("devcard", "DevCard", "On npm", OK,
     "npx ganeshak11: my business card in the terminal.",
     ["Interactive palette, QR code to the portfolio", "And a duck you can summon"],
     ["TypeScript", "Node.js", "Inquirer"]),
    ("fortis-observe", "FortisObserve", "Deployed", OK,
     "Privacy-first telemetry and command centre for my site.",
     ["TOTP and WebAuthn at the edge", "Live 3D globe of connections"],
     ["Next.js", "Supabase", "WebGL"]),
    ("fortis-ci", "Fortis-CI", "~80%", HOT,
     "Deployment observability: pipelines as a graph, RCA and rollback.",
     ["Idempotent webhook ingestion, health polling", "One-click rollback from the dashboard"],
     ["TypeScript", "Neo4j", "GitHub Actions"]),
]


def project(name, status, scol, tagline, points, stack, side="L"):
    W, H = 480, 262
    b = [f'<circle cx="34" cy="36" r="4.5" fill="{scol}"/>',
         f'<text x="46" y="40" class="cap" fill="{DIM}">{esc(status.upper())}</text>',
         f'<text x="30" y="88" class="script" font-size="32" fill="{FG}">{esc(name)}</text>',
         text_lines(30, 118, wrap(tagline, W - 60, 13)[:2], 13, TEXT, lh=19)]
    y = 118 + 19 * (len(wrap(tagline, W - 60, 13)[:2]) - 1) + 28
    for p in points:
        b.append(f'<text x="30" y="{y}" class="mono" font-size="11.5" fill="{DIM}"><tspan fill="{RED}">›</tspan> {esc(p)}</text>')
        y += 19
    c, _ = chips(30, H - 54, stack, size=11)
    b.append(c)
    b.append(f'<text x="{W - 30}" y="42" class="mono" font-size="14" fill="{DIM}" text-anchor="end">↗</text>')
    gut = 8
    return card(W, H, "\n  ".join(b), glow=(1.0, 0.0), rx=18, margin=(0, gut, 2 * gut) if side == "L" else (gut, 0, 2 * gut))


# ------------------------------------------------------------------ stack

def stack():
    W = 1000
    groups = [
        ("SYSTEMS & SECURITY", ["Rust", "Linux PAM", "systemd", "Unix sockets", "Tailscale / WireGuard", "SQLCipher", "Argon2id", "Android Keystore"]),
        ("CLOUD & INFRA", ["Linux", "Nginx", "GCP", "AWS EC2", "Docker", "Compose", "Terraform", "Kubernetes"]),
        ("CI/CD & RELEASE", ["GitHub Actions", "Vercel", "PM2", "Git (rebase, cherry-pick, tags)", "Bash"]),
        ("BACKEND", ["Node.js", "Express", "PostgreSQL", "Redis", "Neo4j", "Socket.IO", "MCP"]),
        ("APPS & DESKTOP", ["Kotlin", "Jetpack Compose", "Tauri", "Next.js", "React Native", "QML / KDE Plasma"]),
        ("LANGUAGES", ["Rust", "Kotlin", "TypeScript", "Python", "Bash", "C", "C++", "Java"]),
    ]
    b, y = [], 44
    for label, items in groups:
        b.append(f'<text x="44" y="{y + 16}" class="cap">{esc(label)}</text>')
        c, bot = chips(254, y, items, size=12, max_w=W - 298, accent=(label == "LANGUAGES"))
        b.append(c)
        y = bot + 22
    return card(W, y + 22, "\n  ".join(b), glow=(0.0, 0.0))


# ------------------------------------------------------------------ footer

def footer():
    W, H = 1000, 236
    status = "open to roles in systems, cloud, DevOps/SRE"
    sw = 14 + len(status) * 0.6 * 13           # dot + gap + text
    sx = (W - sw) / 2
    b = [f'<text x="{W // 2}" y="84" class="script" font-size="40" fill="{FG}" text-anchor="middle">Infrastructure isn’t magic.</text>',
         f'<text x="{W // 2}" y="118" class="mono" font-size="14" fill="{SOFT}" text-anchor="middle">It’s thousands of engineering decisions and their trade-offs.</text>',
         f'<circle cx="{sx + 5:.0f}" cy="164" r="5" fill="{OK}"><animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/></circle>',
         f'<text x="{sx + 18:.0f}" y="169" class="mono" font-size="13" fill="{TEXT}">{status}</text>',
         f'<text x="{W // 2}" y="198" class="mono" font-size="12" fill="{DIM}" text-anchor="middle">email is the fastest way to reach me</text>']
    return card(W, H, "\n  ".join(b), glow=(0.5, 1.1))


def main():
    os.makedirs(OUT, exist_ok=True)
    save("banner.svg", banner())
    for idx, cmd, title in HEADERS:
        save(f"head-{idx}.svg", header(idx, cmd, title))
    save("fortis.svg", fortis())
    save("experience.svg", experience())
    for i, (key, *rest) in enumerate(PROJECTS):
        save(f"project-{key}.svg", project(*rest, side="LR"[i % 2]))
    save("stack.svg", stack())
    save("footer.svg", footer())


if __name__ == "__main__":
    main()
