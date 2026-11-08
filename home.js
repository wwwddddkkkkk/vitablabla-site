/* Progressive enhancements; brand links and editorial cards work without JS. */
(() => {
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  function closeMenu() {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    menu.hidden = true;
  }
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    toggle.setAttribute('aria-label', expanded ? 'Open navigation' : 'Close navigation');
    menu.hidden = expanded;
  });
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !menu.hidden) {
      closeMenu();
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 681px)').addEventListener('change', (event) => {
    if (event.matches) closeMenu();
  });

  const phases = {
    freeze: ['01 / FREEZE', 'First, a little chill.'],
    vacuum: ['02 / SUBLIMATE', 'Water out. Possibility in.'],
    enjoy: ['03 / REDISCOVER', 'Same fruit. A whole new crunch.']
  };
  const visual = document.querySelector('.science-visual');
  const steps = document.querySelectorAll('.science-step');
  steps.forEach((step) => {
    step.addEventListener('click', () => {
      const phase = step.dataset.phase;
      visual.dataset.phase = phase;
      document.getElementById('phase-number').textContent = phases[phase][0];
      document.getElementById('phase-caption').textContent = phases[phase][1];
      steps.forEach((item) => {
        const active = item === step;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
    });
  });
  document.getElementById('copyright-year').textContent = new Date().getFullYear();

  // Keep complete, crawlable editorial cards if the registry is unavailable.
  async function refreshJournal() {
    try {
      const registry = await VB.loadRegistry();
      const today = new Date();
      const localDate = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')].join('-');
      const posts = VB.sortByDateDesc(registry.posts || [])
        .filter((post) => /^\d{4}-\d{2}-\d{2}$/.test(post.date) && post.date <= localDate)
        .slice(0, 3);
      if (!posts.length) return;
      const grid = document.getElementById('journalGrid');
      const colors = ['cover-fruit', 'cover-coffee', 'cover-joy'];
      const fragment = document.createDocumentFragment();
      posts.forEach((post, index) => {
        const story = document.createElement('a');
        story.className = 'journal-story';
        story.href = VB.postURL(post.slug);
        const cover = document.createElement('div');
        cover.className = `journal-cover ${colors[index]}`;
        const category = document.createElement('span');
        category.className = 'cover-category';
        category.textContent = (post.categories || [])[0] || 'From the house';
        const title = document.createElement('h3');
        const sourceTitle = new DOMParser().parseFromString(post.cardTitle || post.title, 'text/html');
        title.textContent = sourceTitle.body.textContent;
        const arrow = document.createElement('span');
        arrow.className = 'cover-arrow';
        arrow.setAttribute('aria-hidden', 'true');
        arrow.textContent = '↗';
        const excerpt = document.createElement('p');
        excerpt.textContent = post.excerpt || '';
        cover.append(category, title, arrow);
        story.append(cover, excerpt);
        fragment.append(story);
      });
      grid.replaceChildren(fragment);
    } catch (error) {
      console.warn('Journal preview kept its editorial fallback:', error.message);
    }
  }
  refreshJournal();
})();
