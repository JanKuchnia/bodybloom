# BODY BLOOM: Site Structure and Page Content Plan

Language: Polish. URLs: lowercase, no diacritics, trailing slash. Placeholders `[CONFIRM]` = client must supply or approve (see SEO-STRATEGY.md section 2).

## 1. URL hierarchy

```
/                                  Home
├── /treningi-personalne/          Personal training
├── /treningi-grupowe/             Group training (+ Zumba etc.)
├── /fizjoterapia/                 Physiotherapy
├── /masaz/                        Massage
├── /dietetyk/                     [CONDITIONAL: only if dietitian confirmed]
├── /cennik/                       Price list (all services)
├── /grafik/                       Class schedule
├── /multisport/                   MultiSport info
├── /bon-podarunkowy/              Gift vouchers
├── /wydarzenia/                   Events (Krąg Kobiet, Andrzejki, birthday...)
├── /o-nas/                        About the studio
├── /zespol/                       [CONDITIONAL: team, credentials]
├── /opinie/                       [LAUNCH LATER: needs real reviews]
├── /faq/                          Questions and answers
├── /blog/                         Articles (hub)
│   └── /blog/<slug>/
├── /kontakt/                      Contact, map, hours
├── /dobczyce/                     [CONDITIONAL: only if a real second location]
├── /polityka-prywatnosci/
└── /regulamin/
```

**Launch set: 14 pages** (home, 4 services, cennik, grafik, multisport, bon, o-nas, faq, kontakt, polityka, regulamin). Add the conditional ones as facts are confirmed. Blog starts empty and fills per CONTENT-CALENDAR.md.

**Deliberately not built:** per-town landing pages, per-treatment micro pages (e.g. one page per massage type) until there is real content and demand, a shop, a login area.

## 2. Navigation

Header: Treningi (dropdown: personalne, grupowe) · Fizjoterapia · Masaż · Cennik · Grafik · Kontakt · **[Zadzwoń 533 620 733]** (button, `tel:+48533620733`).
Footer: NAP block, hours, links to all pages, Instagram/Facebook, polityka, regulamin, MultiSport badge.
Mobile: sticky bottom bar with "Zadzwoń" and "Dojazd" (opens Maps).

## 3. Internal linking rules

- Home links to all 4 services, cennik, grafik, kontakt.
- Every service page links to: cennik (anchor to its section), grafik or booking, kontakt, and 1-2 sibling services ("training + physio" cross-sell is the main differentiator).
- Every blog post links to the relevant service page with descriptive anchor text, and to kontakt.
- Service pages link back to supporting blog posts in a "Warto przeczytać" block.
- Breadcrumbs on all pages except home.
- No orphan pages: every URL reachable in ≤ 2 clicks from home.

## 4. Page specs

### `/` Home
- **Title:** BODY BLOOM Myślenice | Studio treningowe, fizjoterapia i masaż (≤ 60 chars)
- **Meta:** Treningi grupowe i personalne, fizjoterapia, masaż i MultiSport w Myślenicach. Ignacego Daszyńskiego 9. Zadzwoń: 533 620 733. (≤ 155 chars)
- **H1:** `[CONFIRM audience]` e.g. "Studio treningowe, fizjoterapia i masaż w Myślenicach"
- **Sections:** hero with call/directions buttons and today's open/closed status → 4 service cards → "Dlaczego BODY BLOOM" (3 points: trening + regeneracja pod jednym dachem, mała ekipa i zero spiny, MultiSport) → nearest schedule slots → events/Instagram thumbnails (static) → real reviews `[CONFIRM]` → contact strip with hours and map image.
- **Words:** 500-700. **Schema:** HealthClub/LocalBusiness, WebSite.

### `/treningi-personalne/`
- **Title:** Trening personalny w Myślenicach | BODY BLOOM
- **H1:** Trening personalny w Myślenicach
- **Outline:** for whom (beginners, returning after injury, specific goals) → how it works (consultation, plan, sessions) → what a first session looks like → who trains you `[CONFIRM names/credentials]` → price pointer to cennik → FAQ (3-5) → CTA.
- **Words:** 800+. Link to fizjoterapia ("trening po kontuzji").

### `/treningi-grupowe/`
- **Title:** Treningi grupowe w Myślenicach | Zumba, fitness | BODY BLOOM
- **H1:** Treningi grupowe w Myślenicach
- **Outline:** class types `[CONFIRM list from grafik]` → group size and level (all levels, no pressure) → schedule snippet → MultiSport note → trial class `[CONFIRM]` → FAQ → CTA.
- **Words:** 800+.

