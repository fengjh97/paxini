"""
Coconala Pipeline — Public Request Scraper (v2)

Two-phase approach:
  Phase 1: List page → extract request IDs + titles from links
  Phase 2: Detail page → extract full info via CSS selectors + meta tags
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from config import (
    REQUESTS_URL, BASE_URL, CATEGORIES, USER_AGENT,
    REQUEST_INTERVAL, POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS, MIN_BUDGET,
)
from db import init_db, listing_exists, save_listing


def parse_budget(budget_str):
    """Extract numeric budget value from string like '10,000円〜20,000円' or '50000'."""
    if not budget_str:
        return 0
    clean = budget_str.replace(',', '').replace('，', '')
    nums = re.findall(r'\d+', clean)
    if nums:
        # Return the first (minimum) number
        return int(nums[0])
    return 0


def score_listing(title, description, budget_value, proposer_count=0):
    """Score relevance 0-100 based on keywords, budget, and competition."""
    text = f"{title} {description}".lower()
    score = 0

    # Positive keyword matches
    for kw in POSITIVE_KEYWORDS:
        if kw.lower() in text:
            score += 8

    # Negative keyword penalty
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text:
            score -= 15

    # Budget bonus
    if budget_value >= 50000:
        score += 20
    elif budget_value >= 20000:
        score += 10
    elif budget_value >= MIN_BUDGET:
        score += 5
    elif budget_value > 0 and budget_value < MIN_BUDGET:
        score -= 10

    # Competition penalty (too many proposers = harder to win)
    if proposer_count > 30:
        score -= 10
    elif proposer_count > 15:
        score -= 5
    elif proposer_count == 0:
        score += 5  # No competition yet!

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

def run_scraper(categories=None, max_pages=2, fetch_details=True, detail_limit=10):
    """Main scraper entry point.

    Args:
        categories: dict of {id: name} to scrape
        max_pages: pages per category on list view
        fetch_details: whether to fetch detail pages for top candidates
        detail_limit: max number of detail pages to fetch
    """
    init_db()

    if categories is None:
        categories = CATEGORIES

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
            relevance = score_listing(
                detail.get("title", item["title"]),
                desc,
                budget_value,
                proposer_count,
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
            }
            all_listings.append(listing)
            save_listing(listing)

            status = f"OK (score={relevance}, budget={detail.get('budget','?')}, proposals={proposer_count})"
            print(status)

            time.sleep(REQUEST_INTERVAL)
    else:
        # Quick mode: save with minimal data
        for item in unique_ids:
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
                "relevance_score": score_listing(item["title"], "", 0),
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
