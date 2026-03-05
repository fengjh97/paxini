"""
Coconala Pipeline — Proposal Generator v2
Generates professional proposals based on scraped listings.
Uses full description from detail page for accurate classification.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import re
import json
import os
from config import OUR_STRENGTHS, PRICING, OUTPUT_DIR


# ─── Classification ──────────────────────────────────────────

def classify_project(title, description):
    """Classify the project type based on content. Order matters — specific first."""
    text = f"{title} {description}".lower()

    # Banner / single graphic (highest priority — avoid misclassifying as website)
    if any(kw in text for kw in ["バナー", "banner", "告知画像", "サムネイル", "アイキャッチ"]):
        return "banner"

    # Logo design
    if any(kw in text for kw in ["ロゴ", "logo"]) and "ロゴ" in title.lower():
        return "logo"

    # LP (landing page)
    if any(kw in text for kw in ["lp", "ランディング", "1ページ", "1p"]):
        return "simple_lp"

    # Image/illustration set
    if any(kw in text for kw in ["イラスト", "AI画像", "画像生成", "画像素材セット"]):
        return "image_generation"

    # Design mockup only (no coding)
    if any(kw in text for kw in ["デザインのみ", "デザイン案", "カンプ", "モックアップ", "デザインカンプ"]):
        return "design_only"

    # EC / online shop
    if any(kw in text for kw in ["ec", "ショップ", "通販", "shopify", "ecサイト"]):
        return "corporate_site"

    # Rich animated site
    if any(kw in text for kw in [
        "アニメーション", "リッチ", "動き", "モーション",
        "インタラクティブ",
    ]):
        return "rich_site"

    # Corporate / general website
    if any(kw in text for kw in [
        "コーポレート", "企業", "会社", "ホームページ", "hp",
        "web制作", "webサイト", "サイト制作", "ウェブサイト",
    ]):
        return "corporate_site"

    return "corporate_site"  # Default


def detect_industry(title, description):
    """Detect the industry/business type. Title gets priority over description."""
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
    # Remove common boilerplate
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


# ─── Pricing ─────────────────────────────────────────────────

# Extended pricing with new types
EXTENDED_PRICING = {
    **PRICING,
    "banner": {"min": 3000, "max": 10000, "label": "バナー・画像デザイン"},
    "logo": {"min": 5000, "max": 20000, "label": "ロゴデザイン"},
}


# ─── Proposal Generation ─────────────────────────────────────

def generate_proposal(listing):
    """Generate a full proposal for a listing."""
    title = listing.get("title", "")
    desc = listing.get("description", "") or listing.get("full_description", "")
    budget = listing.get("budget", "")
    budget_value = listing.get("budget_value", 0)

    project_type = classify_project(title, desc)
    industry = detect_industry(title, desc)
    requirements = extract_requirements(title, desc)
    pricing = EXTENDED_PRICING.get(project_type, EXTENDED_PRICING["corporate_site"])
    desc_summary = summarize_description(desc)

    # Smart price matching
    proposed_price = pricing["min"]
    if budget_value > 0:
        if budget_value >= pricing["min"]:
            proposed_price = min(budget_value, pricing["max"])
        else:
            # Client budget is low — match it if reasonable
            proposed_price = max(budget_value, pricing["min"])

    # Build proposal
    proposal_body = _get_proposal_body(project_type, industry, desc)
    strengths = _get_relevant_strengths(project_type)
    estimate_breakdown = _get_estimate_breakdown(project_type, proposed_price)

    proposal = f"""はじめまして。ご依頼内容を拝見し、提案させていただきます。

【ご依頼内容の理解】
{_format_understanding(title, desc_summary, industry, pricing['label'], requirements)}

【ご提案内容】
{proposal_body}

【当方の強み】
{chr(10).join(f"✓ {s}" for s in strengths)}

【お見積もり】
{pricing['label']}: {proposed_price:,}円（税込）
{estimate_breakdown}

【納期】
作業着手から{_get_delivery_days(project_type)}で納品可能です。

【修正対応】
{OUR_STRENGTHS['revision_rounds']}

【実績・ポートフォリオ】
以下にて制作実績をご確認いただけます:
{chr(10).join(OUR_STRENGTHS['portfolio_urls'])}

