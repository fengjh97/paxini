"""
Coconala Pipeline — Configuration
"""

# === Scraping Settings ===
BASE_URL = "https://coconala.com"
REQUESTS_URL = f"{BASE_URL}/requests/categories"

# Target categories for our skills (Web制作, デザイン, etc.)
CATEGORIES = {
    22:  "Web制作・HP作成・EC構築",
    500: "ホームページ作成・サイト制作",
    501: "WEBサイトデザイン・UI設計",
    503: "LP作成・ランディングページデザイン",
    18:  "デザイン制作",
    507: "ECサイト制作・ネットショップ構築",
    230: "作業自動化・効率化",
}

# Keywords to boost relevance score
POSITIVE_KEYWORDS = [
    "ホームページ", "HP", "ウェブサイト", "Webサイト", "web制作",
    "ランディングページ", "LP", "コーポレートサイト",
    "デザイン", "おしゃれ", "かっこいい", "モダン",
    "レスポンシブ", "スマホ対応",
    "画像生成", "AI", "バナー", "ロゴ",
    "飲食店", "美容室", "サロン", "ホテル", "旅館", "民宿",
    "クリニック", "歯科", "整骨院", "ジム",
    "新規", "リニューアル", "作成", "制作",
]

# Keywords that indicate jobs outside our skillset
NEGATIVE_KEYWORDS = [
    "WordPress", "ワードプレス",  # We do static sites
    "Shopify",
    "システム開発", "アプリ開発", "API連携",
    "SEO対策のみ", "記事作成のみ", "ライティング",
]

# Minimum budget filter (yen)
MIN_BUDGET = 5000

# Request interval (seconds) — be polite
REQUEST_INTERVAL = 5

# User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Database
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "coconala.db")

# Output
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# === Proposal Settings ===
# Our strengths to highlight
OUR_STRENGTHS = {
    "skills": [
        "Claude Code（AI駆動のフルスタック開発）",
        "Nano Banana Pro（AI画像生成 — Gemini 3 Pro）",
        "レスポンシブ HTML/CSS/JS（フレームワーク不要の軽量構成）",
        "GSAP/ScrollTrigger（リッチアニメーション）",
        "デザインリサーチ → カラーパレット → 実装の一貫ワークフロー",
    ],
    "portfolio_urls": [
        # GitHub Pages or similar — update when deployed
        "https://github.com/fengjh97/paxini",
    ],
    "delivery_speed": "最短3日〜",
    "revision_rounds": "2回まで無料修正",
}

# Pricing tiers (yen, pre-commission)
PRICING = {
    "simple_lp": {"min": 15000, "max": 30000, "label": "シンプルLP（1ページ）"},
    "corporate_site": {"min": 30000, "max": 80000, "label": "コーポレートサイト（3-5ページ）"},
    "rich_site": {"min": 50000, "max": 150000, "label": "リッチサイト（アニメーション付き5-10ページ）"},
    "design_only": {"min": 10000, "max": 30000, "label": "デザインのみ"},
    "image_generation": {"min": 5000, "max": 20000, "label": "AI画像生成セット"},
}
