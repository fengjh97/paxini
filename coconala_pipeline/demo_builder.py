"""
Coconala Pipeline — Demo Builder
Generates a quick demo site + AI images based on a listing.
Uses the same patterns as our hotel/salon/yakiniku websites.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import re
import json
from config import OUTPUT_DIR, TRACKS
from proposal import detect_industry, classify_project

# Industry-specific design presets
DESIGN_PRESETS = {
    "飲食店": {
        "palette": {
            "bg": "#1a1410", "text": "#F5E6D3", "accent": "#D4543A",
            "accent2": "#C49A6C", "surface": "#2a2018",
        },
        "fonts": {
            "display": "Shippori Mincho B1",
            "body": "Noto Sans JP",
            "accent": "Cormorant Garamond",
        },
        "hero_prompt": (
            "A cinematic wide shot of a premium Japanese restaurant interior at night. "
            "Warm amber lighting, dark wood, and glowing lanterns create an intimate atmosphere. "
            "Steam rises from a beautifully plated dish in the foreground. "
            "Shot for a luxury dining magazine. Cinematic 21:9, warm moody tones."
        ),
        "sections": ["hero", "concept", "menu", "gallery", "access", "reserve"],
        "mood": "温かみ・高級感・和の趣",
    },
    "美容・サロン": {
        "palette": {
            "bg": "#FAF8F5", "text": "#3D3333", "accent": "#D4929B",
            "accent2": "#B8C4A3", "surface": "#FFFFFF",
        },
        "fonts": {
            "display": "Zen Maru Gothic",
            "body": "Noto Sans JP",
            "accent": "Quicksand",
        },
        "hero_prompt": (
            "A bright, airy Japanese beauty salon interior with minimalist Scandinavian-Japanese design. "
            "White walls, light oak wood, touches of dusty rose pink. Large round mirrors, "
            "fresh eucalyptus in ceramic vases. Shot for an interior design magazine. Wide-angle, bright."
        ),
        "sections": ["hero", "concept", "menu", "stylist", "gallery", "access"],
        "mood": "明るい・清潔感・やわらかさ",
    },
    "ホテル・旅館": {
        "palette": {
            "bg": "#F5F0E8", "text": "#2B2520", "accent": "#7B4B3A",
            "accent2": "#897D5A", "surface": "#FFFCF5",
        },
        "fonts": {
            "display": "Shippori Mincho",
            "body": "Noto Sans JP",
            "accent": "Cormorant Garamond",
        },
        "hero_prompt": (
            "A breathtaking wide shot of a traditional Japanese ryokan inn at twilight. "
            "Warm cedar wood exterior, soft light through shoji screens. Stone lantern illuminates "
            "the garden path. Misty mountains in background. Cinematic 21:9, golden hour."
        ),
        "sections": ["hero", "concept", "rooms", "onsen", "dining", "access"],
        "mood": "侘び寂び・静謐・日本の美",
    },
    "医療・クリニック": {
        "palette": {
            "bg": "#F8FAFB", "text": "#2C3E50", "accent": "#3498DB",
            "accent2": "#27AE60", "surface": "#FFFFFF",
        },
        "fonts": {
            "display": "Noto Sans JP",
            "body": "Noto Sans JP",
            "accent": "Josefin Sans",
        },
        "hero_prompt": (
            "A modern, clean medical clinic reception area with bright natural lighting. "
            "White walls, light wood accents, green plants. Warm and welcoming healthcare space. "
            "Professional interior photography, bright and clean."
        ),
        "sections": ["hero", "about", "services", "doctor", "access", "reserve"],
        "mood": "清潔感・信頼・安心",
    },
    "フィットネス": {
        "palette": {
            "bg": "#0D0D0D", "text": "#F5F5F5", "accent": "#FF6B35",
            "accent2": "#00D4AA", "surface": "#1A1A1A",
        },
        "fonts": {
            "display": "Anton",
            "body": "Noto Sans JP",
            "accent": "Bebas Neue",
        },
        "hero_prompt": (
            "A dynamic wide shot of a modern fitness gym with dramatic lighting. "
            "Dark interior with orange accent lights, professional equipment, "
            "energetic atmosphere. Shot for a fitness brand campaign. Cinematic, bold contrast."
        ),
        "sections": ["hero", "about", "programs", "trainers", "facility", "trial"],
        "mood": "エネルギッシュ・モダン・力強い",
    },
    "一般企業": {
        "palette": {
            "bg": "#FAFAFA", "text": "#333333", "accent": "#2563EB",
            "accent2": "#10B981", "surface": "#FFFFFF",
        },
        "fonts": {
            "display": "Noto Sans JP",
            "body": "Noto Sans JP",
            "accent": "Inter",
        },
        "hero_prompt": (
            "A modern corporate office with clean, professional interior. "
            "Bright natural light, minimalist design, green plants. "
            "Glass walls and open workspace. Professional architectural photography."
        ),
        "sections": ["hero", "about", "services", "works", "company", "contact"],
        "mood": "プロフェッショナル・信頼・クリーン",
    },
}

SECTION_LABELS = {
    "hero": "ヒーロー（メインビジュアル）",
    "concept": "コンセプト",
    "about": "私たちについて",
    "menu": "メニュー・料金",
    "services": "サービス",
    "gallery": "ギャラリー",
    "stylist": "スタイリスト",
    "rooms": "客室",
    "onsen": "温泉",
    "dining": "お食事",
    "doctor": "ドクター紹介",
    "programs": "プログラム",
    "trainers": "トレーナー",
    "facility": "施設紹介",
    "works": "実績",
    "company": "会社概要",
    "access": "アクセス",
    "reserve": "ご予約",
    "trial": "体験申込",
    "contact": "お問い合わせ",
}


def generate_demo_html(listing, proposal_data=None, hero_image=None):
    """Generate a demo HTML page for a listing."""
    title = listing.get("title", "Demo Site")
    desc = listing.get("description", "") or listing.get("full_description", "")
    industry = proposal_data["industry"] if proposal_data else detect_industry(title, desc)

    preset = DESIGN_PRESETS.get(industry, DESIGN_PRESETS["一般企業"])
    p = preset["palette"]
    f = preset["fonts"]
    sections = preset["sections"]

    # Extract business name from title/description or use placeholder
    biz_name = _extract_business_name(title, desc) or "サンプルビジネス"

    sections_html = "\n".join(
        _generate_section_html(s, biz_name, industry, preset, hero_image=hero_image)
        for s in sections
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{biz_name} — Demo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={f['display'].replace(' ', '+')}&family={f['body'].replace(' ', '+')}:wght@300;400;500;700&family={f['accent'].replace(' ', '+')}&display=swap" rel="stylesheet">
<style>
:root {{
    --color-bg: {p['bg']};
    --color-text: {p['text']};
    --color-accent: {p['accent']};
    --color-accent2: {p['accent2']};
    --color-surface: {p['surface']};
    --font-display: '{f['display']}', serif;
    --font-body: '{f['body']}', sans-serif;
    --font-accent: '{f['accent']}', sans-serif;
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
    font-family: var(--font-body);
    background: var(--color-bg);
    color: var(--color-text);
    line-height: 1.8;
    overflow-x: hidden;
}}

/* === NAV === */
.nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    padding: 1rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
    transition: background 0.3s, box-shadow 0.3s;
}}
.nav.scrolled {{
    background: {p['surface']}ee;
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
}}
.nav-logo {{
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--color-accent);
    text-decoration: none;
}}
.nav-links {{ display: flex; gap: 2rem; list-style: none; }}
.nav-links a {{
    color: var(--color-text);
    text-decoration: none;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    transition: color 0.3s;
}}
.nav-links a:hover {{ color: var(--color-accent); }}

/* === HERO === */
.hero {{
    min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    position: relative;
    background: linear-gradient(135deg, {p['bg']}, {p['surface']});
    overflow: hidden;
}}
.hero-overlay {{
    position: absolute; inset: 0;
    background: linear-gradient(to bottom,
        {p['bg']}00 0%, {p['bg']}88 60%, {p['bg']} 100%);
    z-index: 1;
}}
.hero-content {{
    position: relative; z-index: 2;
    text-align: center;
    padding: 2rem;
}}
.hero-subtitle {{
    font-family: var(--font-accent);
    font-size: clamp(0.75rem, 1.5vw, 1rem);
    letter-spacing: 0.3em;
    color: var(--color-accent);
    margin-bottom: 1rem;
}}
.hero-title {{
    font-family: var(--font-display);
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 1.5rem;
}}
.hero-cta {{
    display: inline-block;
    padding: 1rem 3rem;
    background: var(--color-accent);
    color: {p['surface']};
    text-decoration: none;
    font-size: 0.9rem;
    letter-spacing: 0.1em;
    border-radius: 50px;
    transition: transform 0.3s, box-shadow 0.3s;
}}
.hero-cta:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 30px {p['accent']}44;
}}

/* === SECTIONS === */
.section {{
    padding: clamp(4rem, 8vw, 8rem) clamp(1rem, 5vw, 4rem);
    max-width: 1200px;
    margin: 0 auto;
}}
.section-label {{
    font-family: var(--font-accent);
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--color-accent);
    margin-bottom: 0.5rem;
}}
.section-title {{
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    margin-bottom: 2rem;
    line-height: 1.4;
}}
.section-text {{
    max-width: 640px;
    font-size: 0.95rem;
    line-height: 2;
    opacity: 0.85;
}}

/* === GRID === */
.grid {{ display: grid; gap: 2rem; }}
.grid-2 {{ grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.grid-3 {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}

/* === CARD === */
.card {{
    background: var(--color-surface);
    border-radius: 12px;
    padding: 2rem;
    transition: transform 0.3s, box-shadow 0.3s;
}}
.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.1);
}}
.card-img {{
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, {p['accent']}22, {p['accent2']}22);
    border-radius: 8px;
    margin-bottom: 1rem;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    color: var(--color-accent);
    opacity: 0.6;
}}
.card-title {{
    font-family: var(--font-display);
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}}
.card-text {{ font-size: 0.85rem; opacity: 0.7; }}

/* === CTA SECTION === */
.cta-section {{
    text-align: center;
    padding: 6rem 2rem;
    background: linear-gradient(135deg, {p['accent']}11, {p['accent2']}11);
}}

/* === FOOTER === */
.footer {{
    text-align: center;
    padding: 3rem 2rem;
    font-size: 0.8rem;
    opacity: 0.5;
}}

/* === DEMO BADGE === */
.demo-badge {{
    position: fixed;
    bottom: 2rem; right: 2rem;
    background: var(--color-accent);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
    box-shadow: 0 4px 20px {p['accent']}66;
    z-index: 1000;
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

/* === RESPONSIVE === */
@media (max-width: 768px) {{
    .nav-links {{ display: none; }}
    .section {{ padding: 3rem 1.5rem; }}
}}

/* === REVEAL === */
.reveal {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}}
.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav" id="nav">
    <a href="#" class="nav-logo">{biz_name}</a>
    <ul class="nav-links">
        {' '.join(f'<li><a href="#{s}">{SECTION_LABELS.get(s, s)}</a></li>' for s in sections)}
    </ul>
</nav>

{sections_html}

<!-- FOOTER -->
<footer class="footer">
    <p>&copy; 2025 {biz_name}. All rights reserved.</p>
</footer>

<!-- DEMO BADGE -->
<div class="demo-badge">DEMO</div>

<script>
// Scroll nav
window.addEventListener('scroll', () => {{
    document.getElementById('nav').classList.toggle('scrolled', window.scrollY > 80);
}});
// Reveal
const observer = new IntersectionObserver(entries => {{
    entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
}}, {{ threshold: 0.15 }});
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>
</body>
</html>"""

    return html


