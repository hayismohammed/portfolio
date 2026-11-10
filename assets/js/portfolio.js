/* Progressive enhancement: all section links remain usable without JavaScript. */
(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    const narrow = window.matchMedia('(max-width: 760px)');
    const close = () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.hidden = narrow.matches;
    };
    const sync = () => {
      const active = document.activeElement;
      toggle.hidden = !narrow.matches;
      close();
      if (nav.hidden && nav.contains(active)) toggle.focus();
      else if (toggle.hidden && active === toggle) nav.querySelector('a')?.focus();
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      nav.hidden = !open;
    });
    nav.addEventListener('click', (event) => {
      const link = event.target.closest('a');
      if (!link || !narrow.matches) return;
      close();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        target.setAttribute('tabindex', '-1');
        target.focus();
      }
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && narrow.matches && !nav.hidden) {
        close();
        toggle.focus();
      }
    });
    narrow.addEventListener('change', sync);
    sync();
  }
  const copy = document.getElementById('copy-email');
  const status = document.getElementById('copy-status');
  if (copy && status) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const address = 'hayis.mohammed@gmail.com';
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(address);
        } else {
          const field = document.createElement('textarea');
          field.value = address;
          field.setAttribute('aria-label', 'البريد الإلكتروني للنسخ');
          field.style.position = 'fixed';
          field.style.insetInlineStart = '-9999px';
          document.body.appendChild(field);
          field.select();
          const copied = document.execCommand('copy');
          field.remove();
          copy.focus();
          if (!copied) throw new Error('Copy unavailable');
        }
        status.textContent = 'تم نسخ البريد الإلكتروني.';
      } catch {
        status.textContent = 'تعذّر النسخ التلقائي. يمكنك تحديد عنوان البريد الظاهر ونسخه يدويًا.';
      }
    });
  }
})();