### `/fizjoterapia/`
- **Title:** Fizjoterapia w Myślenicach | BODY BLOOM
- **H1:** Fizjoterapia w Myślenicach
- **Outline:** what we help with (describe conditions generally, no cure claims) → how a visit goes (interview, assessment, therapy, home advice) → visit length and price `[CONFIRM]` → NFZ vs private: state clearly that it is a private practice `[CONFIRM]` → physiotherapist bio `[CONFIRM]` → FAQ (referral needed? what to bring?) → CTA.
- **Words:** 900+. Disclaimer: informational, not a substitute for medical advice. **Schema:** Service only.

### `/masaz/`
- **Title:** Masaż w Myślenicach | leczniczy, relaksacyjny | BODY BLOOM
- **H1:** Masaż w Myślenicach
- **Outline:** types offered `[CONFIRM]` as H2 blocks with duration + price → who it suits → contraindications in plain language → how to prepare → gift voucher link → FAQ → CTA.
- **Words:** 800+.

### `/dietetyk/` `[CONDITIONAL]`
Only if the dietitian is part of the studio. Package structure comes from the dietitian herself (ZnanyLekarz shows a 3-month package at 1 200 zł, but that is her listing, not confirmed for this studio). No weight-loss promises.

### `/cennik/`
- **Title:** Cennik | BODY BLOOM Myślenice
- **H1:** Cennik
- **Outline:** one table per service (training, physio, massage) as real HTML text, **not an image** → MultiSport rules `[CONFIRM]` → vouchers → cancellation policy → "ważny od [date]" stamp.
- **Words:** 200-400 + tables. Highest-intent page after contact: keep it current.

### `/grafik/`
- Weekly timetable as an HTML table, not an image, with level/type labels. Update date visible. Link to booking/phone.

### `/multisport/`
- Which activities accept MultiSport, how to book, limits `[CONFIRM]`. 300-500 words. Captures "MultiSport Myślenice" intent.

### `/bon-podarunkowy/`
- Voucher options, how to order (phone/message), validity `[CONFIRM]`, delivery (printed/PDF). Seasonal push before Christmas, Dzień Kobiet, Dzień Matki.

### `/wydarzenia/`
- Upcoming + past events (Krąg Kobiet, Andrzejki, birthday, Zumba starts). Each event a short card with date; past events kept as proof of community. Use `Event` schema for upcoming ones only.

### `/o-nas/`
- Story, values ("zero spiny"), the space (real photos), what makes the combination of training + physio + massage different. Owner/team names only after confirmation. Do not state an opening date `[CONFIRM]`. 500+ words.

### `/zespol/` `[CONDITIONAL]`
- Person cards: name, role, credentials, specialties, photo. Only verified.

### `/faq/`
- 15-20 questions grouped by service (see content plan). Mark up visibly; link out to service pages.

### `/kontakt/`
- NAP, hours table (matches GBP), click-to-call, directions button, static map image, parking/public transport note `[CONFIRM]`, how to find the entrance (shared building with other businesses at Daszyńskiego 9), contact form (name, phone, message) with consent checkbox, "Obsługujemy też klientów z: Dobczyc, Sułkowic, Pcimia" in one sentence. **Schema:** ContactPage + LocalBusiness.

### `/opinie/` `[LAUNCH LATER]`
- Publish only real reviews with permission, linked to the Google profile. Add `AggregateRating` only when the review text appears on this page.

### `/dobczyce/` `[CONDITIONAL]`
- Only if a second location actually exists. Own address, hours, classes there, own GBP. Otherwise mention Dobczyce once on kontakt.

### `/blog/`
- Category hub plus posts. See CONTENT-CALENDAR.md.

## 5. Sitemap rules

- `sitemap.xml` lists only indexable 200 pages with `lastmod` from the actual edit date.
- Exclude thank-you pages, search, tag pages.
- Submit to Search Console and Bing Webmaster.

## 6. URL and on-page conventions

- One H1 per page, containing the primary keyword naturally.
- Title ≤ 60 chars, ends with "BODY BLOOM" or "Myślenice".
- Meta description 120-155 chars with a call to action.
- Images: descriptive Polish alt text, e.g. "Trening grupowy w studiu BODY BLOOM w Myślenicach". Real photos only.
- Canonical on every page, self-referencing.
- Open Graph image 1200×630 per key page (see `seo-image-gen` later if wanted).
