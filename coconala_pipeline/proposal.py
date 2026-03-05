"""
Coconala Pipeline — Proposal Generator v3 (Multi-Track)
Generates professional proposals for 6 tracks:
  web, documents, graphic, writing, translation, it_dev
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import re
import json
import os
from config import OUR_STRENGTHS, TRACKS, OUTPUT_DIR


# ─── Classification ──────────────────────────────────────────

def classify_project(title, description, track_id=None):
    """Classify the project type based on content and track."""
    text = f"{title} {description}".lower()

    if track_id == "documents":
        return _classify_documents(text)
    elif track_id == "graphic":
        return _classify_graphic(text)
    elif track_id == "writing":
        return _classify_writing(text)
    elif track_id == "translation":
        return _classify_translation(text)
    elif track_id == "it_dev":
        return _classify_it_dev(text)
    else:
        return _classify_web(text)


def _classify_web(text):
    if any(kw in text for kw in ["バナー", "banner", "告知画像", "サムネイル", "アイキャッチ"]):
        return "banner"
    if any(kw in text for kw in ["ロゴ", "logo"]):
        return "logo"
    if any(kw in text for kw in ["lp", "ランディング", "1ページ", "1p"]):
        return "simple_lp"
    if any(kw in text for kw in ["イラスト", "AI画像", "画像生成", "画像素材セット"]):
        return "image_generation"
    if any(kw in text for kw in ["デザインのみ", "デザイン案", "カンプ", "モックアップ"]):
        return "design_only"
    if any(kw in text for kw in ["アニメーション", "リッチ", "動き", "モーション", "インタラクティブ"]):
        return "rich_site"
    return "corporate_site"


def _classify_documents(text):
    if any(kw in text for kw in ["補助金", "助成金", "申請"]):
        return "subsidy_doc"
    if any(kw in text for kw in ["事業計画", "計画書", "ビジネスプラン"]):
        return "business_plan"
    if any(kw in text for kw in ["企画書", "提案書", "プレゼン"]):
        return "proposal_doc"
    return "simple_doc"


def _classify_graphic(text):
    if any(kw in text for kw in ["サムネイル", "サムネ"]):
        return "thumbnail"
    if any(kw in text for kw in ["ロゴ", "logo"]):
        return "logo"
    if any(kw in text for kw in ["表紙", "書籍", "kindle", "本の"]):
        return "book_cover"
    if any(kw in text for kw in ["チラシ", "フライヤー"]):
        return "flyer"
    if any(kw in text for kw in ["名刺"]):
        return "business_card"
    if any(kw in text for kw in ["パッケージ", "ラベル"]):
        return "package"
    if any(kw in text for kw in ["ec", "商品画像", "商品ページ"]):
        return "product_image"
    return "banner"


def _classify_writing(text):
    if any(kw in text for kw in ["seo", "検索"]):
        return "seo_article"
    if any(kw in text for kw in ["キャッチコピー", "コピーライティング", "コピー"]):
        return "copywriting"
    if any(kw in text for kw in ["校正", "リライト", "修正", "添削"]):
        return "proofreading"
    if any(kw in text for kw in ["長文", "3000字", "5000字", "連載"]):
        return "long_article"
    return "short_article"


def _classify_translation(text):
    if any(kw in text for kw in ["ローカライズ", "サイト翻訳", "多言語"]):
        return "localization"
    if any(kw in text for kw in ["法律", "契約", "技術文書", "マニュアル", "特許"]):
        return "technical_translation"
    if any(kw in text for kw in ["文書", "資料", "報告書", "論文"]):
        return "document_translation"
    return "short_translation"


def _classify_it_dev(text):
    if any(kw in text for kw in ["ai", "機械学習", "chatgpt", "gemini", "画像生成", "チャットボット"]):
        return "ai_app"
    if any(kw in text for kw in ["webアプリ", "webサービス", "ウェブアプリ"]):
        return "web_app"
    if any(kw in text for kw in ["システム", "基幹", "管理画面", "データベース"]):
        return "system"
    if any(kw in text for kw in ["自動化", "rpa", "効率化", "vba", "gas", "excel"]):
        return "automation"
    return "small_tool"


def detect_industry(title, description):
    """Detect the industry/business type."""
    title_text = title or ""
    desc_text = (description or "")[:300]

    industry_rules = [
        ("医療・クリニック", ["クリニック", "歯科", "医院", "病院", "整骨院", "接骨院", "薬局", "医療", "美容外科"]),
        ("教育", ["学習塾", "塾", "スクール", "教室", "学習", "習い事", "予備校"]),
        ("美容・サロン", ["美容室", "ヘアサロン", "ネイルサロン", "エステサロン", "まつげサロン", "美容院"]),
        ("飲食店", ["飲食店", "レストラン", "カフェ", "居酒屋", "焼肉", "寿司", "ラーメン", "バー", "食堂"]),
        ("ホテル・旅館", ["ホテル", "旅館", "民宿", "宿泊", "旅行", "観光"]),
        ("フィットネス", ["ジム", "フィットネス", "ヨガ", "ピラティス", "トレーニング"]),
        ("不動産", ["不動産", "物件", "賃貸", "マンション"]),
        ("コンサル・士業", ["コンサル", "税理士", "行政書士", "弁護士", "会計士"]),
        ("EC・物販", ["ネットショップ", "通販", "物販"]),
        ("IT・テック", ["SaaS", "アプリ開発", "システム開発", "テック"]),
    ]

    for industry, keywords in industry_rules:
        if any(kw in title_text for kw in keywords):
            return industry

    full_text = f"{title_text} {desc_text}"
    for industry, keywords in industry_rules:
        if any(kw in full_text for kw in keywords):
            return industry

    return "一般企業"


def extract_requirements(title, description):
    """Extract specific requirements from the description."""
    reqs = []
    text = f"{title} {description}"

    page_match = re.search(r'(\d+)\s*(?:ページ|p|P)', text)
    if page_match:
        reqs.append(f"ページ数: 約{page_match.group(1)}ページ")

    if any(kw in text for kw in ["スマホ", "レスポンシブ", "モバイル"]):
        reqs.append("スマホ対応（レスポンシブ）: 対応可能")
    if any(kw in text for kw in ["参考サイト", "参考URL", "参考デザイン"]):
        reqs.append("参考デザインあり — 方向性に沿って制作します")
    if any(kw in text for kw in ["写真", "画像", "素材"]):
        reqs.append("画像素材: AI画像生成でオリジナル制作可能")
    if any(kw in text for kw in ["納品希望", "急ぎ", "至急"]):
        reqs.append("スピード対応可能")

    return reqs


def summarize_description(desc, max_len=200):
    """Extract a clean summary from the meta description."""
    if not desc:
        return ""
    lines = desc.split("\n")
    clean = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(("ココナラ", "coconala", "※")):
            continue
        clean.append(line)
    summary = " ".join(clean)
    if len(summary) > max_len:
        summary = summary[:max_len] + "..."
    return summary


# ─── Proposal Generation ─────────────────────────────────────

def generate_proposal(listing):
    """Generate a full proposal for a listing (track-aware)."""
    title = listing.get("title", "")
    desc = listing.get("description", "") or listing.get("full_description", "")
    budget_value = listing.get("budget_value", 0)
    track_id = listing.get("track_id", "web")

    project_type = classify_project(title, desc, track_id)
    industry = detect_industry(title, desc)
    requirements = extract_requirements(title, desc)
    desc_summary = summarize_description(desc)

    # Get track-specific pricing
    track = TRACKS.get(track_id, TRACKS["web"])
    pricing = track["pricing"].get(project_type)
    if not pricing:
        first_key = next(iter(track["pricing"]))
        pricing = track["pricing"][first_key]

    # Smart price matching
    proposed_price = pricing["min"]
    if budget_value > 0:
        if budget_value >= pricing["min"]:
            proposed_price = min(budget_value, pricing["max"])
        else:
            proposed_price = max(budget_value, pricing["min"])

    # Build proposal
    proposal_body = _get_proposal_body(project_type, industry, desc, track_id)
    strengths = _get_relevant_strengths(track_id)
    estimate_breakdown = _get_estimate_breakdown(project_type, proposed_price, track_id)

    proposal = f"""はじめまして。ご依頼内容を拝見し、提案させていただきます。

