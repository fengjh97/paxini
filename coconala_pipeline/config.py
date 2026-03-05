"""
Coconala Pipeline — Configuration (Multi-Track)
"""
import os

# === Scraping Settings ===
BASE_URL = "https://coconala.com"
REQUESTS_URL = f"{BASE_URL}/requests/categories"
MIN_BUDGET = 5000
REQUEST_INTERVAL = 5

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

DB_PATH = os.path.join(os.path.dirname(__file__), "coconala.db")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# === Track Definitions ===
TRACKS = {
    "web": {
        "name": "Web制作",
        "categories": {
            22:  "Web制作・HP作成・EC構築",
            500: "ホームページ作成・サイト制作",
            501: "WEBサイトデザイン・UI設計",
            503: "LP作成・ランディングページデザイン",
            507: "ECサイト制作・ネットショップ構築",
            230: "作業自動化・効率化",
        },
        "positive_keywords": [
            "ホームページ", "HP", "ウェブサイト", "Webサイト", "web制作",
            "ランディングページ", "LP", "コーポレートサイト",
            "デザイン", "おしゃれ", "かっこいい", "モダン",
            "レスポンシブ", "スマホ対応",
            "画像生成", "AI", "バナー", "ロゴ",
            "飲食店", "美容室", "サロン", "ホテル", "旅館", "民宿",
            "クリニック", "歯科", "整骨院", "ジム",
            "新規", "リニューアル", "作成", "制作",
        ],
        "negative_keywords": [
            "WordPress", "ワードプレス", "Shopify",
            "システム開発", "アプリ開発", "API連携",
            "SEO対策のみ", "記事作成のみ", "ライティング",
        ],
        "pricing": {
            "banner": {"min": 3000, "max": 10000, "label": "バナー・画像デザイン"},
            "logo": {"min": 5000, "max": 20000, "label": "ロゴデザイン"},
            "simple_lp": {"min": 15000, "max": 30000, "label": "シンプルLP（1ページ）"},
            "corporate_site": {"min": 30000, "max": 80000, "label": "コーポレートサイト（3-5ページ）"},
            "rich_site": {"min": 50000, "max": 150000, "label": "リッチサイト（アニメーション付き5-10ページ）"},
            "design_only": {"min": 10000, "max": 30000, "label": "デザインのみ"},
            "image_generation": {"min": 5000, "max": 20000, "label": "AI画像生成セット"},
        },
        "strengths": [
            "Claude Code（AI駆動のフルスタック開発）",
            "Nano Banana Pro（AI画像生成 — Gemini 3 Pro）でオリジナル画像を追加費用なしでご提供",
            "レスポンシブ HTML/CSS/JS（フレームワーク不要の軽量構成）",
            "GSAP/ScrollTriggerによるリッチなアニメーション対応可",
            "デザインリサーチ → カラーパレット → 実装の一貫ワークフロー",
        ],
        "delivery_speed": "最短3日〜",
        "demo_type": "html",
    },
    "documents": {
        "name": "資料・企画書作成",
        "categories": {
            427: "資料・企画書作成",
            272: "事業計画書作成支援",
            673: "ビジネス文書作成",
        },
        "positive_keywords": [
            "資料", "企画書", "提案書", "事業計画", "計画書", "プレゼン",
            "PowerPoint", "PPT", "パワポ", "PDF", "スライド",
            "営業資料", "会社案内", "マニュアル", "研修", "テキスト",
            "補助金", "助成金", "申請書",
            "プレスリリース", "リリース",
        ],
        "negative_keywords": [
            "翻訳", "Web制作", "プログラミング",
        ],
        "pricing": {
            "simple_doc": {"min": 10000, "max": 25000, "label": "シンプル資料（10ページ以内）"},
            "proposal_doc": {"min": 20000, "max": 50000, "label": "企画書・提案書"},
            "business_plan": {"min": 30000, "max": 80000, "label": "事業計画書"},
            "subsidy_doc": {"min": 30000, "max": 100000, "label": "補助金申請書"},
        },
        "strengths": [
            "Claude Code（AI駆動のビジネス文書生成）",
            "Nano Banana Pro（プレゼン用AI画像・図解生成）",
            "財務計算・市場分析を組み込んだ計画書作成",
            "業界別テンプレートで迅速対応",
        ],
        "delivery_speed": "最短1日〜",
        "demo_type": "document",
    },
    "graphic": {
        "name": "グラフィックデザイン",
        "categories": {
            353: "バナー・ヘッダー制作",
            355: "サムネイル・画像デザイン",
            351: "ロゴ作成・ロゴデザイン",
            608: "書籍デザイン・表紙作成",
            362: "チラシ作成・フライヤーデザイン",
            364: "パッケージデザイン・ラベル作成",
            357: "名刺作成・名刺デザイン",
            681: "EC商品画像・ページ作成",
        },
        "positive_keywords": [
            "バナー", "ヘッダー", "サムネイル", "ロゴ", "表紙",
            "チラシ", "フライヤー", "パッケージ", "ラベル", "名刺",
            "EC商品", "商品画像", "SNS画像", "アイキャッチ",
            "Kindle", "書籍", "本の表紙",
            "おしゃれ", "高級感", "モダン",
        ],
        "negative_keywords": [
            "コーディング", "プログラミング", "システム",
        ],
        "pricing": {
            "banner": {"min": 3000, "max": 10000, "label": "バナー・SNS画像"},
            "thumbnail": {"min": 3000, "max": 8000, "label": "サムネイル"},
            "logo": {"min": 5000, "max": 25000, "label": "ロゴデザイン"},
            "book_cover": {"min": 8000, "max": 25000, "label": "書籍表紙デザイン"},
            "flyer": {"min": 8000, "max": 20000, "label": "チラシ・フライヤー"},
            "business_card": {"min": 5000, "max": 10000, "label": "名刺デザイン"},
            "package": {"min": 8000, "max": 25000, "label": "パッケージ・ラベル"},
            "product_image": {"min": 5000, "max": 15000, "label": "EC商品画像"},
        },
        "strengths": [
            "Nano Banana Pro（AI画像生成 — Gemini 3 Pro）で高品質オリジナル画像を生成",
            "フリー素材不要 — すべてオリジナル生成で著作権クリア",
            "複数デザインバリエーションを短時間で提案",
            "サイズ展開（Web/SNS/印刷）にも柔軟対応",
        ],
        "delivery_speed": "最短1日〜",
        "demo_type": "image",
    },
    "writing": {
        "name": "ライティング",
        "categories": {
            372: "記事・Webコンテンツ作成",
            370: "コピーライティング",
            371: "文章校正・編集・リライト",
        },
        "positive_keywords": [
            "記事", "ブログ", "コンテンツ", "ライティング",
            "コピー", "キャッチコピー", "SEO記事",
            "校正", "リライト", "文章", "原稿",
            "メルマガ", "プレスリリース", "コラム",
        ],
        "negative_keywords": [
            "翻訳", "プログラミング", "デザインのみ",
        ],
        "pricing": {
            "short_article": {"min": 3000, "max": 8000, "label": "短文記事（1000字以内）"},
            "long_article": {"min": 5000, "max": 15000, "label": "長文記事（3000字以上）"},
            "seo_article": {"min": 8000, "max": 20000, "label": "SEO記事"},
            "copywriting": {"min": 5000, "max": 15000, "label": "コピーライティング"},
            "proofreading": {"min": 3000, "max": 10000, "label": "文章校正・リライト"},
        },
        "strengths": [
            "Claude Code（AI駆動の高品質文章生成）",
            "SEO最適化を意識した記事構成",
            "業界別の専門知識に基づくライティング",
            "高速納品 — AIアシストにより通常の3倍速",
        ],
        "delivery_speed": "最短即日〜",
        "demo_type": "article",
    },
    "translation": {
        "name": "翻訳",
        "categories": {
            290: "外国語翻訳",
        },
        "positive_keywords": [
            "翻訳", "translation", "英訳", "和訳",
            "英日", "日英", "中日", "日中",
            "多言語", "ローカライズ",
            "法律文書", "技術文書", "マニュアル",
        ],
        "negative_keywords": [
            "ライティング", "記事作成", "Web制作",
        ],
        "pricing": {
            "short_translation": {"min": 5000, "max": 15000, "label": "短文翻訳（1000字以内）"},
            "document_translation": {"min": 10000, "max": 50000, "label": "文書翻訳"},
            "technical_translation": {"min": 20000, "max": 80000, "label": "技術・法律翻訳"},
            "localization": {"min": 30000, "max": 100000, "label": "Webサイトローカライズ"},
        },
        "strengths": [
            "Claude Code（AI駆動の高精度翻訳）",
            "英語・中国語・フランス語など多言語対応",
            "技術文書・ビジネス文書の専門翻訳",
            "ネイティブチェック品質のAI翻訳 + 人手仕上げ",
        ],
        "delivery_speed": "最短即日〜",
        "demo_type": "article",
    },
    "it_dev": {
        "name": "IT/AI開発",
        "categories": {
            231: "プログラミング・ソフト開発",
            232: "システム開発・制作",
            237: "アプリ開発・制作",
            813: "Webシステム・アプリ制作",
            774: "AIアプリケーション開発・制作",
            775: "画像生成AI活用・プロンプト作成",
            776: "チャット生成AI活用・プロンプト作成",
        },
        "positive_keywords": [
            "Python", "JavaScript", "プログラミング", "開発",
            "システム", "ツール", "自動化", "API",
            "スクレイピング", "Chrome拡張", "データ",
            "AI", "機械学習", "ChatGPT", "Gemini", "画像生成",
            "VBA", "GAS", "Excel", "業務効率化",
        ],
        "negative_keywords": [
            "MQL", "PLC", "VST",  # niche hardware/trading
            "Unity", "Unreal",    # game engines
        ],
        "pricing": {
            "small_tool": {"min": 10000, "max": 30000, "label": "小規模ツール開発"},
            "automation": {"min": 20000, "max": 60000, "label": "業務自動化"},
            "web_app": {"min": 30000, "max": 100000, "label": "Webアプリ開発"},
            "ai_app": {"min": 30000, "max": 150000, "label": "AI活用・導入"},
            "system": {"min": 50000, "max": 200000, "label": "システム開発"},
        },
        "strengths": [
            "Claude Code（AI駆動のフルスタック開発）",
            "Python / JavaScript / SQL / REST API",
            "AI活用（画像生成・テキスト生成・チャットボット構築）",
            "業務自動化・データ処理の豊富な経験",
            "GitHub管理・テスト済みコードの納品",
        ],
        "delivery_speed": "最短3日〜",
        "demo_type": "code",
    },
}

