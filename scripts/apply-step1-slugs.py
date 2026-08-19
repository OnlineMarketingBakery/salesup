#!/usr/bin/env python3
"""Assign Step 1 slugs on unpublished salesup-theme drafts only.

Safety:
- PATCH /cms/v3/pages/site-pages/{id}/draft only (never the live object)
- Refuse unless HubSpot still reports state=DRAFT and templatePath contains salesup-theme
- Refuse if the target slug is already used by a published page
- Never send state=PUBLISHED
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "salesup-theme/content/slug-map-step1.json"


def hs_api(method: str, endpoint: str, data: dict | None = None) -> dict:
    cmd = ["npx", "hs", "api", endpoint, "-X", method, "--json", "-a", "salesUp"]
    if data is not None:
        cmd.extend(["--data", json.dumps(data)])
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    raw = proc.stdout + proc.stderr
    start = raw.find("{")
    if start < 0:
        raise RuntimeError(f"No JSON from hs api {method} {endpoint}:\n{raw[-2000:]}")
    payload = json.loads(raw[start:])
    if payload.get("status") == "error" or payload.get("category"):
        raise RuntimeError(json.dumps(payload, indent=2)[:2000])
    return payload


def fetch_all_pages() -> list[dict]:
    pages: list[dict] = []
    after = None
    while True:
        endpoint = "/cms/v3/pages/site-pages?limit=100&archived=false"
        if after:
            endpoint += f"&after={after}"
        data = hs_api("GET", endpoint)
        pages.extend(data.get("results", []))
        after = ((data.get("paging") or {}).get("next") or {}).get("after")
        if not after:
            break
    return pages


def main() -> int:
    mapping = json.loads(MAP_PATH.read_text())
    wanted = {p["id"]: p for p in mapping["pages"] if p.get("id")}
    pages = fetch_all_pages()
    by_id = {str(p["id"]): p for p in pages}

    published_slugs = {
        p["slug"]
        for p in pages
        if p.get("state") == "PUBLISHED_OR_SCHEDULED"
    }

    errors = []
    updated = []
    skipped = []

    for page_id, spec in wanted.items():
        current = by_id.get(page_id)
        if not current:
            errors.append(f"{page_id} {spec['name']}: not found")
            continue
        if current.get("state") != "DRAFT":
            errors.append(
                f"{page_id} {spec['name']}: refused, state={current.get('state')}"
            )
            continue
        if "salesup-theme" not in (current.get("templatePath") or ""):
            errors.append(
                f"{page_id} {spec['name']}: refused, template={current.get('templatePath')}"
            )
            continue
        target = spec["draft_slug_now"]
        if target in published_slugs:
            errors.append(
                f"{page_id} {spec['name']}: refused, {target!r} is a live slug"
            )
            continue
        if current.get("slug") == target:
            skipped.append({"id": page_id, "name": spec["name"], "slug": target})
            continue
        result = hs_api(
            "PATCH",
            f"/cms/v3/pages/site-pages/{page_id}/draft",
            {"slug": target},
        )
        if result.get("state") not in (None, "DRAFT") and result.get("published") is True:
            errors.append(f"{page_id} {spec['name']}: unexpected publish after patch")
            continue
        updated.append(
            {
                "id": page_id,
                "name": spec["name"],
                "from": current.get("slug"),
                "to": result.get("slug", target),
                "state": result.get("state", current.get("state")),
            }
        )
        print(f"OK {spec['name']}: {current.get('slug')} -> {target}", flush=True)

    report = {
        "updated": updated,
        "already_ok": skipped,
        "errors": errors,
        "updated_count": len(updated),
        "error_count": len(errors),
    }
    out = ROOT / "salesup-theme/content/slug-map-step1-result.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({"updated": len(updated), "skipped": len(skipped), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