【ご依頼内容の理解】
{_format_understanding(title, desc_summary, industry, pricing['label'], requirements, track_id)}

【ご提案内容】
{proposal_body}

【当方の強み】
{chr(10).join(f"✓ {s}" for s in strengths)}

【お見積もり】
{pricing['label']}: {proposed_price:,}円（税込）
{estimate_breakdown}

【納期】
作業着手から{_get_delivery_days(project_type, track_id)}で納品可能です。

【修正対応】
{OUR_STRENGTHS['revision_rounds']}

【実績・ポートフォリオ】
以下にて制作実績をご確認いただけます:
{chr(10).join(OUR_STRENGTHS['portfolio_urls'])}

{_get_demo_offer(project_type, industry, track_id)}
ご不明点がございましたら、お気軽にメッセージください。
ご検討のほどよろしくお願いいたします。"""

    return {
        "proposal_text": proposal,
        "project_type": project_type,
        "industry": industry,
        "proposed_price": proposed_price,
        "pricing_label": pricing["label"],
        "track_id": track_id,
    }


def _format_understanding(title, desc_summary, industry, type_label, requirements, track_id=None):
    lines = [f"「{title}」について、以下のように理解しております。"]
    if desc_summary:
        lines.append(f"→ {desc_summary}")
    if track_id in (None, "web", "graphic"):
        lines.append(f"- 業種: {industry}")
    lines.append(f"- 制作タイプ: {type_label}")
    for r in requirements:
        lines.append(f"- {r}")
    return "\n".join(lines)


# ─── Proposal Bodies by Track ────────────────────────────────

def _get_proposal_body(project_type, industry, desc, track_id=None):
    if track_id == "documents":
        return _body_documents(project_type)
    elif track_id == "graphic":
        return _body_graphic(project_type, industry)
    elif track_id == "writing":
        return _body_writing(project_type)
    elif track_id == "translation":
        return _body_translation(project_type)
    elif track_id == "it_dev":
        return _body_it_dev(project_type)
    else:
        return _body_web(project_type, industry)


def _body_web(project_type, industry):
    if project_type == "banner":
        return f"""AI画像生成ツール（Nano Banana Pro / Gemini 3 Pro）を活用し、
{industry}に最適なバナー・告知画像を制作いたします。