def _extract_business_name(title, desc):
    """Try to extract a business name from the listing."""
    text = f"{title} {desc}"

    # Look for quotes
    match = re.search(r'[「『](.+?)[」』]', text)
    if match:
        return match.group(1)

    # Look for patterns like "〇〇の" before ホームページ等
    match = re.search(r'(.{2,15}?)の(?:ホームページ|HP|Webサイト|サイト|LP)', text)
    if match:
        return match.group(1)

    return None


def _generate_section_html(section_id, biz_name, industry, preset, hero_image=None):
    """Generate HTML for a specific section."""
    label = SECTION_LABELS.get(section_id, section_id)

    if section_id == "hero":
        hero_bg = ""
        if hero_image:
            hero_bg = f"""
    <img src="{hero_image}" alt="{biz_name}" style="
        position:absolute; inset:0; width:100%; height:100%;
        object-fit:cover; z-index:0;">"""
        return f"""
<!-- HERO -->
<section class="hero" id="hero">{hero_bg}
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <p class="hero-subtitle">{industry}のための上質な空間</p>
        <h1 class="hero-title">{biz_name}</h1>
        <a href="#contact" class="hero-cta">お問い合わせ</a>
    </div>
</section>"""

    if section_id in ["concept", "about"]:
        return f"""
<!-- {label.upper()} -->
<section class="section" id="{section_id}">
    <div class="reveal">
        <p class="section-label">{section_id.upper()}</p>
        <h2 class="section-title">{biz_name}の想い</h2>
        <p class="section-text">
            お客様一人ひとりに寄り添い、最高の体験をご提供することが私たちの使命です。
            細部までこだわり抜いた空間で、特別なひとときをお過ごしください。
        </p>
    </div>
</section>"""

    if section_id in ["menu", "services", "programs"]:
        items = _get_menu_items(industry)
        cards = "\n".join(f"""
            <div class="card reveal">
                <div class="card-img">AI画像生成で制作</div>
                <h3 class="card-title">{item['name']}</h3>
                <p class="card-text">{item['desc']}</p>
            </div>""" for item in items)
        return f"""
<!-- {label.upper()} -->
<section class="section" id="{section_id}">
    <p class="section-label reveal">{section_id.upper()}</p>
    <h2 class="section-title reveal">{label}</h2>
    <div class="grid grid-3">
        {cards}
    </div>
</section>"""

    if section_id in ["gallery", "works", "facility"]:
        return f"""
<!-- {label.upper()} -->
<section class="section" id="{section_id}">
    <p class="section-label reveal">{section_id.upper()}</p>
    <h2 class="section-title reveal">{label}</h2>
    <div class="grid grid-3">
        <div class="card reveal"><div class="card-img" style="height:250px">AI画像 1</div></div>
        <div class="card reveal"><div class="card-img" style="height:250px">AI画像 2</div></div>
        <div class="card reveal"><div class="card-img" style="height:250px">AI画像 3</div></div>
    </div>
</section>"""

    if section_id in ["stylist", "doctor", "trainers"]:
        return f"""
<!-- {label.upper()} -->
<section class="section" id="{section_id}">
    <p class="section-label reveal">{section_id.upper()}</p>
    <h2 class="section-title reveal">{label}</h2>
    <div class="grid grid-2">
        <div class="card reveal">
            <div class="card-img">スタッフ写真（AI生成）</div>
            <h3 class="card-title">スタッフ名</h3>
            <p class="card-text">経歴やメッセージをここに記載</p>
        </div>
        <div class="card reveal">
            <div class="card-img">スタッフ写真（AI生成）</div>
            <h3 class="card-title">スタッフ名</h3>
            <p class="card-text">経歴やメッセージをここに記載</p>
        </div>
    </div>
</section>"""

    if section_id in ["rooms", "onsen", "dining"]:
        return f"""
<!-- {label.upper()} -->
<section class="section" id="{section_id}">
    <p class="section-label reveal">{section_id.upper()}</p>
    <h2 class="section-title reveal">{label}</h2>
    <div class="grid grid-2">
        <div class="card reveal">
            <div class="card-img" style="height:250px">AI画像（{label}）</div>
            <h3 class="card-title">{label}のご案内</h3>
            <p class="card-text">こだわりの空間で特別な体験をお届けします。</p>
        </div>
        <div class="card reveal">
            <div class="card-img" style="height:250px">AI画像（{label}）</div>
            <h3 class="card-title">{label}の詳細</h3>
            <p class="card-text">季節ごとの魅力をお楽しみください。</p>
        </div>
    </div>
</section>"""

    if section_id == "access":
        return f"""
<!-- ACCESS -->
<section class="section" id="access">
    <p class="section-label reveal">ACCESS</p>
    <h2 class="section-title reveal">アクセス</h2>
    <div class="reveal">
        <p class="section-text">〒000-0000 東京都○○区○○ 1-2-3</p>
        <p class="section-text">TEL: 03-0000-0000</p>
        <p class="section-text" style="margin-top:1rem; opacity:0.6;">
            ※ Google Maps埋め込みスペース
        </p>
    </div>
</section>"""

    if section_id in ["reserve", "trial", "contact"]:
        return f"""
<!-- CTA -->
<section class="cta-section" id="{section_id}">
    <div class="reveal">
        <p class="section-label">{section_id.upper()}</p>
        <h2 class="section-title">{label}</h2>
        <p class="section-text" style="margin: 0 auto 2rem;">
            お気軽にお問い合わせください。
        </p>
        <a href="#" class="hero-cta">ご予約・お問い合わせ</a>
    </div>
</section>"""

    return ""


