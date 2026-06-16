#!/usr/bin/env python3
"""
Build LinkedIn warm-path people-search URLs from a list of resolved company IDs.

Why this exists: the search URL format is fiddly (JSON-array params, URL
encoding, degree codes) and we rebuild it on every run. Doing it in one place
keeps it correct and lets the skill focus on the hard part (resolving names to
company IDs) instead of re-deriving URL syntax each time.

The mechanic (validated against a real logged-in LinkedIn account):
  - currentCompany=["id","id",...]  stacks multiple target companies in ONE search
  - network=["F","S"]               filters to 1st (F) and 2nd (S) degree only
  - keywords=role OR role OR role   carries the buyer-role terms

Free LinkedIn only. We batch companies because the basic search caps how many
companies one URL reliably applies (default 10 per link); a long target list
becomes a few links rather than one.

Usage:
  python build_search_urls.py --ids 10266768 11835624 --roles "operations,supply chain,founder"
  python build_search_urls.py --ids-file ids.txt --roles "head of talent,recruiter,founder" --degrees FS --batch 10
"""
import argparse
import json
import urllib.parse


BASE = "https://www.linkedin.com/search/results/people/"
DEGREE_CODE = {"1": "F", "F": "F", "2": "S", "S": "S", "3": "O", "O": "O"}


def build_url(company_ids, role_terms, degrees):
    company_json = json.dumps([str(c) for c in company_ids], separators=(",", ":"))
    network_json = json.dumps(list(degrees), separators=(",", ":"))
    params = {
        "currentCompany": company_json,
        "network": network_json,
        "origin": "FACETED_SEARCH",
    }
    if role_terms:
        # Quote multi-word roles so LinkedIn treats them as phrases, OR-joined.
        terms = []
        for t in role_terms:
            t = t.strip()
            if not t:
                continue
            terms.append(f'"{t}"' if " " in t else t)
        if terms:
            params["keywords"] = " OR ".join(terms)
    return BASE + "?" + urllib.parse.urlencode(params, safe="", quote_via=urllib.parse.quote)


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=[], help="company IDs, space separated")
    ap.add_argument("--ids-file", help="file with one company ID per line")
    ap.add_argument("--roles", default="", help="comma-separated role terms for keywords")
    ap.add_argument("--degrees", default="FS", help="connection degrees, e.g. FS = 1st+2nd, F = 1st only")
    ap.add_argument("--batch", type=int, default=10, help="max companies per search link")
    args = ap.parse_args()

    ids = list(args.ids)
    if args.ids_file:
        with open(args.ids_file) as f:
            ids += [ln.strip() for ln in f if ln.strip()]
    ids = [i for i in ids if i]
    if not ids:
        ap.error("no company IDs provided")

    degrees = [DEGREE_CODE[d] for d in args.degrees.upper() if d in DEGREE_CODE]
    if not degrees:
        degrees = ["F", "S"]

    role_terms = [r for r in args.roles.split(",")] if args.roles else []

    batches = list(chunk(ids, max(1, args.batch)))
    for n, batch in enumerate(batches, 1):
        url = build_url(batch, role_terms, degrees)
        label = f"Link {n} of {len(batches)} ({len(batch)} companies)" if len(batches) > 1 else "Search link"
        print(f"{label}:\n{url}\n")


if __name__ == "__main__":
    main()