- ご要望に合わせた複数のデザイン案をご提案
- AI生成によるオリジナルビジュアル（フリー素材不使用）
- テキスト配置・カラーリングの微調整対応
- 各種サイズ展開（Web/SNS/印刷）にも対応可能"""

    if project_type == "logo":
        return f"""AI画像生成技術を活用し、{industry}のブランドイメージに合った
オリジナルロゴを制作いたします。

- コンセプトに合わせた複数のデザイン案をご提案
- ベクターデータ（SVG/AI）での納品対応
- カラーバリエーション（フルカラー/モノクロ）
- 各種メディアへの展開ガイド"""

    if project_type == "simple_lp":
        return """訴求力の高いランディングページを制作いたします。

- ファーストビュー: AI生成の高品質オリジナル画像 + キャッチコピー
- サービス/商品の魅力を伝える構成設計
- お客様の声・実績セクション
- CTA（お問い合わせ/申し込み）への導線設計
- スマホ完全対応のレスポンシブデザイン
- スクロールアニメーションによる印象的な見せ方"""

    if project_type == "rich_site":
        return f"""{industry}のブランド価値を最大限に引き出す、
印象的で記憶に残るウェブサイトを制作いたします。

- GSAP/ScrollTriggerによる洗練されたスクロールアニメーション
- パララックス効果とマイクロインタラクション
- AI生成によるオリジナル高品質画像（10枚以上）
- モバイルファーストのレスポンシブ設計
- {industry}のブランドに合わせた独自カラーパレット"""

    if project_type == "image_generation":
        return f"""AI画像生成ツール（Nano Banana Pro / Gemini 3 Pro）を活用し、
{industry}に最適な高品質オリジナル画像をご提供いたします。

