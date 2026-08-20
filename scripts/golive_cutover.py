#!/usr/bin/env python3
"""SalesUp go-live cutover. Uses HUBSPOT_ACCESS_TOKEN (Service Key).

Order:
1. Draft+rename published NL pages that occupy target slugs or redirect sources
2. Set go-live slugs + htmlTitle + metaDescription on new-theme drafts
3. Publish those drafts
4. Create 301s

Never publishes the 5 generic template shells. Leaves /blog, French pages,
privacy-policy, algemene-voorwaarden, and /telefonische-prospectie alone.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("HUBSPOT_ACCESS_TOKEN")
API = "https://api.hubapi.com"
REPORT_PATH = ROOT / "salesup-theme/content/golive-cutover-result.json"

KEEP_LIVE_SLUGS = {
    "privacy-policy",
    "algemene-voorwaarden",
    "telefonische-prospectie",
}
KEEP_LIVE_PREFIXES = ("fr-be/", "fr/")
TEST_SLUGS = {
    "bluedragontest",
    "test-animatie",
    "widget-testing",
    "contact-old",
    "over-ons-old",
}

# Old live URLs → new IA (in addition to redirects.json)
EXTRA_REDIRECTS = [
    ("/client-cases", "/cases"),
    ("/client-cases-old", "/cases"),
    ("/jobs", "/werken-bij"),
    ("/attract-leads", "/marketing"),
    ("/boost-sales", "/sales-contact-center"),
    ("/keep-clients", "/after-sales"),
    ("/online-marketing", "/marketing"),
    ("/callcenter-b2b", "/sales-contact-center"),
    ("/face2face", "/face2face-sales"),
    ("/website-laten-maken", "/website"),
    ("/sales-traingen", "/training"),
    ("/ai-prospectie", "/ai-aanpak"),
    ("/inbound-customer-service", "/after-sales"),
    ("/klanttevredenheids-campagnes", "/after-sales"),
    ("/meer-klanten-terugwinnen", "/after-sales"),
    ("/cross-en-upselling", "/after-sales"),
    ("/axians", "/cases/axians"),
    ("/cesano", "/cases/cesano"),
    ("/hivolta", "/cases/hivolta"),
    ("/ichoosr", "/cases/ichoosr"),
    ("/immo-van-middelem", "/cases/immo-van-middelem"),
    ("/q8oils", "/cases/q8oils"),
    ("/sobelhor", "/cases/sobelhor"),
    ("/unizo", "/cases/unizo"),
    ("/meer-afspraken-voor-vm-building-services", "/cases/vm-building"),
    ("/meer-verkopen-voor-eurocircuits", "/cases/eurocircuits"),
    ("/jaguar-land-rover-benelux-kiest-salesup-voor-effectieve-leads", "/cases/jaguar-land-rover"),
    ("/salesup-overstijgt-de-verwachting-spm", "/cases/spm"),
    ("/salesup-strategische-telefonische-prospectie-partner-van-alindus", "/cases/alindus"),
    ("/salesup-versterkt-de-wereldwijde-aanwezigheid-van-geodis", "/cases/geodis"),
    ("/telefonische-prospectie-voor-ev-shop", "/cases/ev-shop"),
    ("/telefonische-prospectie-voor-ikaros-solar", "/cases/ikaros-solar"),
    ("/telefonische-prospectie-voor-upgrade", "/cases/upgrade-estate"),
    ("/duurzame-samenwerking-tussen-messer-group-en-salesup", "/cases/messer-group"),
    ("/van-heurck-strategische-marktbevraging", "/cases/van-heurck"),
]


def req(method: str, path: str, body=None, retries: int = 4):
    data = None if body is None else json.dumps(body).encode()
    last = None
    for attempt in range(retries):
        r = urllib.request.Request(
            API + path,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(r, timeout=60) as resp:
                raw = resp.read().decode()
                return resp.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {"raw": raw[:800]}
            last = (e.code, payload)
            if e.code in (429, 502, 503, 504) and attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            return last
        except Exception as e:
            last = (0, {"message": str(e)})
            time.sleep(1)
    return last


def fetch_all_pages():
    pages = []
    after = None
    while True:
        url = "/cms/v3/pages/site-pages?limit=100&archived=false"
        if after:
            url += f"&after={after}"
        status, data = req("GET", url)
        if status != 200:
            raise RuntimeError(f"list pages failed {status} {data}")
        pages.extend(data.get("results") or [])
        after = ((data.get("paging") or {}).get("next") or {}).get("after")
        if not after:
            break
    return pages


def fetch_all_redirects():
    rows = []
    after = None
    while True:
        url = "/cms/v3/url-redirects?limit=100"
        if after:
            url += f"&after={after}"
        status, data = req("GET", url)
        if status != 200:
            raise RuntimeError(f"list redirects failed {status} {data}")
        rows.extend(data.get("results") or [])
        after = ((data.get("paging") or {}).get("next") or {}).get("after")
        if not after:
            break
    return rows


def page_state(p):
    return p.get("currentState") or p.get("state")


def should_keep_live(slug: str) -> bool:
    slug = slug or ""
    if slug in KEEP_LIVE_SLUGS or slug in TEST_SLUGS:
        return True
    return any(slug.startswith(p) for p in KEEP_LIVE_PREFIXES)


def legacy_slug(slug: str) -> str:
    if not slug:
        return "legacy-2026-home"
    safe = slug.strip("/").replace("/", "-")
    return f"legacy-2026-{safe}"


def main() -> int:
    if not TOKEN:
        raise SystemExit("HUBSPOT_ACCESS_TOKEN is not set")

    mapping = json.loads((ROOT / "salesup-theme/content/slug-map-step1.json").read_text())
    audit = json.loads((ROOT / "salesup-theme/content/draft-page-seo-audit.json").read_text())
    file_redirects = json.loads((ROOT / "salesup-theme/content/redirects.json").read_text())

    audit_by_id = {str(p["id"]): p for p in audit["pages"] if p.get("id")}
    map_pages = [p for p in mapping["pages"] if p.get("id")]
    do_not_publish = {
        str(p["id"])
        for p in map_pages
        if p.get("go_live_slug") is None
    }
    do_not_publish |= {
        str(p["id"])
        for p in audit["pages"]
        if p.get("doNotPublish") and p.get("id")
    }

    report = {
        "drafted_live": [],
        "slug_meta": [],
        "published": [],
        "redirects_created": [],
        "skipped": [],
        "errors": [],
    }

    print("Fetching pages…", flush=True)
    pages = fetch_all_pages()
    by_id = {str(p["id"]): p for p in pages}

    target_slugs = set()
    for spec in map_pages:
        if str(spec["id"]) in do_not_publish:
            continue
        target_slugs.add(spec.get("go_live_slug") if spec.get("go_live_slug") is not None else spec["draft_slug_now"])

    # Phase 1: free live slugs
    print("Phase 1: draft+rename live NL pages that block go-live…", flush=True)
    for p in pages:
        pid = str(p["id"])
        slug = p.get("slug") or ""
        tmpl = p.get("templatePath") or ""
        if "salesup-theme" in tmpl:
            continue
        if page_state(p) not in ("PUBLISHED", "PUBLISHED_OR_SCHEDULED"):
            continue
        if should_keep_live(slug):
            report["skipped"].append({"id": pid, "slug": slug, "reason": "keep-live"})
            continue
        occupies_target = slug in target_slugs
        # Also retire NL case/service pages so 301s can own those URLs
        lang = (p.get("language") or "").lower()
        is_fr = slug.startswith("fr-be/") or slug.startswith("fr/") or lang in ("fr-be", "fr")
        if is_fr:
            report["skipped"].append({"id": pid, "slug": slug, "reason": "french-keep"})
            continue
        if not occupies_target and lang not in ("nl-be", "nl", ""):
            continue
        if not occupies_target and slug in TEST_SLUGS:
            continue
        # Draft all remaining published NL pages so old URLs can 301
        new_slug = legacy_slug(slug)
        body = {"state": "DRAFT", "slug": new_slug}
        status, result = req("PATCH", f"/cms/v3/pages/site-pages/{pid}", body)
        entry = {
            "id": pid,
            "name": p.get("name"),
            "from": slug,
            "to": new_slug,
            "http": status,
            "state": (result or {}).get("currentState") or (result or {}).get("state"),
        }
        if status not in (200, 204) or entry["state"] not in ("DRAFT", None):
            # slug clash: try a suffix
            if status not in (200, 204):
                body["slug"] = new_slug + "-retired"
                status, result = req("PATCH", f"/cms/v3/pages/site-pages/{pid}", body)
                entry["to"] = body["slug"]
                entry["http"] = status
                entry["state"] = (result or {}).get("currentState") or (result or {}).get("state")
                entry["retry"] = (result or {}).get("message") or (result or {}).get("category")
        if status in (200, 204) and (entry["state"] in ("DRAFT", None) or (result or {}).get("slug")):
            report["drafted_live"].append(entry)
            print(f"  DRAFT {p.get('name')}: /{slug} -> /{entry['to']}", flush=True)
        else:
            entry["error"] = (result or {}).get("message") or (result or {}).get("category") or result
            report["errors"].append({"phase": "draft-live", **entry})
            print(f"  ERROR drafting {p.get('name')} /{slug}: {entry.get('error')}", flush=True)
        time.sleep(0.15)

    # Refresh
    pages = fetch_all_pages()
    by_id = {str(p["id"]): p for p in pages}

    # Phase 2: slugs + SEO on new drafts
    print("Phase 2: slugs + titles/meta on new-theme drafts…", flush=True)
    for spec in map_pages:
        pid = str(spec["id"])
        if pid in do_not_publish:
            report["skipped"].append({"id": pid, "name": spec["name"], "reason": "doNotPublish"})
            continue
        current = by_id.get(pid)
        if not current:
            report["errors"].append({"phase": "slug-meta", "id": pid, "name": spec["name"], "error": "not found"})
            continue
        if "salesup-theme" not in (current.get("templatePath") or ""):
            report["errors"].append({"phase": "slug-meta", "id": pid, "name": spec["name"], "error": "not salesup-theme"})
            continue
        if page_state(current) not in ("DRAFT",):
            report["errors"].append({"phase": "slug-meta", "id": pid, "name": spec["name"], "error": f"state={page_state(current)}"})
            continue

        target = spec.get("go_live_slug")
        if target is None:
            continue
        seo = (audit_by_id.get(pid) or {}).get("proposed") or {}
        title = (seo.get("htmlTitle") or "").strip()
        if not title:
            report["errors"].append({"phase": "slug-meta", "id": pid, "name": spec["name"], "error": "missing htmlTitle"})
            continue
        body = {
            "slug": target,
            "htmlTitle": title,
            "metaDescription": (seo.get("metaDescription") or "").strip(),
            "language": seo.get("language") or "nl",
        }
        status, result = req("PATCH", f"/cms/v3/pages/site-pages/{pid}/draft", body)
        entry = {
            "id": pid,
            "name": spec["name"],
            "slug": (result or {}).get("slug", target),
            "htmlTitle": (result or {}).get("htmlTitle", title),
            "http": status,
            "state": (result or {}).get("state") or (result or {}).get("currentState"),
        }
        if status in (200, 204):
            report["slug_meta"].append(entry)
            print(f"  META {spec['name']}: /{target} | {title}", flush=True)
        else:
            entry["error"] = (result or {}).get("message") or (result or {}).get("category") or result
            report["errors"].append({"phase": "slug-meta", **entry})
            print(f"  ERROR meta {spec['name']}: {entry.get('error')}", flush=True)
        time.sleep(0.15)

    # Phase 3: publish
    print("Phase 3: publish new-theme drafts…", flush=True)
    pages = fetch_all_pages()
    by_id = {str(p["id"]): p for p in pages}
    for spec in map_pages:
        pid = str(spec["id"])
        if pid in do_not_publish:
            continue
        current = by_id.get(pid)
        if not current:
            report["errors"].append({"phase": "publish", "id": pid, "name": spec["name"], "error": "not found"})
            continue
        if page_state(current) in ("PUBLISHED", "PUBLISHED_OR_SCHEDULED"):
            report["skipped"].append({"id": pid, "name": spec["name"], "reason": "already-published"})
            continue
        # Confirm title present
        draft_status, draft = req("GET", f"/cms/v3/pages/site-pages/{pid}/draft")
        if not (draft or {}).get("htmlTitle"):
            report["errors"].append({"phase": "publish", "id": pid, "name": spec["name"], "error": "empty htmlTitle, refused"})
            continue
        status, result = req("PATCH", f"/cms/v3/pages/site-pages/{pid}", {"state": "PUBLISHED"})
        st = (result or {}).get("currentState") or (result or {}).get("state")
        entry = {
            "id": pid,
            "name": spec["name"],
            "http": status,
            "state": st,
            "slug": (result or {}).get("slug") or current.get("slug"),
            "url": (result or {}).get("url"),
        }
        if status in (200, 204) and st == "PUBLISHED":
            report["published"].append(entry)
            print(f"  LIVE {spec['name']}: /{entry['slug']}", flush=True)
        else:
            entry["error"] = (result or {}).get("message") or (result or {}).get("category") or result
            report["errors"].append({"phase": "publish", **entry})
            print(f"  ERROR publish {spec['name']}: {entry.get('error')}", flush=True)
        time.sleep(0.2)

    # Phase 4: redirects
    print("Phase 4: create 301s…", flush=True)
    existing = fetch_all_redirects()
    existing_from = {(r.get("routePrefix") or "").rstrip("/") for r in existing}

    wanted = []
    for row in file_redirects:
        src = row.get("from") or ""
        dest = row.get("to") or ""
        if src and dest:
            wanted.append((src, dest))
    wanted.extend(EXTRA_REDIRECTS)

    # Dedup, skip identity, skip telefonische-prospectie service page
    seen = set()
    for src, dest in wanted:
        src_n = "/" + src.lstrip("/")
        dest_n = dest if dest.startswith("/") or dest == "/" else "/" + dest
        if src_n.rstrip("/") == "/telefonische-prospectie":
            continue
        if src_n.rstrip("/") == dest_n.rstrip("/"):
            continue
        key = src_n.rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        if key in existing_from or src_n in existing_from:
            report["skipped"].append({"redirect": src_n, "reason": "already-exists"})
            continue
        status, result = req(
            "POST",
            "/cms/v3/url-redirects",
            {
                "routePrefix": src_n,
                "destination": dest_n,
                "redirectStyle": 301,
                "isMatchFullUrl": False,
                "isMatchQueryString": False,
                "isOnlyAfterNotFound": False,
                "isPattern": False,
                "isProtocolAgnostic": True,
                "isTrailingSlashOptional": True,
                "precedence": 0,
            },
        )
        entry = {
            "from": src_n,
            "to": dest_n,
            "http": status,
            "id": (result or {}).get("id"),
        }
        if status in (200, 201):
            report["redirects_created"].append(entry)
            existing_from.add(key)
            print(f"  301 {src_n} -> {dest_n}", flush=True)
        else:
            entry["error"] = (result or {}).get("message") or (result or {}).get("category") or result
            report["errors"].append({"phase": "redirect", **entry})
            print(f"  ERROR redirect {src_n}: {entry.get('error')}", flush=True)
        time.sleep(0.1)

    report["counts"] = {
        "drafted_live": len(report["drafted_live"]),
        "slug_meta": len(report["slug_meta"]),
        "published": len(report["published"]),
        "redirects_created": len(report["redirects_created"]),
        "skipped": len(report["skipped"]),
        "errors": len(report["errors"]),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], indent=2), flush=True)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
