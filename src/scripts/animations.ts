// CTF — animation runtime
// Built on GSAP (free, MIT — including ScrollTrigger since the Webflow acquisition).
// Re-runs on every astro:page-load so View Transitions stay animated.

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const PREFERS_REDUCED = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Track ScrollTrigger instances so we can clean up across page transitions
let activeTriggers: ScrollTrigger[] = [];
function trackST(st: ScrollTrigger | ScrollTrigger[]) {
  if (Array.isArray(st)) activeTriggers.push(...st);
  else activeTriggers.push(st);
}
function killAll() {
  activeTriggers.forEach((t) => t.kill());
  activeTriggers = [];
  gsap.killTweensOf('*');
}

/* ============================================================
   Hero entrance — staggered reveal of first-paint elements.
   Uses bespoke easing curves for that "luxury slow-in" feeling.
   ============================================================ */
function runEntrance() {
  if (PREFERS_REDUCED()) {
    document
      .querySelectorAll<HTMLElement>('.fx-fade, .fx-rise, .fx-rise-lg, .fx-stagger > *, .fx-scale-in')
      .forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
    return;
  }

  const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });

  tl.to('.fx-rise-lg', {
    opacity: 1, y: 0,
    duration: 1.4, stagger: 0.09,
  });
  tl.to('.fx-rise', {
    opacity: 1, y: 0,
    duration: 1.0, stagger: 0.06,
  }, '-=1.05');
  tl.to('.fx-fade', {
    opacity: 1,
    duration: 0.9, stagger: 0.05,
  }, '-=0.85');
  tl.to('.fx-scale-in', {
    opacity: 1, scale: 1,
    duration: 1.1, stagger: 0.05,
  }, '-=1.0');

  document.querySelectorAll<HTMLElement>('.fx-stagger').forEach((group) => {
    gsap.to(group.children, {
      opacity: 1, y: 0,
      duration: 1.1, ease: 'expo.out',
      stagger: 0.07,
    });
  });
}

/* ============================================================
   ScrollTrigger reveals — fade + rise as sections enter viewport.
   Replaces the previous IntersectionObserver wiring for smoother
   curves and proper batching.
   ============================================================ */
function runScrollReveal() {
  const targets = gsap.utils.toArray<HTMLElement>('[data-reveal]');
  if (!targets.length) return;

  if (PREFERS_REDUCED()) {
    targets.forEach((el) => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  targets.forEach((el) => {
    gsap.set(el, { opacity: 0, y: 40, willChange: 'transform, opacity' });
    const delay = Number(el.dataset.revealDelay || 0) / 1000;
    const st = ScrollTrigger.create({
      trigger: el,
      start: 'top 88%',
      once: true,
      onEnter: () => {
        gsap.to(el, {
          opacity: 1, y: 0,
          duration: 1.1, ease: 'expo.out', delay,
        });
      },
    });
    trackST(st);
  });
}

/* ============================================================
   Parallax — elements with [data-parallax="0.25"] translate at
   that fraction of scroll speed while in view. Negative values
   move opposite direction.
   ============================================================ */
function runParallax() {
  if (PREFERS_REDUCED()) return;
  const els = gsap.utils.toArray<HTMLElement>('[data-parallax]');
  els.forEach((el) => {
    const factor = Number(el.dataset.parallax || 0.2);
    const st = ScrollTrigger.create({
      trigger: el,
      start: 'top bottom',
      end: 'bottom top',
      scrub: 0.6,
      onUpdate(self) {
        const range = 120 * factor;
        const y = (self.progress - 0.5) * range * 2;
        gsap.set(el, { y });
      },
    });
    trackST(st);
  });
}

/* ============================================================
   Magnetic hover — buttons drift toward the cursor with a
   spring snap-back on leave.
   ============================================================ */
function runMagnets() {
  if (PREFERS_REDUCED()) return;
  document.querySelectorAll<HTMLElement>('[data-magnet]').forEach((el) => {
    const strength = Number(el.dataset.magnet || 22);
    const onMove = (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - (rect.left + rect.width / 2);
      const y = e.clientY - (rect.top + rect.height / 2);
      gsap.to(el, {
        x: (x / rect.width) * strength,
        y: (y / rect.height) * strength,
        duration: 0.55, ease: 'power3.out',
      });
    };
    const onLeave = () => {
      gsap.to(el, {
        x: 0, y: 0,
        duration: 0.9, ease: 'elastic.out(1, 0.55)',
      });
    };
    el.addEventListener('mousemove', onMove);
    el.addEventListener('mouseleave', onLeave);
  });
}

/* ============================================================
   Card tilt — subtle 3D rotation on hover.
   [data-tilt="6"] sets max degrees.
   ============================================================ */
function runTilts() {
  if (PREFERS_REDUCED()) return;
  document.querySelectorAll<HTMLElement>('[data-tilt]').forEach((card) => {
    card.style.transformStyle = 'preserve-3d';
    card.style.willChange = 'transform';
    card.style.perspective = '1000px';
    const max = Number(card.dataset.tilt || 6);
    let raf = 0;
    const onMove = (e: MouseEvent) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        gsap.to(card, {
          rotateY: px * max,
          rotateX: -py * max,
          y: -6,
          scale: 1.01,
          duration: 0.6, ease: 'power2.out',
          transformPerspective: 1000,
        });
      });
    };
    const onLeave = () => {
      gsap.to(card, {
        rotateY: 0, rotateX: 0, y: 0, scale: 1,
        duration: 1.1, ease: 'elastic.out(1, 0.55)',
      });
    };
    card.addEventListener('mousemove', onMove);
    card.addEventListener('mouseleave', onLeave);
  });
}