- ヒーロー画像（メインビジュアル）
- サービス/商品イメージ
- スタッフ/店舗イメージ
- バナー・SNS素材
すべてオリジナル生成のため、著作権の心配がありません。"""

    if project_type == "design_only":
        return f"""{industry}にふさわしいデザインカンプを制作いたします。

- ブランドイメージに合わせた配色・フォント選定
- ワイヤーフレームからビジュアルデザインまで
- AI画像生成でビジュアル素材も同時にご用意
- デザインガイドライン（カラー・フォント・余白）の提供"""

    return f"""{industry}にふさわしい、信頼感のあるウェブサイトを制作いたします。

- トップページ: AI生成オリジナル画像 + ブランドメッセージ
- サービス/事業紹介ページ
- 会社概要/店舗情報ページ
- アクセス情報（Google Maps連携可）
- お問い合わせセクション
- 全ページスマホ対応（レスポンシブ）
- SEO基本設定"""


def _body_documents(project_type):
    if project_type == "subsidy_doc":
        return """補助金・助成金の申請書類を作成いたします。

- 事業概要・実施計画の策定
- 経費明細・資金計画の作成
- 審査基準に沿った構成設計
- 図表・グラフの挿入で視覚的にわかりやすく
- AI分析による市場データ・根拠資料の補強
- PowerPoint/PDF形式での納品"""

    if project_type == "business_plan":
        return """説得力のある事業計画書を作成いたします。

- エグゼクティブサマリー
- 事業概要・ビジョン・ミッション
- 市場分析（AI調査による最新データ）
- マーケティング戦略
- 収支計画・財務予測（3-5年）
- リスク分析と対策
- AI生成の図表・インフォグラフィックで視覚化"""

    if project_type == "proposal_doc":
        return """インパクトのある企画書・提案書を作成いたします。

- 目的・背景の明確な整理
- 提案内容の論理的構成
- AI生成の高品質なビジュアル・図解
- データに基づく説得力のある資料設計
- PowerPoint/PDF形式での納品
- 印刷・プロジェクター投影どちらにも最適化"""

    return """ご要望に合わせた資料を作成いたします。

- ヒアリング内容に基づく構成設計
- 読みやすいレイアウト・フォント選定
- AI生成の図解・イラストで視覚的にわかりやすく
- PowerPoint/PDF形式での納品
- テンプレートとしての再利用も可能な設計"""


def _body_graphic(project_type, industry):
    if project_type == "book_cover":
        return """AI画像生成技術を活用し、目を引く書籍表紙を制作いたします。

- コンセプトに合わせた3パターンのデザイン案をご提案
- AI生成によるオリジナルビジュアル（著作権クリア）
- タイトル・著者名の視認性を重視したレイアウト
- Kindle/電子書籍・紙書籍の両対応
- 帯・背表紙・裏表紙の一括制作も可能"""

    if project_type == "flyer":
        return f"""AI画像生成で、{industry}に最適なチラシ・フライヤーを制作いたします。

- A4/A5/B5 各サイズ対応
- AI生成のオリジナル画像でインパクトのあるデザイン
- 印刷用（CMYK/350dpi）データ納品
- 表裏両面デザイン対応"""

    if project_type == "business_card":
        return """印象に残る名刺をデザインいたします。

- AI生成のオリジナルアクセントデザイン
- 表裏両面デザイン
- 印刷用データ（AI/PDF）納品
- 複数デザインパターンのご提案"""

    if project_type == "product_image":
        return """EC向け商品画像を制作いたします。

- 白背景・ライフスタイル撮影風のAI画像生成
- 複数アングル・バリエーション対応
- 楽天・Amazon・Shopify 各モールの規格に対応
- 商品説明バナーの制作も可能"""

    if project_type == "logo":
        return f"""AI画像生成技術を活用し、{industry}のブランドに合った
オリジナルロゴを制作いたします。

