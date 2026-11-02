/* Typewriter effect for all H1 and H2 headings.
   Text stays in the DOM (SEO, screen readers); characters are only made visible one by one,
   so the layout never shifts. Skipped for reduced motion. */
(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const heads = [...document.querySelectorAll('main h1, main h2')];
  if (!heads.length || !('IntersectionObserver' in window)) return;

  function split(el) {
    const chars = [];
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          for (const ch of n.textContent) {
            const s = document.createElement('span');
            s.className = 'tw-c';
            s.textContent = ch;
            frag.appendChild(s);
            chars.push(s);
          }
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains('hero-cursor')) {
          walk(n);
        }
      });
    };
    walk(el);
    return chars;
  }

  function type(el) {
    const chars = el._tw;
    if (!chars || el._typed) return;
    el._typed = true;
    const cursor = document.createElement('span');
    cursor.className = 'tw-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    const step = Math.max(14, Math.min(42, 1100 / chars.length));
    let i = 0;
    const next = () => {
      if (i < chars.length) {
        chars[i].classList.add('on');
        chars[i].after(cursor);
        i++;
        setTimeout(next, chars[i - 1].textContent === ' ' ? step * 0.5 : step);
      } else {
        el.classList.add('tw-done');
        setTimeout(() => cursor.remove(), el.tagName === 'H1' ? 3200 : 1400);
      }
    };
    next();
  }

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { io.unobserve(e.target); type(e.target); }
    });
  }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' });

  heads.forEach(h => {
    h._tw = split(h);
    h.classList.add('tw');
    io.observe(h);
  });
})();
