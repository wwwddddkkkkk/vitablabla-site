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
    'Studio Notes': 'work',
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
    return 'post.html?slug=' + encodeURIComponent(slug);
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
        <div class="title-block ${post.color || 'tb-sage'}">
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
        <div class="title-block feature ${post.color || 'tb-sage'}">
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
        <div class="title-block ${post.color || 'tb-sage'}">
          <div class="tb-top"><span class="tb-num">No. ${post.number} &middot; ${primaryCat}</span><span class="tb-num">${post.readTime || ''}</span></div>
          <h3 class="tb-title">${title.replace(/<em>/g, '<span class="ital">').replace(/<\/em>/g, '</span>')}</h3>
          <div class="tb-bottom"><span>${primaryCat}</span><span>${formatDateShort(post.date)}</span></div>
        </div>
        <p class="excerpt">${post.excerpt || ''}</p>
      </a>
    `;
  }

  async function loadRegistry() {
    return fetch('posts.json', { cache: 'no-cache' }).then(r => r.json());
  }

  return {
    tagClass,
    formatDateLong,
    formatDateShort,
    postURL,
    sortByDateDesc,
    cardHTML,
    featureCardHTML,
    sidekickCardHTML,
    loadRegistry
  };
})();