- コンセプトに合わせた複数のデザイン案をご提案
- AI生成による完全オリジナル（著作権クリア）
- カラーバリエーション（フルカラー/モノクロ/反転）
- 各種メディアへの展開ガイド"""

    return """AI画像生成ツール（Nano Banana Pro）を活用し、
高品質な画像デザインを制作いたします。

- ご要望に合わせた複数のデザイン案をご提案
- AI生成によるオリジナルビジュアル（フリー素材不使用）
- テキスト配置・カラーリングの微調整対応
- 各種サイズ展開（Web/SNS/印刷）にも対応可能"""


def _body_writing(project_type):
    if project_type == "seo_article":
        return """SEOを意識した高品質な記事を執筆いたします。

- ターゲットキーワードの選定・構成設計
- 検索意図に沿った見出し構成（H2/H3）
- E-E-A-T（経験・専門性・権威性・信頼性）を意識した執筆
- メタディスクリプション・タイトルタグの最適化
- WordPress/CMS入稿対応"""

    if project_type == "copywriting":
        return """心を動かすコピーライティングをご提供いたします。

- ターゲット分析に基づくメッセージ設計
- キャッチコピー + ボディコピーのセット提案
- 複数パターンのA/Bテスト用コピー
- LP・広告・SNS等の媒体に最適化"""

    if project_type == "proofreading":
        return """原稿の校正・リライトを丁寧に行います。

- 誤字脱字・文法チェック
- 表現の統一性・読みやすさの向上
- 文章構成の改善提案
- 原文の意図を活かしたリライト"""

    if project_type == "long_article":
        return """読み応えのある長文記事を執筆いたします。

- 事前リサーチに基づく充実した内容
- 論理的な構成で最後まで読ませる文章
- 適切な見出し・段落構成
- 必要に応じた図表・画像の挿入提案"""

    return """ご要望に合わせた記事コンテンツを執筆いたします。

- ターゲット読者を意識した文体・トーン
- わかりやすい構成設計
- AI調査による正確な情報収集
- 納品後の修正にも柔軟に対応"""


def _body_translation(project_type):
    if project_type == "localization":
        return """Webサイト・アプリのローカライズ対応を行います。

- 単なる翻訳ではなく、文化的ニュアンスを考慮した適応
- UI/UXテキストの自然な翻訳
- SEO対応の多言語メタデータ
- HTML/JSON/YAML等のファイル形式に対応
- 翻訳メモリを活用した一貫性のある翻訳"""

    if project_type == "technical_translation":
        return """専門性の高い技術・法律文書の翻訳を行います。

- 分野別の専門用語を正確に翻訳
- AI翻訳 + 人手による品質チェック
- 用語集の作成・統一
- 原文のフォーマット・レイアウトを維持"""

    if project_type == "document_translation":
        return """ビジネス文書の翻訳を行います。

- ビジネスに適したフォーマルな文体
- 原文の意図を正確に伝える自然な翻訳
- 用語の一貫性チェック
- 校正済みの完成原稿を納品"""

    return """迅速・正確な翻訳をご提供いたします。

- AI翻訳エンジンによる高速一次翻訳
- ネイティブ品質の自然な表現に仕上げ
- 用途に合わせた文体調整（カジュアル/フォーマル）
- 短納期対応可能"""


def _body_it_dev(project_type):
    if project_type == "ai_app":
        return """AI技術を活用したアプリケーション・ツールを開発いたします。

- ChatGPT/Gemini API等の最新AI技術の導入
- 画像生成AI・テキスト生成AIの活用
- チャットボット・自動応答システム
- テスト済みコードの納品 + ドキュメント整備"""

    if project_type == "web_app":
        return """フルスタックのWebアプリケーションを開発いたします。

- Python (Flask/FastAPI) / JavaScript (Node.js) によるバックエンド
- レスポンシブなフロントエンド
- データベース設計・API開発
- ユーザー認証・セキュリティ対応
- GitHubリポジトリでのコード管理"""

    if project_type == "system":
        return """業務システムの開発・カスタマイズを行います。

