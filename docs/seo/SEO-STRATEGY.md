# BODY BLOOM: SEO Strategy

Date: 2026-11-23. Template used: `local-service` (multi-service variant). No keyword-volume data was available (no DataForSEO), so keyword targets below are hypotheses to validate in Search Console after launch.

## 1. Business snapshot (only confirmed facts)

| Item | Value | Status |
|---|---|---|
| Name | BODY BLOOM - Studio Treningowe, Fizjoterapia i Masaż | client-confirmed |
| Address | ul. Ignacego Daszyńskiego 9, 32-400 Myślenice | client-confirmed |
| Phone | 533 620 733 | client-confirmed |
| Hours | Mon 07:00-20:00, Tue-Thu 07:30-20:00, Fri 07:30-19:00, Sat 08:00-11:00, Sun closed | client-confirmed |
| Services | group training, personal training, physiotherapy, massage, MultiSport accepted | Instagram bio |
| Vibe | "Kobieca ekipa i zero spiny", warm, casual, no-pressure | Instagram |
| Online presence today | Instagram (471 followers), Facebook page, registry listings. **No website** | research |
| Age | roughly 1 year, so few or no reviews | research |

## 2. Blockers: client must answer before copy is final

The site must not print anything below until confirmed. Each has a placeholder in the content plan.

1. **Who is the face of the studio?** Registry says Maciej Hudaszek; a Facebook video names the owner as "Karolina", a physiotherapist and trainer. Decide what names, credentials and photos go on the site.
2. **Women-only or everyone?** The bio says "kobieca ekipa" and the opening was "dla kobiet". This decides the whole positioning and the H1.
3. **Current price list and class schedule.** Only exists as an image on Instagram (post of 2026-01-08). Needed for `/cennik/` and `/grafik/`, which are the highest-converting pages.
4. **Dobczyce (ul. Jagiellońska 44e).** Second location or one-off class venue? If a second location, it gets its own page and its own Google Business Profile.
5. **Dietitian.** Paulina Guzik-Krzystek lists the studio on ZnanyLekarz. Is she part of the team? If not, no dietitian page.
6. **Booking method.** Phone only, or add a booking tool (Booksy, Fresha, a form)?
7. **Email address and domain.** None found. Check whether `bodybloom.pl` is free before assuming it.
8. **Opening date.** Sources conflict (13 Sept 2025 event vs 15 Oct 2025 post vs registry 24 Jun 2025). Don't print one.
9. **Relationship to "Baby Trenują".** Fresha once listed it at the same address, but it now has its own site at ul. Niepodległości 22 and looks like a separate studio. Treat it as a competitor; never mention it.
10. **Real Google reviews.** Ask for 3-5 real ones, or confirm there are none. Never write placeholders or invented testimonials.

## 3. Goals and KPIs

Primary conversion: **phone call or tap-to-message from mobile.** Secondary: trial/consultation booking, voucher purchase enquiry, directions request.

| Metric | Baseline | 3 mo | 6 mo | 12 mo |
|---|---|---|---|---|
| Indexed pages | 0 | 15-20 | 25-30 | 40-50 |
| Branded queries ("body bloom myślenice") rank | n/a | #1 | #1 | #1 |
| Non-brand local queries in top 10 (tracked set of ~25) | 0 | 3-5 | 8-12 | 15+ |
| Google Maps local pack (top 3) for "studio treningowe Myślenice" | not tracked | reach top 5 | top 3 | top 3 |
| GBP actions (calls + directions + website clicks) / month | measure on day 1 | +50% vs baseline | +100% | +200% |
| Organic sessions / month | 0 | 100-200 | 300-600 | 800-1500 |
| Google reviews | unknown | 15 | 30 | 50+ |
| Core Web Vitals (mobile, lab) | n/a | LCP < 2.5 s, INP < 200 ms, CLS < 0.1 | same | same |

Targets are estimates for a town of about 18k people with weak local competition. They are guidance, not promises. Re-baseline after month 1 with real Search Console data.

## 4. Positioning (what search and AI engines should learn)

Competitors split into single-service sites. **Nobody found in the research combines training + physiotherapy + massage under one roof in Myślenice** (inference, not verified). Own that: "one place to get stronger, recover, and relax."

- Core promise: training and recovery together, without pressure.
- Differentiators to prove with real content: physiotherapist-led training, small groups, MultiSport accepted, community events (Krąg Kobiet, Andrzejki, Zumba), gift vouchers.
- Voice: informal "Ty" form, warm, short sentences, no gym-bro language, no diet-culture claims.

## 5. Keyword map (hypotheses, no volume data)

| Page | Primary keyword | Secondary |
|---|---|---|
| Home | studio treningowe Myślenice | fizjoterapia i masaż Myślenice, body bloom |
| Treningi personalne | trening personalny Myślenice | trener personalny Myślenice, trener dla kobiet |
| Treningi grupowe | treningi grupowe Myślenice | zajęcia fitness Myślenice, zumba Myślenice |
| Fizjoterapia | fizjoterapia Myślenice | fizjoterapeuta Myślenice, ból kręgosłupa Myślenice |
| Masaż | masaż Myślenice | masaż leczniczy / relaksacyjny / sportowy Myślenice |
| MultiSport | MultiSport Myślenice | siłownia MultiSport Myślenice |
| Voucher | bon podarunkowy masaż / trening | prezent dla kobiety Myślenice |
| Dietetyk (conditional) | dietetyk Myślenice | |