/* ============================================================
   Word morph — cycles a list of words inside any element marked
   with [data-morph]. Words come from a comma-separated
   `data-morph-words` attribute (the element's current text is
   used as the first word).
   ============================================================ */
function runWordMorph() {
  if (PREFERS_REDUCED()) return;
  document.querySelectorAll<HTMLElement>('[data-morph]').forEach((el) => {
    const list = (el.dataset.morphWords || '')
      .split(',')
      .map((w) => w.trim())
      .filter(Boolean);
    if (!list.length) return;
    const all = [el.textContent?.trim() || list[0], ...list];
    // Match width to longest word so the highlight doesn't jitter
    const span = el;
    span.style.display = 'inline-block';
    span.style.willChange = 'transform, opacity';
    let i = 0;
    const tick = () => {
      i = (i + 1) % all.length;
      gsap.to(span, {
        yPercent: -90, opacity: 0,
        duration: 0.32, ease: 'power2.in',
        onComplete() {
          span.textContent = all[i];
          gsap.fromTo(
            span,
            { yPercent: 90, opacity: 0 },
            { yPercent: 0, opacity: 1, duration: 0.55, ease: 'expo.out' },
          );
        },
      });
    };
    const interval = Number(el.dataset.morphInterval || 2800);
    const id = window.setInterval(tick, interval);
    // Park the interval handle so we clear it on unload
    (el as any)._morphId = id;
  });
}

/* ============================================================
   Stats velocity marquee — homepage stats row drifts horizontally.
   - Default: slow left drift (~30 px/s)
   - Scroll DOWN  → push faster LEFT (proportional to scroll velocity)
   - Scroll UP    → reverse to RIGHT
   - After ~1.5s idle → ease back to slow left drift
   The row is duplicated so the loop is seamless.
   ============================================================ */
function runStatsMarquee() {
  const track = document.querySelector<HTMLElement>('.stats-marquee-track');
  if (!track || track.dataset.marqueeInit === '1') return;
  if (PREFERS_REDUCED()) return;
  track.dataset.marqueeInit = '1';

  // Duplicate the children once for a seamless wrap
  Array.from(track.children).forEach((c) =>
    track.appendChild(c.cloneNode(true)),
  );

  const BASE_SPEED = 26; // px/sec — the "very slow" idle drift
  const BASE_DIR = -1;   // default: drift left

  let x = 0;
  let dir = BASE_DIR;
  let targetSpeed = BASE_SPEED;
  let speed = BASE_SPEED;
  let idleTimer: number | undefined;
  let lastY = window.scrollY;
  let lastT = performance.now();
  // EMA of scroll velocity (signed: + = down, - = up)
  let velEMA = 0;

  const onScroll = () => {
    const now = performance.now();
    const dy = window.scrollY - lastY;
    const dt = Math.max((now - lastT) / 1000, 0.001);
    const inst = dy / dt; // px/sec, signed
    velEMA = velEMA * 0.5 + inst * 0.5;
    lastY = window.scrollY;
    lastT = now;
    // Scrolling DOWN (dy>0) → drift LEFT faster
    // Scrolling UP   (dy<0) → reverse to RIGHT, also faster
    dir = velEMA > 0 ? -1 : 1;
    targetSpeed = Math.min(BASE_SPEED + Math.abs(velEMA) * 0.35, 520);
    if (idleTimer) window.clearTimeout(idleTimer);
    idleTimer = window.setTimeout(() => {
      // Idle: settle into the slow default
      dir = BASE_DIR;
      targetSpeed = BASE_SPEED;
      velEMA = 0;
    }, 1500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // Single set width — we recompute on resize
  let oneSetWidth = track.scrollWidth / 2;
  const onResize = () => {
    oneSetWidth = track.scrollWidth / 2;
  };
  window.addEventListener('resize', onResize);

  let last = performance.now();
  const tickerFn = () => {
    const now = performance.now();
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    // Smoothly ease speed toward target
    speed += (targetSpeed - speed) * 0.08;
    x += dir * speed * dt;
    if (oneSetWidth > 0) {
      while (x <= -oneSetWidth) x += oneSetWidth;
      while (x > 0) x -= oneSetWidth;
    }
    track.style.transform = `translate3d(${x}px, 0, 0)`;
  };
  gsap.ticker.add(tickerFn);
  // Stash for cleanup
  (track as any)._tickerFn = tickerFn;
  (track as any)._onScroll = onScroll;
  (track as any)._onResize = onResize;
}

/* ============================================================
   Cursor spotlight — soft glow follows the cursor on cards
   marked with [data-spotlight].
   ============================================================ */
function runSpotlight() {
  if (PREFERS_REDUCED()) return;
  document.querySelectorAll<HTMLElement>('[data-spotlight]').forEach((card) => {
    const onMove = (e: MouseEvent) => {
      const r = card.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      card.style.setProperty('--sx', `${x}%`);
      card.style.setProperty('--sy', `${y}%`);
    };
    card.addEventListener('mousemove', onMove);
    card.addEventListener('mouseleave', () => {
      card.style.setProperty('--sx', `50%`);
      card.style.setProperty('--sy', `50%`);
    });
  });
}

/* ============================================================
   Init — wire everything, then refresh ScrollTrigger to recalc
   positions after layout settles.
   ============================================================ */
function init() {
  killAll();
  runEntrance();
  runScrollReveal();
  runParallax();
  runMagnets();
  runTilts();
  runWordMorph();
  runStatsMarquee();
  runSpotlight();
  // Recompute after fonts settle
  document.fonts?.ready?.then(() => ScrollTrigger.refresh());
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}

// Re-run after Astro view-transition navigation
document.addEventListener('astro:page-load', init);
