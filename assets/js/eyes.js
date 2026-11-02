/* Pixel avatars: pupils follow the pointer while you hover the person's card or section. */
(() => {
  const svgs = document.querySelectorAll('svg[data-eyes]');
  if (!svgs.length) return;
  svgs.forEach((svg, i) => {
    const pupils = svg.querySelector('.pupils');
    const lids = svg.querySelector('.lids');
    if (lids) lids.style.animationDelay = (i * 1.7) % 5 + 's';
    const host = svg.closest('[data-eyes-host]') || svg.closest('.ticket') || svg.parentElement;
    const look = (x, y) => pupils.setAttribute('transform', `translate(${x} ${y})`);
    host.addEventListener('pointermove', e => {
      const r = svg.getBoundingClientRect();
      const cx = r.left + r.width * (12 / 24);
      const cy = r.top + r.height * (10.5 / 24);
      const dx = e.clientX - cx, dy = e.clientY - cy;
      const dead = r.width * 0.07;
      look(Math.abs(dx) < dead ? 0 : Math.sign(dx), Math.abs(dy) < dead ? 0 : Math.sign(dy));
    });
    host.addEventListener('pointerleave', () => look(0, 0));
  });
})();
