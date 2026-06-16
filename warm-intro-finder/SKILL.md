---
name: warm-intro-finder
version: 1.0.0
description: >
  Turn "I want intros to companies or funds like X" into shareable warm-intro
  assets. Two modes. (1) Broadcast: build a ranked target list, resolve each to a
  LinkedIn company, and produce ONE search link plus a short message you share
  widely; anyone who opens it sees their OWN 1st/2nd-degree connections to
  the targets (degree is relative to the viewer), crowdsourcing intros across a
  whole network. (2) Own-network map: scrape your own warm connections, rank
  connectors by reach and mutual count, and draft the connector ask. Self-serve
  for founders, job seekers, and anyone working a network. Use ANY TIME someone wants warm intros, to map a network
  onto target companies/funds, or a shareable intro link. Trigger
  on "find warm intros to [funds/brands]", "who do I know at these companies",
  "make me an intro list to share", "I want intros to seed funds", "saved search
  for intros", or any fundraise,
  job-search, or BD outreach where the bottleneck is finding who can open the
  door. Lean toward triggering.
---

# Warm intro finder

Help the person turn a fuzzy "who I want to meet" into concrete warm-intro assets:
a target list, the LinkedIn searches that surface who can open each door, and the
message that asks for the intro. The person might be a founder raising or selling,
a job seeker, or anyone trying to reach a set of people. Talk to whoever is in front
of you, warm and plain.

The exact LinkedIn URL format, the company-ID resolver, and the results scraper are
in `references/linkedin-mechanics.md`. Read that reference before resolving IDs or
scraping.

## The mental model: minimize intro leakage

Warm intros are the highest-converting path to almost anyone, but every extra step
between "I want to meet these targets" and "a mutual said yes" loses intros. Think
of it like revenue leakage. Compress the steps so the process converts and so it's
easy for whoever helps.

## The one insight that drives everything

On LinkedIn, connection degree is always computed relative to whoever is logged in.
A search filtered to `network=["F","S"]` (1st + 2nd degree) shows *the viewer's* own
connections, not the person who built the link. That single fact is why this skill
has two very different modes, and why the broadcast mode scales so well.

## The two modes

### Mode 2 — Broadcast (default, highest leverage)

The user shares ONE search link plus a short message with their whole network (10,
100, 1,000+ people). Each recipient opens it on their own logged-in LinkedIn and
sees the people *they* know at the target companies. You are crowdsourcing the
network-matching to every recipient. Reach isn't capped by one person's network,
it's the union of everyone who opens the link.

This is also the simplest to build: no scraping. It's the target list, the stacked
search link, and a good broadcast blurb.

### Mode 1 — Own-network map (deep, for working your own contacts)

The user runs the searches on their own account, and you scrape the results to build
a spreadsheet keyed by connector: who they know at each target, which of their
contacts can open each door, and how many total mutuals exist per target (the
triangulation signal for who's most worth a personal ask). Heavier, because it
scrapes, and it's bounded by the user's own network.

Default to Mode 2. Offer Mode 1 when the user wants to work their own contacts
deliberately, or asks "who specifically do I know there." Many users want both: a
link to broadcast AND a sheet for their own network.

## Scope of v1

Free LinkedIn only, no Sales Navigator. For Mode 1 (scraping), assume the user is
signed into LinkedIn and you can drive their browser via the Chrome tools. Mode 2
needs no special access beyond resolving company IDs.

## The hard line you must respect

You cannot see anyone's connection graph from outside their session. So never imply
the skill itself shows mutuals or has an in-app "request intro" button. In Mode 2,
LinkedIn shows each viewer their own paths when they open the link. In Mode 1, you
read what the user's own logged-in search returns.

## Shared steps (both modes)

### 1. Get the brief sharp before you build

Thin briefs produce generic intros. A request like "I want intros to AI startups"
isn't enough to make a good ask, so don't just run with it. Gather enough context
that the resulting intro is one a connector would actually want to pass along. Get,
in plain language:

- Who the requester is and their edge. The one or two lines that make them credible
  to the person being introduced (what they've built, traction, background). This is
  what a connector forwards.
- The target persona and why, not just the company. WHO at these targets do they
  need (founder, VP Eng, hiring manager, a specific kind of engineer) and what makes
  a good match. This sets the role search terms and sharpens fit.
- The target set and constraints: companies or funds, sector, stage, size,
  geography, "like X and Y".
- The use case, since it changes the persona: raising (partners/investors), selling
  (the buyer role), recruiting (candidates in a role, e.g. engineers), or BD.

Ask the few questions that matter, conversationally, one or two at a time. If the
requester already gave rich detail, skip ahead. The goal is a brief good enough that
the broadcast message or connector ask reads like the requester did their homework.

### 2. Build and rank the target list

Research and produce a list of fitting targets. Filter for FIT, not just name match.
Hold a one-line reason each. If the user brought a list, use it.

### 3. Resolve each target to a LinkedIn company ID

This is the engine. Follow `references/linkedin-mechanics.md`: company search to find
the right entity and slug, then the company page to extract the `fsd_company` ID
anchored on `universalName`. Watch for same-name companies and "similar companies"
noise; when unsure, show the user the options instead of guessing.

## Mode 2 steps (broadcast)

### 4a. Build the search link(s)

Run `scripts/build_search_urls.py` with the resolved IDs and any role terms, degrees
`FS`. It batches a long list into a few links (10 companies each) and encodes
correctly.

### 5a. Write the broadcast message

Short, shareable, and clear that the recipient should open the link on their own
LinkedIn. Make the ask tiny.

> We're looking for warm intros to a set of [sector] companies. [One-line why.]
> This link shows you anyone YOU know there (open it logged into LinkedIn):
> [link]. If you can intro us to even one, reply and I'll send a short blurb you
> can forward. Thank you.

The user shares this in DMs, email, a founder update, Slack communities, wherever
their network is.

## Mode 1 steps (own-network map)

### 4b. Run and scrape the searches

On the user's account, run one search per company (or the stacked search) filtered to
`network=["F","S"]`, and scrape each result's name, title, degree, and the named
mutual connections plus the "+N others" count. Use the scraper in
`references/linkedin-mechanics.md`.

### 5b. Build the connector spreadsheet

Run `scripts/build_connector_sheet.py` with the scraped JSON. It inverts target →
mutuals into connector → targets, ranks connectors by how many doors they open,
lists total mutual counts per target for triangulation, and writes a clean workbook
(Read me, By connector, By target, Target brands, Email 1). Flag plainly whose
network it reflects: the connectors are whoever was logged in.

Note the named-mutuals limit: LinkedIn names ~2 mutuals per target, hiding the rest
behind "+N others." So the sheet's named connectors are the tip; the total-mutual
count tells you where the depth is. Optionally expand a shortlist by clicking each
target's "+N others" to pull the full connector list (slower, rate-limited).

### 6b. Draft the connector ask, then hand off

The sheet includes Email 1, the connector ask ("you're connected to people at these
companies, can I send you forwardable blurbs?"). Email 2 is the forwardable blurbs
themselves: hand off to the `forwardable-intro` skill once a connector says yes.

## Output shapes

- Mode 2: the target list (one-line fit each), the search link(s) with a one-sentence
  "here's what opening this shows you," and the broadcast message.
- Mode 1: the spreadsheet, plus a short note on the top connectors to ask first and
  whose network it reflects.

## Surprise and delight

Keep the delight on the helper's side: the ask is so clean and easy to say yes to
that it signals the user did their homework. No GIFs or gimmicks in the ask.
