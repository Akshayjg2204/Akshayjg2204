import urllib.request
import re
import os
import datetime

def fetch_contributions(username="Akshayjg2204"):
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        return []

    td_pattern = re.compile(r'<td\s+[^>]*data-date="([^"]+)"[^>]*id="([^"]+)"[^>]*data-level="([^"]+)"', re.DOTALL)
    matches = td_pattern.findall(html)

    tooltip_pattern = re.compile(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', re.DOTALL)
    tips = dict(tooltip_pattern.findall(html))

    days = []
    for date, day_id, level in matches:
        lvl = int(level)
        tip_text = tips.get(day_id, "")
        cnt_match = re.search(r'(\d+)\s+contribution', tip_text)
        count = int(cnt_match.group(1)) if cnt_match else (lvl if lvl > 0 else 0)
        days.append({"date": date, "level": lvl, "count": count})

    return days

def compute_stats(days):
    total = sum(d["count"] for d in days)
    
    # Calculate current streak and longest streak
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for d in days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Current streak from the end
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        elif current_streak > 0:
            break
            
    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_days": sum(1 for d in days if d["count"] > 0)
    }

def render_hud_svg(filepath):
    svg = f"""<svg width="860" height="195" viewBox="0 0 860 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cyber-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0EA5E9" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#EC4899" />
    </linearGradient>
    <linearGradient id="panel-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B1120" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#070A13" stop-opacity="0.98" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <style>
    .mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, monospace; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .glow-cyan {{ filter: drop-shadow(0 0 4px rgba(14, 165, 233, 0.4)); }}
    .glow-purple {{ filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.4)); }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.96); }}
    }}
    .pulse-dot {{
      animation: pulse 2.4s ease-in-out infinite;
      transform-origin: 28px 26px;
    }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="856" height="191" rx="10" fill="url(#panel-bg)" stroke="url(#cyber-border)" stroke-width="1.2" />

  <!-- Corner Brackets -->
  <path d="M 8 24 L 8 10 Q 8 8 10 8 L 24 8" stroke="#38BDF8" stroke-width="2" fill="none" />
  <path d="M 852 24 L 852 10 Q 852 8 850 8 L 836 8" stroke="#A855F7" stroke-width="2" fill="none" />
  <path d="M 8 171 L 8 185 Q 8 187 10 187 L 24 187" stroke="#38BDF8" stroke-width="2" fill="none" />
  <path d="M 852 171 L 852 185 Q 852 187 850 187 L 836 187" stroke="#EC4899" stroke-width="2" fill="none" />

  <!-- Top Status Bar -->
  <circle cx="28" cy="26" r="4.5" fill="#10B981" class="pulse-dot" />
  <text x="42" y="30" class="mono" font-size="11.5" font-weight="700" fill="#F8FAFC" letter-spacing="1.5">STREAMLINE TELEMETRY FLIGHT-DECK</text>
  <text x="360" y="30" class="mono" font-size="10.5" fill="#64748B">//</text>
  <text x="382" y="30" class="mono" font-size="10.5" font-weight="600" fill="#38BDF8">V-SYNC: 60 FPS [WEBGL ENGINE]</text>

  <!-- Top Right Live Chip -->
  <rect x="702" y="18" width="138" height="20" rx="10" fill="#0369A1" fill-opacity="0.25" stroke="#0284C7" stroke-width="0.8" />
  <text x="771" y="31.5" class="mono" font-size="9.5" font-weight="700" fill="#38BDF8" text-anchor="middle" letter-spacing="1">STATUS: SHIPPING</text>

  <!-- Divider Line -->
  <line x1="24" y1="46" x2="836" y2="46" stroke="#1E293B" stroke-width="1" />

  <!-- Left Column: Fleet & Engines -->
  <g transform="translate(26, 62)">
    <rect x="0" y="0" width="390" height="116" rx="6" fill="#0F172A" fill-opacity="0.4" stroke="#1E293B" stroke-width="0.8" />
    <text x="14" y="20" class="mono" font-size="10.5" font-weight="700" fill="#A855F7" letter-spacing="1">01 // PRODUCTION FLEET</text>
    
    <text x="14" y="44" class="sans" font-size="12" font-weight="600" fill="#E2E8F0">📱 TruSkies (AirSafeIndia)</text>
    <text x="175" y="44" class="mono" font-size="10.5" fill="#10B981">[Google Play Live App]</text>
    <text x="14" y="60" class="sans" font-size="11" fill="#94A3B8">React Native • Expo Router • Supabase PostgreSQL</text>

    <text x="14" y="84" class="sans" font-size="12" font-weight="600" fill="#E2E8F0">🏎️ Chill Drift</text>
    <text x="105" y="84" class="mono" font-size="10.5" fill="#38BDF8">[60 FPS Three.js Engine]</text>
    <text x="14" y="100" class="sans" font-size="11" fill="#94A3B8">WebGL • Simplex Procedural Terrain • Web Audio</text>
  </g>

  <!-- Right Column: Mission Control -->
  <g transform="translate(444, 62)">
    <rect x="0" y="0" width="390" height="116" rx="6" fill="#0F172A" fill-opacity="0.4" stroke="#1E293B" stroke-width="0.8" />
    <text x="14" y="20" class="mono" font-size="10.5" font-weight="700" fill="#0EA5E9" letter-spacing="1">02 // ARCHITECTURE MATRIX</text>
    
    <text x="14" y="44" class="sans" font-size="12" font-weight="600" fill="#E2E8F0">⚡ Full-Stack &amp; Web Systems</text>
    <text x="14" y="60" class="sans" font-size="11" fill="#94A3B8">Next.js 16 • React 19 • Tailwind v4 • TypeScript</text>

    <text x="14" y="84" class="sans" font-size="12" font-weight="600" fill="#E2E8F0">🚀 Streamline.dev</text>
    <text x="135" y="84" class="mono" font-size="10.5" fill="#EC4899">[Agency Studio]</text>
    <text x="14" y="100" class="sans" font-size="11" fill="#94A3B8">Panvel, Maharashtra, India • High-Performance Web</text>
  </g>
</svg>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Rendered: {filepath}")

def render_spectrum_svg(days, stats, filepath):
    total = stats["total"]
    streak = stats["current_streak"]
    
    palette = [
        "#111827", # Level 0: dark space
        "#0284C7", # Level 1: electric cyan deep
        "#38BDF8", # Level 2: neon sky cyan
        "#8B5CF6", # Level 3: radiant violet
        "#EC4899"  # Level 4: neon pink peak
    ]
    
    # We display up to 53 weeks (371 days)
    # Group days into weeks of 7 days
    weeks = []
    current_week = []
    
    # Take the last 371 days (or all)
    display_days = days[-371:] if len(days) >= 371 else days
    
    for i, d in enumerate(display_days):
        current_week.append(d)
        if len(current_week) == 7 or i == len(display_days) - 1:
            weeks.append(current_week)
            current_week = []
            
    num_weeks = len(weeks)
    
    # Months labels logic
    months_labels = []
    last_month = ""
    for w_idx, week in enumerate(weeks):
        first_day_of_week = week[0]["date"]
        month_abbr = datetime.datetime.strptime(first_day_of_week, "%Y-%m-%d").strftime("%b")
        if month_abbr != last_month and w_idx < num_weeks - 2:
            months_labels.append((w_idx * 14.8 + 26, month_abbr))
            last_month = month_abbr

    rects_svg = []
    for w_idx, week in enumerate(weeks):
        x = 24 + w_idx * 14.8
        for d_idx, day in enumerate(week):
            y = 52 + d_idx * 14.8
            lvl = min(day["level"], 4)
            color = palette[lvl]
            rects_svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="11" height="11" rx="2.5" fill="{color}" />')

    months_svg = "".join([f'<text x="{x:.1f}" y="44" class="mono" font-size="9" fill="#64748B">{m}</text>' for x, m in months_labels])

    svg = f"""<svg width="860" height="188" viewBox="0 0 860 188" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="spectrum-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#EC4899" />
    </linearGradient>
    <linearGradient id="matrix-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B1120" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#060913" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <style>
    .mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, monospace; }}
    @keyframes sweep {{
      0% {{ opacity: 0.1; transform: translateY(4px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .matrix-grid {{ animation: sweep 0.8s ease-out forwards; }}
  </style>

  <!-- Panel Background -->
  <rect x="2" y="2" width="856" height="184" rx="10" fill="url(#matrix-bg)" stroke="#1E293B" stroke-width="1.2" />

  <!-- Top Header Bar -->
  <text x="24" y="26" class="mono" font-size="11.5" font-weight="700" fill="#F8FAFC" letter-spacing="1">⚡ CONTRIBUTION SPECTRUM MATRIX</text>
  <text x="290" y="26" class="mono" font-size="10" fill="#64748B">// 53-WEEK SYNTHWAVE ACTIVITY</text>

  <!-- Metrics on Right -->
  <g transform="translate(560, 14)">
    <rect x="0" y="0" width="276" height="22" rx="11" fill="#0F172A" stroke="#334155" stroke-width="0.8" />
    <text x="14" y="15" class="mono" font-size="10" font-weight="600" fill="#94A3B8">ANNUAL COMMITS:</text>
    <text x="115" y="15" class="mono" font-size="10.5" font-weight="700" fill="#38BDF8">{total}</text>
    <text x="145" y="15" class="mono" font-size="10" fill="#475569">|</text>
    <text x="156" y="15" class="mono" font-size="10" font-weight="600" fill="#94A3B8">STREAK:</text>
    <text x="208" y="15" class="mono" font-size="10.5" font-weight="700" fill="#EC4899">{streak} DAYS</text>
  </g>

  <!-- Months Header -->
  {months_svg}

  <!-- Days Grid -->
  <g class="matrix-grid">
    {''.join(rects_svg)}
  </g>

  <!-- Footer Legend -->
  <g transform="translate(640, 166)">
    <text x="0" y="9" class="mono" font-size="9" fill="#64748B">Less</text>
    <rect x="30" y="0" width="10" height="10" rx="2" fill="{palette[0]}" />
    <rect x="44" y="0" width="10" height="10" rx="2" fill="{palette[1]}" />
    <rect x="58" y="0" width="10" height="10" rx="2" fill="{palette[2]}" />
    <rect x="72" y="0" width="10" height="10" rx="2" fill="{palette[3]}" />
    <rect x="86" y="0" width="10" height="10" rx="2" fill="{palette[4]}" />
    <text x="104" y="9" class="mono" font-size="9" fill="#EC4899">Peak Spectrum</text>
  </g>
  <text x="24" y="175" class="mono" font-size="9.5" fill="#475569">Auto-synchronized daily via GitHub Actions • 100% Self-Hosted SVG</text>
</svg>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Rendered: {filepath}")

def main():
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    hud_path = os.path.join(assets_dir, "telemetry-hud.svg")
    spectrum_path = os.path.join(assets_dir, "activity-spectrum.svg")
    
    print("Scraping public GitHub contributions...")
    days = fetch_contributions("Akshayjg2204")
    stats = compute_stats(days)
    print(f"Stats computed: {stats}")
    
    render_hud_svg(hud_path)
    render_spectrum_svg(days, stats, spectrum_path)
    print("Telemetry assets successfully built!")

if __name__ == "__main__":
    main()
