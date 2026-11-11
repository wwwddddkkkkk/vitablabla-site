# Vitablabla continuing maintenance plan

Approved continuation: November 9, 2026. Effective November 13, 2026, with no fixed end date. Standing authorization for routine maintenance releases: November 10, 2026, effective immediately for November 10–12 and the continuing queue.

**Current release policy:** the user authorized routine bounded B2C maintenance to be locally verified, then automatically committed, pushed with `git push origin main`, deployed to the existing Cloudflare site and verified in production. The user reviews releases weekly. This replaces the earlier per-release approval gate only for that routine scope; both Sunday tasks remain read-only. Complete the isolated-source review, all applicable local checks and affected mobile/desktop browser checks before release. Preserve concurrent and unknown-ownership drafts. GSC writes, published-URL deletion/merging/redirects, permissions, credentials, Git remotes and unrelated online Cloudflare configuration still require separate explicit approval.

`content-plan-2026-10-14-to-2026-11-12.md` remains the historical recovery plan through November 12. From November 13, use this plan, the current `README.md`, and `vitablabla-content-rules.md`; do not repeat expired calendar slots or stop because the old cycle ended.

## SEO audit update — November 9, 2026

Use the audit priorities below when preparing the next work, including November 10–12. They take precedence over a calendar slot that would otherwise commission another new URL. Evidence is recorded in `scripts/seo-audits/2026-11-09.json`; recount after approved releases. This November 9 audit recorded priorities rather than publication permission; routine releases now follow the separate November 10 standing authorization above. Its evidence and counts remain historical.

The direct live HTTP scan checked all 227 sitemap URLs: 223 articles and four core pages. All returned 200, with unique titles/descriptions and self-canonical URLs; all articles had Article/Breadcrumb structured data. Those are verified technical results, not proof of Google indexing or traffic growth. The published source was `41f7d21`. Compared with the pre-recovery content baseline, only one new article and three existing article refreshes were verified as published; do not report the old eight-new/twenty-refresh targets as completed.

The largest verified discovery gap is the Journal's initial HTML: it links to only three articles. Following raw HTML anchors from the homepage reaches 21 of 223 articles; the other 202 remain in the sitemap and JavaScript registry but are outside that navigation graph. This does not mean Google has deindexed them. Published image metadata exists on four articles; 219 lack Article/social images. The 86 articles missing custom keyword/date registry fields still have rendered HTML titles, descriptions and canonicals, so they must not be reported as pages missing basic SEO tags. Concurrent uncommitted image/content drafts are excluded from the published counts.

### Verified search baseline and interpretation

Source: native Google Search Console, property `sc-domain:vitablabla.com`, Web (text), October 11–November 7 versus September 13–October 10, 2026. Exact counts came from the report tables and full-value metric tooltips, with dates checked in the comparison dialog. GSC Wizard remains subscription-blocked, but native Chrome access succeeded after the user enabled Apple Events; TinyFish was not used.

| Metric | Previous 28 days | Latest 28 days | Interpretation |
| --- | ---: | ---: | --- |
| Property clicks | 34 | 107 | +73 / +214.7% |
| Property impressions | 3,235 | 3,373 | +138 / +4.3% |
| Property CTR, computed from exact totals | 1.05% | 3.17% | +2.12 percentage points; mix changed |
| Average position, rounded UI values | 6.9 | 6.6 | Modest improvement; lower is better |
| Journal `/a/` page-row clicks | 14 | 18 | +4 / +28.6%, on a small base |
| Journal `/a/` page-row impressions | 2,217 | 2,332 | +5.2%; cohort CTR 0.63% → 0.77% |

The homepage's 57 versus five clicks and old `/ohcrisp` page's 29 versus 12 clicks account for 69 of the 73 net additional property clicks (94.5%). The exact `vitablabla` query alone rose from zero to 52 clicks. Growth is real but concentrated in brand/navigation demand. The Journal's entire net four-click gain comes from the existing rehydration page, which rose from two to six clicks and 522 to 776 page impressions; other article-page impressions combined fell by 139. Do not describe this as broad content growth or use the property CTR to claim the Journal achieved its target.

