"""
Coconala Pipeline — Public Request Scraper (v2)

Two-phase approach:
  Phase 1: List page → extract request IDs + titles from links
  Phase 2: Detail page → extract full info via CSS selectors + meta tags
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import requests
from bs4 import BeautifulSoup
import re
import time
import json
from config import (
    REQUESTS_URL, BASE_URL, CATEGORIES, USER_AGENT,
    REQUEST_INTERVAL, POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS, MIN_BUDGET,
    TRACKS, get_track_for_category, get_track_categories,
)
from db import init_db, listing_exists, save_listing


def parse_budget(budget_str):
    """Extract numeric budget value from string like '3万円〜5万円' or '5千円未満'."""
    if not budget_str:
        return 0
    clean = budget_str.replace(',', '').replace('，', '').replace(' ', '')

    # Handle Japanese unit multipliers: 万 = x10000, 千 = x1000
    # Find all amounts with their position to get the first (minimum) one
    amounts = []
    for match in re.finditer(r'(\d+(?:\.\d+)?)\s*万', clean):
        amounts.append((match.start(), int(float(match.group(1)) * 10000)))
    for match in re.finditer(r'(\d+(?:\.\d+)?)\s*千', clean):
        amounts.append((match.start(), int(float(match.group(1)) * 1000)))

    if amounts:
        amounts.sort(key=lambda x: x[0])  # Sort by position in string
        return amounts[0][1]  # Return first occurrence (minimum)

    # Fallback: plain numbers (e.g., '10,000円〜20,000円' or '3,000円')
    nums = re.findall(r'\d+', clean)
    if nums:
        return int(nums[0])
    return 0


def score_listing(title, description, budget_value, proposer_count=0, track_id=None):
    """Score listing using AI (Gemini) with keyword fallback."""
    # Try AI scoring first
    ai_result = _score_with_ai(title, description, budget_value, proposer_count, track_id)
    if ai_result is not None:
        return ai_result

    # Fallback: keyword-based scoring
    return _score_with_keywords(title, description, budget_value, proposer_count, track_id)


# ─── AI Scoring (Gemini) ─────────────────────────────────────

_gemini_client = None

def _get_gemini_client():
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        _gemini_client = genai.Client(api_key=api_key)
        return _gemini_client
    except ImportError:
        return None


def _score_with_ai(title, description, budget_value, proposer_count, track_id):
    """Let Gemini evaluate whether this listing is a good fit for us."""
    client = _get_gemini_client()
    if client is None:
        return None

    track = TRACKS.get(track_id, TRACKS["web"])

    prompt = f"""あなたはフリーランスの案件評価AIです。
以下のココナラ公開依頼を、私たちのスキルセットで「受注すべきか」を0〜100点で評価してください。

## 私たちの能力
- ツール: Claude Code（AI駆動開発）、Nano Banana Pro（AI画像生成 — Gemini 3 Pro）
- 得意分野: {track['name']}
- 強み: {', '.join(track['strengths'])}
- 価格帯: {json.dumps(track['pricing'], ensure_ascii=False)}

## 案件情報
- タイトル: {title}
- 説明: {description[:500]}
- 予算: {budget_value}円（0=見積り希望）
- 現在の提案数: {proposer_count}件

## 評価基準（重要度順）
1. 【最重要】実現可能性: 私たちのツールで実際に納品できるか？
   - 可能: HTML/CSS/JS制作、Python開発、AI画像生成、文書作成、翻訳
   - 不可能（0点にすべき）: WordPress/Shopify構築、MQL/PLC/Unity等の専門言語、ハードウェア制御、既存システムの保守・改修（ソースコード読解が必要）
   - 判断のコツ: 「WordPressから脱却したい」→HTML化なので可能。「WordPressで構築して」→WP専門知識が必要なので不可。
2. 自動化度: Claude Code/Nano Bananaでどれだけ自動化できるか？高いほど高得点
3. 競争優位: AI活用で他の提案者より良い提案ができるか？
4. 収益性: 予算と作業量のバランスは？（見積り希望=価格設定可能なのでプラス評価）
5. 競争度: 提案数が少ないほど有利