{_get_demo_offer(project_type, industry)}
ご不明点がございましたら、お気軽にメッセージください。
ご検討のほどよろしくお願いいたします。"""

    return {
        "proposal_text": proposal,
        "project_type": project_type,
        "industry": industry,
        "proposed_price": proposed_price,
        "pricing_label": pricing["label"],
    }


def _format_understanding(title, desc_summary, industry, type_label, requirements):
    """Show the client we actually read their request."""
    lines = [f"「{title}」について、以下のように理解しております。"]
    if desc_summary:
        lines.append(f"→ {desc_summary}")
    lines.append(f"- 業種: {industry}")
    lines.append(f"- 制作タイプ: {type_label}")
    for r in requirements:
        lines.append(f"- {r}")
    return "\n".join(lines)


def _get_relevant_strengths(project_type):
    """Return only relevant strengths for the project type."""
    all_strengths = OUR_STRENGTHS["skills"]

    if project_type in ["banner", "logo", "image_generation"]:
        # Image/design focused — emphasize AI image generation
        return [
            "Nano Banana Pro（AI画像生成 — Gemini 3 Pro）でプロ品質のオリジナル画像を生成",
            "フリー素材不要 — すべてオリジナル生成で著作権クリア",
            "複数のデザインバリエーションを短時間で提案可能",
            "修正・調整も迅速対応",
        ]

    if project_type == "simple_lp":
        return [
            "レスポンシブ HTML/CSS/JS（軽量・高速表示）",
            "AI画像生成でオリジナルビジュアルをご用意（追加費用なし）",
            "GSAP/ScrollTriggerによるリッチなスクロールアニメーション",
            "CVR（コンバージョン率）を意識した構成設計",
        ]

    if project_type == "rich_site":
        return all_strengths

    # Default: corporate site
    return [
        "レスポンシブ HTML/CSS/JS（フレームワーク不要の軽量構成）",
        "AI画像生成（Nano Banana Pro）でオリジナル画像を追加費用なしでご提供",
        "GSAP/ScrollTriggerによるリッチなアニメーション対応可",
        "デザインリサーチ → カラーパレット → 実装の一貫ワークフロー",
    ]


def _get_proposal_body(project_type, industry, desc):
    """Generate the main proposal body."""
    if project_type == "banner":
        return f"""AI画像生成ツール（Nano Banana Pro / Gemini 3 Pro）を活用し、
{industry}に最適なバナー・告知画像を制作いたします。

- ご要望に合わせた複数のデザイン案をご提案
- AI生成によるオリジナルビジュアル（フリー素材不使用）
- テキスト配置・カラーリングの微調整対応
- 各種サイズ展開（Web/SNS/印刷）にも対応可能

高品質なビジュアルをスピーディーにお届けいたします。"""

    if project_type == "logo":
        return f"""AI画像生成技術を活用し、{industry}のブランドイメージに合った
オリジナルロゴを制作いたします。

- コンセプトに合わせた複数のデザイン案をご提案
- ベクターデータ（SVG/AI）での納品対応
- カラーバリエーション（フルカラー/モノクロ）
- 各種メディアへの展開ガイド"""

    if project_type == "simple_lp":
        return f"""訴求力の高いランディングページを制作いたします。

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

    # Default: corporate site
    return f"""{industry}にふさわしい、信頼感のあるウェブサイトを制作いたします。

- トップページ: AI生成オリジナル画像 + ブランドメッセージ
- サービス/事業紹介ページ
- 会社概要/店舗情報ページ
- アクセス情報（Google Maps連携可）
- お問い合わせセクション
- 全ページスマホ対応（レスポンシブ）
- SEO基本設定"""


def _get_estimate_breakdown(project_type, price):
    """Generate an estimate breakdown appropriate for the project type."""
    if project_type in ["banner", "logo"]:
        return f"""
内訳:
- デザイン制作: {int(price * 0.7):,}円
- AI画像生成・素材制作: {int(price * 0.3):,}円"""

    if project_type == "image_generation":
        return f"""
内訳:
- AI画像生成（{_get_image_count(project_type)}枚）: {int(price * 0.8):,}円
- 調整・レタッチ: {int(price * 0.2):,}円"""

    return f"""
内訳:
- デザイン・コーディング: {int(price * 0.6):,}円
- AI画像生成（{_get_image_count(project_type)}枚程度）: {int(price * 0.2):,}円
- レスポンシブ対応: {int(price * 0.2):,}円"""


def _get_image_count(project_type):
    counts = {
        "banner": "1-3",
        "logo": "3-5",
        "simple_lp": "3-5",
        "corporate_site": "8-12",
        "rich_site": "12-15",
        "design_only": "3-5",
        "image_generation": "10-20",
    }
    return counts.get(project_type, "8-12")


def _get_delivery_days(project_type):
    days = {
        "banner": "1〜3営業日",
        "logo": "3〜5営業日",
        "simple_lp": "3〜5営業日",
        "corporate_site": "5〜10営業日",
        "rich_site": "10〜14営業日",
        "design_only": "3〜5営業日",
        "image_generation": "1〜3営業日",
    }
    return days.get(project_type, "7〜10営業日")


def _get_demo_offer(project_type, industry):
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
    filepath = os.path.join(OUTPUT_DIR, f"proposal_{listing_id}.md")

    proposer_count = listing.get("proposer_count", "?")
    deadline = listing.get("deadline", "")

    content = f"""# 提案書 — {listing.get('title', '')}

## 案件情報
- **URL**: {listing.get('url', '')}
- **カテゴリ**: {listing.get('category_name', '')}
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
    # Test classifications
    tests = [
        ("美容外科クリニックのイベント告知バナー", "バナー制作"),
        ("焼肉店のホームページを作成してほしい", "5ページ、スマホ対応"),
        ("【学習塾集客】LP制作依頼", "ランディングページ"),
        ("ロゴデザインをお願いしたい", "会社ロゴ"),
        ("AI画像を10枚生成してほしい", "商品画像"),
    ]
    for title, desc in tests:
        ptype = classify_project(title, desc)
        industry = detect_industry(title, desc)
        print(f"[{ptype:20s}] [{industry:12s}] {title}")
