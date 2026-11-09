/* Shared interior navigation, system motion preference, and contact email handoff. */
(() => {
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  function motion() {
    document.body.dataset.motion = document.documentElement.dataset.motion = media.matches ? 'reduced' : 'full';
  }
  media.addEventListener('change', motion);
  motion();
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const header = document.querySelector('.house-header');
  function closeMenu(focus = false) {
    menu.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    if (focus) toggle.focus();
  }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  menu.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('pointerdown', e => { if (!header.contains(e.target)) closeMenu(); });
  header.addEventListener('focusout', e => { if (e.relatedTarget && !header.contains(e.relatedTarget)) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) closeMenu(true); });
  matchMedia('(min-width:681px)').addEventListener('change', e => { if (e.matches) closeMenu(); });
  document.getElementById('copyright-year').textContent = new Date().getFullYear();
  const form = document.getElementById('contact-form');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const data = new FormData(form);
    const subject = `[${data.get('reason')}] ${data.get('name')}`;
    const body = `Name: ${data.get('name')}\nEmail: ${data.get('email')}\n\n${data.get('message')}`;
    location.href = `mailto:info@vitablabla.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
})();
