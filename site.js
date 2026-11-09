/* Vitablabla — shared client helpers used by blog.html, post.html, index.html. */

window.VB = (function () {

  const TAG_CLASS = {
    'Frozili': 'frozili',
    'OhCrisp': 'ohcrisp',
    'Coffee Candy': 'coffee',
    'Freeze-Dried Fruit': 'fruit',
    'Refreshing Snacks': 'refresh',
    'Travel & Work': 'travel',
    'Travel & Work Snacks': 'travel',
    'Workday Snacks': 'work',
    'Taste Notes': 'work',
    'Notes': 'work',
    'Better-for-You': 'bfu',
    'Snack Ideas': 'work'
  };

  const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const SHORT_MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  function tagClass(label) {
    return TAG_CLASS[label] || 'work';
  }

  function formatDateLong(iso) {
    if (!iso) return '';
    const [y, m, d] = iso.split('-').map(Number);
    return MONTHS[m - 1] + ' ' + d + ', ' + y;
  }

  function formatDateShort(iso) {
    if (!iso) return '';
    const [y, m, d] = iso.split('-').map(Number);
    return SHORT_MONTHS[m - 1] + ' ' + String(d).padStart(2, '0');
  }

  function postURL(slug) {
    return '/a/' + encodeURIComponent(slug) + '/';
  }

  // Content chooses the print collection; displayed neighbors choose the final mix.
  // Keep these recipes aligned with scripts/cover_theme.py.
  const coverPatterns = ['checker', 'gingham', 'pinstripe', 'diagonal', 'dots', 'stars', 'citrus', 'berry-ribbon', 'cherry-check', 'heart-gingham', 'patchwork', 'wavy-check', 'cocoa-dots', 'stripes'];
  const coverColors = ['tb-ice', 'tb-coffee', 'tb-blush', 'tb-peach', 'tb-sun', 'tb-sage', 'tb-violet', 'tb-cream', 'tb-pop'];
  const fixedCoverColors = {stars:'tb-sun', citrus:'tb-sun', 'berry-ribbon':'tb-blush', 'cherry-check':'tb-ice', 'wavy-check':'tb-ice', patchwork:'tb-pop', 'cocoa-dots':'tb-coffee'};
  function coverOptions(post) {
    const slug = post.slug || '';
    const seed = [...slug].reduce((sum, char, index) => sum + (index + 1) * char.charCodeAt(0), 0);
    let patterns = coverPatterns, colors = coverColors;
    if (/rehydrat|sublimat|freeze-drying|how-ohcrisp-is-made/.test(slug)) {
      patterns = ['wavy-check', 'checker', 'diagonal', 'pinstripe', 'dots', 'gingham'];
      colors = ['tb-ice', 'tb-sage', 'tb-violet', 'tb-cream'];
    } else if (/strawberry|berry|acai|yogurt/.test(slug)) {
      patterns = ['berry-ribbon', 'cherry-check', 'heart-gingham', 'gingham', 'pinstripe', 'checker'];
      colors = ['tb-blush', 'tb-ice', 'tb-violet', 'tb-cream', 'tb-peach'];
    } else if (/mango|pineapple|citrus|tropical|lemonade/.test(slug)) {
      patterns = ['citrus', 'gingham', 'stripes', 'checker', 'pinstripe', 'dots'];
      colors = ['tb-sun', 'tb-peach', 'tb-sage', 'tb-ice', 'tb-cream'];
    } else if (/(^|-)(tea|ohviva)(-|$)/.test(slug)) {
      patterns = ['citrus', 'gingham', 'pinstripe', 'wavy-check', 'dots', 'checker'];
      colors = ['tb-sage', 'tb-ice', 'tb-sun', 'tb-peach', 'tb-cream'];
    } else if (/coffee|espresso|ohsip|frozili|slow-melt/.test(slug)) {
      patterns = ['cocoa-dots', 'pinstripe', 'heart-gingham', 'diagonal', 'gingham', 'dots'];
      colors = ['tb-coffee', 'tb-cream', 'tb-ice', 'tb-violet', 'tb-peach'];
    } else if (/freeze-dried-fruit|fruit-crunch|fruit-snack/.test(slug)) {
      patterns = ['gingham', 'cherry-check', 'checker', 'citrus', 'berry-ribbon', 'heart-gingham', 'pinstripe', 'diagonal', 'dots', 'wavy-check'];
      colors = ['tb-peach', 'tb-blush', 'tb-sun', 'tb-sage', 'tb-ice', 'tb-cream'];
    }
    if (/red-eye|night|stargaz|evening|movie|theatre|theater/.test(slug)) {
      patterns = ['stars', 'dots', 'pinstripe', 'checker', 'diagonal', 'gingham'];
      colors = ['tb-violet', 'tb-ice', 'tb-cream', 'tb-coffee', 'tb-blush'];
    } else if (/airplane|airport|road-trip|travel|hotel|flight|train|commute/.test(slug)) {
      patterns = ['patchwork', 'stars', 'wavy-check', 'stripes', 'dots', 'pinstripe', 'gingham'];
      colors = ['tb-ice', 'tb-sun', 'tb-sage', 'tb-cream', 'tb-violet'];
    } else if (/beach|pool|summer|picnic|outdoor|camp|hiking|lake|heatwave/.test(slug)) {
      patterns = ['stripes', 'gingham', 'dots', 'checker', 'pinstripe', 'wavy-check'];
      colors = ['tb-sun', 'tb-ice', 'tb-sage', 'tb-peach', 'tb-cream'];
    } else if (/chocolate|smores|hot-chocolate/.test(slug)) {
      patterns = ['cocoa-dots', 'diagonal', 'heart-gingham', 'pinstripe', 'gingham', 'checker'];
      colors = ['tb-coffee', 'tb-cream', 'tb-peach', 'tb-blush', 'tb-violet'];
    }
    else if (/bagel|toast|pancake|waffle|oat|cereal|grain-bowl|muffin|crepe|scone|bread/.test(slug)) {
      patterns = ['gingham', 'checker', 'heart-gingham', 'cherry-check', 'pinstripe', 'berry-ribbon'];
      colors = ['tb-peach', 'tb-blush', 'tb-ice', 'tb-cream', 'tb-sage'];
    }
    if (colors.includes(post.color)) colors = [post.color, ...colors.filter(color => color !== post.color)];
    let offset = seed % patterns.length;
    patterns = [...patterns.slice(offset), ...patterns.slice(0, offset)];
    offset = Math.floor(seed / 7) % colors.length;
    colors = [...colors.slice(offset), ...colors.slice(0, offset)];
    const options = [];
    patterns.forEach((pattern, pi) => colors.forEach((palette, ci) => {
      const color = fixedCoverColors[pattern] || palette;
      if (!options.some(option => option.pattern === pattern && option.color === color)) {
        options.push({pattern, color, rank:pi * 3 + ci});
      }
    }));
    return options;
  }
  function themeClass(theme) { return `content-cover ${theme.color} pattern-${theme.pattern}`; }
  function coverClass(post) { return post.coverTheme || themeClass(coverOptions(post)[0]); }
  function arrangeCovers(posts) {
    const chosen = [];
    return posts.map(post => {
      const neighbors = chosen.slice(-3).reverse();
      const score = option => neighbors.reduce((sum, neighbor, index) => sum + (3 - index) *
        (200 * Number(option.pattern === neighbor.pattern) + 160 * Number(option.color === neighbor.color)), option.rank);
      const theme = coverOptions(post).reduce((best, option) => score(option) < score(best) ? option : best);
      chosen.push(theme);
      return {...post, coverTheme:themeClass(theme)};
    });
  }

  // Sort posts: newest first by date, ties broken by number desc.
  function sortByDateDesc(posts) {
    return posts.slice().sort((a, b) => {
      if (a.date < b.date) return 1;
      if (a.date > b.date) return -1;
      return (b.number || '').localeCompare(a.number || '');
    });
  }

  // HTML for a card used in blog grid + related sections + home journal section.
  function cardHTML(post) {
    const title = post.cardTitle || post.title;
    const primaryCat = (post.categories && post.categories[0]) || '';
    return `
      <a class="article" href="${postURL(post.slug)}">
        <div class="title-block ${coverClass(post)}">
          <div class="tb-top"><span class="tb-num">No. ${post.number}</span><span class="tb-num">${post.readTime || ''}</span></div>
          <h3 class="tb-title">${title.replace(/<em>/g, '<span class="ital">').replace(/<\/em>/g, '</span>')}</h3>
          <div class="tb-bottom"><span>${primaryCat}</span><span>${formatDateShort(post.date)}</span></div>
        </div>
        <p>${post.excerpt || ''}</p>
      </a>
    `;
  }

  // HTML for the homepage's larger feature card (used for the latest post).
  function featureCardHTML(post) {
    const title = post.cardTitle || post.title;
    const primaryCat = (post.categories && post.categories[0]) || '';
    return `
      <a class="article-card feature" href="${postURL(post.slug)}">
        <div class="title-block feature ${coverClass(post)}">
          <div class="tb-top"><span class="tb-num">No. ${post.number} &middot; ${primaryCat}</span><span class="tb-num">${post.readTime || ''} read</span></div>
          <div class="tb-glyph"></div>
          <h3 class="tb-title large">${title.replace(/<em>/g, '<span class="ital">').replace(/<\/em>/g, '</span>')}</h3>
          <div class="tb-bottom"><span>${primaryCat}</span><span>${formatDateShort(post.date)}, ${post.date.slice(0,4)}</span></div>
        </div>
        <p class="excerpt">${post.excerpt || ''}</p>
      </a>
    `;
  }

  // Smaller home-journal sidekick card (matches .article-card without .feature).
  function sidekickCardHTML(post) {
    const title = post.cardTitle || post.title;
    const primaryCat = (post.categories && post.categories[0]) || '';
    return `
      <a class="article-card" href="${postURL(post.slug)}">
        <div class="title-block ${coverClass(post)}">
          <div class="tb-top"><span class="tb-num">No. ${post.number} &middot; ${primaryCat}</span><span class="tb-num">${post.readTime || ''}</span></div>
          <h3 class="tb-title">${title.replace(/<em>/g, '<span class="ital">').replace(/<\/em>/g, '</span>')}</h3>
          <div class="tb-bottom"><span>${primaryCat}</span><span>${formatDateShort(post.date)}</span></div>
        </div>
        <p class="excerpt">${post.excerpt || ''}</p>
      </a>
    `;
  }

  async function loadRegistry() {
    try {
      const response = await fetch('posts.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error('Could not load posts.json');
      return response.json();
    } catch (fetchError) {
      return new Promise((resolve, reject) => {
        const request = new XMLHttpRequest();
        request.overrideMimeType('application/json');
        request.open('GET', 'posts.json', true);
        request.onload = () => {
          if (request.status === 0 || (request.status >= 200 && request.status < 300)) {
            try {
              resolve(JSON.parse(request.responseText));
            } catch (parseError) {
              reject(parseError);
            }
          } else {
            reject(fetchError);
          }
        };
        request.onerror = () => reject(fetchError);
        request.send();
      });
    }
  }

  return {
    tagClass,
    formatDateLong,
    formatDateShort,
    postURL,
    coverClass,
    arrangeCovers,
    sortByDateDesc,
    cardHTML,
    featureCardHTML,
    sidekickCardHTML,
    loadRegistry
  };
})();