Intent notes: "fizjoterapia Myślenice" SERP is dominated by directories (rejestrmedyczny, pkt.pl, NFZ, Fresha) and clinics, so expect Maps and directory listings to matter more than the organic blue links. "Masaż Myślenice" is led by Booksy/Fresha profiles and small studios. "Trening personalny Myślenice" has 5-6 small studios with their own sites (Studio MP, KAMO, Studio Ruchu, The Spot, in.Time, Baby Trenują), so a proper site with real pages already puts BODY BLOOM level with them.

## 6. Technical foundation

- **Stack:** static or lightly dynamic site (Astro/Next static export or similar). Content is stable, so avoid a heavy CMS. If the owner must edit prices and schedule alone, use a simple CMS or a single JSON/Markdown file.
- **Performance:** mobile LCP < 2.5 s, images in WebP/AVIF with width/height, self-hosted fonts, no sliders, no autoplay video above the fold.
- **Mobile first:** sticky "Zadzwoń" button, `tel:` links on every phone number, big tap targets. Most visitors will come from phones on Instagram or Maps.
- **Privacy:** GA4 is intentionally skipped elsewhere to avoid a cookie banner. Do the same here: use Search Console + GBP insights + optionally a cookieless tool (Plausible/Umami). Embedded Instagram feeds and Google Maps iframes set cookies, so use a static map image linking to Maps and static Instagram thumbnails.
- **Required legal pages:** polityka prywatności; regulamin (training rules, cancellation); physio/massage disclaimers.
- **HTTPS, www to non-www (or reverse) 301, trailing-slash consistency, `lang="pl"`.**
- **Files:** `robots.txt` allowing all including AI crawlers, `sitemap.xml`, optional `llms.txt`.

## 7. Schema plan

| Page | Schema |
|---|---|
| Home | `HealthClub` (or `SportsActivityLocation`) + `LocalBusiness` with `address`, `geo`, `telephone`, `openingHoursSpecification`, `areaServed`, `sameAs` (Instagram, Facebook, GBP). Add `priceRange` only after prices are confirmed |
| Service pages | `Service` with `provider` referencing the business `@id` |
| Physio / massage | `Service` only. Do not use `MedicalBusiness` or health claims unless credentials are confirmed |
| FAQ | Visible FAQ content. `FAQPage` markup no longer yields rich results for most sites, so it is optional |
| Team | `Person` only for people who consent and whose credentials are verified |
| Blog | `Article` + `BreadcrumbList` |
| Reviews | `AggregateRating` **only** if real reviews are displayed on the page itself |
| All | `BreadcrumbList`, `WebSite` |

NAP in the schema must match GBP exactly: "BODY BLOOM - Studio Treningowe, Fizjoterapia i Masaż", Ignacego Daszyńskiego 9, 32-400 Myślenice, +48 533 620 733.

## 8. Local SEO (the biggest lever)

1. **Google Business Profile**: claim/verify (video verification), primary category "Studio treningowe" or "Siłownia"; add "Fizjoterapeuta" and "Masażysta" as secondary only if allowed and honest. Add services with descriptions, hours (exactly as above, and set Saturday/holiday hours), 15+ real photos, weekly posts, and the website URL once live.
2. **Review engine**: QR code at reception + WhatsApp/SMS link after sessions. Ask every happy client. Reply to every review. Target 15 in 3 months.
3. **NAP consistency** across: Instagram bio, Facebook, GBP, ZnanyLekarz (if applicable), panoramafirm.pl, Fresha/Booksy (if used), Apple Maps, Bing Places, pkt.pl, Yelp-style directories, MultiSport finder.
4. **Local mentions**: gazeta.myslenice.pl and local portals (they cover local studios), Myślenice town hall events page, local Facebook groups (disclose affiliation), Instagram collabs with local businesses.
5. **Do not create doorway pages** for surrounding towns. Name nearby towns (Dobczyce, Sułkowice, Pcim, Lubień) once on the contact page as `areaServed` text, nothing more.

## 9. E-E-A-T plan

- Real photos of the studio, equipment, team, classes (with consent). No stock photos for the team.
- Named practitioners with verified credentials (physiotherapy license, trainer certifications) on `/zespol/`.
- Health content reviewed by the physiotherapist, with a "zawsze skonsultuj się z lekarzem" note where relevant.
- Real testimonials with permission and first name + initial only.
- Transparent prices and cancellation terms.

## 10. AI search (GEO) readiness

- One quotable "answer paragraph" at the top of each service page (what, for whom, how long, price range once confirmed).
- FAQ blocks written as natural Polish questions ("Czy mogę przyjść na pierwszy trening bez doświadczenia?").
- Consistent entity data: same name, address, phone, sameAs links everywhere.
- Get listed on local "best of / gdzie na masaż w Myślenicach" lists and directories, since AI answers for local queries lean on them. One Instagram reel in the research claims a "#1 in Myślenice according to ChatGPT" for a competitor, which shows this is already a competitive angle locally.
- Allow GPTBot, PerplexityBot, Google-Extended in `robots.txt`.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Unconfirmed facts get published (prices, names, second location) | Blocker list in section 2, placeholders marked `[CONFIRM]` in all drafts |
| Health claims on physio/massage pages | Describe the service and process, not cures; physiotherapist signs off |
| Same-name noise ("The Body Bloom" AU chiropractor, Body Bloom powder) | Always pair the brand with "Myślenice"; consistent `sameAs`; GBP and schema do the disambiguation |
| No reviews yet, so weak local pack | Review campaign from week 1; Instagram social proof until then |
| Owner has no time to maintain a blog | Plan is deliberately small: 1 post per 2 weeks, reuse Instagram content |
| Directory sites outrank the site on "fizjoterapia Myślenice" | Also claim directory profiles (ZnanyLekarz, Booksy/Fresha if used) and link them to the site |
