# Vitablabla Journal Content Rules

Vitablabla Journal is the brand-house magazine for Vitablabla, Frozili, and OhCrisp. It should feel more editorial than a standard SEO blog: thoughtful, visual, lightly literary, and useful enough that someone would actually read it.

The goal is to build long-term brand taste while still supporting search discovery for Frozili icy coffee candy and OhCrisp freeze-dried fruit.

## Positioning

Vitablabla Journal is not the same as Best Snack or the Shopify blogs.

- Best Snack is an external SEO guide site. It can be more direct, searchable, and comparison-led.
- Shopify blogs are product education and conversion pages. They should answer buyer questions clearly.
- Vitablabla Journal is the brand magazine. It can tell stories, explain trends, describe taste, and make the brands feel considered.

Every Vitablabla article should still have a useful search angle, but the writing should feel like a well-edited magazine note rather than a keyword page.

## Daily Publishing Shape

Default cadence: 1 Vitablabla Journal post per day when automation is enabled.

Recommended rotation:

- 2 Frozili-leaning posts per week
- 2 OhCrisp-leaning posts per week
- 2 broad snack culture / industry / routine posts per week
- 1 founder note, studio note, trend observation, or cross-brand post per week

If another site already covered a topic that day, Vitablabla should use a different angle. For example, if Best Snack publishes "best freeze-dried fruit snacks," Vitablabla might publish "Why fruit crunch feels more joyful than chewiness."

## Article Style

The voice should be:

- aesthetic but not vague
- specific but not stiff
- lightly story-driven
- calm, clever, and sensory
- premium without sounding expensive for its own sake
- useful enough for search, but not written like an SEO checklist

Good Vitablabla sentences often start from a scene:

- "Open a snack drawer in the middle of a long workday..."
- "The first thing you notice about freeze-dried fruit is not the flavor. It is the sound."
- "Coffee has always been more than caffeine. It is a pause with a smell."

Avoid:

- generic wellness claims
- exaggerated health promises
- overusing "best" unless the article is genuinely a guide
- sounding like an ad
- stuffing brand names into every paragraph
- copying the same Shopify article structure

## SEO Philosophy

Use SEO as the spine, not the skin. Each article should have a clear search target, but the reader should not feel the keyword machinery.

Each post needs:

- one primary keyword theme
- 3 to 6 secondary keywords
- a title that can rank but still feels editorial
- a clear excerpt in `posts.json`
- category tags that match the intent
- internal links to related Vitablabla posts and brand pages
- natural mentions of Frozili and/or OhCrisp when relevant

Keyword phrases should appear naturally in:

- `title`
- `cardTitle`
- `excerpt`
- first 2 paragraphs
- at least one `h2`
- one later paragraph near the brand mention

Do not repeat the exact keyword awkwardly. Variations are better.

## Frozili SEO Themes

Use Frozili when the article touches cooling candy, coffee candy, refreshing snacks, workday rituals, dry throat moments, non-gum refreshers, summer candy, or grown-up candy alternatives.

Primary keyword pool:

- coffee candy
- iced coffee candy
- coffee flavored candy
- cooling candy
- refreshing candy
- candy for summer
- weird cold candy
- adult candy
- candy for dry throat
- non gum refresher
- mint alternative
- breath freshening candy
- workday pick me up
- pocket candy
- slow melting candy

Natural brand language:

- Frozili icy coffee candy
- coffee flavor with a cooling finish
- a small reset, not a snack replacement
- slow-melting refresh candy
- coffee, icy, soothing, slow melt

Frozili should feel like a small ritual: after lunch, before a meeting, during a long drive, between tasks, or when someone wants a cleaner finish without another drink.

## OhCrisp SEO Themes

Use OhCrisp when the article touches freeze-dried fruit, crunchy fruit snacks, healthy-looking snacks, toppings, breakfast bowls, lunchboxes, snack boards, travel snacks, or colorful modern snacking.

Primary keyword pool:

- freeze-dried fruit
- freeze dried fruit snacks
- healthy snack
- healthy sweet snack
- crunchy fruit snack
- fruit snack for adults
- yogurt bowl toppings
- smoothie bowl toppings
- oatmeal toppings
- lunchbox snacks
- travel-friendly fruit snacks
- shelf-stable fruit snacks
- dessert toppings
- snack mix ideas

Natural brand language:

- OhCrisp freeze-dried fruit
- real fruit crunch
- colorful, playful fruit snacks
- a crunchy way to make simple routines feel brighter
- freeze-dried fruit for bowls, boards, and everyday snacking

OhCrisp should feel colorful, textural, bright, and fun without becoming childish.

## Broad Vitablabla Themes

These articles can mention both brands or neither at first, then connect them near the end.

