# Vitablabla website

Static Vitablabla brand site and Journal, deployed to Cloudflare Workers with static assets.

## Architecture

- `posts.json` is the metadata registry and source of truth.
- `posts/<slug>.html` contains each article body fragment.
- `scripts/build-vitablabla.py` validates the registry and bodies, pre-renders a complete crawlable page at `a/<slug>/index.html`, and regenerates `sitemap.xml`.
- Public article URLs use `https://vitablabla.com/a/<slug>/`.
- `worker.js` permanently redirects legacy `post.html?slug=<slug>` links to the clean article URL.
- Public HTTP and `www` requests redirect with 308 to `https://vitablabla.com`, preserving their path and query string. The Worker runs before assets so existing files cannot bypass normalization; localhost and Workers preview hosts remain usable.
- `site.js` renders home, Journal, and related cards with clean article links.
- The build also pre-renders the complete Journal archive in `blog.html`, including its featured article, ordered cards, cover mix and count. Every registered article is reachable from the homepage via `/blog` without JavaScript. `journal.js` enhances that same list with category filters and search; a registry failure leaves the full static archive available.

The generated article pages contain the complete body, title, description, canonical URL, Open Graph/Twitter metadata, and Article, Breadcrumb, and visible FAQ structured data before JavaScript runs.

## Add a Journal post

1. Generate and inspect a topic-specific editorial image with the built-in image-generation tool, save an optimized asset under `assets/editorial/`, and record it in `scripts/journal-image-assets.json`. Copy `posts/_template.html` to `posts/<slug>.html` and write the body.
2. Add a matching entry to the top of the `posts` array in `posts.json`.
3. Include `primaryKeyword`, `secondaryKeywords`, and `dateModified` for every new post. Add `faqs` only when the body contains a useful matching Q&A section.
4. Use `/a/<slug>/` for article links and `/about#<brand>` for in-house brand introductions, and direct official brand URLs for shopping.
5. Run:

   ```bash
   python3 scripts/build-vitablabla.py
   python3 scripts/validate-static-seo.py
   python3 scripts/validate-cover-themes.py
   python3 scripts/test-journal-build.py
   ```

6. Do not publish if the build reports an error. Legacy metadata warnings are non-blocking.
7. Commit the body, `posts.json`, `sitemap.xml`, and the generated `a/<slug>/index.html` page.

## Metadata fields

Required registry fields: `slug`, `number`, `title`, `excerpt`, `date`, `categories`, and `cta`.

New posts should also include:

- `cardTitle`
- `readTime`
- `color`
- `crumbs`
- `related`
- `primaryKeyword`
- `secondaryKeywords`
- `faqs` (optional; must match visible Q&A copy when present)
- `dateModified`
- `image` (`src`, `alt`, `width`, `height`; required for new and substantially refreshed articles)

FAQ metadata should mirror the visible FAQ section. The build uses visible FAQ copy for structured data when old metadata differs, and renders metadata as visible content when an older body has no FAQ section.

## Local preview

The site uses `fetch()` on the home and Journal pages, so preview it through HTTP:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. A generated article is available at `http://localhost:8000/a/<slug>/`.

## Validation and deployment

The pinned Wrangler requires Node.js 22.12 or newer. Install the exact locked dependencies with `npm ci`, then validate without publishing:

```bash
npm test
npx wrangler deploy --dry-run
```

Deploy the validated source with:

```bash
npx wrangler deploy
```

Cloudflare account selection is fixed in `wrangler.jsonc`. Never commit secrets or authentication tokens.

`npm test` checks canonical redirects, path/query preservation, legacy article redirects, local previews and asset 404 responses. Review dependency updates with `npm audit` before deployment.

## Continuing maintenance

The original recovery calendar runs through November 12, 2026. From November 13, follow `content-maintenance-continuation.md` for the rolling queue of article, image, metadata, internal-link and technical maintenance. Daily preparation runs at 09:00 and the read-only weekly review runs Sundays at 16:00, both in America/Los_Angeles, without a fixed end date. Scheduled changes still require human approval before publication. Determine pending work from current Git state and current approval evidence rather than an old automation memory entry.

