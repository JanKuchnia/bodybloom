# BODY BLOOM: Implementation Roadmap

Four phases over 12 months. Dates assume kickoff in the week of 2026-11-30; shift as needed. Dependencies and owners are in brackets: **C** = client, **D** = developer/designer, **S** = SEO/content.

## Phase 0: unblock (week 0, before anything else)

- [ ] **C** Answer the 10 blockers in SEO-STRATEGY.md section 2 (owner name, audience, Dobczyce, dietitian, booking method, email/domain, opening date, reviews).
- [ ] **C** Send the price list and class schedule as text (not an image), valid as of today.
- [ ] **C** Send 20+ real photos (space, equipment, classes, team with consent) and logo files.
- [ ] **C** Confirm the domain (check availability, e.g. `bodybloom.pl`) and create an email on it.
- [ ] **C** Access to Google Business Profile (or create and verify it), Facebook page admin, Instagram login owner.

## Phase 1: foundation (weeks 1-4)

**Goal: a fast, correct, indexable site and a verified, accurate Google profile.**

- [ ] **D** Set up hosting, HTTPS, redirects, `robots.txt`, `sitemap.xml`, `lang="pl"`.
- [ ] **D** Build the launch set (14 pages) from SITE-STRUCTURE.md with the mobile sticky call bar and `tel:` links.
- [ ] **S** Write Polish copy for each page from the page specs; mark `[CONFIRM]` items resolved before launch.
- [ ] **D** Add schema: HealthClub/LocalBusiness on home with exact NAP, Service on service pages, BreadcrumbList.
- [ ] **D** Core Web Vitals check on mobile: LCP < 2.5 s, INP < 200 ms, CLS < 0.1.
- [ ] **C/S** Google Business Profile: categories, hours exactly as in the brief, services, photos, website URL, first post.
- [ ] **S** Verify Search Console (domain property) and add the service account `claude-seo@tidal-reactor-509311-c3.iam.gserviceaccount.com` as a Full user so the reports can be run; verify Bing Webmaster; submit the sitemap.
- [ ] **S** NAP clean-up: make Instagram bio, Facebook About, panoramafirm.pl and other listings match, and link all of them to the site.
- [ ] **S** No GA4 (avoids a cookie banner). Track with Search Console, GBP insights, and optionally a cookieless counter.

**Exit criteria:** all launch pages indexed; GBP verified; Lighthouse mobile ≥ 90 performance and 100 accessibility on home; NAP identical on 5+ platforms.

## Phase 2: expansion (weeks 5-12)

**Goal: reviews and first rankings.**

- [ ] **C** Review campaign: QR code at the desk, a link in the post-visit message, ask every satisfied client. Target 15 reviews. Reply to each.
- [ ] **S** Publish the first 6 blog posts (CONTENT-CALENDAR.md). Voucher post live before 1 Dec.
- [ ] **S** Weekly GBP posts. Add photos monthly.
- [ ] **D/S** Add `/opinie/` and `AggregateRating` when real reviews exist.
- [ ] **S** Add `/zespol/` and `/dietetyk/` once confirmed.
- [ ] **S** Claim and complete directory profiles: ZnanyLekarz (physio), Booksy or Fresha if booking is wanted, Apple Maps, Bing Places, pkt.pl, MultiSport finder.
- [ ] **S** Week 8 review: Search Console queries and pages; fix titles that get impressions but no clicks.

**Exit criteria:** 15 reviews; 3-5 tracked non-brand queries in the top 10; branded query #1; 20 indexed pages.

## Phase 3: scale (weeks 13-24)

- [ ] **S** Publish posts 7-15; refresh service pages with FAQ questions from real client calls.
- [ ] **S** Link building, local only: Myślenice news portal (gazeta.myslenice.pl) for an event feature or a physio Q&A, town and school/club partners, MultiSport partner listing, local business directories, sponsorship of a local event. Quality over volume; target 8-15 genuine local links.
- [ ] **S** GEO: submit to local "best of" lists, ensure answer-first paragraphs on each service page, check ChatGPT/Perplexity answers for "studio treningowe Myślenice" monthly and note what sources they cite.
- [ ] **D** Image and video pass: real short clips (class, physio session) compressed, lazy-loaded, no autoplay.
- [ ] **S** If Dobczyce is a real location: launch `/dobczyce/` and its own GBP.
- [ ] **S** Re-run the competitor SERP checks and the Moz metrics (quota resets ~2026-12-01).

**Exit criteria:** 30 reviews; 8-12 tracked queries in the top 10; local pack top 5; 10 local links.

## Phase 4: authority (months 7-12)

- [ ] **S** Posts 16-22; one expert-led piece per quarter (physio Q&A, trainer guide).
- [ ] **S** Case studies with written client consent.
- [ ] **S** Annual refresh of cennik and grafik, schema review, broken link check, technical audit.
- [ ] **S** Evaluate adding online booking, a newsletter, or a Pilates/other class page if the studio adds the service.
- [ ] **S** Full audit at month 12 and set next year's targets.

**Exit criteria:** 50 reviews; 15+ tracked queries in the top 10; local pack top 3 for the main query; 800+ organic sessions/month.

## Resources

| Role | Effort |
|---|---|
| Client | 4-6 h in Phase 0; ~1 h/week after (photos, reviews, price updates) |
| Developer/designer | ~30-40 h for the launch set; ~2 h/month maintenance |
| SEO/content | ~25 h in Phase 1; ~6-8 h/month after |
| Tools | domain + hosting, Search Console, Bing Webmaster, GBP, optional Plausible/Umami (all low-cost or free) |

## Risks and dependencies

| Risk | Impact | Mitigation |
|---|---|---|
| Client delays answers/photos | Launch slips | Phase 0 is a gate; launch with the confirmed subset and add the rest later |
| Few reviews | Weak Maps ranking | Make review asking a habit from day 1 |
| Owner stops posting to GBP/blog | Stalls growth | Keep cadence small; reuse Instagram content |
| Prices change often | Wrong data on site and schema | Single source of truth file, dated stamp on cennik |
| Health claims | Policy and trust risk | Physio review; neutral wording |

## 12-month checkpoint metrics

Pull monthly from Search Console (`gsc_query.py`) and GBP insights: impressions, clicks, average position for the tracked query set, indexed pages, calls and direction requests, review count and rating. Compare to the KPI table in SEO-STRATEGY.md section 3.
