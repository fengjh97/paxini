"""
Coconala Pipeline — SQLite Database for dedup & history
"""
import sqlite3
import json
from config import DB_PATH


def init_db():
    """Create tables if not exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            url TEXT,
            title TEXT,
            description TEXT,
            budget TEXT,
            budget_value INTEGER DEFAULT 0,
            category_id INTEGER,
            category_name TEXT,
            proposer_count INTEGER DEFAULT 0,
            deadline TEXT,
            scraped_at TEXT DEFAULT (datetime('now','localtime')),
            relevance_score REAL DEFAULT 0,
            status TEXT DEFAULT 'new',
            proposal_generated INTEGER DEFAULT 0,
            demo_generated INTEGER DEFAULT 0,
            track_id TEXT DEFAULT 'web',
            raw_data TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id TEXT REFERENCES listings(id),
            proposal_text TEXT,
            pricing_estimate TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    # Migration: add track_id if not present (for existing DBs)
    try:
        c.execute("ALTER TABLE listings ADD COLUMN track_id TEXT DEFAULT 'web'")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()


def listing_exists(listing_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM listings WHERE id = ?", (listing_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def save_listing(listing):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO listings
        (id, url, title, description, budget, budget_value,
         category_id, category_name, proposer_count, deadline,
         relevance_score, track_id, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        listing["id"],
        listing["url"],
        listing["title"],
        listing.get("description", ""),
        listing.get("budget", ""),
        listing.get("budget_value", 0),
        listing.get("category_id", 0),
        listing.get("category_name", ""),
        listing.get("proposer_count", 0),
        listing.get("deadline", ""),
        listing.get("relevance_score", 0),
        listing.get("track_id", "web"),
        json.dumps(listing, ensure_ascii=False),
    ))
    inserted = c.rowcount > 0
    conn.commit()
    conn.close()
    return inserted


def get_new_listings(min_score=0, limit=20, track_id=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if track_id:
        c.execute("""
            SELECT * FROM listings
            WHERE status = 'new' AND relevance_score >= ? AND track_id = ?
            ORDER BY relevance_score DESC, scraped_at DESC
            LIMIT ?
        """, (min_score, track_id, limit))
    else:
        c.execute("""
            SELECT * FROM listings
            WHERE status = 'new' AND relevance_score >= ?
            ORDER BY relevance_score DESC, scraped_at DESC
            LIMIT ?
        """, (min_score, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def mark_listing(listing_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE listings SET status = ? WHERE id = ?", (status, listing_id))
    conn.commit()
    conn.close()


def save_proposal(listing_id, text, pricing):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO proposals (listing_id, proposal_text, pricing_estimate)
        VALUES (?, ?, ?)
    """, (listing_id, text, pricing))
    c.execute("UPDATE listings SET proposal_generated = 1 WHERE id = ?", (listing_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM listings")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM listings WHERE status = 'new'")
    new = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM listings WHERE proposal_generated = 1")
    proposed = c.fetchone()[0]
    conn.close()
    return {"total": total, "new": new, "proposed": proposed}