JSONのみで回答してください（説明不要）:
{{"score": <0-100の整数>, "reason": "<日本語で1行の理由>"}}"""

    try:
        from google.genai import types
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=200,
            ),
        )
        text = response.text.strip()
        # Extract JSON from response
        json_match = re.search(r'\{[^}]+\}', text)
        if json_match:
            result = json.loads(json_match.group())
            score = int(result.get("score", 0))
            reason = result.get("reason", "")
            if reason:
                print(f"[AI] {score}点 — {reason}", end=" | ", flush=True)
            return max(0, min(100, score))
    except Exception as e:
        print(f"[AI score error: {e}]", end=" ", flush=True)

    return None


# ─── Keyword Fallback ─────────────────────────────────────────

def _score_with_keywords(title, description, budget_value, proposer_count, track_id):
    """Fallback: score based on keyword matching when AI is unavailable."""
    text = f"{title} {description}".lower()
    score = 0

    if track_id and track_id in TRACKS:
        pos_kws = TRACKS[track_id]["positive_keywords"]
        neg_kws = TRACKS[track_id]["negative_keywords"]
    else:
        pos_kws = POSITIVE_KEYWORDS
        neg_kws = NEGATIVE_KEYWORDS

    for kw in pos_kws:
        if kw.lower() in text:
            score += 8
    for kw in neg_kws:
        if kw.lower() in text:
            score -= 15

    if budget_value >= 50000:
        score += 20
    elif budget_value >= 20000:
        score += 10
    elif budget_value >= MIN_BUDGET:
        score += 5
    elif budget_value > 0 and budget_value < MIN_BUDGET:
        score -= 10

    if proposer_count > 30:
        score -= 10
    elif proposer_count > 15:
        score -= 5
    elif proposer_count == 0:
        score += 5

    return max(0, min(100, score))


# ─── Phase 1: List Page ───────────────────────────────────────

def scrape_category_ids(category_id, category_name, max_pages=3, session=None):
    """Phase 1: Get request IDs and titles from the list page."""
    if session is None:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

    found = []
    seen_ids = set()

    for page in range(1, max_pages + 1):
        url = f"{REQUESTS_URL}/{category_id}?page={page}"
        print(f"  [{category_name}] page {page}...", end=" ", flush=True)

        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"ERROR: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # Find all links to /requests/{id} (both relative and absolute)
        pattern = re.compile(r'(?:https?://coconala\.com)?/requests/(\d+)')
        links = soup.find_all("a", href=pattern)

        # First pass: collect all IDs and their best title
        id_titles = {}  # rid -> best title
        for link in links:
            match = pattern.search(link.get("href", ""))
            if not match:
                continue
            rid = match.group(1)
            title = link.get_text(strip=True)
            # Keep the longest (most informative) title for each ID
            if rid not in id_titles or (title and len(title) > len(id_titles[rid])):
                id_titles[rid] = title

        page_ids = []
        for rid, title in id_titles.items():
            if rid in seen_ids:
                continue
            if not title or len(title) < 5:
                continue  # Skip if no meaningful title found
            seen_ids.add(rid)

            page_ids.append({
                "id": rid,
                "title": title[:200],
                "category_id": category_id,
                "category_name": category_name,
            })

        found.extend(page_ids)
        print(f"{len(page_ids)} items")

        if page < max_pages:
            time.sleep(REQUEST_INTERVAL)

    return found


# ─── Phase 2: Detail Page ──────────────────────────────────────

def scrape_listing_detail(listing_id, session=None):
    """Phase 2: Scrape full detail from a listing's detail page.

    Extracts:
    - Full description (from meta tag — most reliable)
    - Budget (from .d-requestBudget_emphasis)
    - Deadline (from page text pattern)
    - Proposer count (from .c-requestOutlineRowContent_emphasis-proposalsLink)
    - Delivery date
    """
    if session is None:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

    url = f"{BASE_URL}/requests/{listing_id}"

    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return {"error": str(e)}

    soup = BeautifulSoup(resp.text, "html.parser")

    # 1. Full description — meta description is the best source
    full_desc = ""
    meta = soup.find("meta", {"name": "description"})
    if meta and meta.get("content"):
        full_desc = meta["content"]

    # Fallback: try the detail content div
    if not full_desc or len(full_desc) < 50:
        detail_div = soup.select_one(".c-requestDetailContents")
        if detail_div:
            full_desc = detail_div.get_text("\n", strip=True)[:2000]

    # 2. Title from h1
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    # 3. Budget
    budget = ""
    budget_el = soup.select_one(".d-requestBudget_emphasis, [class*='requestBudget']")
    if budget_el:
        budget = budget_el.get_text(strip=True)

    # Fallback: find budget from outline text
    if not budget or budget == "見積り希望":
        outline = soup.select_one(".c-requestDetailContents_cassette")
        if outline:
            text = outline.get_text(" ", strip=True)
            budget_match = re.search(r'予算\s*([\d,]+円[^\s]*)', text)
            if budget_match:
                budget = budget_match.group(1)

    budget_value = parse_budget(budget)

    # 4. Proposer count
    proposer_count = 0
    proposer_el = soup.select_one(
        "[class*='proposalsLink'], [class*='proposalCount']"
    )
    if proposer_el:
        nums = re.findall(r'\d+', proposer_el.get_text())
        if nums:
            proposer_count = int(nums[0])

    # 5. Dates: delivery + deadline
    delivery_date = ""
    deadline = ""
    page_text = soup.get_text(" ", strip=True) if soup.body else ""

    delivery_match = re.search(r'納品希望日\s*(\d{4}年\d{1,2}月\d{1,2}日)', page_text)
    if delivery_match:
        delivery_date = delivery_match.group(1)

    deadline_match = re.search(r'締切日\s*(\d{4}年\d{1,2}月\d{1,2}日)', page_text)
    if deadline_match:
        deadline = deadline_match.group(1)

    # 6. Category from page
    category = ""
    cat_link = soup.select_one("a[href*='/requests/categories/']")
    if cat_link:
        category = cat_link.get_text(strip=True)

    return {
        "id": listing_id,
        "url": url,
        "title": title,
        "full_description": full_desc,
        "budget": budget,
        "budget_value": budget_value,
        "proposer_count": proposer_count,
        "delivery_date": delivery_date,
        "deadline": deadline,
        "category": category,
    }


# ─── Combined Pipeline ────────────────────────────────────────

def run_scraper(categories=None, max_pages=2, fetch_details=True, detail_limit=10, track_ids=None):
    """Main scraper entry point.

    Args:
        categories: dict of {id: name} to scrape (overrides track_ids)
        max_pages: pages per category on list view
        fetch_details: whether to fetch detail pages for top candidates
        detail_limit: max number of detail pages to fetch
        track_ids: list of track IDs to scrape (e.g., ["web", "documents"])
    """
    init_db()

    if categories is None:
        categories = get_track_categories(track_ids)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    print("=" * 50)
    print("Coconala 公開依頼スクレイパー v2")
    print(f"  対象カテゴリ: {len(categories)}件")
    print("=" * 50)

    # Phase 1: Collect IDs from list pages
    all_ids = []
    for cat_id, cat_name in categories.items():
        ids = scrape_category_ids(cat_id, cat_name, max_pages=max_pages, session=session)
        new_ids = [x for x in ids if not listing_exists(x["id"])]
        all_ids.extend(new_ids)
        print(f"  → {len(ids)}件取得, うち新規: {len(new_ids)}件")
        time.sleep(REQUEST_INTERVAL)

    # Deduplicate
    seen = set()
    unique_ids = []
    for item in all_ids:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique_ids.append(item)

    print(f"\n合計新規: {len(unique_ids)}件")

    if not unique_ids:
        print("新規案件なし。")
        return []

    # Phase 2: Fetch details for candidates
    all_listings = []

    if fetch_details:
        # Fetch detail for all new listings (up to detail_limit)
        to_fetch = unique_ids[:detail_limit]
        print(f"\n詳細取得中 ({len(to_fetch)}件)...")

        for i, item in enumerate(to_fetch, 1):
            print(f"  [{i}/{len(to_fetch)}] {item['title'][:50]}...", end=" ", flush=True)
            detail = scrape_listing_detail(item["id"], session=session)

            if "error" in detail:
                print(f"ERROR: {detail['error']}")
                continue

            # Merge list data + detail data
            desc = detail.get("full_description", "")
            budget_value = detail.get("budget_value", 0)
            proposer_count = detail.get("proposer_count", 0)
            item_track = get_track_for_category(item["category_id"])
            relevance = score_listing(
                detail.get("title", item["title"]),
                desc,
                budget_value,
                proposer_count,
                track_id=item_track,
            )

            listing = {
                "id": item["id"],
                "url": f"{BASE_URL}/requests/{item['id']}",
                "title": detail.get("title") or item["title"],
                "description": desc[:1000],
                "budget": detail.get("budget", ""),
                "budget_value": budget_value,
                "category_id": item["category_id"],
                "category_name": item["category_name"],
                "proposer_count": proposer_count,
                "deadline": detail.get("deadline", ""),
                "delivery_date": detail.get("delivery_date", ""),
                "relevance_score": relevance,
                "track_id": item_track,
            }
            all_listings.append(listing)
            save_listing(listing)

            status = f"OK (score={relevance}, budget={detail.get('budget','?')}, proposals={proposer_count})"
            print(status)

            time.sleep(REQUEST_INTERVAL)
    else:
        # Quick mode: save with minimal data
        for item in unique_ids:
            item_track = get_track_for_category(item["category_id"])
            listing = {
                "id": item["id"],
                "url": f"{BASE_URL}/requests/{item['id']}",
                "title": item["title"],
                "description": "",
                "budget": "",
                "budget_value": 0,
                "category_id": item["category_id"],
                "category_name": item["category_name"],
                "proposer_count": 0,
                "deadline": "",
                "relevance_score": score_listing(item["title"], "", 0, track_id=item_track),
                "track_id": item_track,
            }
            all_listings.append(listing)
            save_listing(listing)

    print(f"\n保存完了: {len(all_listings)}件")
    return all_listings


if __name__ == "__main__":
    listings = run_scraper(max_pages=1, detail_limit=10)

    scored = sorted(listings, key=lambda x: x["relevance_score"], reverse=True)
    print(f"\n--- Top 10 (スコア順) ---")
    for i, l in enumerate(scored[:10], 1):
        print(f"{i}. [{l['relevance_score']:.0f}点] {l['title'][:60]}")
        print(f"   予算: {l['budget'] or '未定'} | 提案数: {l['proposer_count']} | {l['url']}")
