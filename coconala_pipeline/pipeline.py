"""
Coconala Pipeline — Full Orchestrator (Multi-Track)
Scrape → Filter → Propose → Demo — all in one run.
Supports 6 tracks: web, documents, graphic, writing, translation, it_dev
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import json
import argparse
from scraper import run_scraper, scrape_listing_detail
from proposal import generate_proposal, save_proposal_file
from demo_builder import build_demo
from db import init_db, get_new_listings, mark_listing, save_proposal, get_stats
from config import CATEGORIES, OUTPUT_DIR, MIN_BUDGET, TRACKS


def run_pipeline(
    max_pages=1,
    min_score=15,
    top_n=5,
    generate_demos=True,
    categories=None,
    track_ids=None,
):
    """Run the full coconala pipeline."""
    init_db()

    # Determine active tracks
    if track_ids:
        active_tracks = {tid: TRACKS[tid] for tid in track_ids if tid in TRACKS}
    else:
        active_tracks = TRACKS

    track_names = ", ".join(t["name"] for t in active_tracks.values())

    print("=" * 60)
    print("  Coconala 自動提案パイプライン (Multi-Track)")
    print(f"  対象トラック: {track_names}")
    print("=" * 60)

    # Step 1: Scrape
    print("\n[STEP 1] 公開依頼をスクレイピング中...")
    all_listings = run_scraper(
        categories=categories,
        max_pages=max_pages,
        fetch_details=True,
        detail_limit=top_n * 3,
        track_ids=track_ids,
    )

    # Step 2: Filter & Rank (per track)
    print(f"\n[STEP 2] フィルタリング (最低スコア: {min_score}点)...")

    top_listings = []
    for tid in active_tracks:
        track_listings = get_new_listings(min_score=min_score, limit=top_n, track_id=tid)
        if track_listings:
            print(f"  [{TRACKS[tid]['name']}] {len(track_listings)}件の候補")
            top_listings.extend(track_listings)

    if not top_listings:
        print("  → 条件に合う新着案件がありませんでした。")
        print("  ヒント: min_score を下げるか、カテゴリを増やしてみてください。")
        stats = get_stats()
        print(f"\n  DB統計: 総案件={stats['total']}, 新規={stats['new']}, 提案済={stats['proposed']}")
        return []

    print(f"  → 合計 {len(top_listings)}件の候補案件を発見!\n")

    # Step 3 & 4: Propose + Demo
    results = []
    for i, listing in enumerate(top_listings, 1):
        track_id = listing.get("track_id", "web")
        track_name = TRACKS.get(track_id, {}).get("name", track_id)

        print(f"{'─' * 50}")
        print(f"[案件 {i}/{len(top_listings)}] {listing['title'][:50]}")
        print(f"  トラック: {track_name}")
        print(f"  URL: {listing['url']}")
        print(f"  予算: {listing['budget'] or '未定'}")
        print(f"  提案数: {listing.get('proposer_count', '?')}")
        print(f"  スコア: {listing['relevance_score']:.0f}点")
        print(f"  カテゴリ: {listing['category_name']}")

        # Generate proposal
        print("  → 提案書を生成中...")
        proposal_data = generate_proposal(listing)
        proposal_path = save_proposal_file(listing, proposal_data)
        save_proposal(
            listing["id"],
            proposal_data["proposal_text"],
            f"{proposal_data['proposed_price']:,}円",
        )
        print(f"  → 提案書保存: {proposal_path}")

        # Generate demo
        demo_result = None
        if generate_demos:
            print("  → デモを生成中...")
            demo_result = build_demo(listing, proposal_data, generate_images=generate_demos)
            print(f"  → デモ保存: {demo_result['html_path']}")
            if demo_result.get("hero_image"):
                print(f"  → AI画像: {demo_result['hero_image']}")

        mark_listing(listing["id"], "proposed")

        results.append({
            "listing": listing,
            "proposal": proposal_data,
            "proposal_path": proposal_path,
            "demo": demo_result,
        })
        print()

    # Summary
    print("=" * 60)
    print("  パイプライン完了!")
    print("=" * 60)
    stats = get_stats()
    print(f"\n  DB統計: 総案件={stats['total']}, 新規={stats['new']}, 提案済={stats['proposed']}")
    print(f"\n  今回の処理: {len(results)}件の提案書+デモを生成")
    print(f"  出力先: {OUTPUT_DIR}")

    # Group by track
    by_track = {}
    for r in results:
        tid = r["proposal"].get("track_id", "web")
        by_track.setdefault(tid, []).append(r)

    print(f"\n  生成ファイル:")
    for tid, items in by_track.items():
        track_name = TRACKS.get(tid, {}).get("name", tid)
        print(f"\n  【{track_name}】")
        for r in items:
            print(f"    📄 {r['proposal_path']}")
            if r.get("demo"):
                print(f"    🌐 {r['demo']['html_path']}")

    print(f"\n  次のステップ:")
    print(f"  1. 各提案書を確認・編集")
    print(f"  2. デモサイト/サンプルをブラウザで確認")
    print(f"  3. ココナラで手動提案送信")

    return results


def show_stats():
    """Show database statistics."""
    init_db()
    stats = get_stats()
    print(f"Coconala DB 統計:")
    print(f"  総案件数: {stats['total']}")
    print(f"  新規（未処理）: {stats['new']}")
    print(f"  提案済: {stats['proposed']}")


def list_tracks():
    """Display all available tracks."""
    print("利用可能なトラック:")
    print()
    for tid, track in TRACKS.items():
        cats = ", ".join(f"{v}" for v in track["categories"].values())
        print(f"  {tid:14s} | {track['name']:16s} | {len(track['categories'])}カテゴリ | {track['delivery_speed']}")
        print(f"  {'':14s} | カテゴリ: {cats[:60]}{'...' if len(cats) > 60 else ''}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coconala 自動提案パイプライン (Multi-Track)")
    parser.add_argument("--pages", type=int, default=1, help="スクレイピングページ数 (default: 1)")
    parser.add_argument("--min-score", type=int, default=15, help="最低スコア (default: 15)")
    parser.add_argument("--top", type=int, default=5, help="トラック毎の上位N件を処理 (default: 5)")
    parser.add_argument("--no-demo", action="store_true", help="デモ生成をスキップ")
    parser.add_argument("--stats", action="store_true", help="DB統計のみ表示")
    parser.add_argument("--track", nargs="+", metavar="TRACK",
                        help="対象トラック (例: web documents graphic)")
    parser.add_argument("--list-tracks", action="store_true", help="全トラック一覧を表示")
    args = parser.parse_args()

    if args.list_tracks:
        list_tracks()
    elif args.stats:
        show_stats()
    else:
        run_pipeline(
            max_pages=args.pages,
            min_score=args.min_score,
            top_n=args.top,
            generate_demos=not args.no_demo,
            track_ids=args.track,
        )
