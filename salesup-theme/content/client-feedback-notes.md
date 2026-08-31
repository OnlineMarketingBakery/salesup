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

#### Round 7 — Case Logos with Contrast Badges, 404 System Pages & Blog Legacy Redirects
- **1. Case Listing Logos (`/cases`):**
  - Restored real client logo image assets on `/cases` cards (`Orange`, `Q8Oils`, `Liantis`, `Geodis`, `Trustteam`, `Astara`, `iChoosr`, `Upgrade Estate`, `Eurocircuits`, `Jaguar Land Rover`, `Hivolta`, `Audika`, etc.).
  - Wrapped logos in `.case-logo-wrap.is-light-bg` with a sleek navy badge (`background: var(--navy-deep); border-radius: 8px; padding: 6px 14px; min-height: 38px;`). This ensures transparent and white logos have crisp contrast against the white cards and look unified with the brand identity.
- **2. 404 & 500 Error Pages (New Theme):**
  - Created brand-new dedicated `404.html` and `500.html` system templates in `salesup-theme` with the new design header, footer, Poppins typography, and modern CTA buttons.
  - Uploaded to HubSpot CMS. In HubSpot portal settings (**Settings → Website → Pages → System Pages**), select `salesUp — 404 Pagina niet gevonden` under 404 error page to replace the old POWER THEME 404 page globally.
- **3. Blog Inner Links & Legacy Case Redirects:**
  - Diagnosed that old blog posts and HubSpot CTA buttons pointed to legacy long-tail URLs on the old theme (e.g. `/client-cases/liantis-x-salesup-mensen-laten-groeien-om-groei-mogelijk-te-maken`).
  - Added full 301 redirect mappings for all 23 legacy `/client-cases/...` URLs to their new respective `/cases/<slug>` pages in `redirects.json`.
  - Updated all blog post JSON content so internal links point directly to `/cases/<slug>` and `/groeipodcast-salesup`.

#### Round 8 — Unified Case Logo Sizing & Single-Line Hero Layout (Listing & Detail Pages)
- **Single-Line Hero Header:** Updated single case pages so the logo badge and the eyebrow text (`CLIENT CASE · SECTOR`) sit side-by-side on one clean horizontal line.
- **UNIZO Logo Display:** Fixed UNIZO and other theme vector logos on single case detail pages by mapping direct public asset URLs with robust error fallbacks so no blank badges appear.
- **Listing Cards (`/cases`):** Standardized all cards to use a consistent 44px dark navy badge (`.case-logo-wrap`) with optical scaling classes (`is-pad` and `is-pad-large`) for padded and square assets (`Liantis`, `Zambon`, `JLR`, `Astara`, `Orange`, `Trustteam`, `Hivolta`, etc.).
- **Case Hero Detail Pages (`/cases/<slug>`):** Standardized case heroes with a matching 44px dark navy badge (`.case-hero-logo-wrap`) aligned inline with the eyebrow label.

#### Round 9 — Official Web Logos for Text-Only Cases & Complete Visual Polish
- **Official Brand Assets Pulled & Integrated:**
  - **UNIZO:** Extracted official SVG vector symbol from unizo.be, styled with signature orange badge (`#EF7D00`) and crisp white cutout typography.
  - **Van Heurck:** Downloaded official vector logo mark (`logo.svg`) from vanheurck.com, rendered in crisp white on navy.
  - **VM Building Solutions:** Downloaded official vector SVG (`logo-vmbso.svg`) from vmbuildingsolutions.com, rendered in crisp white on navy.
  - **Messer Group:** Sourced official vector SVG from Wikimedia Commons, styled with brand gas emblem and white typography.
  - **Axians:** Sourced official Axians brand logo and vector mark, rendered with orange accent and white lettering.
  - **Radiance Energy:** Created dedicated vector solar icon badge with clean geometric typography.
  - **Alindus:** Created dedicated vector badge with stylized A emblem and bold white wordmark.
  - **EV Shop:** Created electric vehicle badge with plug/lightning motif and crisp typography.
  - **SPM Technologies:** Created proptech symbol badge with clean white typography.
  - **Immo Van Middelem:** Created real estate vector badge with property emblem and crisp typography.
  - **Cesano, Sobelhor & Ikaros Solar:** Created matching vector SVGs with clean brand motifs.
- **Full Fallback & Rollback Safety:**
  - Backup branch created (`backup/case-logos-pre-fetch`) for instant reversion if needed.
  - All logo `<img>` tags include `onerror` handlers gracefully revealing styled text if any network asset fails to load.

#### Round 10 — Global Logo Marquee Slider Upgrade (All Pages)
- **Universal Logo Assets in Marquee Slider:**
  - Mapped all new vector SVGs and official PNG assets (`UNIZO`, `Van Heurck`, `Axians`, `VM Building Solutions`, `Radiance Energy`, `Messer Group`, `Alindus`, `EV Shop`, `SPM Technologies`, `Immo Van Middelem`, `Cesano`, `Sobelhor`, `Ikaros Solar`) into `proof-marquee.module/module.html`.
  - Replaced text fallbacks with high-contrast, scalable logo image assets across every page marquee slider on the entire website.
  - Preserved individual custom logo arrays per template/page completely intact.
  - Added robust `onerror` fallbacks to smoothly degrade to typography if any image fails.
- **Rollback Safety & Git Tags:**
  - Tagged `rollback-marquee-logos` and created backup branch `backup/marquee-logos-pre-update`.

---

#### Open / next
- **Meetings embed:** Waiting on client HubSpot setup + connected calendar URL (organizer / branded link).
