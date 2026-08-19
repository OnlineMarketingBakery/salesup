# salesUp HubSpot CMS

Local workspace for the salesUp HubSpot website theme (`salesup-theme`).

## What this gives you

- Edit **templates**, **modules**, **CSS/JS**, and theme fields locally
- Upload changes with `npm run upload` or `npm run watch`
- Use **HubSpotDev** MCP in Cursor for AI-assisted CMS development

## HubSpot account

- Portal: **salesUp** (25245585)
- CLI auth: `~/.hscli/config.yml`

## Commands

```bash
npm run list          # list remote CMS files
npm run fetch         # re-fetch theme (see package.json)
npm run watch         # auto-upload on save
npm run upload        # upload local theme to HubSpot
```

## MCP in Cursor

1. **HubSpot** plugin — CRM, landing pages (already connected)
2. **HubSpotDev** — CMS templates/modules via CLI (`~/.cursor/mcp.json`)

Restart Cursor if HubSpotDev does not appear under **Settings → Tools & MCP**.

## Git vs GitHub

**GitHub is not required.** This folder uses local git only for your own history. The workflow is:

`local files → HubSpot CLI upload → HubSpot portal`

No GitHub in the middle unless you want team backup or CI.

## Menu changes

Navigation **items** (links, order) are still edited in HubSpot:
**Settings → Website → Navigation**

Menu **design/code** lives in theme modules (e.g. `salesup-theme/modules/`).

## Other themes on the portal

- `SalesUp_May2022`, `SalesUp_2025`, `TEMPLATES SALESUP`, `POWER THEME x ShakeUp`

Only `salesup-theme` is fetched here. Say if you need another theme pulled down.
