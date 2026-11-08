# Vitablabla website

Static Vitablabla brand site and Journal, deployed to Cloudflare Workers with static assets.

## Architecture

- `posts.json` is the metadata registry and source of truth.
- `posts/<slug>.html` contains each article body fragment.
- `scripts/build-vitablabla.py` validates the registry and bodies, pre-renders a complete crawlable page at `a/<slug>/index.html`, and regenerates `sitemap.xml`.
- Public article URLs use `https://vitablabla.com/a/<slug>/`.
- `worker.js` permanently redirects legacy `post.html?slug=<slug>` links to the clean article URL.
- `site.js` renders home, Journal, and related cards with clean article links.

The generated article pages contain the complete body, title, description, canonical URL, Open Graph/Twitter metadata, and Article, Breadcrumb, and visible FAQ structured data before JavaScript runs.

## Add a Journal post

1. Copy `posts/_template.html` to `posts/<slug>.html` and write the body.
2. Add a matching entry to the top of the `posts` array in `posts.json`.
3. Include `primaryKeyword`, `secondaryKeywords`, and `dateModified` for every new post. Add `faqs` only when the body contains a useful matching Q&A section.
4. Use `/a/<slug>/` for article links and root-relative clean links such as `/ohcrisp` and `/frozili`.
5. Run:

   ```bash
   python3 scripts/build-vitablabla.py
   python3 scripts/validate-static-seo.py
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

FAQ metadata should mirror the visible FAQ section. The build uses visible FAQ copy for structured data when old metadata differs, and renders metadata as visible content when an older body has no FAQ section.

## Local preview

The site uses `fetch()` on the home and Journal pages, so preview it through HTTP:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. A generated article is available at `http://localhost:8000/a/<slug>/`.

## Validation and deployment

Install the pinned Wrangler dependency once with `npm install`, then validate without publishing:

```bash
npx wrangler deploy --dry-run
```

Deploy the validated source with:

```bash
npx wrangler deploy
```

Cloudflare account selection is fixed in `wrangler.jsonc`. Never commit secrets or authentication tokens.

## Important files

- `index.html`, `home.css`, `home.js`: brand-first homepage, responsive navigation, interactive freeze-drying explainer, and Journal preview. The four brand doors link directly to ohcrisp.com, getohsip.com, drinkohviva.com, and frozili.com. Homepage styles are scoped to `.brand-house`.
- `assets/brands/`: optimized WebP versions of the brands' existing public product imagery. Source URLs are recorded in `scripts/homepage-assets.json`. OHSIP's supplied front/back artwork is framed with CSS; product photography is not regenerated.
- The homepage includes three static Journal cards for crawling and offline/error fallback; JavaScript refreshes them from published entries in `posts.json`.

- `robots.txt`: crawler permissions and sitemap location.
- `_headers`: prevents raw body fragments under `/posts/*` from being indexed.
- `.assetsignore`: prevents source, dependencies, and deployment files from being published as static assets.
- `vitablabla-content-rules.md`: editorial, SEO, GEO, metadata, and linking rules.