def _get_menu_items(industry):
    """Get placeholder menu items for industry."""
    menus = {
        "飲食店": [
            {"name": "おすすめコース", "desc": "厳選された旬の食材を使用"},
            {"name": "ランチメニュー", "desc": "お得なランチセット"},
            {"name": "ドリンク", "desc": "こだわりのワイン・日本酒"},
        ],
        "美容・サロン": [
            {"name": "カット", "desc": "あなたに似合うスタイルをご提案"},
            {"name": "カラー", "desc": "トレンドカラーで印象チェンジ"},
            {"name": "トリートメント", "desc": "髪本来の輝きを取り戻す"},
        ],
        "ホテル・旅館": [
            {"name": "和室", "desc": "伝統的な畳の寛ぎ空間"},
            {"name": "露天風呂付客室", "desc": "プライベートな湯浴み"},
            {"name": "お食事処", "desc": "地元食材の懐石料理"},
        ],
        "医療・クリニック": [
            {"name": "一般診療", "desc": "丁寧な診察と治療"},
            {"name": "専門治療", "desc": "最新の医療技術"},
            {"name": "予防・検診", "desc": "定期的な健康チェック"},
        ],
        "フィットネス": [
            {"name": "パーソナルトレーニング", "desc": "マンツーマン指導"},
            {"name": "グループレッスン", "desc": "楽しく続けられる"},
            {"name": "施設利用", "desc": "充実の設備環境"},
        ],
    }
    return menus.get(industry, [
        {"name": "サービス A", "desc": "お客様のニーズに合わせたサービス"},
        {"name": "サービス B", "desc": "高品質なサポート体制"},
        {"name": "サービス C", "desc": "信頼と実績のソリューション"},
    ])


