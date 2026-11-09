/* Progressive enhancements: direct brand links and editorial content work without JS. */
(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  let motionReduced = reduceMotion.matches;
  function setMotion() {
    motionReduced = reduceMotion.matches;
    const mode = motionReduced ? 'reduced' : 'full';
    document.body.dataset.motion = mode;
    document.documentElement.dataset.motion = mode;
    window.dispatchEvent(new CustomEvent('vb-motion-change'));
  }
  reduceMotion.addEventListener('change', setMotion);
  setMotion();

  const toggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const header = document.querySelector('.house-header');
  function closeMenu(restoreFocus = false) {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    menu.hidden = true;
    if (restoreFocus) toggle.focus();
  }
  toggle?.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    toggle.setAttribute('aria-label', expanded ? 'Open navigation' : 'Close navigation');
    menu.hidden = expanded;
  });
  menu?.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('pointerdown', (event) => {
    if (!menu.hidden && !header.contains(event.target)) closeMenu();
  });
  header?.addEventListener('focusout', (event) => {
    if (event.relatedTarget && !header.contains(event.relatedTarget)) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !menu.hidden) closeMenu(true);
  });
  window.matchMedia('(min-width: 681px)').addEventListener('change', (event) => {
    if (event.matches) closeMenu();
  });

  // Section navigation follows the page; native anchors retain normal browser history.
  const chapters = ['brands', 'technology', 'story', 'journal'].map((id) => document.getElementById(id)).filter(Boolean);
  const chapterLinks = document.querySelectorAll('[data-chapter]');
  const progressBar = document.querySelector('.reading-progress > span');
  let navigationFrame = 0;
  function updateNavigation() {
    navigationFrame = 0;
    if (document.documentElement.classList.contains('world-open')) return;
    const threshold = header.offsetHeight + Math.min(innerHeight * 0.25, 180);
    let current = chapters[0]?.id;
    chapters.forEach((section) => {
      if (section.getBoundingClientRect().top <= threshold) current = section.id;
    });
    chapterLinks.forEach((link) => {
      if (link.dataset.chapter === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    const available = document.documentElement.scrollHeight - innerHeight;
    const progress = available > 0 ? Math.max(0, Math.min(1, scrollY / available)) : 0;
    if (progressBar) progressBar.style.transform = `scaleX(${progress})`;
  }
  function queueNavigation() {
    if (!navigationFrame) navigationFrame = requestAnimationFrame(updateNavigation);
  }
  window.addEventListener('scroll', queueNavigation, { passive: true });
  window.addEventListener('resize', queueNavigation);
  window.addEventListener('pageshow', queueNavigation);
  queueNavigation();

  // A light physical response, with stable geometry and no tilt on touch or reduced motion.
  const rack = document.querySelector('.collection-rack');
  const caption = document.getElementById('collection-caption');
  const defaultCaption = caption.textContent;
  rack.querySelectorAll('.brand-item').forEach((item) => {
    const door = item.querySelector('.brand-door');
    const sleeve = door.querySelector('.album-cover');
    let frame = 0;
    const showWorld = () => { caption.textContent = door.dataset.world; };
    const resetTilt = () => {
      cancelAnimationFrame(frame);
      frame = 0;
      sleeve.style.removeProperty('--tilt-x');
      sleeve.style.removeProperty('--tilt-y');
    };
    item.addEventListener('pointerenter', showWorld);
    item.addEventListener('focusin', showWorld);
    door.addEventListener('pointermove', (event) => {
      if (!finePointer.matches || motionReduced || event.pointerType === 'touch') return;
      cancelAnimationFrame(frame);
      const x = event.clientX;
      const y = event.clientY;
      frame = requestAnimationFrame(() => {
        const bounds = door.getBoundingClientRect();
        const horizontal = Math.max(-1, Math.min(1, ((x - bounds.left) / bounds.width - 0.5) * 2));
        const vertical = Math.max(-1, Math.min(1, ((y - bounds.top) / bounds.height - 0.5) * 2));
        sleeve.style.setProperty('--tilt-x', `${(-vertical * 4).toFixed(2)}deg`);
        sleeve.style.setProperty('--tilt-y', `${(horizontal * 6).toFixed(2)}deg`);
        frame = 0;
      });
    });
    door.addEventListener('pointerleave', resetTilt);
    door.addEventListener('pointercancel', resetTilt);
    finePointer.addEventListener('change', resetTilt);
    window.addEventListener('vb-motion-change', resetTilt);
  });
  rack.addEventListener('pointerleave', () => {
    if (!rack.contains(document.activeElement)) caption.textContent = defaultCaption;
  });
  rack.addEventListener('focusout', (event) => {
    if (!rack.contains(event.relatedTarget)) caption.textContent = defaultCaption;
  });

  const worlds = [
    { key: 'ohcrisp', name: 'OhCrisp', tagline: 'Real fruit. A very happy crunch.', description: 'Colorful freeze-dried fruit with a light, airy crunch. Straight from the bag, sprinkled over breakfast, or packed for your next little adventure.', facts: ['Freeze-dried fruit', 'Crunchy & airy', 'Snack. Sprinkle. Share.'], url: 'https://www.ohcrisp.com' },
    { key: 'ohsip', name: 'OHSIP', tagline: 'Coffee. By the cube.', description: 'Already-brewed Arabica coffee, freeze-dried into one whole cube. Drop it into ice water, stir or shake until dissolved, and make the cup your own.', facts: ['100% Arabica coffee', 'Dissolves in ice water', 'Just add water'], url: 'https://getohsip.com' },
    { key: 'ohviva', name: 'OHVIVA', tagline: 'A fruit tea café. Anywhere.', description: 'Real fruit pieces and vibrant tea, brought together in a freeze-dried cube. Add liquid, stir and enjoy a bright little tea break. Follow your flavor’s pack for hot or cold preparation.', facts: ['Real fruit pieces', 'Fruit tea cubes', 'Stir. Sip. Oh!'], url: 'https://drinkohviva.com' },
    { key: 'frozili', name: 'Frozili', tagline: 'Big coffee flavor. A little icy reset.', description: 'Icy coffee candy with a smooth, slow melt and a clean cooling finish. A pocket-sized ritual for the moments between everything else.', facts: ['Icy coffee candy', 'Slow-melting', 'A cooling finish'], url: 'https://www.frozili.com' }
  ];
  const dialog = document.getElementById('brand-dialog');
  const worldArt = document.getElementById('world-art');
  let worldIndex = -1;
  let returnFocus = null;
  let closePending = false;
  function renderWorld(index) {
    if (index === worldIndex) return;
    worldIndex = index;
    const world = worlds[index];
    dialog.dataset.brand = world.key;
    document.getElementById('world-title').textContent = world.name;
    document.getElementById('world-tagline').textContent = world.tagline;
    document.getElementById('world-description').textContent = world.description;
    const facts = world.facts.map((fact) => {
      const item = document.createElement('li');
      item.textContent = fact;
      return item;
    });
    document.getElementById('world-facts').replaceChildren(...facts);
    const visit = document.getElementById('world-visit');
    visit.href = world.url;
    visit.replaceChildren(document.createTextNode(`Visit ${world.name} `));
    const arrow = document.createElement('span');
    arrow.textContent = '↗';
    arrow.setAttribute('aria-hidden', 'true');
    visit.append(arrow);
    const number = String(index + 1).padStart(2, '0');
    document.getElementById('world-edition').textContent = `${number} / THE EVERYDAY COLLECTION`;
    document.getElementById('world-count').textContent = `${number} / 04`;
    document.getElementById('world-announcement').textContent = `${world.name}, brand ${index + 1} of 4.`;
    const poster = rack.querySelector(`[data-brand="${world.key}"] .album-cover`).cloneNode(true);
    poster.style.removeProperty('--tilt-x');
    poster.style.removeProperty('--tilt-y');
    poster.style.setProperty('--rest-rotate', '-4deg');
    poster.querySelectorAll('img').forEach((image) => { image.draggable = false; });
    worldArt.replaceChildren(poster);
  }
  function syncWorld() {
    const match = location.hash.match(/^#world-(ohcrisp|ohsip|ohviva|frozili)$/);
    if (match) {
      const firstOpen = !dialog.open;
      if (firstOpen && !returnFocus) returnFocus = document.activeElement;
      renderWorld(worlds.findIndex((world) => world.key === match[1]));
      if (firstOpen) {
        closeMenu();
        document.documentElement.classList.add('world-open');
        dialog.showModal();
        dialog.scrollTop = 0;
        window.dispatchEvent(new Event('vb-world-open'));
      }
    } else {
      if (dialog.open) dialog.close();
      document.documentElement.classList.remove('world-open');
      worldIndex = -1;
      closePending = false;
      if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
      returnFocus = null;
      queueNavigation();
    }
  }
  function closeWorld() {
    if (closePending) return;
    if (history.state?.vbWorld) {
      closePending = true;
      history.back();
    } else {
      history.replaceState(history.state, '', `${location.pathname}${location.search}#brands`);
      syncWorld();
    }
  }
  function stepWorld(direction) {
    if (!dialog.open || worldIndex < 0) return;
    const next = worlds[(worldIndex + direction + worlds.length) % worlds.length];
    history.replaceState(history.state, '', `#world-${next.key}`);
    syncWorld();
  }
  if (dialog && typeof dialog.showModal === 'function') {
    document.querySelectorAll('[data-preview]').forEach((button) => {
      button.hidden = false;
      button.addEventListener('click', () => {
        returnFocus = button;
        history.pushState({ ...history.state, vbWorld: true }, '', `#world-${button.dataset.preview}`);
        syncWorld();
      });
    });
    dialog.querySelector('.world-close').addEventListener('click', closeWorld);
    dialog.querySelector('.world-previous').addEventListener('click', () => stepWorld(-1));
    dialog.querySelector('.world-next').addEventListener('click', () => stepWorld(1));
    dialog.addEventListener('cancel', (event) => { event.preventDefault(); closeWorld(); });
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeWorld();
    });
    dialog.addEventListener('keydown', (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        stepWorld(event.key === 'ArrowLeft' ? -1 : 1);
      }
    });
    let swipeStart = null;
    worldArt.addEventListener('pointerdown', (event) => {
      if (!event.isPrimary || event.button !== 0) return;
      swipeStart = { x: event.clientX, y: event.clientY, id: event.pointerId };
      worldArt.setPointerCapture(event.pointerId);
    });
    worldArt.addEventListener('pointerup', (event) => {
      if (!swipeStart || swipeStart.id !== event.pointerId) return;
      const x = event.clientX - swipeStart.x;
      const y = event.clientY - swipeStart.y;
      swipeStart = null;
      if (Math.abs(x) > 55 && Math.abs(x) > Math.abs(y) * 1.5) stepWorld(x < 0 ? 1 : -1);
    });
    worldArt.addEventListener('pointercancel', () => { swipeStart = null; });
    window.addEventListener('popstate', syncWorld);
    window.addEventListener('hashchange', syncWorld);
    window.addEventListener('pageshow', syncWorld);
    syncWorld();
  }

  // One process controller keeps dragging, steps, ingredients and playback in sync.
  const visual = document.querySelector('.science-visual');
  const labObject = document.querySelector('.lab-object');
  const ingredientImage = document.getElementById('lab-ingredient-image');
  const steps = [...document.querySelectorAll('.science-step')];
  const stepTrack = document.querySelector('.science-step-track');
  const mobileProcess = window.matchMedia('(max-width: 680px)');
  const range = document.getElementById('process-range');
  const playButton = document.querySelector('.process-play');
  const sampleChoices = document.querySelector('.lab-samples');
  const phases = ['freeze', 'vacuum', 'enjoy'];
  const phaseNames = ['FREEZE', 'SUBLIMATE', 'REDISCOVER'];
  const samples = {
    fruit: { image: '/assets/brands/fruit-specimen.webp', name: 'Strawberry', formats: ['Frozen fruit', 'Porous structure', 'Crisp fruit'], captions: ['First, a little chill.', 'Water out. Fruit stays.', 'Real fruit. A whole new crunch.'] },
    coffee: { image: '/assets/brands/coffee-cube.webp', name: 'Brewed coffee', formats: ['Frozen coffee', 'Porous structure', 'Coffee cube'], captions: ['Brewed coffee, frozen in shape.', 'Let the ice leave the cube.', 'Add water. Your coffee returns.'] },
    tea: { image: '/assets/brands/tea-cube.webp', name: 'Fruit tea', formats: ['Frozen fruit tea', 'Porous structure', 'Fruit tea cube'], captions: ['Fruit and tea, frozen together.', 'Let the ice leave the cube.', 'Just add water. Stir. Sip.'] }
  };
  const methods = ['Freezing', 'Sublimation', 'Ready to enjoy'];
  const sampleReadout = document.getElementById('lab-sample-name');
  const methodReadout = document.getElementById('lab-method');
  const formatReadout = document.getElementById('lab-format');
  let sample = 'fruit';
  let processProgress = 0;
  let processPhase = -1;
  let playing = false;
  let processFrame = 0;
  function alignProcessStep(phase, animate = true) {
    if (!mobileProcess.matches) return;
    const trackBounds = stepTrack.getBoundingClientRect();
    const stepBounds = steps[phase].getBoundingClientRect();
    const padding = parseFloat(getComputedStyle(stepTrack).scrollPaddingInlineStart) || 0;
    stepTrack.scrollTo({ left: stepBounds.left - trackBounds.left + stepTrack.scrollLeft - padding, behavior: animate && !motionReduced ? 'smooth' : 'instant' });
  }
  window.addEventListener('resize', () => alignProcessStep(Math.max(0, processPhase), false));
  function updatePlayLabel() {
    if (motionReduced) playButton.removeAttribute('aria-pressed');
    else playButton.setAttribute('aria-pressed', String(playing));
    playButton.setAttribute('aria-label', motionReduced ? 'Go to the next freeze-drying step' : 'Play the freeze-drying process');
    playButton.querySelector('.play-symbol').textContent = motionReduced ? '→' : playing ? 'Ⅱ' : '▷';
    playButton.querySelector('.play-label').textContent = motionReduced ? 'Next step' : playing ? 'Pause the process' : processProgress >= 100 ? 'Play it again' : 'Play the process';
  }
  function setProgress(value, forceCaption = false) {
    processProgress = Math.max(0, Math.min(100, value));
    range.value = String(Math.round(processProgress));
    range.style.setProperty('--fill', `${processProgress}%`);
    visual.style.setProperty('--process', String(processProgress / 100));
    const phase = processProgress < 33 ? 0 : processProgress < 67 ? 1 : 2;
    if (phase !== processPhase || forceCaption) {
      processPhase = phase;
      visual.dataset.phase = phases[phase];
      steps.forEach((step, index) => {
        step.classList.toggle('is-active', index === phase);
        step.setAttribute('aria-pressed', String(index === phase));
      });
      document.getElementById('phase-number').textContent = `0${phase + 1} / ${phaseNames[phase]}`;
      document.getElementById('phase-caption').textContent = samples[sample].captions[phase];
      sampleReadout.textContent = samples[sample].name;
      methodReadout.textContent = methods[phase];
      formatReadout.textContent = samples[sample].formats[phase];
      range.setAttribute('aria-valuetext', `Step ${phase + 1} of 3: ${phaseNames[phase].toLowerCase()}`);
      alignProcessStep(phase);
    }
  }
  function stopProcess() {
    cancelAnimationFrame(processFrame);
    processFrame = 0;
    playing = false;
    updatePlayLabel();
  }
  steps.forEach((step, index) => {
    step.addEventListener('click', () => { stopProcess(); setProgress(index * 50); updatePlayLabel(); });
  });
  range.addEventListener('input', () => { stopProcess(); setProgress(Number(range.value)); updatePlayLabel(); });
  function setSample(next) {
    if (!samples[next]) return;
    sample = next;
    ingredientImage.src = samples[sample].image;
    labObject.dataset.sample = sample;
    document.getElementById('specimen-code').textContent = `0${Object.keys(samples).indexOf(sample) + 1}`;
    setProgress(processProgress, true);
  }
  sampleChoices.addEventListener('change', (event) => setSample(event.target.value));
  window.addEventListener('pageshow', () => {
    const restoredProgress = Number(range.value);
    setSample(sampleChoices.querySelector('input:checked').value);
    setProgress(restoredProgress, true);
    stopProcess();
  });
  playButton.addEventListener('click', () => {
    if (motionReduced) { setProgress(processPhase === 2 ? 0 : (processPhase + 1) * 50); return; }
    if (playing) { stopProcess(); return; }
    if (processProgress >= 100) setProgress(0);
    const started = performance.now() - processProgress * 72;
    playing = true;
    updatePlayLabel();
    const frame = (time) => {
      setProgress((time - started) / 72);
      if (processProgress >= 100) stopProcess();
      else processFrame = requestAnimationFrame(frame);
    };
    processFrame = requestAnimationFrame(frame);
  });
  window.addEventListener('vb-motion-change', stopProcess);
  window.addEventListener('vb-world-open', stopProcess);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopProcess(); });
  sampleChoices.hidden = false;
  document.querySelector('.science-controls').hidden = false;
  document.querySelector('.lab-footnote-default').textContent = 'Pick an ingredient. Drag, play, or choose a step.';
  setProgress(0);
  updatePlayLabel();
  document.getElementById('copyright-year').textContent = new Date().getFullYear();

  // Keep complete, crawlable editorial cards if the registry is unavailable.
  async function refreshJournal() {
    try {
      const registry = await VB.loadRegistry();
      const today = new Date();
      const localDate = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')].join('-');
      const posts = VB.arrangeCovers(VB.sortByDateDesc(registry.posts || [])
        .filter((post) => /^\d{4}-\d{2}-\d{2}$/.test(post.date) && post.date <= localDate)
        .slice(0, 3));
      if (!posts.length) return;
      const grid = document.getElementById('journalGrid');
      const fragment = document.createDocumentFragment();
      posts.forEach((post, index) => {
        const story = document.createElement('a');
        story.className = 'journal-story';
        story.href = VB.postURL(post.slug);
        const cover = document.createElement('div');
        cover.className = `journal-cover ${VB.coverClass(post)}`;
        const category = document.createElement('span');
        category.className = 'cover-category';
        category.textContent = (post.categories || [])[0] || 'From the house';
        const title = document.createElement('h3');
        const sourceTitle = new DOMParser().parseFromString(post.cardTitle || post.title, 'text/html');
        title.textContent = sourceTitle.body.textContent;
        const arrow = document.createElement('span');
        arrow.className = 'cover-arrow';
        arrow.setAttribute('aria-hidden', 'true');
        arrow.textContent = 'Read story ↗';
        const excerpt = document.createElement('p');
        excerpt.textContent = post.excerpt || '';
        cover.append(category, title, arrow);
        story.append(cover, excerpt);
        fragment.append(story);
      });
      grid.replaceChildren(fragment);
      queueNavigation();
    } catch (error) {
      console.warn('Journal preview kept its editorial fallback:', error.message);
    }
  }
  refreshJournal();
})();