Query rows disclose only 73 of 107 current clicks and 1,074 of 3,373 property impressions. All disclosed click-bearing queries are identifiable brand terms, but the remaining clicks are unattributed; do not label them all branded or all non-branded. Page-row impression sums differ from property impressions and must retain their own denominator. The November 9 redesign/new guide falls outside this report window, so its impact is not yet measured.

The November 5 Page indexing snapshot reports 226 indexed and 726 excluded known URLs. Most exclusions are redirects (273), noindex (180), proper alternate canonicals (163) or robots blocks (82); do not call them 726 broken articles. The 12 crawled-not-indexed examples include only two current clean article URLs (`road-trip-snacks-freeze-dried-fruit` and `beach-bag-snacks-freeze-dried-fruit`), plus nine legacy query variants and an old `/pages/about` path. Review the two current articles individually rather than requesting indexing for every excluded URL. Eight duplicate-without-selected-canonical and eight 404 examples still need URL-level triage before action. This older, all-known-URL snapshot is not the coverage rate of the current 227 sitemap URLs.

The native Sitemaps report has zero submitted sitemaps; `robots.txt` does advertise the live sitemap. Prepare the already validated `https://vitablabla.com/sitemap.xml` for submission after the existing separate approval. Mobile and desktop Core Web Vitals both report insufficient usage data over the last 90 days (report updated November 7); no field-performance pass/fail claim is supported.

The old crunchy-query overlap is not currently reproduced: all 14 current impressions for `how to keep freeze dried fruit crunchy` go to the yogurt answer, while granola and storage have zero (previous period: 13, two and one). Preserve that answer as owner and improve its incoming links; do not merge the supporting URLs based on the old report. `frozili` still split pre-release impressions across homepage (24) and old brand page (14), with zero clicks and 36 property impressions. Observe the existing brand redirect and future `/about` cohort before proposing another routing change.

Prepare work in this order for the next two weeks, using this baseline and revising the order when new settled data is available:

| Priority | Bounded work | Acceptance evidence |
| --- | --- | --- |
| 1 | Preserve the verified Search Console baseline, monitor the old/new brand landing-page families together, and prepare the validated sitemap submission for separate approval. | Record exact dates, property, search type, totals and missing data. Use native Google Search Console as the user requested; do not use TinyFish. Do not retry subscription-blocked GSC Wizard repeatedly or treat expected exclusions as defects. Confirm post-release Google canonicals/indexing read-only. |
| 2 | Prepare a complete crawlable Journal archive/list from `posts.json`, retaining the current design, category/search behavior and clean article URLs. | Every currently registered article is reachable from the homepage in at most three actual HTML anchor hops without JavaScript. Verify the full graph, future-post generation, canonicals, mobile layout and existing cover rules; sitemap presence alone is insufficient. |
| 3 | Strengthen the existing rehydration, crunchy-yogurt, overnight-oats, chia-pudding, granola and oatmeal cluster, starting with the two useful answers lacking incoming body/related links. | Rehydration currently has 776 page impressions, six clicks and position 7.9; crunchy yogurt has 127, one and 8.0. Add useful incoming body links, clarify moist soaking versus last-minute dry toppings, and verify rendered links. Consider a bounded title/description test without changing the URL or promising a CTR benchmark; preserve strong answers rather than rewriting for length. |
| 4 | Review `how-ohcrisp-is-made` and `why-snacks-keep-getting-smaller` for unsupported claims. | Obtain reliable evidence for manufacturing timing, product assortment, market-share numbers and causal trend claims, or remove/narrow them. Do not invent first-party tests or use generated images as evidence. |
| 5 | Replace old article art within the selected useful refreshes, synchronizing visible images, `posts.json`, social/Article metadata and image provenance. | Validate each complete article change. Missing social images are an appearance/editorial gap, not a promised ranking gain; do not treat replacing all 219 images as the primary SEO outcome. Preserve the separate in-progress storage/snack-mix/coffee-candy drafts. |
| 6 | Reassess eligible OhCrisp/OHSIP/OHVIVA briefs only after the discovery and useful-content work. | Require a distinct user question and reliable product facts; no new URL just to fill a calendar slot. Frozili/coffee-candy remains maintenance only. Similar titles alone never authorize merging or redirecting pages. |

