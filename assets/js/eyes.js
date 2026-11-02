/* Pixel avatars: pupils follow the pointer anywhere on the page.
   On touch devices (no hover) the eyes look around on their own. */
(() => {
  const svgs = [...document.querySelectorAll('svg[data-eyes]')];
  if (!svgs.length) return;
  svgs.forEach((svg, i) => {
    const lids = svg.querySelector('.lids');
    if (lids) lids.style.animationDelay = ((i * 1.7) % 5) + 's';
  });

  const look = (svg, x, y) => {
    const p = svg.querySelector('.pupils');
    const t = `translate(${x} ${y})`;
    if (p && p.getAttribute('transform') !== t) p.setAttribute('transform', t);
  };

  let mx = null, my = null, queued = false;
  const update = () => {
    queued = false;
    svgs.forEach(svg => {
      const r = svg.getBoundingClientRect();
      if (r.bottom < -50 || r.top > innerHeight + 50 || !r.width) return;
      const cx = r.left + r.width * 0.5, cy = r.top + r.height * (10.5 / 24);
      const dx = mx - cx, dy = my - cy, dead = r.width * 0.12;
      look(svg, Math.abs(dx) < dead ? 0 : Math.sign(dx), Math.abs(dy) < dead ? 0 : Math.sign(dy));
    });
  };
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };

  window.addEventListener('pointermove', e => { mx = e.clientX; my = e.clientY; queue(); }, { passive: true });
  window.addEventListener('scroll', () => { if (mx !== null) queue(); }, { passive: true });
  // Flying avatars move, so keep eyes aimed while they drift
  if (document.querySelector('[data-flyers]')) setInterval(() => { if (mx !== null) queue(); }, 120);

  // No hover (phones, tablets): idle look-around
  if (window.matchMedia('(hover: none)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const dirs = [[0, 0], [1, 0], [-1, 0], [0, -1], [1, 1], [-1, 1], [0, 0]];
    setInterval(() => {
      svgs.forEach(svg => { const d = dirs[Math.floor(Math.random() * dirs.length)]; look(svg, d[0], d[1]); });
    }, 1400);
  }
})();
