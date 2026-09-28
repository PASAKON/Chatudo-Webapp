# Chatudo-Webapp

The public website for Chatudo (chatudo.com): home, pricing, privacy policy,
terms of service and the data-deletion instructions page.

**CEO decision D2 (2026-09-28): this repo is the public site ONLY.**
It never holds bot code and never holds customer data. The chat-reply engine,
its data pipeline, and anything that touches a real conversation live in a
separate project and talk to this repo (if ever) only through an API, never
through shared files or shared code. Do not add server logic, databases,
customer records or the LINE/Messenger/IG integration code here.

This supersedes the previous version of this README, which described an
"AI chat-reply engine SaaS extracted from MoonieX's internal LuNar chat
support system" living in this repo. That plan changed; the engine is not
part of Chatudo-Webapp.

## What's here

- Plain, static HTML/CSS. No JavaScript, no build framework runtime, no
  server-side code, no client-side analytics/trackers/chat widgets.
- `build/render.py` is a small offline generator (Python 3 stdlib only) that
  turns the content and layout defined in `build/` into `public/`, which is
  the folder actually served. Re-run it after any content or config change:
  `./scripts/build.sh`
- `site.config.json` is the single place every not-yet-confirmed fact lives
  (legal entity name, registered address, contact email/phone, LINE OA /
  Facebook page URL, data retention period, effective date). Anything still
  `null` there renders on the live pages as a visible `[รอยืนยัน: ...]`
  placeholder so it can never be mistaken for a confirmed fact. Fill in a
  value and rebuild to make it live.
- The legal copy on `/privacy`, `/terms` and `/data-deletion` is a first
  draft written for CEO/legal review, not yet CEO-approved language.

## Local development

```bash
./scripts/build.sh                 # generate public/ from build/render.py
python3 -m http.server 8931 --bind 127.0.0.1 -d public   # preview locally
./scripts/check.sh                 # lint the generated site (see below)
```

`scripts/check.sh` fails the build if: a required page is missing, an
internal link is broken, the text `—` (em dash) appears anywhere, any
`<script>` tag is present, or any emoji codepoint appears in the page text.

## Deploying

`Dockerfile` builds an nginx image serving `public/`. `docker-compose.yml`
wires it to the shared `n8n_default` Traefik network with router `chatudo-web`
for `chatudo.com` / `www.chatudo.com` (www redirects to the apex). Nobody
should start this compose stack or touch Traefik/DNS from this repo without
the CTO doing the deploy.

## Brand

Brand assets and the "Clay Signature" design system come from
`PASAKON/MoonieX-ClaudeSign`, `design-templates/chatudo/` (`BRAND.md`).
Only the files the site actually serves (logo PNGs, the four OFL-licensed
font families, the Meta app icon) are copied into `assets/` here; the
ClaudeSign repo is not a dependency of this one.
