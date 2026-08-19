#!/usr/bin/env python3
"""Assign salesup-theme blog templates on the Dutch blog.

Requires HUBSPOT_ACCESS_TOKEN with blog-settings read/write (content scope).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.hubapi.com"
BLOG_ID = "44736920565"
ITEM_TEMPLATE = "salesup-theme/templates/blog-post.html"
LISTING_TEMPLATE = "salesup-theme/templates/blog-index.html"


def req(method: str, path: str, token: str, body: dict | None = None) -> tuple[int, dict | None]:
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw[:500]}
        return e.code, payload


def load_token() -> str | None:
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if token:
        return token
    token_file = os.environ.get("HUBSPOT_TOKEN_FILE")
    if not token_file:
        return None
    import re
    from pathlib import Path

    text = Path(token_file).read_text(encoding="utf-8")
    match = re.search(r"TOKEN='(pat-eu1-[a-f0-9-]+)'", text)
    return match.group(1) if match else None


def main() -> int:
    token = load_token()
    if not token:
        print("HUBSPOT_ACCESS_TOKEN is not set", file=sys.stderr)
        return 1

    status, blog = req("GET", f"/content/api/v2/blogs/{BLOG_ID}", token)
    if status != 200 or not blog:
        print(f"Failed to fetch blog {BLOG_ID}: HTTP {status}", file=sys.stderr)
        print(json.dumps(blog, indent=2)[:1000], file=sys.stderr)
        return 1

    print("Current item_template_path:", blog.get("item_template_path"))
    print("Current listing_template_path:", blog.get("listing_template_path"))

    body = dict(blog)
    body["item_template_path"] = ITEM_TEMPLATE
    body["listing_template_path"] = LISTING_TEMPLATE
    for key in ("id", "portal_id", "created", "updated", "created_date_time", "updated_date_time"):
        body.pop(key, None)

    status, updated = req("PUT", f"/content/api/v2/blogs/{BLOG_ID}", token, body)
    if status != 200 or not updated:
        print(f"Failed to update blog template: HTTP {status}", file=sys.stderr)
        print(json.dumps(updated, indent=2)[:1000], file=sys.stderr)
        return 1

    print("Updated item_template_path:", updated.get("item_template_path"))
    print("Updated listing_template_path:", updated.get("listing_template_path"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
