# Vitablabla — website

Static, GitHub-Pages-ready site for [vitablabla.com](#). One source of truth for posts (`posts.json`), one folder of body files (`posts/`), one dynamic template that renders any post (`post.html?slug=…`).

## Folder map

```
.
├── index.html             home — auto-shows the 3 latest posts in the Journal section
├── about.html             company story
├── contact.html           contact form (mailto) + FAQ
├── frozili.html           Frozili brand page
├── ohcrisp.html           OhCrisp brand page
├── blog.html              journal index — auto-renders cards from posts.json
├── post.html              ONE template that renders any post via ?slug=…
├── styles.css             shared styles (typography, colors, components)
├── site.js                shared JS helpers: card rendering, date formatting, registry loader
│
├── posts.json             ⭐ the registry — every post's metadata lives here
└── posts/                 ⭐ post bodies — one HTML file per post
    ├── _template.html         copy this when starting a new post
    ├── slow-melt.html
    ├── freeze-drying-strawberry.html
    └── …                  (one file per slug in posts.json)
```

There's no build step. Open `index.html` in a browser and the site works (over `http://`, not `file://` — see below).

## How posts work

Each post = **two things**:

1. An entry in `posts.json` (metadata: title, date, color, etc.)
2. An HTML body file at `posts/<slug>.html` (the article content only — no nav, no footer)

When a user visits `post.html?slug=slow-melt`, the page:

1. Reads `posts.json` and finds the entry where `slug === 'slow-melt'`.
2. Fetches `posts/slow-melt.html` and drops its content into the article body.
3. Renders the title, crumbs, category tags, related cards, and CTA from the metadata.

So to **edit** a post you change one of those two files. To **create** a new one you add both.

## Adding a new post (your daily flow)

1. **Pick a slug.** Lowercase, hyphenated, URL-safe. e.g. `2026-05-08-cherry-season` or `cherry-season`.
2. **Copy the template:**
   ```bash
   cp posts/_template.html posts/cherry-season.html
   ```
   Open it and replace the placeholder text with your post. The first paragraph automatically gets the dropcap. See `posts/_template.html` for every available block (h2, blockquote, list, figure, pull-quote).
3. **Add an entry to the top of the `posts` array in `posts.json`:**
   ```json
   {
     "slug": "cherry-season",
     "number": "015",
     "title": "Cherries, briefly: the <em>two-week window.</em>",
     "cardTitle": "Cherries, briefly: the <em>two-week window.</em>",
     "excerpt": "On the small panic of stone-fruit season, and what we freeze-dry first.",
     "date": "2026-05-08",
     "readTime": "4 min",
     "color": "tb-pop",
     "categories": ["OhCrisp", "Freeze-Dried Fruit"],
     "crumbs": ["OhCrisp", "Freeze-Dried Fruit"],
     "cta": "ohcrisp",
     "related": ["ugly-mango", "freeze-drying-strawberry", "how-ohcrisp-is-made"]
   }
   ```
4. **Commit and push:**
   ```bash
   git add posts.json posts/cherry-season.html
   git commit -m "post: cherries, briefly"
   git push
   ```
   GitHub Pages picks it up in ~30 seconds.

The home page's Journal section, the blog index, and any related-card slot that points to it will all update automatically — there is **nothing else to edit**.

### Field reference for `posts.json` entries

| Field | Required | Notes |
|---|---|---|
| `slug` | ✅ | URL-safe ID. Must match the body filename: `posts/<slug>.html`. |
| `number` | ✅ | Display number, e.g. `"015"`. Shown in the title-block top-left. |
| `title` | ✅ | Full headline shown on the post page. Use `<em>…</em>` for italic accents. |
| `cardTitle` | optional | Shorter version for cards. Falls back to `title` if omitted. |
| `excerpt` | ✅ | One-sentence card description. Plain text. |
| `date` | ✅ | ISO format `YYYY-MM-DD`. Used for sorting (newest first). |
| `readTime` | ✅ | e.g. `"4 min"`. Shown on cards and in the post meta row. |
| `color` | ✅ | Title-block tone. One of: `tb-ice tb-coffee tb-blush tb-peach tb-sun tb-sage tb-violet tb-cream tb-pop`. |
| `categories` | ✅ | Array of category labels. The first one is the "primary" shown on cards. Used by the chip filter on `blog.html`. |
| `crumbs` | optional | Breadcrumbs above the post title. Defaults to no extra crumbs. |
| `cta` | optional | `"frozili"` or `"ohcrisp"` — picks the colored CTA strip at the bottom of the post. Defaults to `"frozili"`. |
| `related` | optional | Array of 3 slugs for the "Keep reading" section. If omitted, the 3 next-newest posts are used. |

### Categories shown on the blog filter

Edit the `categories` array under `settings`'s sibling `categories` in `posts.json` to add/remove chips on `blog.html`. They're matched against each post's `categories` array.

## Editing an existing post

- **Body changes** → edit `posts/<slug>.html`.
- **Title, date, category, color, related, etc.** → edit the post's entry in `posts.json`.

Then commit and push — same as above.

## Renaming or deleting a post

- **Rename:** change the `slug` in `posts.json`, then `git mv posts/old-slug.html posts/new-slug.html`. Any link with `?slug=old-slug` will break — update those if you've shared them.
- **Delete:** remove the entry from `posts.json` *and* delete the body file. Also remove any `related: ["…"]` references to the deleted slug in other entries.

## Running the site locally

The site uses `fetch()` to load `posts.json`, which doesn't work over `file://`. You need a local web server. Easiest options:

```bash
# Python 3
python3 -m http.server 8000

# Node (if you have it)
npx serve .
```

Then open <http://localhost:8000>.

## Deploying to GitHub Pages

1. Push this folder to a GitHub repo (any name — usually `<your-username>.github.io` for a personal site, or any repo for a project site).
2. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / root**.
3. Wait ~30 seconds. The site goes live at `https://<username>.github.io/<repo>/` (or your custom domain if configured).

The empty `.nojekyll` file in this folder tells GitHub Pages to skip Jekyll processing — important so paths like `posts/_template.html` (leading underscore) are still served.

### Custom domain

To use `vitablabla.com`:

1. Add a `CNAME` file with the single line `vitablabla.com`.
2. Configure your DNS at the registrar to CNAME `www` to `<username>.github.io` and add A records for the apex per [GitHub's docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
3. In **Settings → Pages**, set the custom domain. Enable "Enforce HTTPS" once the cert provisions.

## Common gotchas

- **A new post isn't showing up.** Check that the `slug` in `posts.json` exactly matches the filename in `posts/`. Also check `posts.json` is valid JSON — a stray comma will break the whole site. Paste it into <https://jsonlint.com/> if unsure.
- **The post page says "Body content for this post is missing."** The metadata is there but the file `posts/<slug>.html` isn't. Add it.
- **The "Keep reading" cards point to broken posts.** A `related` slug in `posts.json` doesn't exist anymore. Update or remove it.
- **Site works locally but breaks on GitHub Pages.** Probably a path issue. All paths in this site are relative (no leading `/`), which is correct for project pages. If you're at a custom domain root, both forms work.