The former `/ohcrisp` and `/frozili` pages now redirect to `/about#ohcrisp` and `/about#frozili`. Track their historical URL families and the new `/about` page together, with brand-query splits: the fragment sections are not separate canonical pages. A successful redirect response does not prove the old landing-page traffic transferred. Confirm sitemap submission and selected Google canonical/indexing states read-only; any submission or routing change still needs its existing separate approval.

Keep an outcome ledger distinct from the release ledger. Weekly results should report current organic clicks/impressions/CTR by comparable query and page cohorts, indexing evidence and any measured brand-site outbound clicks; a completed task, new picture or passed validator is not a conversion. Cloudflare's injected analytics beacon was observed, but dedicated brand-outbound events were not verified. Propose instrumentation separately if those business outcomes cannot be measured. Do not label missing analytics as zero traffic.

Use weekly reviews to inspect discovery and processing. The first complete post-November-9-release cohort is November 10–December 7, compared with October 12–November 8, once both periods have settled; keep later release cohorts separate. These are review windows, not promises of ranking change. Google can take time to recrawl and process improvements. See [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), [helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), and [URL-migration monitoring](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).

## November 10 archive checkpoint

The complete `/blog` archive has been prepared and locally verified from an isolated release snapshot based on `ab6578f`: all 223 registered articles are linked once in initial HTML and reachable from the homepage in at most two anchor hops. The build regenerates the featured article, list and cover mix for future registry entries. Search/category enhancement and the full static fallback passed browser checks. Publication evidence is recorded separately in `scripts/maintenance-runs/2026-11-10-journal-archive.json`; consult its status before repeating this task.

The earlier audit inventory is historical. After the four approved November 9 article refreshes, the isolated baseline contains eight articles with editorial-image metadata and 215 without it. Keep any concurrent breakfast-article drafts separate from this archive release. Once the archive publication is verified, move to the useful existing-article link/answer work in priority 3; GSC-dependent checks remain limited by subscription access.

## Scope and priorities

Keep the existing B2C brand, product, taste and snack-culture scope. Prioritize useful existing URLs, accurate copy, generated editorial images, metadata and internal links. Frozili and coffee-candy work is maintenance only: no new URLs, occasion variants, disguised unbranded substitutes or substantially new coffee-candy articles.

Work in this order, using current evidence:

1. Repair reproducible availability, asset, navigation, validation or security problems. Prepare any routing or published-URL consolidation proposal separately for approval.
2. Refresh useful older articles with unsupported claims or weak answers. Start with the recovery plan's proven utility queue when fresh evidence does not identify a better candidate; historical impressions are not current performance.
3. Replace old SVG/title-block body art with inspected, optimized generated editorial raster images. Update the body, `posts.json` image metadata and `scripts/journal-image-assets.json` together.
4. Fill missing keyword metadata and improve contextual links to existing clean URLs. Change `dateModified` only for substantive visible body changes.
5. Consider at most two distinct new-content briefs per week for OhCrisp, OHSIP or OHVIVA when the intent and factual evidence support them. This is a ceiling, not a production target; use every slot for maintenance when that is more useful. No Frozili/coffee-candy new-content slots remain.

