/* Snake section: demo snake when scrolled into view, real game on any key press. */
(() => {
  const sec = document.getElementById('play');
  if (!sec) return;
  const cv = sec.querySelector('canvas');
  const ctx = cv.getContext('2d');
  const scoreEl = sec.querySelector('[data-score]');
  const bestEl = sec.querySelector('[data-best]');
  const overEl = sec.querySelector('[data-over-score]');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const HEAD = [124, 120, 255];
  const TAIL = [246, 220, 241];
  // Latin cross, relative to its centre cell
  const CROSS = [[0, -1], [-1, 0], [0, 0], [1, 0], [0, 1], [0, 2]];
  const SAFE_TOP = 3, SAFE_BOTTOM = 3;

  let W = 0, H = 0, cell = 24, cols = 0, rows = 0, offX = 0, offY = 0;
  let mode = 'idle'; // idle | demo | play | over
  let snake = [], dir = { x: 1, y: 0 }, queue = [], grow = 0, cross = null;
  let score = 0, best = 0, step = 115, acc = 0, last = 0, inView = false, overAt = 0;

  try { best = parseInt(localStorage.getItem('ctf-snake-best') || '0', 10) || 0; } catch (e) { best = 0; }
  if (bestEl) bestEl.textContent = best;

  function resize() {
    const r = sec.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width; H = r.height;
    cell = W < 600 ? 18 : 24;
    cols = Math.floor(W / cell);
    rows = Math.floor(H / cell);
    offX = Math.floor((W - cols * cell) / 2);
    offY = Math.floor((H - rows * cell) / 2);
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (mode === 'demo' || mode === 'idle') setupDemo();
    draw();
  }

  function crossCells(c) { return CROSS.map(([dx, dy]) => ({ x: c.x + dx, y: c.y + dy })); }
  function onSnake(p) { return snake.some(s => s.x === p.x && s.y === p.y); }

  function placeCross() {
    for (let i = 0; i < 200; i++) {
      const c = {
        x: 2 + Math.floor(Math.random() * Math.max(1, cols - 4)),
        y: SAFE_TOP + 1 + Math.floor(Math.random() * Math.max(1, rows - SAFE_TOP - SAFE_BOTTOM - 3))
      };
      if (!crossCells(c).some(onSnake)) { cross = c; return; }
    }
    cross = { x: Math.floor(cols / 2), y: Math.floor(rows / 2) };
  }

  function setupDemo() {
    const y = Math.max(SAFE_TOP, Math.floor(rows * 0.58));
    const len = Math.min(12, Math.max(6, Math.floor(cols / 5)));
    snake = [];
    for (let i = 0; i < len; i++) snake.push({ x: len - 1 - i, y });
    dir = { x: 1, y: 0 };
    cross = { x: Math.max(2, Math.floor(cols * 0.74)), y: Math.max(SAFE_TOP + 1, Math.floor(rows * 0.26)) };
  }

  function start() {
    const r = sec.getBoundingClientRect();
    const hdr = document.querySelector('.site-header');
    const top = hdr ? hdr.getBoundingClientRect().height : 0;
    if (r.top < top || r.bottom > window.innerHeight) {
      sec.scrollIntoView({ block: 'end', behavior: reduce ? 'auto' : 'smooth' });
    }
    mode = 'play';
    sec.classList.add('playing');
    sec.classList.remove('over');
    const y = Math.floor(rows / 2);
    snake = [];
    for (let i = 0; i < 5; i++) snake.push({ x: 6 - i, y });
    dir = { x: 1, y: 0 };
    queue = [];
    grow = 0; score = 0; step = 115; acc = 0;
    if (scoreEl) scoreEl.textContent = '0';
    placeCross();
  }

  function gameOver() {
    mode = 'over';
    overAt = performance.now();
    sec.classList.remove('playing');
    sec.classList.add('over');
    if (score > best) {
      best = score;
      try { localStorage.setItem('ctf-snake-best', String(best)); } catch (e) { /* storage unavailable */ }
    }
    if (bestEl) bestEl.textContent = best;
    if (overEl) overEl.textContent = score;
  }

  function exitGame() {
    mode = 'demo';
    sec.classList.remove('playing', 'over');
    setupDemo();
  }

  function tick() {
    if (mode === 'demo') {
      const h = snake[0];
      snake.unshift({ x: (h.x + 1) % cols, y: h.y });
      snake.pop();
      return;
    }
    if (mode !== 'play') return;
    if (queue.length) dir = queue.shift();
    const h = snake[0];
    const n = { x: h.x + dir.x, y: h.y + dir.y };
    if (n.x < 0 || n.y < 0 || n.x >= cols || n.y >= rows) return gameOver();
    const body = grow > 0 ? snake : snake.slice(0, -1);
    if (body.some(s => s.x === n.x && s.y === n.y)) return gameOver();
    snake.unshift(n);
    if (grow > 0) grow--; else snake.pop();
    if (cross && crossCells(cross).some(c => c.x === n.x && c.y === n.y)) {
      score++;
      grow += 3;
      step = Math.max(65, step - 3);
      if (scoreEl) scoreEl.textContent = score;
      placeCross();
    }
  }

  function mix(t) {
    return 'rgb(' + HEAD.map((v, i) => Math.round(v + (TAIL[i] - v) * t)).join(',') + ')';
  }

  function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = 'rgba(255,255,255,0.09)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i <= cols; i++) { const x = offX + i * cell + 0.5; ctx.moveTo(x, offY); ctx.lineTo(x, offY + rows * cell); }
    for (let j = 0; j <= rows; j++) { const y = offY + j * cell + 0.5; ctx.moveTo(offX, y); ctx.lineTo(offX + cols * cell, y); }
    ctx.stroke();

    if (cross) {
      ctx.save();
      ctx.shadowColor = 'rgba(124,120,255,0.9)';
      ctx.shadowBlur = 18;
      ctx.fillStyle = '#fff';
      crossCells(cross).forEach(c => ctx.fillRect(offX + c.x * cell + 1, offY + c.y * cell + 1, cell - 2, cell - 2));
      ctx.restore();
    }

    const n = snake.length;
    snake.forEach((s, i) => {
      ctx.fillStyle = mix(n > 1 ? i / (n - 1) : 0);
      ctx.fillRect(offX + s.x * cell + 1, offY + s.y * cell + 1, cell - 2, cell - 2);
    });
    if (n && (mode === 'play' || mode === 'over')) {
      const h = snake[0];
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.strokeRect(offX + h.x * cell + 2, offY + h.y * cell + 2, cell - 4, cell - 4);
    }
  }

  function loop(t) {
    const dt = Math.min(100, t - (last || t));
    last = t;
    if (inView && (mode === 'demo' || mode === 'play')) {
      acc += dt;
      const s = mode === 'demo' ? 140 : step;
      while (acc >= s) { acc -= s; tick(); if (mode !== 'play' && mode !== 'demo') break; }
      draw();
    }
    requestAnimationFrame(loop);
  }

  const DIRS = {
    ArrowUp: { x: 0, y: -1 }, KeyW: { x: 0, y: -1 },
    ArrowDown: { x: 0, y: 1 }, KeyS: { x: 0, y: 1 },
    ArrowLeft: { x: -1, y: 0 }, KeyA: { x: -1, y: 0 },
    ArrowRight: { x: 1, y: 0 }, KeyD: { x: 1, y: 0 }
  };
  const IGNORE = ['Tab', 'Shift', 'Control', 'Alt', 'Meta', 'CapsLock'];

  function turn(d) {
    const ref = queue.length ? queue[queue.length - 1] : dir;
    if (d.x === -ref.x && d.y === -ref.y) return;
    if (d.x === ref.x && d.y === ref.y) return;
    if (queue.length < 3) queue.push(d);
  }

  window.addEventListener('keydown', e => {
    if (!inView || IGNORE.includes(e.key) || e.metaKey || e.ctrlKey || e.altKey) return;
    const tag = (e.target && e.target.tagName) || '';
    if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    if (e.key === 'Escape') { if (mode === 'play' || mode === 'over') exitGame(); return; }
    const d = DIRS[e.code] || DIRS[e.key];
    if (mode === 'demo' || mode === 'idle') { e.preventDefault(); start(); if (d) turn(d); return; }
    if (mode === 'over') { e.preventDefault(); if (performance.now() - overAt > 350) start(); return; }
    if (mode === 'play') {
      if (d || e.key === ' ') e.preventDefault();
      if (d) turn(d);
    }
  });

  // Touch: tap to start, swipe to steer
  let tx = 0, ty = 0;
  sec.addEventListener('touchstart', e => {
    const t = e.touches[0]; tx = t.clientX; ty = t.clientY;
  }, { passive: true });
  sec.addEventListener('touchend', e => {
    const t = e.changedTouches[0];
    const dx = t.clientX - tx, dy = t.clientY - ty;
    const swipe = Math.max(Math.abs(dx), Math.abs(dy)) > 24;
    if (mode !== 'play') {
      if (!swipe && (mode !== 'over' || performance.now() - overAt > 350)) start();
      return;
    }
    if (!swipe) return;
    turn(Math.abs(dx) > Math.abs(dy) ? { x: Math.sign(dx), y: 0 } : { x: 0, y: Math.sign(dy) });
  });
  sec.addEventListener('touchmove', e => { if (mode === 'play') e.preventDefault(); }, { passive: false });

  new IntersectionObserver(entries => {
    entries.forEach(en => {
      inView = en.isIntersecting;
      if (inView && mode === 'idle') { mode = reduce ? 'idle' : 'demo'; setupDemo(); draw(); }
    });
  }, { threshold: 0.35 }).observe(sec);

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(loop);
})();