- 要件ヒアリングに基づく設計
- データベース設計・バックエンド開発
- 管理画面・ダッシュボードの構築
- 外部API・既存システムとの連携
- テスト・運用ドキュメントの整備"""

    if project_type == "automation":
        return """業務効率化・自動化ツールを開発いたします。

- Excel/スプレッドシートの自動処理（VBA/GAS/Python）
- データ収集・スクレイピングツール
- 定型業務のRPA化
- API連携による業務フロー自動化"""

    return """ご要望に合わせたツール・スクリプトを開発いたします。

- Python / JavaScript / VBA 等で実装
- 使いやすいUI/CLI設計
- エラーハンドリング・ログ出力
- README・使用手順書付きで納品"""


# ─── Helpers ─────────────────────────────────────────────────

def _get_relevant_strengths(track_id=None):
    track = TRACKS.get(track_id, TRACKS["web"])
    return track["strengths"]


def _get_delivery_days(project_type, track_id=None):
    delivery = {
        "web": {
            "banner": "1〜3営業日", "logo": "3〜5営業日", "simple_lp": "3〜5営業日",
            "corporate_site": "5〜10営業日", "rich_site": "10〜14営業日",
            "design_only": "3〜5営業日", "image_generation": "1〜3営業日",
        },
        "documents": {
            "simple_doc": "3〜5営業日", "proposal_doc": "5〜7営業日",
            "business_plan": "7〜10営業日", "subsidy_doc": "7〜14営業日",
        },
        "graphic": {
            "banner": "1〜3営業日", "thumbnail": "1〜2営業日", "logo": "3〜5営業日",
            "book_cover": "3〜5営業日", "flyer": "3〜5営業日",
            "business_card": "2〜3営業日", "package": "5〜7営業日",
            "product_image": "2〜3営業日",
        },
        "writing": {
            "short_article": "1〜2営業日", "long_article": "3〜5営業日",
            "seo_article": "3〜5営業日", "copywriting": "2〜3営業日",
            "proofreading": "1〜2営業日",
        },
        "translation": {
            "short_translation": "1〜2営業日", "document_translation": "3〜5営業日",
            "technical_translation": "5〜7営業日", "localization": "7〜14営業日",
        },
        "it_dev": {
            "small_tool": "3〜5営業日", "automation": "5〜7営業日",
            "web_app": "7〜14営業日", "ai_app": "7〜14営業日",
            "system": "14〜21営業日",
        },
    }
    track_days = delivery.get(track_id or "web", delivery["web"])
    return track_days.get(project_type, "5〜7営業日")


def _get_estimate_breakdown(project_type, price, track_id=None):
    if track_id == "documents":
        return f"""
内訳:
- 構成設計・リサーチ: {int(price * 0.3):,}円
- 文書作成: {int(price * 0.5):,}円
- 図表・デザイン: {int(price * 0.2):,}円"""

    if track_id == "graphic":
        return f"""
内訳:
- デザイン制作: {int(price * 0.7):,}円
- AI画像生成・素材制作: {int(price * 0.3):,}円"""

    if track_id == "writing":
        return f"""
内訳:
- リサーチ・構成: {int(price * 0.3):,}円
- 執筆: {int(price * 0.6):,}円
- 校正・仕上げ: {int(price * 0.1):,}円"""

    if track_id == "translation":
        return f"""
内訳:
- AI翻訳・一次翻訳: {int(price * 0.4):,}円
- 校閲・品質チェック: {int(price * 0.4):,}円
- フォーマット調整: {int(price * 0.2):,}円"""

    if track_id == "it_dev":
        return f"""
内訳:
- 設計・要件整理: {int(price * 0.2):,}円
- 開発・実装: {int(price * 0.6):,}円
- テスト・ドキュメント: {int(price * 0.2):,}円"""

    # Web track
    if project_type in ["banner", "logo"]:
        return f"""
内訳:
- デザイン制作: {int(price * 0.7):,}円
- AI画像生成・素材制作: {int(price * 0.3):,}円"""

    if project_type == "image_generation":
        return f"""
内訳:
- AI画像生成: {int(price * 0.8):,}円
- 調整・レタッチ: {int(price * 0.2):,}円"""

    return f"""