The November 9 inventory is a starting backlog, not a permanent count: 223 articles, 86 without current keyword/date metadata, and 219 without the new raster-image metadata (161 SVG illustrations and 58 title blocks). Four Frozili articles already have new editorial images. Recount after approved releases rather than reporting these figures as live totals.

## Rolling weekly queue

The daily task completes one bounded, reviewable unit at 09:00 America/Los_Angeles, automatically releasing routine maintenance after verification Monday through Saturday. On Sunday it performs read-only checks and queue cleanup. The weekly read-only task reviews results for the user each Sunday at 16:00 in the same time zone. Both continue without an automatic end date.

| Day | Default daily work |
| --- | --- |
| Monday | Review the current queue; repair missing metadata or verify unsupported claims on one useful existing article. |
| Tuesday | Replace one old article image and synchronize its visible and social metadata. |
| Wednesday | Improve one utility article and its contextual links; consider an eligible non-Frozili brief only when evidence supports a distinct need. |
| Thursday | Refresh another existing article or replace its old image. |
| Friday | Check live availability, representative redirects/canonicals, assets, validation and dependency maintenance; prepare specific local fixes when authorized. |
| Saturday | Finish the highest-priority reviewable item or an evidenced non-Frozili brief; do not accumulate another overlapping draft. |
| Sunday | Daily: read-only checks and queue cleanup. Weekly: compare the last seven days, review automatic releases and any separately gated items, and set the next week's priorities for human review. |

A verified failure takes priority over the default day. Do not bulk-rewrite articles or change dates to meet a quota. Keep each change small enough for one traceable release and the weekly human review.

## Evidence, approvals and validation

- Read current files and inspect `git status`, the branch, recent commits and the actual diff first. Memory is historical context. Do not keep an obsolete blocker after the relevant change has been committed or explicitly approved; do not treat an unrelated untracked file as an unapproved content draft. Preserve unrelated work and isolate the intended release source from concurrent drafts. Do not automatically publish overlapping or unknown-ownership earlier edits; if ownership or safe isolation cannot be established, stop that release for review.
- Read GSC only when available. On `payment_required`, `subscription_required`, permission or connection failures, record the dated error and missing metrics, then continue useful local checks and evidence-supported maintenance. Do not invent traffic, indexing, CTR, overlap or demand evidence, reuse old values as current, or repeatedly retry the same failure in a run.
- Under the user's November 10 standing authorization, routine bounded B2C maintenance can automatically commit only intended files, run `git push origin main`, deploy the exact verified source to the existing Cloudflare site and verify live responses. Do not wait for a new per-release approval within this scope. GSC writes (including sitemap submission), published-URL consolidation/deletion/redirects, permission/credential/Git-remote changes and unrelated online Cloudflare configuration still need separate explicit approval. Both Sunday tasks remain read-only.
- Preserve original publication dates and URLs. Follow the current generated-image, caption, cover-variety, shared-navigation and direct official-brand-link rules. Source changing facts from reliable primary material; never invent product tests or measurements.
- For content edits, run `python3 scripts/build-vitablabla.py`, `python3 scripts/validate-static-seo.py`, `python3 scripts/validate-cover-themes.py`, and `git diff --check`. Before automatic publication, also pass applicable tests and the deployment dry-run, affected desktop/mobile browser checks of pages, images and neighboring covers, and review of the exact isolated source. If a required check is unavailable, retain the change locally and report the limitation. On a read-only review, do not run the build because it rewrites files. Stop on validation, push or deployment failure.
- Report the prepared/published/blocked URLs separately, changed files, evidence and missing data, checks, remaining risks, commits, deployment/live verification and any action still requiring separate approval. Keep release records available for weekly human review. A successful task run alone does not mean new content was published. Weekly reviews remain read-only and may propose zero new briefs.

Keep the November 12 recovery-cycle report as a historical checkpoint. Assess later results with settled data and rolling cohorts; never declare SEO success from a few days of movement. Continue until the user changes or pauses the tasks.
