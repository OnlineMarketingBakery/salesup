#!/usr/bin/env python3
"""Step 6 (pre-publish): write HubSpot page Settings metadata on drafts only.

Applies from salesup-theme/content/draft-page-seo-audit.json:
  - htmlTitle (required to publish)
  - metaDescription
  - language

Does NOT publish. Run after redirects/slugs are ready, immediately before publish.

Safety:
- PATCH /cms/v3/pages/site-pages/{id}/draft only
- Only salesup-theme drafts in state=DRAFT
- Skips pages marked doNotPublish (generic template shells)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "salesup-theme/content/draft-page-seo-audit.json"


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


def main() -> int:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    updated = []
    skipped = []
    errors = []

    for page in audit.get("pages", []):
        if page.get("doNotPublish"):
            skipped.append({"id": page["id"], "name": page["name"], "reason": "doNotPublish"})
            continue

        if not page.get("id"):
            skipped.append({"id": None, "name": page.get("name"), "reason": "HubSpot page not created yet"})
            continue

        pid = page["id"]
        proposed = page.get("proposed") or {}
        title = (proposed.get("htmlTitle") or "").strip()
        if not title:
            errors.append(f"{pid} {page.get('name')}: missing proposed htmlTitle")
            continue

        body: dict = {
            "htmlTitle": title,
            "metaDescription": (proposed.get("metaDescription") or "").strip(),
            "language": proposed.get("language") or "nl",
        }
        featured = proposed.get("featuredImageUrl")
        if featured:
            body["featuredImage"] = featured

        # Verify still a salesup-theme draft before writing
        current = hs_api("GET", f"/cms/v3/pages/site-pages/{pid}/draft")
        if current.get("state") != "DRAFT":
            errors.append(
                f"{pid} {page.get('name')}: refused, state={current.get('state')}"
            )
            continue
        if "salesup-theme" not in (current.get("templatePath") or ""):
            errors.append(
                f"{pid} {page.get('name')}: refused, template={current.get('templatePath')}"
            )
            continue

        result = hs_api(
            "PATCH",
            f"/cms/v3/pages/site-pages/{pid}/draft",
            body,
        )
        if result.get("published"):
            errors.append(f"{pid} {page.get('name')}: unexpected published=true after patch")
            continue

        updated.append(
            {
                "id": pid,
                "name": page.get("name"),
                "htmlTitle": result.get("htmlTitle", title),
                "metaDescriptionChars": len(body.get("metaDescription") or ""),
            }
        )
        print(f"OK {page.get('name')}: {title}", flush=True)

    report = {
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "updatedCount": len(updated),
        "skippedCount": len(skipped),
        "errorCount": len(errors),
    }
    out = ROOT / "salesup-theme/content/draft-page-seo-apply-result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
