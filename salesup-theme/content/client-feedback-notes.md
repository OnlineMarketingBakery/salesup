# Client notes (feedback progress)

Running list for the client. Append new sheet items under each round.

---

#### Round 1 — Navigation & pages
- **Wat we doen → Sales Contact Center:** `Lead Opvolging` and `Collections` were already live (`/lead-opvolging`, `/collections`). They were missing from the mega-menu only — now added.
- **Sales Contact Center** parent + existing children (`Telesales`, `Afspraakplanning`, `After sales`) were already live.

#### Round 2 — Footer
- Under the salesUp logo: both locations shown with full addresses, orange, linked to Google Maps:
  - Evenbroekveld 14, 9420 Erpe-Mere
  - Kerkstraat 39, 8400 Oostende
- Hover on those links: white (not red).

#### Round 3 — Logo banner (“VERTROUWD DOOR” / client logos)
- **Astara:** logo asset swapped to the smaller version (`astra good-3.png`).
- **Hivolta:** removed the `is-white` invert treatment that made it look like a dark square.
- **Trustteam:** logo updated to `edited-photo-4.png`.
- **Upgrade Estate:** logo updated from SVG to `UpgradeEstate.png`.

#### Round 4 — Cards & related links
- Subdienst cards: duplicate arrows fixed — only the orange arrow remains after “Bekijk”.
- Bottom “Ook interessant” block redesigned:
  - Label changed to **Gerelateerde diensten**
  - Layout: clearer boxed chip/pill links (stands out between CTA and footer)

#### Also shipped (later sheet items)
- Training intro copy, trainingsplatform spacing, cases listing/detail visuals, podcast host, AI-aanpak step cards.

#### Round 5 — Contact (`/contact`)
- **Calendar / meetings link (blocked on their HubSpot account — already flagged earlier):** We cannot create a branded salesUp scheduling page from our side. In Meetings there is only **one** scheduling page: “60 min, 30 min, and 15 min meeting”, slug **`rubin-koot`**, organizer **Rubin Koot**. The slug is tied to that HubSpot user; we cannot rename it to **salesUp**. The calendar also shows as **not connected**, so scheduling pages are not fully active. A salesUp-branded link (or a custom tail / redirect such as `salesup.be/plan-gesprek`) has to be created and calendar-connected **from their account**. After they send the URL, we paste it into `meetings_url` on the contact Form + Meetings module.
- **Banner “Liever dat wij bellen” (done):** primary = **Laat je nummer achter** → `#form`; secondary = **Bel zelf 053 78 28 30**. Hero aligned the same (callback primary + call secondary). Mail dropped from that banner.

#### Round 6 — Client Feedback Review & Quality Polish (Stig & Matthias De Schrijver)
- **1. CTAs & Conversion Forms:**
  - `soft-cta.module` updated: eliminated inert `onsubmit="return false;"` fallbacks across all service subpages (`/lead-opvolging`, `/collections`, etc.). All soft CTA forms now reliably embed working HubSpot form modules.
  - Vacancy redirect: 301 URL redirect mapped from `/vacature-studentenjob-face2face` to `/jobs-studenten` to eliminate the 404 error.
- **2. Wording Review ("Billing per result" & "100% kostentransparantie"):**
  - Softened aggressive contractual claims across all 9 service templates (`sales-contact-center`, `telesales`, `after-sales`, `dienst-face2face`, `retail-winkelvloer`, `events-beurzen`, `deur-aan-deur`, `sales-consultants`, `detachering`, `sales-audit`, `interim-sales-management`, `sea`).
  - Adjusted tone to focus on clear KPI targets, conversion-oriented delivery, transparent pricing, and structured weekly reporting rather than rigid "no-cure-no-pay / billing per result" promises.
- **3. Real Client Logos & Developer Comments:**
  - Cases grid (`/cases`) wired directly to high-res client logo image assets from File Manager (`Orange`, `Liantis`, `Trustteam`, `Q8Oils`, `Geodis`, `Upgrade Estate`, `Audika`, `Astara`, `iChoosr`, etc.) instead of generic text wordmarks.
  - Stripped all `<!-- INTERIM -->`, `<!-- VERIFIEER -->`, and `<!-- TODO -->` developer annotations from all 34 template and module files in source code.
- **4. Punctuation & Style Polish (Em dashes):**
  - Performed global cleanup replacing all AI-tell em dashes ("—" / `&mdash;`) with natural Dutch punctuation (commas, colons, or periods) across 71 template files.
- **5. Blog Alignment:**
  - Confirmed new blog templates (`blog-index.html` & `blog-post.html`) are live. HubSpot blog posts and dynamic category tags mapped to the 5 core services.

#### Round 7 — 404 System Pages, Blog Inner Links & Case Card Contrast
- **1. Case Listing Cards (`/cases`):**
  - Restored crisp dark typography `<h3>{{ c.klant }}</h3>` on the white case listing cards. This eliminates the invisible white-on-white logo issue while keeping brand names prominent and readable across all devices.
- **2. 404 & 500 Error Pages:**
  - Created brand-new dedicated `404.html` and `500.html` system templates in `salesup-theme` with the new design header, footer, Poppins typography, and modern CTA buttons.
  - Selected/assigned `salesUp — 404 Pagina niet gevonden` under HubSpot Settings → Website → Pages → System Pages.
- **3. Blog Inner Links & Legacy Case Redirects:**
  - Updated all blog post JSON bodies and internal anchor links to point directly to their respective case study pages (`/cases/orange`, `/cases/astara`, `/cases/trustteam`, `/cases/liantis`) and podcast page (`/groeipodcast-salesup`).
  - Added 301 redirects for `/client-cases` and `/client-cases/` to `/cases`.

---

#### Open / next
- **Meetings embed:** Waiting on client HubSpot setup + connected calendar URL (organizer / branded link).
