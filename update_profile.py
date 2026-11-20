import datetime
import json
import os
import urllib.request
import calendar

# Birthdate: January 13, 2006
BIRTHDATE = datetime.datetime(2006, 1, 13, 0, 0, 0, tzinfo=datetime.timezone.utc)

def get_uptime(birthday, now):
    # Calculate exact difference in years, months, days, hours, minutes, seconds
    years = now.year - birthday.year
    months = now.month - birthday.month
    days = now.day - birthday.day
    hours = now.hour - birthday.hour
    minutes = now.minute - birthday.minute
    seconds = now.second - birthday.second

    if seconds < 0:
        minutes -= 1
        seconds += 60
    if minutes < 0:
        hours -= 1
        minutes += 60
    if hours < 0:
        days -= 1
        hours += 24
    if days < 0:
        months -= 1
        # Get days in previous month
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        _, days_in_prev = calendar.monthrange(prev_year, prev_month)
        days += days_in_prev
    if months < 0:
        years -= 1
        months += 12

    return years, months, days, hours, minutes, seconds

def fetch_github_stats(username):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "User-Agent": "ganeshak11-github-profile-readme",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    # Default fallback values based on user's current README
    stats = {
        "commits": 2116,
        "stars": 342,
        "repos": 95,
        "followers": 196
    }

    def get_json(url):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    # 1. Fetch User Profile
    user_data = get_json(f"https://api.github.com/users/{username}")
    if user_data:
        stats["repos"] = user_data.get("public_repos", stats["repos"])
        stats["followers"] = user_data.get("followers", stats["followers"])

    # 2. Fetch Stars count (by summing stargazers_count across public repos)
    repos_data = get_json(f"https://api.github.com/users/{username}/repos?per_page=100")
    if repos_data and isinstance(repos_data, list):
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        stats["stars"] = total_stars

    # 3. Fetch Commits count
    commits_data = get_json(f"https://api.github.com/search/commits?q=author:{username}")
    if commits_data and "total_count" in commits_data:
        stats["commits"] = commits_data["total_count"]

    return stats