内訳:
- デザイン・コーディング: {int(price * 0.6):,}円
- AI画像生成: {int(price * 0.2):,}円
- レスポンシブ対応: {int(price * 0.2):,}円"""


def _get_demo_offer(project_type, industry, track_id=None):
    if track_id == "documents":
        return """【サンプルのご提供】
ご採用前に、類似テーマのサンプル資料（2-3ページ）をお見せすることも可能です。
"""
    if track_id == "graphic":
        return """【サンプルのご提供】
ご採用前に、イメージに近いAI生成サンプル画像を2-3パターンお見せいたします。
"""
    if track_id == "writing":
        return """【サンプルのご提供】
ご採用前に、テーマに沿ったサンプル原稿（冒頭300字程度）をお見せすることも可能です。
"""
    if track_id == "translation":
        return """【サンプルのご提供】
ご採用前に、原稿の一部（冒頭200字程度）を翻訳したサンプルをお見せいたします。
"""
    if track_id == "it_dev":
        return """【サンプルのご提供】
ご採用前に、類似ツールのデモ版やスクリーンショットをお見せすることも可能です。
GitHubにて過去の開発実績もご確認いただけます。
"""

    # Web track
    if project_type in ["simple_lp", "corporate_site", "rich_site"]:
        return f"""【デモのご提供】
ご採用前に、{industry}向けのデモサイトをご確認いただけます。
実際の制作クオリティを事前にご確認いただけるため、安心してご依頼いただけます。
"""
    if project_type in ["banner", "logo", "image_generation"]:
        return """【サンプルのご提供】
ご採用前に、イメージに近いサンプル画像をお見せすることも可能です。
"""
    return ""


def save_proposal_file(listing, proposal_data):
    """Save proposal to a file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    listing_id = listing.get("id", "unknown")
    track_id = proposal_data.get("track_id", "web")
    filepath = os.path.join(OUTPUT_DIR, f"proposal_{track_id}_{listing_id}.md")

    proposer_count = listing.get("proposer_count", "?")
    deadline = listing.get("deadline", "")
    track_name = TRACKS.get(track_id, {}).get("name", track_id)

    content = f"""# 提案書 — {listing.get('title', '')}

## 案件情報
- **URL**: {listing.get('url', '')}
- **カテゴリ**: {listing.get('category_name', '')}
- **トラック**: {track_name}
- **予算**: {listing.get('budget', '未定')}
- **提案数**: {proposer_count}件
- **締切**: {deadline or '不明'}
- **業種判定**: {proposal_data['industry']}
- **制作タイプ**: {proposal_data['pricing_label']}
- **提案価格**: {proposal_data['proposed_price']:,}円

---

## 提案文（コピペ用）

{proposal_data['proposal_text']}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


if __name__ == "__main__":
    tests = [
        ("美容外科クリニックのイベント告知バナー", "バナー制作", "web"),
        ("焼肉店のホームページを作成してほしい", "5ページ、スマホ対応", "web"),
        ("営業代行の提案資料を作成してほしい", "営業用のPowerPoint資料", "documents"),
        ("小規模事業者持続化補助金の申請書", "補助金申請", "documents"),
        ("Kindle本の表紙デザイン", "イラスト集の表紙", "graphic"),
        ("YouTube用サムネイルを作成", "サムネイル", "graphic"),
        ("SEO記事を5000字で執筆", "不動産のSEO記事", "writing"),
        ("キャッチコピーを10案作成", "新商品のコピー", "writing"),
        ("英語の契約書を日本語に翻訳", "法律文書の翻訳", "translation"),
        ("Webサイトの多言語化", "英語・中国語対応", "translation"),
        ("Pythonでスクレイピングツール開発", "データ収集の自動化", "it_dev"),
        ("ChatGPTを活用した社内ツール", "AI活用", "it_dev"),
    ]
    for title, desc, track in tests:
        ptype = classify_project(title, desc, track)
        industry = detect_industry(title, desc)
        print(f"[{track:12s}] [{ptype:22s}] [{industry:12s}] {title}")
