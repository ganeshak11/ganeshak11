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
    years, months, days, hours, minutes, seconds = uptime
    
    # Format metrics with thousands separator
    commits_str = f"{stats['commits']:,}"
    stars_str = f"{stats['stars']:,}"
    repos_str = f"{stats['repos']:,}"
    followers_str = f"{stats['followers']:,}"

    # Build Uptime string
    uptime_str = f"{years}y {months}m {days}d {hours}h {minutes}m {seconds}s"

    # Static definitions for information fields (matching local Ubuntu system)
    specs = [
        ("OS", "Ubuntu 24.04.4 LTS"),
        ("Host", "ganeshak11-Vostro-15-3515"),
        ("Uptime", uptime_str),
        ("Kernel", "6.8.0-134-generic"),
        ("Shell", "/bin/bash"),
        ("IDE", "VS Code, Vim"),
        ("Languages", "TypeScript, Python, Shell, C"),
    ]

    # Generate specs rows with alignment using absolute coordinates (flat sibling tspans)
    spec_rows = []
    for key, val in specs:
        spec_rows.append(
            f'<tspan x="480" dy="18" class="key">{key}</tspan>'
            f'<tspan x="570" class="separator">:</tspan>'
            f'<tspan x="590" class="val">{val}</tspan>'
        )

    # Wrap and render long building text
    building_lines = wrap_text("Fortis Ecosystem (Fortis-CI, Observe)", 42)
    spec_rows.append(
        f'<tspan x="480" dy="24" class="key">Building</tspan>'
        f'<tspan x="570" class="separator">:</tspan>'
        f'<tspan x="590" class="val">{building_lines[0]}</tspan>'
    )
    for line in building_lines[1:]:
        spec_rows.append(f'<tspan x="590" dy="18" class="val">{line}</tspan>')

    # Wrap and render long telemetry text
    telemetry_lines = wrap_text("S1 (8-Puzzle: 3s) | S2 (Rubik: 48s) | S3 (Sudoku: 52s)", 42)
    spec_rows.append(
        f'<tspan x="480" dy="18" class="key">Telemetry</tspan>'
        f'<tspan x="570" class="separator">:</tspan>'
        f'<tspan x="590" class="val">{telemetry_lines[0]}</tspan>'
    )
    for line in telemetry_lines[1:]:
        spec_rows.append(f'<tspan x="590" dy="18" class="val">{line}</tspan>')

    specs_block = "\n".join(spec_rows)

    svg_content = rf"""<svg width="100%" height="100%" viewBox="0 0 960 540" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Subtle window drop shadow filter -->
  <defs>
    <filter id="shadow" x="0" y="0" width="960" height="540" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000000" flood-opacity="0.5" />
    </filter>
  </defs>

  <style>
    .terminal {{
      font-family: "Fira Code", "JetBrains Mono", "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 12px;
      fill: #C9D1D9;
    }}
    .title-bar {{
      fill: #161B22;
    }}
    .body {{
      fill: #0D1117;
    }}
    .border {{
      stroke: #30363D;
      stroke-width: 1.5;
    }}
    .red-btn {{ fill: #FF5F56; }}
    .yellow-btn {{ fill: #FFBD2E; }}
    .green-btn {{ fill: #27C93F; }}
    
    .title-text {{
      fill: #8B949E;
      font-size: 12px;
      text-anchor: middle;
      font-weight: 500;
    }}
    
    .ascii-text {{
      fill: #E3B341;
      font-family: "JetBrains Mono","Cascadia Code","Fira Code","Consolas", monospace;
      font-weight: bold;
      font-size: 11.5px;
      white-space: pre;
      letter-spacing: 0;
    }}
    
    .status-panel-bg {{
      fill: #161B22;
      stroke: #30363D;
      stroke-width: 1.5;
    }}
    
    .prompt-user {{
      fill: #E3B341;
      font-weight: bold;
    }}
    .prompt-at {{
      fill: #8B949E;
    }}
    .prompt-host {{
      fill: #58A6FF;
      font-weight: bold;
    }}
    
    .key {{
      fill: #58A6FF;
      font-weight: bold;
    }}
    .val {{
      fill: #C9D1D9;
    }}
    .separator {{
      fill: #30363D;
      stroke-width: 1.5;
    }}
    .heading {{
      font-size: 13px;
      font-weight: bold;
    }}
    .green-text {{
      fill: #3FB950;
      font-weight: bold;
    }}
    .yellow-text {{
      fill: #E3B341;
      font-weight: bold;
    }}
    .blue-text {{
      fill: #58A6FF;
      font-weight: bold;
    }}
    .dim-text {{
      fill: #8B949E;
    }}
    
    .cursor {{
      fill: #58A6FF;
      animation: blink 1s step-end infinite;
    }}
    @keyframes blink {{
      from, to {{ fill: transparent }}
      50% {{ fill: #58A6FF }}
    }}
  </style>

  <g filter="url(#shadow)">
    <!-- Terminal Window Background -->
    <rect x="8" y="8" width="944" height="524" rx="8" class="body border" />
    
    <!-- Title Bar -->
    <path d="M 8 16 A 8 8 0 0 1 16 8 L 944 8 A 8 8 0 0 1 952 16 L 952 40 L 8 40 Z" fill="#161B22" />
    <line x1="8" y1="40" x2="952" y2="40" stroke="#30363D" stroke-width="1.5" />
    
    <!-- Window Controls -->
    <circle cx="28" cy="24" r="6" class="red-btn" />
    <circle cx="48" cy="24" r="6" class="yellow-btn" />
    <circle cx="68" cy="24" r="6" class="green-btn" />
    
    <!-- Title Bar Text -->
    <text x="480" y="28" class="title-text">ganesh@ubuntu: ~</text>
  </g>

  <!-- Left Column: Logo and Status Panels -->
  <g class="terminal">
    <!-- ASCII Art Logo (Moved up to y=75) -->
    <text x="48" y="75" class="ascii-text" xml:space="preserve">
      <tspan x="48" dy="15">  ██████╗  █████╗ ███╗   ██╗███████╗███████╗██╗  ██╗</tspan>
      <tspan x="48" dy="15"> ██╔════╝ ██╔══██╗████╗  ██║██╔════╝██╔════╝██║  ██║</tspan>
      <tspan x="48" dy="15"> ██║  ███╗███████║██╔██╗ ██║█████╗  ███████╗███████║</tspan>
      <tspan x="48" dy="15"> ██║   ██║██╔══██║██║╚██╗██║██╔══╝  ╚════██║██╔══██║</tspan>
      <tspan x="48" dy="15"> ╚██████╔╝██║  ██║██║ ╚████║███████╗███████║██║  ██║</tspan>
      <tspan x="48" dy="15">  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝</tspan>
    </text>

    <!-- Status Panel Box (Moved up to y=218 and height adjusted) -->
    <rect x="78" y="218" width="300" height="136" rx="6" class="status-panel-bg" />
    
    <!-- Status Panel Text inside the Box -->
    <text x="98" y="248" class="ascii-text">
      <tspan x="98" dy="0"><tspan class="key">Status    </tspan><tspan class="dim-text">:</tspan> <tspan class="green-text">Active</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">Memory    </tspan><tspan class="dim-text">:</tspan> <tspan class="val">3.9 / 5.7 GiB</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">Disk      </tspan><tspan class="dim-text">:</tspan> <tspan class="val">176 / 468 GiB</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">Docker    </tspan><tspan class="dim-text">:</tspan> <tspan class="val">0 Run | 13 Stop</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">CPU Load  </tspan><tspan class="dim-text">:</tspan> <tspan class="val">2.88</tspan></tspan>
    </text>

    <!-- DevOps Telemetry Box (Fills empty space in lower-left) -->
    <rect x="78" y="368" width="300" height="92" rx="6" class="status-panel-bg" />
    <text x="98" y="398" class="ascii-text">
      <tspan x="98" dy="0"><tspan class="key">Pipeline   </tspan><tspan class="dim-text">:</tspan> <tspan class="green-text">Healthy</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">Containers </tspan><tspan class="dim-text">:</tspan> <tspan class="green-text">Running</tspan></tspan>
      <tspan x="98" dy="20"><tspan class="key">Infra State</tspan><tspan class="dim-text">:</tspan> <tspan class="blue-text">Synced</tspan></tspan>
    </text>
  </g>

  <!-- Right Column: Specs and Stats -->
  <g class="terminal">
    <!-- User/Host Prompt (Lowered to y=110) -->
    <text x="480" y="110">
      <tspan class="prompt-user">ganesh</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">ubuntu</tspan>
    </text>
    
    <!-- Solid Grid Separator Line (Lowered to y=126) -->
    <line x1="480" y1="126" x2="912" y2="126" stroke="#30363D" stroke-width="1.5" />

    <!-- Specs Section (Lowered start to y=136) -->
    <text x="480" y="136">
      {specs_block}
    </text>

    <!-- Solid Grid Separator Line (Lowered to y=346) -->
    <line x1="480" y1="346" x2="912" y2="346" stroke="#30363D" stroke-width="1.5" />

    <!-- Dynamic Metrics Section Header (Lowered to y=374) -->
    <text x="480" y="374" class="heading green-text">GitHub Dynamic Metrics</text>

    <!-- Metrics Table Rows (Tab-stop layout with dy increased by 2px) -->
    <text x="480" y="386">
      <tspan x="480" dy="24"><tspan class="key">Commits</tspan><tspan x="620" class="val">{commits_str}</tspan></tspan>
      <tspan x="480" dy="22"><tspan class="key">Stars</tspan><tspan x="620" class="val">{stars_str}</tspan></tspan>
      <tspan x="480" dy="22"><tspan class="key">Repositories</tspan><tspan x="620" class="val">{repos_str}</tspan></tspan>
      <tspan x="480" dy="22"><tspan class="key">Followers</tspan><tspan x="620" class="val">{followers_str}</tspan></tspan>
    </text>

    <!-- Pinned Terminal Prompt (Raised to y=500 for better margin) -->
    <text x="480" y="500">
      <tspan class="prompt-user">ganesh</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">ubuntu</tspan><tspan class="val">:~$ </tspan><tspan class="cursor">█</tspan>
    </text>
  </g>
</svg>
"""
    return svg_content

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    uptime = get_uptime(BIRTHDATE, now)
    
    print("Fetching GitHub statistics...")
    stats = fetch_github_stats("ganeshak11")
    print(f"Stats fetched: {stats}")
    
    svg = generate_svg(uptime, stats)
    
    output_path = "terminal.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully.")

if __name__ == "__main__":
    main()