## Important files

- `styles.css`: shared palette tokens for the whole site, inspired by Lemme's orchid/near-white/black pairing with violet and lime accents. Home, company, Journal, contact, and generated article pages share these tokens; product artwork and brand colors remain independent.
- `index.html`, `home.css`, `home.js`: brand-first homepage with four collectible brand covers, responsive section navigation, an interactive freeze-drying explainer, and Journal preview. Covers link directly to ohcrisp.com, getohsip.com, drinkohviva.com, and frozili.com. Separate quick-look buttons open accessible brand previews with arrow-key/touch navigation, shareable `#world-<brand>` links, browser Back/Forward, and focus restoration. After the collection, `.tech-tail` alternates a dark science lab, an orchid company section with a clickable product sticker wall, a near-white Journal, and a lime contact section. Shared linework and typography connect the sections. Key panels use Lemme product-page-inspired black outlines, rounded corners, orchid selection fills, and black pill buttons. The science controller synchronizes ingredient photography, the vector chamber's scan position, process/format labels, scrubbing, steps, and finite play/pause. These labels explain the process; they are not live manufacturing measurements. Decorative motion follows the operating system’s reduced-motion preference; there is no site-level Motion toggle. Homepage styles are scoped to `.brand-house`.
- `assets/brands/`: optimized WebP versions of the brands' existing public product imagery. Source URLs are recorded in `scripts/homepage-assets.json`. OHSIP's supplied front/back artwork is framed with CSS; product photography is not regenerated.
- The homepage includes three static Journal cards for crawling and offline/error fallback; JavaScript refreshes them from published entries in `posts.json`.

- `robots.txt`: crawler permissions and sitemap location.
- `_headers`: prevents raw body fragments under `/posts/*` from being indexed.
- `.assetsignore`: prevents source, dependencies, and deployment files from being published as static assets.
- `vitablabla-content-rules.md`: editorial, SEO, GEO, metadata, and linking rules.

## House pages and navigation

- `about.html` contains all four brand introductions (`#ohcrisp`, `#ohsip`, `#ohviva`, `#frozili`). `_redirects` sends the former OhCrisp and Frozili page URLs to their sections with 301 responses.
- `pages.css` and `page.js` keep Our story, Journal, Contact and article pages aligned with the homepage's purple panels, black outlines, rounded cards and pill buttons. `scripts/site_chrome.py` derives their crawlable header and footer from the homepage during the article build. Every footer brand link goes directly to that brand's official website.
- The Contact form opens an email draft; it does not claim to send a message to a server.
- On mobile, freeze-drying controls sit between the specimen and the horizontal, snapping step cards. Phase changes scroll only the card rail. The process play/pause button remains separate from decorative motion, which follows the system setting.

Journal covers use nine content-related color families and fourteen print patterns, including cloth gingham, narrow stripes, fruit-and-ribbon prints, stars, hearts and paper collage. `covers.css` and the small native SVG tiles in `assets/covers/` provide the patterns. `VB.arrangeCovers` and `scripts/cover_theme.py` choose content- and occasion-related prints, then avoid repeating the same print or visible palette among the previous three cards. This covers one-, two- and three-column neighbors, and runs again after filtering/searching. Homepage and static related cards use the same rules. The mix is deterministic for a given displayed list; illustrated prints are counted by their actual colors. `scripts/validate-cover-themes.py` checks real category/search/related lists and browser/static parity. Keep SEO writing and publication aligned with `vitablabla-content-rules.md`.

The shared Vitablabla wordmark uses a six-armed, forked snowflake SVG, echoed in `favicon.svg`. Product cutouts use their image silhouettes, without white background wedges.

From November 10, 2026, Frozili/coffee-candy work is maintenance of existing URLs and replacement of old article art only. The November 9 guide is the final explicitly requested new draft. New and substantially refreshed articles use generated editorial raster images rather than the legacy SVG motif/title-block workflow, with matching social/Article image metadata. See `vitablabla-content-rules.md` for the current publishing and image rules.
