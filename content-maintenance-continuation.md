# Vitablabla continuing maintenance plan

Approved continuation: November 9, 2026. Effective November 13, 2026, with no fixed end date.

`content-plan-2026-10-14-to-2026-11-12.md` remains the historical recovery plan through November 12. From November 13, use this plan, the current `README.md`, and `vitablabla-content-rules.md`; do not repeat expired calendar slots or stop because the old cycle ended.

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

The daily task prepares one bounded, reviewable unit at 09:00 America/Los_Angeles. The weekly task reviews results each Sunday at 16:00 in the same time zone. Both continue without an automatic end date.

| Day | Default daily work |
| --- | --- |
| Monday | Review the current queue; repair missing metadata or verify unsupported claims on one useful existing article. |
| Tuesday | Replace one old article image and synchronize its visible and social metadata. |
| Wednesday | Improve one utility article and its contextual links; consider an eligible non-Frozili brief only when evidence supports a distinct need. |
| Thursday | Refresh another existing article or replace its old image. |
| Friday | Check live availability, representative redirects/canonicals, assets, validation and dependency maintenance; prepare specific local fixes when authorized. |
| Saturday | Finish the highest-priority reviewable item or an evidenced non-Frozili brief; do not accumulate another overlapping draft. |
| Sunday | Daily: read-only checks and queue cleanup. Weekly: compare the last seven days, review pending approval items and set the next week's priorities. |

A verified failure takes priority over the default day. Do not bulk-rewrite articles or change dates to meet a quota. Keep each prepared change small enough for one approval decision.

## Evidence, approvals and validation

- Read current files and inspect `git status`, the branch, recent commits and the actual diff first. Memory is historical context. Do not keep an obsolete blocker after the relevant change has been committed or explicitly approved; do not treat an unrelated untracked file as an unapproved content draft. Preserve unrelated work and stop overlapping or unknown-ownership edits for review.
- Read GSC only when available. On `payment_required`, `subscription_required`, permission or connection failures, record the dated error and missing metrics, then continue useful local checks and evidence-supported maintenance. Do not invent traffic, indexing, CTR, overlap or demand evidence, reuse old values as current, or repeatedly retry the same failure in a run.
- Scheduled tasks prepare and validate only. They do not commit, push, deploy, delete published URLs, change credentials/permissions/remotes or online Cloudflare settings, or write to GSC. Publication needs explicit human approval in the current conversation; GSC writes and consolidation, deletion or redirects of published URLs need separate approval. This continuation does not grant automatic publication.
- Preserve original publication dates and URLs. Follow the current generated-image, caption, cover-variety, shared-navigation and direct official-brand-link rules. Source changing facts from reliable primary material; never invent product tests or measurements.
- For content edits, run `python3 scripts/build-vitablabla.py`, `python3 scripts/validate-static-seo.py`, `python3 scripts/validate-cover-themes.py`, and `git diff --check`. Verify affected desktop/mobile pages, images and neighboring covers when browser access is available; record any validation limit. On a read-only review, do not run the build because it rewrites files. Stop on validation failure.
- Report the prepared/published/blocked URLs separately, changed files, evidence and missing data, checks, remaining risks, and the exact next approval decision. A successful task run alone does not mean new content was published. Weekly reviews remain read-only and may propose zero new briefs.

Keep the November 12 recovery-cycle report as a historical checkpoint. Assess later results with settled data and rolling cohorts; never declare SEO success from a few days of movement. Continue until the user changes or pauses the tasks.