# === Helper Functions ===

def get_track_for_category(category_id):
    """Return the track ID for a given Coconala category ID."""
    for track_id, track in TRACKS.items():
        if category_id in track["categories"]:
            return track_id
    return "web"


def get_track_categories(track_ids=None):
    """Return merged categories dict for given track IDs (or all)."""
    if track_ids is None:
        return CATEGORIES
    result = {}
    for tid in track_ids:
        if tid in TRACKS:
            result.update(TRACKS[tid]["categories"])
    return result


# === Backward Compatibility ===
CATEGORIES = {}
POSITIVE_KEYWORDS = []
NEGATIVE_KEYWORDS = []
for _track in TRACKS.values():
    CATEGORIES.update(_track["categories"])
    POSITIVE_KEYWORDS.extend(_track["positive_keywords"])
    NEGATIVE_KEYWORDS.extend(_track["negative_keywords"])
POSITIVE_KEYWORDS = list(dict.fromkeys(POSITIVE_KEYWORDS))
NEGATIVE_KEYWORDS = list(dict.fromkeys(NEGATIVE_KEYWORDS))

PRICING = TRACKS["web"]["pricing"]

OUR_STRENGTHS = {
    "skills": TRACKS["web"]["strengths"],
    "portfolio_urls": ["https://github.com/fengjh97/paxini"],
    "delivery_speed": TRACKS["web"]["delivery_speed"],
    "revision_rounds": "2回まで無料修正",
}
