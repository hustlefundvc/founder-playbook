# LinkedIn mechanics

Everything here was validated live against a real logged-in LinkedIn account in 2026. Read this when you need the exact method to turn a company name into a LinkedIn company ID, or to understand the search URL the skill produces.

## The search URL (what we hand the user)

```
https://www.linkedin.com/search/results/people/?currentCompany=["10266768","11835624"]&network=["F","S"]&keywords=operations OR "supply chain" OR founder
```

- `currentCompany` takes a JSON array of numeric company IDs. Multiple targets stack into one search. This is the whole reason the tool saves time: no clicking company by company.
- `network` filters to connection degree. `F` = 1st, `S` = 2nd, `O` = 3rd+. We use `["F","S"]` so the user sees only warm paths.
- `keywords` carries the buyer-role terms, OR-joined. Quote multi-word phrases.

Don't hand-build this. Use `scripts/build_search_urls.py`, which encodes it correctly and batches a long list across links.

## Resolving a name to a company ID (the hard part)

You cannot guess the URL slug. cocojune's handle is `cocojuneproducts`, not `cocojune`. So resolve in two steps, both run in the user's logged-in browser via the Chrome tools.

### Step 1: find the right company entity

Navigate to a company search for the name:

```
https://www.linkedin.com/search/results/companies/?keywords=<NAME>
```

Keep the query to just the brand name. Adding extra words ("cocojune yogurt") can return zero results. Then read the first real company result's slug:

```javascript
(() => {
  const a = [...document.querySelectorAll('a[href*="/company/"]')].map(x => x.href);
  const slug = (a[0] || "").match(/company\/([^\/?]+)/);
  return JSON.stringify({ firstCompanyLink: a[0] || null, slug: slug && slug[1] });
})()
```

If there are several plausible matches (same name, different company), this is a disambiguation point. Prefer the result whose industry, size, and location match the user's intent. When unsure, show the user the top 2-3 and let them pick rather than guessing wrong, since a wrong ID quietly poisons the whole search.

### Step 2: pull the numeric ID off the company page

Navigate to `https://www.linkedin.com/company/<slug>/`, wait for it to load, then extract the `fsd_company` ID tied to the matching `universalName`:

```javascript
(() => {
  const html = document.documentElement.innerHTML;
  const slug = "<SLUG>";
  const idx = html.indexOf(`"universalName":"${slug}"`);
  let id = null;
  if (idx >= 0) {
    const around = html.slice(idx - 800, idx + 100);
    const m = around.match(/urn:li:fsd_company:(\d+)/);
    id = m && m[1];
  }
  return JSON.stringify({ title: document.title, id });
})()
```

Anchoring on `universalName` matters. A company page also lists "similar companies," so a naive grab of the first `fsd_company:` ID can return a competitor, not the target.

### Why not the old typeahead API

The legacy `voyager/api/typeahead/hitsV2` endpoint now returns 404. Don't rely on it. The company-search-then-page-DOM path above is what currently works.

## Batching and limits

Free LinkedIn (no Sales Navigator in v1):

- The UI lets you click up to ~10 companies into the current-company filter. The URL sometimes accepts more, but treat 10 per link as the safe default and split longer lists.
- LinkedIn enforces a monthly commercial-use limit on searches. Heavy runs can hit it. If results suddenly stop, that's the likely cause, not a bug in the skill.

## Degree codes quick reference

- `F` = 1st degree (direct connection)
- `S` = 2nd degree (one mutual away, the prime intro target)
- `O` = 3rd+ degree

We default to `["F","S"]`. Drop to `["S"]` if the user only wants intros to people they don't already know directly.

## Degree is relative to the viewer (why broadcast works)

LinkedIn computes connection degree against whoever is logged in. The same search URL with `network=["F","S"]` shows each viewer THEIR own 1st and 2nd-degree connections at the target companies. This is the engine behind Mode 2: build one link, share it widely, and every recipient who opens it sees their own warm paths. You are not handing them your network, you are letting their own LinkedIn match their network against your target list.

## Scraping results for the own-network map (Mode 1)

Run on the user's own logged-in account. Each search result is rendered as one big anchor whose innerText holds the whole card, with a bullet separating name and degree. This scraper pulls name, degree, headline, and the mutual-connections line:

```javascript
(()=>{
 const seen=new Set(), out=[];
 document.querySelectorAll('a[href*="/in/"]').forEach(a=>{
   const t=a.innerText||"";
   const d=t.match(/•\s*(1st|2nd|3rd\+?)/);   // bullet + degree
   if(!d) return;
   const u=a.href.split("?")[0];
   if(seen.has(u)) return; seen.add(u);
   const L=t.split("\n").map(s=>s.trim()).filter(Boolean);
   const di=L.findIndex(s=>/•\s*(1st|2nd|3rd)/.test(s));
   out.push({name:L[0], deg:d[1], headline:(L[di+1]||"").slice(0,80),
             mut:(L.find(s=>/mutual connection/.test(s))||"")});
 });
 return JSON.stringify(out);
})()
```

Notes:
- Run one search per company (`currentCompany=["id"]`, `network=["F","S"]`) so each scraped person is cleanly attributed to a known company. Wait ~3s after navigation before scraping.
- The `mut` string looks like `"Katie Dunn, Angelika O'Reilly and 7 other mutual connections"`. The named people are the connectors LinkedIn exposes; the `+N` is hidden depth. Parse both: named connectors drive the connector pivot; the total count (named + hidden) is the triangulation signal for who's most worth a personal ask.
- Empty results for a company usually means no warm 1st/2nd-degree path in that account, not a bug. After many searches LinkedIn may throttle (monthly commercial-use limit); if results suddenly go empty across the board, that's the cause.

`scripts/build_connector_sheet.py` takes the scraped `{company: [people]}` JSON and builds the workbook (connector pivot, mutual counts, Email 1).
