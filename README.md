# Founder Playbook

The Founder Playbook turns the tips and tricks founders usually learn the hard way into tactical [Claude](https://claude.ai) skills you can use to win customers, build your company, and fundraise.

Open-source and built by Hustle Fund.

Raising is hard enough. The fastest intros happen when you make it effortless for the people who already believe in you — friends, advisors, your current cap table — to help. These skills are built to do exactly that.

## Skills

### `forwardable-intro`

Make it really easy for your friends or current cap table to help you by sharing a short, forwardable blurb. This skill walks you through writing a warm, personalized intro-request email a connector can forward with zero editing — generating a tailored blurb for each intro you ask for.

Give it **one investor or a whole list**, and it helps you write:
- a short **cover note** to your connector, and
- a **forwardable blurb** to each target investor — opening with something specific to *them*, then a problem-first take on your company, a team line, a traction line, an optional raise line (your call), and your deck.

→ [`forwardable-intro/`](./forwardable-intro)

### `warm-intro-finder`

Figure out *who can actually open the door* to the companies or funds you want to meet — then make it easy for them to help. Works for fundraising (seed funds), sales (target accounts), recruiting (engineers at companies you admire), or any outreach where the bottleneck is the warm path.

Two modes:
- **Broadcast.** Build a ranked target list, turn it into **one LinkedIn search link** plus a short message you share widely. Anyone who opens the link sees *their own* 1st and 2nd-degree connections to your targets — because LinkedIn degree is relative to whoever's viewing. One link crowdsources warm paths across your whole network.
- **Own-network map.** Surface who *you* personally know at each target, ranked by connector (the people who can open the most doors), with a connector-ask email ready to send. Pairs naturally with `forwardable-intro` for the blurb you send next.

→ [`warm-intro-finder/`](./warm-intro-finder)

## How to use a skill

1. Download the skill folder (e.g. `forwardable-intro/`) and zip it.
2. In **claude.ai**, go to **Settings → Features** and upload the zip.
   - Available on Pro, Max, Team, and Enterprise plans with code execution enabled.
   - Skills are per-user on claude.ai — each person uploads their own copy.
3. Then just ask Claude in plain language, e.g. *"Help me write a forwardable intro to [investor]"* or *"Find me warm intros to seed funds that back technical founders."*

You can also use these in Claude Code by dropping the folder into `~/.claude/skills/`.

> A skill lets Claude run code on your behalf — treat installing one like installing software, and only use skills from sources you trust.

## License

MIT — see [LICENSE](./LICENSE). Use it, fork it, adapt it for your own founders.