def generate_hero_image(demo_dir, prompt, api_key=None):
    """Generate hero image using Gemini API (nano-banana-pro pattern)."""
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

    import base64
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("    (google-genai not installed, skipping image generation)")
        return None

    client = genai.Client(api_key=api_key)
    img_dir = os.path.join(demo_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    filepath = os.path.join(img_dir, "hero.png")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )
        parts = response.candidates[0].content.parts
        for part in parts:
            if part.inline_data:
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)
                with open(filepath, "wb") as f:
                    f.write(image_data)
                return filepath
    except Exception as e:
        print(f"    Image gen error: {type(e).__name__}: {e}")

    return None


def _build_demo_html(listing, proposal_data=None, generate_images=True):
    """Build HTML demo for web track."""
    listing_id = listing.get("id", "unknown")
    demo_dir = os.path.join(OUTPUT_DIR, f"demo_{listing_id}")
    os.makedirs(demo_dir, exist_ok=True)

    industry = proposal_data["industry"] if proposal_data else detect_industry(
        listing.get("title", ""), listing.get("description", "")
    )
    preset = DESIGN_PRESETS.get(industry, DESIGN_PRESETS["一般企業"])

    # Generate hero image with AI
    hero_image_path = None
    if generate_images:
        print("    → AI画像生成中 (hero)...", end=" ", flush=True)
        hero_image_path = generate_hero_image(demo_dir, preset["hero_prompt"])
        if hero_image_path:
            print(f"OK ({os.path.getsize(hero_image_path)//1024} KB)")
        else:
            print("skipped")

    html = generate_demo_html(listing, proposal_data, hero_image="images/hero.png" if hero_image_path else None)
    filepath = os.path.join(demo_dir, "index.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    # Save image prompts for reference
    prompts_file = os.path.join(demo_dir, "image_prompts.json")
    prompts = {
        "hero": preset["hero_prompt"],
        "hero_generated": hero_image_path is not None,
        "note": "Run with nano-banana-pro to generate additional images",
    }
    with open(prompts_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

    return {
        "demo_dir": demo_dir,
        "html_path": filepath,
        "prompts_path": prompts_file,
        "hero_image": hero_image_path,
        "industry": industry,
        "sections": preset["sections"],
    }


def build_demo(listing, proposal_data=None, generate_images=True):
    """Build demo based on track_id. Dispatches to track-specific builder."""
    track_id = listing.get("track_id", "web")

    if track_id == "graphic":
        return _build_demo_images(listing, proposal_data, generate_images)
    elif track_id in ("writing", "translation"):
        return _build_demo_article(listing, proposal_data, track_id)
    elif track_id == "it_dev":
        return _build_demo_code(listing, proposal_data)
    elif track_id == "documents":
        return _build_demo_document(listing, proposal_data)
    else:
        return _build_demo_html(listing, proposal_data, generate_images)


def _build_demo_images(listing, proposal_data=None, generate_images=True):
    """Graphic track: generate 2-3 sample images with AI."""
    listing_id = listing.get("id", "unknown")
    demo_dir = os.path.join(OUTPUT_DIR, f"demo_{listing_id}")
    img_dir = os.path.join(demo_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    title = listing.get("title", "")
    desc = listing.get("description", "")

    # Build prompt from listing content
    prompt = (
        f"Create a professional graphic design sample for: {title}. "
        f"Context: {desc[:200]}. "
        "High quality, clean design, suitable for commercial use. "
        "Professional product photography style."
    )

    generated = []
    if generate_images:
        print("    → AI画像生成中 (graphic demo)...", end=" ", flush=True)
        for i in range(2):
            img_path = os.path.join(img_dir, f"sample_{i+1}.png")
            result = generate_hero_image(demo_dir, prompt)
            if result:
                os.rename(result, img_path)
                generated.append(img_path)
        print(f"{len(generated)}枚生成" if generated else "skipped")

    # Save prompts for reference
    prompts_file = os.path.join(demo_dir, "image_prompts.json")
    with open(prompts_file, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt, "count": len(generated)}, f, ensure_ascii=False, indent=2)

    return {
        "demo_dir": demo_dir,
        "html_path": prompts_file,
        "hero_image": generated[0] if generated else None,
        "industry": proposal_data.get("industry", "") if proposal_data else "",
        "sections": [],
    }


def _build_demo_article(listing, proposal_data=None, track_id="writing"):
    """Writing/Translation track: generate sample markdown article."""
    listing_id = listing.get("id", "unknown")
    demo_dir = os.path.join(OUTPUT_DIR, f"demo_{listing_id}")
    os.makedirs(demo_dir, exist_ok=True)

    title = listing.get("title", "")
    desc = listing.get("description", "")

    if track_id == "translation":
        content = f"""# 翻訳サンプル — {title}

## 原文（サンプル）

> この部分に原文テキストが入ります。実際のご依頼時に原稿をいただき次第、
> 同様の品質でサンプル翻訳をお見せいたします。

## 翻訳結果（サンプル）

> This is where the translated text will appear. Upon receiving your actual
> manuscript, we will provide a sample translation of similar quality.

---

**翻訳方針:**
- 原文の意図を正確に伝える自然な翻訳
- 専門用語の一貫性チェック済み
- ネイティブ品質の表現に仕上げ

*サンプルのため、実際のご依頼内容とは異なります。*
"""
    else:
        content = f"""# 記事サンプル — {title}

## はじめに

本記事では、{desc[:100] or title}について解説いたします。
読者の皆様に分かりやすく、実用的な情報をお届けすることを心がけています。

## ポイント1: 背景と概要

ここに本文が入ります。実際のご依頼をいただき次第、
ご要望のテーマに沿った高品質な記事を執筆いたします。

## ポイント2: 具体的な方法

- 項目1: 具体的なアクションステップ
- 項目2: 実践的なアドバイス
- 項目3: 注意点とコツ

## まとめ

以上が{title}についてのサンプル記事です。
実際の記事では、リサーチに基づいた正確な情報と、
読みやすい構成でお届けいたします。

---

*このサンプルは制作クオリティの参考としてご覧ください。*
"""

    filepath = os.path.join(demo_dir, "sample_article.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "demo_dir": demo_dir,
        "html_path": filepath,
        "hero_image": None,
        "industry": proposal_data.get("industry", "") if proposal_data else "",
        "sections": [],
    }


def _build_demo_code(listing, proposal_data=None):
    """IT/AI dev track: generate README + sample code."""
    listing_id = listing.get("id", "unknown")
    demo_dir = os.path.join(OUTPUT_DIR, f"demo_{listing_id}")
    os.makedirs(demo_dir, exist_ok=True)

    title = listing.get("title", "")
    desc = listing.get("description", "")

    readme = f"""# {title}

## 概要

{desc[:300] or 'ご依頼内容に基づいたツール/システムです。'}

## 技術スタック

- Python 3.x
- 必要に応じたライブラリ（requirements.txt に記載）

## セットアップ

```bash
pip install -r requirements.txt
python main.py
```

## 機能

- [ ] 機能1: メイン処理
- [ ] 機能2: データ入出力
- [ ] 機能3: エラーハンドリング

## ファイル構成

```
project/
├── main.py          # メインスクリプト
├── config.py        # 設定ファイル
├── requirements.txt # 依存パッケージ
└── README.md        # このファイル
```

## 納品物

- ソースコード一式（GitHub管理）
- README・使用手順書
- テストコード

---

*このREADMEはサンプルです。実際のご依頼内容に合わせて作成いたします。*
"""

    filepath = os.path.join(demo_dir, "README.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(readme)

    return {
        "demo_dir": demo_dir,
        "html_path": filepath,
        "hero_image": None,
        "industry": proposal_data.get("industry", "") if proposal_data else "",
        "sections": [],
    }


def _build_demo_document(listing, proposal_data=None):
    """Documents track: generate outline/structure sample."""
    listing_id = listing.get("id", "unknown")
    demo_dir = os.path.join(OUTPUT_DIR, f"demo_{listing_id}")
    os.makedirs(demo_dir, exist_ok=True)

    title = listing.get("title", "")
    desc = listing.get("description", "")
    project_type = proposal_data.get("project_type", "simple_doc") if proposal_data else "simple_doc"

    if project_type == "business_plan":
        content = f"""# 事業計画書サンプル — {title}

## 目次（構成案）

1. **エグゼクティブサマリー** (1ページ)
   - 事業概要・ビジョン
   - 市場機会の概要
   - 収益見込み

2. **事業概要** (2ページ)
   - ミッション・ビジョン
   - 事業内容の詳細
   - 競合優位性

3. **市場分析** (3ページ)
   - ターゲット市場の定義
   - 市場規模・成長率
   - 競合分析

4. **マーケティング戦略** (2ページ)
   - ターゲット顧客
   - 集客チャネル
   - 価格戦略

5. **収支計画** (2ページ)
   - 売上予測（3年間）
   - 経費内訳
   - 損益分岐点分析

6. **リスク分析** (1ページ)
   - 想定リスクと対策

---

*この構成案をベースに、ご要望に合わせてカスタマイズいたします。*
"""
    else:
        content = f"""# 資料サンプル — {title}

## 構成案

### スライド1: 表紙
- タイトル・日付・作成者

### スライド2-3: 背景・課題
- 現状の課題整理
- データ・根拠の提示

### スライド4-6: 提案内容
- 解決策の提示
- 具体的なアクションプラン
- スケジュール

### スライド7-8: 効果・期待成果
- 定量的な効果予測
- KPI設定

### スライド9: まとめ・次のステップ

---

**デザインイメージ:**
- クリーンで見やすいレイアウト
- AI生成の図解・インフォグラフィック
- ブランドカラーに合わせた配色

*この構成をベースに、ご要望に合わせてカスタマイズいたします。*
"""

    filepath = os.path.join(demo_dir, "sample_outline.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "demo_dir": demo_dir,
        "html_path": filepath,
        "hero_image": None,
        "industry": proposal_data.get("industry", "") if proposal_data else "",
        "sections": [],
    }


if __name__ == "__main__":
    # Test with sample listing
    sample = {
        "id": "test001",
        "url": "https://coconala.com/requests/12345",
        "title": "焼肉店のホームページを作成してほしい",
        "description": "焼肉店を経営しています。おしゃれなデザインのホームページが欲しいです。",
        "track_id": "web",
    }

    result = build_demo(sample, {"industry": "飲食店"})
    print(f"Demo generated: {result['html_path']}")
    print(f"Sections: {result['sections']}")
