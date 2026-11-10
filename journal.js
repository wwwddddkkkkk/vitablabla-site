(async function () {
  let reg;

  try {
    reg = await VB.loadRegistry();
    // A broken but successful JSON response must not erase the built archive.
    if (!reg || !Array.isArray(reg.categories) || !Array.isArray(reg.posts) || !reg.posts.length ||
        !reg.posts.every(post => post && ['slug', 'date', 'number', 'title'].every(key => typeof post[key] === 'string') &&
          Array.isArray(post.categories))) {
      throw new Error('Invalid Journal registry');
    }
  } catch (e) {
    console.warn('Journal filters unavailable; keeping the complete static archive.', e);
    return;
  }

  const allPosts = VB.sortByDateDesc(reg.posts || []);

  // Build category chips from settings.
  const chipsRoot = document.getElementById('catsRow');
  (reg.categories || []).forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'chip';
    btn.dataset.cat = cat;
    btn.setAttribute('aria-pressed', 'false');
    btn.textContent = cat;
    chipsRoot.appendChild(btn);
  });

  let activeCat = '';
  let searchTerm = '';

  function matches(post) {
    if (activeCat && !(post.categories || []).includes(activeCat)) return false;
    if (searchTerm) {
      const hay = [post.title, post.cardTitle, post.excerpt, (post.categories || []).join(' ')].join(' ').toLowerCase();
      if (!hay.includes(searchTerm)) return false;
    }
    return true;
  }

  function render() {
    const visible = VB.arrangeCovers(allPosts.filter(matches));
    const featSlot = document.getElementById('featuredSlot');
    const grid = document.getElementById('articleGrid');
    const count = document.getElementById('countLabel');

    count.textContent = visible.length + ' ARTICLES';

    if (visible.length === 0) {
      featSlot.innerHTML = '';
      grid.innerHTML = '<div class="empty">Nothing here yet. Try another category.</div>';
      return;
    }

    // Featured = first match (when no filter, this is the latest post).
    const featured = visible[0];
    featSlot.innerHTML = `
      <div class="title-block hero ${VB.coverClass(featured)}">
        <div class="tb-top">
          <span class="tb-num">No. ${featured.number} &middot; ${(featured.categories || []).join(' / ')}</span>
          <span class="tb-num">${featured.readTime || ''} read &middot; ${VB.formatDateLong(featured.date)}</span>
        </div>
        <h2 class="tb-title">${(featured.title || '').replace(/<em>/g,'<span class="ital">').replace(/<\/em>/g,'</span>')}</h2>
        <div class="tb-bottom">
          <a href="${VB.postURL(featured.slug)}" class="cta-pill">Read the article <span class="arrow">↗</span></a>
          <span>The Vitablabla Journal</span>
        </div>
      </div>
    `;

    // Grid = the rest.
    const rest = visible.slice(1);
    grid.innerHTML = rest.length
      ? rest.map(VB.cardHTML).join('')
      : '<div class="empty">Just the featured one for now.</div>';
  }

  chipsRoot.addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    chipsRoot.querySelectorAll('.chip').forEach(c => { c.classList.remove('active'); c.setAttribute('aria-pressed', 'false'); });
    chip.classList.add('active');
    chip.setAttribute('aria-pressed', 'true');
    activeCat = chip.dataset.cat || '';
    render();
  });

  document.getElementById('searchInput').addEventListener('input', e => {
    searchTerm = e.target.value.trim().toLowerCase();
    render();
  });

  render();
  document.getElementById('searchInput').disabled = false;
  chipsRoot.querySelectorAll('.chip').forEach(chip => { chip.disabled = false; });
})();
