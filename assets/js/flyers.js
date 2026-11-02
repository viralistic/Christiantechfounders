/* Homepage hero: pixel avatars drift through space and bounce off the panel edges. */
(() => {
  const box = document.querySelector('[data-flyers]');
  if (!box) return;
  const items = [...box.querySelectorAll('.flyer')];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W = 0, H = 0, visible = true, last = 0;

  const state = items.map((el, i) => ({
    el, x: 0, y: 0,
    vx: (i % 2 ? -1 : 1) * (18 + Math.random() * 14),
    vy: (i % 2 ? 1 : -1) * (12 + Math.random() * 12),
    phase: Math.random() * Math.PI * 2, size: 0
  }));

  function measure() {
    W = box.clientWidth; H = box.clientHeight;
    state.forEach((s, i) => {
      s.size = s.el.offsetWidth;
      if (!s.placed) {
        s.x = (W - s.size) * (0.15 + 0.55 * i / Math.max(1, items.length - 1));
        s.y = (H - s.size) * (0.15 + 0.35 * ((i + 1) % 2));
        s.placed = true;
      }
      s.x = Math.min(Math.max(0, s.x), Math.max(0, W - s.size));
      s.y = Math.min(Math.max(0, s.y), Math.max(0, H - s.size));
    });
  }

  function render(t) {
    state.forEach(s => {
      const bob = Math.sin(t / 900 + s.phase) * 4;
      const tilt = Math.sin(t / 1300 + s.phase) * 7;
      s.el.style.transform = `translate(${s.x.toFixed(1)}px, ${(s.y + bob).toFixed(1)}px) rotate(${tilt.toFixed(1)}deg)`;
    });
  }

  function frame(t) {
    const dt = Math.min(0.05, (t - (last || t)) / 1000);
    last = t;
    if (visible) {
      state.forEach(s => {
        s.x += s.vx * dt; s.y += s.vy * dt;
        if (s.x < 0) { s.x = 0; s.vx = Math.abs(s.vx); }
        if (s.x > W - s.size) { s.x = W - s.size; s.vx = -Math.abs(s.vx); }
        if (s.y < 0) { s.y = 0; s.vy = Math.abs(s.vy); }
        if (s.y > H - s.size) { s.y = H - s.size; s.vy = -Math.abs(s.vy); }
      });
      render(t);
    }
    requestAnimationFrame(frame);
  }

  new IntersectionObserver(es => es.forEach(e => { visible = e.isIntersecting; })).observe(box);
  window.addEventListener('resize', measure);
  measure();
  render(0);
  box.classList.add('ready');
  if (!reduce) requestAnimationFrame(frame);
})();
