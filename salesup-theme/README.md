# salesUp — HubSpot CMS-theme

Afgeleid van de mockup in `../site/`. Leidraad: `../site/CURSOR_HANDOFF.md`.

## Structuur
```
hubspot-theme/
├─ theme.json / fields.json     BrandBook-tokens (kleur, font, layout, tel/mail)
├─ css/                         main.css (HubL-tokens) + pagina-CSS
├─ js/                          hamburger, reduced-motion, Recruitee, cases-filter
├─ modules/                     herbruikbare + pagina-unieke modules
├─ templates/                   page-types + native blog
└─ content/                     blog-posts.json, redirects.json, pages.json, json-ld.json
```

## Uploaden
```bash
npm install -g @hubspot/cli
hs init                       # personal access key
hs upload hubspot-theme salesup-theme
```

Daarna in HubSpot:
1. **Marketing → Website → Menu's** — maak `salesup_hoofdmenu` (Wat we doen · Voor wie · Cases · Over ons · Vacatures · Blog · Podcast) en footer-menu's. Koppel ze in de global header/footer.
2. **Website pages** aanmaken per rij in `content/pages.json` (template + slug). Kopieer copy uit de mockup in de modulevelden. Plak JSON-LD uit `content/json-ld.json` in de json-ld-module.
3. **Blog** — kies `blog-index.html` + `blog-post.html`. Importeer de 20 posts:
   ```bash
   python3 scripts/import_blog.py   # vereist HUBSPOT_ACCESS_TOKEN + HUBSPOT_PORTAL_ID
   ```
   Of plak handmatig vanuit `content/blog-posts.json`. Hero-beelden staan nog op `salesup.be/hubfs/…` — herhost in File Manager (INTERIM).
4. **Forms** — formulier met max 4 velden (naam, e-mail, telefoon, vraag). Koppel in de contact-form-module. **Meetings** — plak de embed-URL.
5. **Redirects** — laad `content/redirects.json` in Settings → Domains & URLs → URL Redirects. Publiceer `overzicht.html` niet.
6. **llms.txt** — upload `../site/llms.txt` naar de site-root (File Manager of extra website page).

## Recruitee
Listings (`open-vacatures`) en de detailpagina fetchen live:
- `https://salesup.recruitee.com/api/offers/`
- `https://salesup.recruitee.com/api/offers/<slug>`

**Solliciteer** gebruikt `careers_apply_url`. Filter listings op `department`.

## WCAG
Nooit wit-op-oranje (oranje knop = navy label). Zichtbare `:focus-visible`. `prefers-reduced-motion` stopt marquee + motor-animatie.

## Markers
Laat `VERIFIEER` / `INTERIM` / `TODO` staan tot content bevestigd is (quotes, sublijsten Face2Face/Consultants, INTERIM-beelden, klantlogo's, GDPR-slot).
