"""
collection_tiers.py — Foreign Intelligence Support Platform (FISP)

Two collection tiers with separate storage, per the platform's minimization
procedures:

  Tier 1 (tier1_osint)    — open-source / commercially licensed material.
                            No individualized authorization required.
  Tier 2 (tier2_targeted) — collection against named selectors under a
                            court order. Each row carries its authorization id.

The tiers are held in separate Postgres instances with separate credentials.
Analyst cross-referencing is done application-side in `crossref()`.
"""

import os
import psycopg2

TIER1_DSN = os.environ["FISP_TIER1_DSN"]  # osint-db.internal
TIER2_DSN = os.environ["FISP_TIER2_DSN"]  # targeted-db.internal (restricted)

VENDOR_API = "https://osint-vendor.example/api/v3/lookup"


def tier1_lookup(selector: str) -> list[dict]:
    """Per-request call to the OSINT vendor. Slow: ~800ms p50, ~4s p99."""
    conn = psycopg2.connect(TIER1_DSN)
    cur = conn.cursor()
    cur.execute(
        "SELECT selector, observed_at, source, payload FROM tier1_osint "
        "WHERE selector = %s ORDER BY observed_at DESC LIMIT 500",
        (selector,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(("selector", "observed_at", "source", "payload"), r)) for r in rows]


def tier2_lookup(selector: str, analyst_id: str) -> list[dict]:
    """Court-authorized holdings. Every read is audited against the order id."""
    conn = psycopg2.connect(TIER2_DSN)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tier2_access_log (analyst_id, selector, accessed_at) "
        "VALUES (%s, %s, NOW())",
        (analyst_id, selector),
    )
    cur.execute(
        "SELECT selector, observed_at, authorization_id, payload FROM tier2_targeted "
        "WHERE selector = %s AND authorization_id IN ("
        "  SELECT id FROM authorizations WHERE selector = %s AND expires_at > NOW()"
        ")",
        (selector, selector),
    )
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return [dict(zip(("selector", "observed_at", "authorization_id", "payload"), r)) for r in rows]


def crossref(selector: str, analyst_id: str) -> dict:
    """
    Application-side join. Two round trips to two instances; ~40s p99 under load,
    which is the current analyst complaint.
    """
    return {
        "selector": selector,
        "tier1": tier1_lookup(selector),
        "tier2": tier2_lookup(selector, analyst_id),
    }