Strong themes:

- why modern snacks are becoming more sensory
- how snack brands are moving beyond basic candy
- texture as a reason people remember snacks
- the rise of small rituals in busy routines
- how premium snacks use format, flavor, and occasion
- why adults want playful snacks too
- how convenience snacks are becoming more beautiful
- snack culture for work, travel, and home

Good SEO phrases:

- modern snack brands
- premium snacks
- better-for-you snacks
- snack trends
- healthy snacks for adults
- workday snacks
- travel snacks
- functional snacks
- sensory snacks
- snack ideas

## Post Structure

Each new post needs two files:

1. A metadata entry at the top of `posts.json`
2. A matching body file at `posts/<slug>.html`

Use the existing HTML style from `posts/_template.html`.

Preferred body structure:

- opening scene with `p.dropcap`
- 1 short framing paragraph
- one memorable `blockquote`
- 3 to 5 sections with `h2`
- one visual `figure` using `.title-block`
- one ordered or unordered list when useful
- one `pull-quote` only if the idea is strong
- closing paragraph with a soft brand or related-post link

Do not use a hard Shopify-style CTA block inside the body. The site already renders the CTA from `posts.json`.

## Metadata Rules

Add every new post to the top of the `posts` array in `posts.json`.

Required fields:

- `slug`: lowercase, hyphenated, URL-safe
- `number`: next number after the latest article
- `title`: full title, can use `<em>` for the emotional or aesthetic accent
- `cardTitle`: shorter title for cards
- `excerpt`: one useful search-friendly sentence
- `date`: current date in `YYYY-MM-DD`
- `readTime`: usually `4 min` or `5 min`
- `color`: choose from `tb-ice`, `tb-coffee`, `tb-blush`, `tb-peach`, `tb-sun`, `tb-sage`, `tb-violet`, `tb-cream`, `tb-pop`
- `categories`: 1 to 3 categories
- `crumbs`: usually same as categories
- `cta`: `frozili` or `ohcrisp`
- `related`: 3 valid existing slugs

Use `cta: "frozili"` for Frozili and broad cooling/coffee/workday posts.
Use `cta: "ohcrisp"` for fruit, crunch, toppings, bowls, and colorful snack posts.

## Category Use

Preferred categories:

- `Frozili`
- `Coffee Candy`
- `Refreshing Snacks`
- `OhCrisp`
- `Freeze-Dried Fruit`
- `Snack Ideas`
- `Better-for-You`
- `Travel & Work`

If a new category is needed, add it to the top-level `categories` array in `posts.json` so it appears in the blog filter.

## Internal Linking

Each article should include 2 to 4 internal links when natural.

Useful links:

- `frozili.html`
- `ohcrisp.html`
- `post.html?slug=slow-melt`
- `post.html?slug=cold-brew-tasting`
- `post.html?slug=freeze-drying-strawberry`
- `post.html?slug=ugly-mango`
- `post.html?slug=snack-drawer`
- `post.html?slug=twelve-hour-flight`
- `post.html?slug=better-for-you-words`

Internal links should feel like editorial references, not forced SEO links.

## Topic Queue

Frozili-leaning ideas:

- Why iced coffee flavor works so well in candy
- Why cooling candy feels especially good in summer
- The strange pleasure of weird cold candy
- Why adults are looking for alternatives to basic mints
- What makes a small treat feel workday-friendly
- Why slow-melting candy feels more like a ritual
- The difference between a snack and a reset
- Why coffee flavor feels grown-up in candy

OhCrisp-leaning ideas:

- Why freeze-dried fruit makes better snack mixes
- Why fruit crunch feels more satisfying than chewiness
- What makes freeze-dried fruit feel premium
- Colorful snacks and the psychology of better routines
- Why healthy snacks still need to be fun
- The rise of fruit snacks for adults
- How freeze-dried fruit became a bowl topping staple
- Why snack boards are better with texture

Broad Vitablabla ideas:

- Why modern snacks are becoming more sensory
- The quiet return of small food rituals
- What makes a snack brand feel memorable
- Why playful snacks are not just for kids
- The new snack shelf: less filler, more feeling
- What "premium snack" actually means now
- Why texture is becoming the new flavor
- How workday snacks became part of personal style

## Quality Bar

Before finishing a Vitablabla post, check:

- Is the title searchable and beautiful?
- Does the first paragraph create a scene?
- Does the post have one useful idea, not just nice words?
- Are Frozili or OhCrisp mentioned naturally where relevant?
- Are the internal links valid?
- Does `posts.json` remain valid JSON?
- Does the body file exist at the matching slug?
- Does the post avoid repeating topics already published?

The reader should leave with a small new way of seeing snacks.