def wrap_text(text, max_len=42):
    if len(text) <= max_len:
        return [text]
    words = text.split(' ')
    lines = []
    current_line = []
    current_len = 0
    for word in words:
        # Add 1 for space if it's not the first word on the line
        space_padding = 1 if current_line else 0
        if current_len + len(word) + space_padding <= max_len:
            current_line.append(word)
            current_len += len(word) + space_padding
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_len = len(word)
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def generate_svg(uptime, stats):
    """The Frost terminal card: a dark glass window in Frost red, with the same fonts as the desktop."""
    from make_banner import font_faces

    years, months, days, hours, minutes, seconds = uptime
    uptime_str = f"{years}y {months}m {days}d {hours}h {minutes}m"

    specs = [
        ("OS", "Ubuntu 26.04.1 LTS"),
        ("Host", "Vostro 15 3515"),
        ("Kernel", "7.0.0-44-generic"),
        ("Uptime", uptime_str),
        ("DE", "KDE Plasma 6 · Frost"),
        ("Shell", "bash · kitty"),
        ("IDE", "VS Code, Vim"),
        ("Languages", "Go, TypeScript, Rust, Python, C"),
        ("Building", "Fortis Ecosystem, Frost"),
    ]
    rows = []
    for i, (key, val) in enumerate(specs):
        y = 132 + i * 24
        rows.append(f'<text x="500" y="{y}" class="mono key">{key}</text>'
                    f'<text x="612" y="{y}" class="mono val">{val}</text>')
    specs_block = "\n    ".join(rows)

    tiles = [("COMMITS", stats["commits"]), ("STARS", stats["stars"]),
             ("REPOS", stats["repos"]), ("FOLLOWERS", stats["followers"])]
    tile_svg = []
    for i, (label, value) in enumerate(tiles):
        x = 500 + i * 106
        tile_svg.append(
            f'<rect x="{x}" y="372" width="96" height="74" rx="14" class="glass"/>'
            f'<text x="{x + 14}" y="396" class="mono cap">{label}</text>'
            f'<text x="{x + 14}" y="428" class="mono big">{value:,}</text>')
    tiles_block = "\n    ".join(tile_svg)

    ascii_rows = [
        "  ██████╗  █████╗ ███╗   ██╗███████╗███████╗██╗  ██╗",
        " ██╔════╝ ██╔══██╗████╗  ██║██╔════╝██╔════╝██║  ██║",
        " ██║  ███╗███████║██╔██╗ ██║█████╗  ███████╗███████║",
        " ██║   ██║██╔══██║██║╚██╗██║██╔══╝  ╚════██║██╔══██║",
        " ╚██████╔╝██║  ██║██║ ╚████║███████╗███████║██║  ██║",
        "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝",
    ]
    ascii_block = "".join(f'<tspan x="44" dy="{0 if i == 0 else 14}">{r}</tspan>' for i, r in enumerate(ascii_rows))

    def kv(x, y, key, val, cls="val", dot=False):
        d = f'<circle cx="{x + 248}" cy="{y - 4}" r="3.5" fill="#F21D43"/>' if dot else ""
        return (f'<text x="{x}" y="{y}" class="mono key2">{key}</text>'
                f'<text x="{x + 360}" y="{y}" class="mono {cls}" text-anchor="end">{val}</text>{d}')

    status = "\n    ".join([
        kv(60, 252, "Status", "Active", "hot"),
        kv(60, 276, "Memory", "4.1 / 5.7 GiB"),
        kv(60, 300, "Disk", "176 / 468 GiB"),
        kv(60, 324, "Phone", "linked over Tailscale"),
    ])
    infra = "\n    ".join([
        kv(60, 400, "Pipeline", "Healthy", "hot"),
        kv(60, 424, "Containers", "Running", "hot"),
        kv(60, 448, "Infra", "Synced", "hot"),
    ])

    return f"""<svg width="100%" height="100%" viewBox="0 0 960 540" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
{font_faces()}
      .mono  {{ font-family: "Frost Mono", "JetBrains Mono", ui-monospace, monospace; font-size: 13px; }}
      .ascii {{ font-family: "Frost Mono", "JetBrains Mono", ui-monospace, monospace; font-size: 11.5px; white-space: pre; font-weight: 500; }}
      .script {{ font-family: "Rufscript", cursive; }}
      .title {{ font-size: 13px; fill: #8a8a94; }}
      .key   {{ fill: #F21D43; font-weight: 500; }}
      .key2  {{ fill: #8a8a94; }}
      .val   {{ fill: #e8e8ee; }}
      .hot   {{ fill: #ff5a76; font-weight: 500; }}
      .cap   {{ font-size: 10px; letter-spacing: 2px; fill: #8a8a94; }}
      .big   {{ font-size: 22px; fill: #f4f4f6; font-weight: 500; }}
      .label {{ font-size: 10.5px; letter-spacing: 3px; fill: #8a8a94; }}
      .glass {{ fill: #ffffff; fill-opacity: 0.035; stroke: #ffffff; stroke-opacity: 0.08; }}
      .cursor {{ fill: #F21D43; animation: blink 1s step-end infinite; }}
      @keyframes blink {{ 50% {{ fill: transparent; }} }}
    </style>
    <radialGradient id="glowA" cx="0.88" cy="0.05" r="0.6">
      <stop offset="0" stop-color="#F21D43" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#F21D43" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.05" cy="1" r="0.55">
      <stop offset="0" stop-color="#F21D43" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#F21D43" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ink" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#ff5a76"/>
      <stop offset="1" stop-color="#F21D43"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.04"/>
    </linearGradient>
    <clipPath id="win"><rect x="8" y="8" width="944" height="524" rx="20"/></clipPath>
    <clipPath id="type-clip">
      <rect x="632" y="482" width="0" height="24">
        <animate attributeName="width" values="0.0;7.8;15.6;23.4;31.2;39.0;46.8;54.6;62.4;70.2;70.2" dur="4s" repeatCount="indefinite" keyTimes="0;0.04;0.08;0.12;0.16;0.2;0.24;0.28;0.32;0.36;1"/>
      </rect>
    </clipPath>
  </defs>

  <g clip-path="url(#win)">
    <rect x="8" y="8" width="944" height="524" fill="#0a0a0d"/>
    <rect x="8" y="8" width="944" height="524" fill="url(#glowA)"/>
    <rect x="8" y="8" width="944" height="524" fill="url(#glowB)"/>
    <rect x="8" y="8" width="944" height="40" fill="#ffffff" fill-opacity="0.03"/>
    <line x1="8" y1="48" x2="952" y2="48" stroke="#ffffff" stroke-opacity="0.07"/>
  </g>
  <rect x="8.5" y="8.5" width="943" height="523" rx="19.5" stroke="url(#edge)"/>

  <!-- title bar: Frost window buttons -->
  <circle cx="32" cy="28" r="6" fill="#F21D43"/>
  <circle cx="52" cy="28" r="6" fill="#ffffff" fill-opacity="0.14"/>
  <circle cx="72" cy="28" r="6" fill="#ffffff" fill-opacity="0.14"/>
  <text x="480" y="32" class="mono title" text-anchor="middle">ganesh@frost: ~</text>

  <!-- left: name and status cards -->
  <text x="44" y="92" class="ascii" fill="url(#ink)" xml:space="preserve">{ascii_block}</text>

  <rect x="40" y="208" width="400" height="136" rx="16" class="glass"/>
  <text x="60" y="230" class="mono label">SYSTEM</text>
    {status}

  <rect x="40" y="358" width="400" height="108" rx="16" class="glass"/>
  <text x="60" y="380" class="mono label">INFRASTRUCTURE</text>
    {infra}

  <text x="44" y="504" class="script" font-size="17" fill="#8a8a94">Infrastructure isn't magic.</text>

  <!-- right: prompt, specs, metrics -->
  <text x="500" y="92" class="mono" font-size="15"><tspan class="key">ganesh</tspan><tspan fill="#8a8a94">@</tspan><tspan class="val" font-weight="500">frost</tspan></text>
  <line x1="500" y1="106" x2="920" y2="106" stroke="#ffffff" stroke-opacity="0.08"/>
    {specs_block}

  <text x="500" y="358" class="mono label">GITHUB</text>
    {tiles_block}

  <text x="500" y="500" class="mono"><tspan class="key">ganesh</tspan><tspan fill="#8a8a94">@</tspan><tspan class="val">frost</tspan><tspan fill="#8a8a94">:~$ </tspan></text>
  <text x="632" y="500" class="mono val" clip-path="url(#type-clip)">fastfetch</text>
  <rect x="632" y="489" width="8" height="15" rx="1" class="cursor">
    <animate attributeName="x" values="632.0;639.8;647.6;655.4;663.2;671.0;678.8;686.6;694.4;702.2;702.2" dur="4s" repeatCount="indefinite" keyTimes="0;0.04;0.08;0.12;0.16;0.2;0.24;0.28;0.32;0.36;1"/>
  </rect>
</svg>
"""

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    uptime = get_uptime(BIRTHDATE, now)
    
    print("Fetching GitHub statistics...")
    stats = fetch_github_stats("ganeshak11")
    print(f"Stats fetched: {stats}")
    
    svg = generate_svg(uptime, stats)
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "terminal.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully.")

if __name__ == "__main__":
    main()
