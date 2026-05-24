# Christian Tech Founders

The CTF website — an Astro site for a curated community of Dutch Christian tech builders.

## Stack

- [Astro 4](https://astro.build) — static site generator, zero JS by default
- [GSAP 3](https://gsap.com) + ScrollTrigger — animations (free MIT under Webflow)
- Native CSS with custom properties — no Tailwind, no CSS-in-JS
- View Transitions API for smooth page-to-page swaps

## Structure

```
src/
├── components/        Astro components (Nav, Footer, Button, Card, Mark, ...)
├── data/              Static content (blog posts)
├── layouts/           Base.astro — wraps every page
├── pages/             File-based routes
│   ├── index.astro    Home
│   ├── blog/          Blog index + dynamic [slug] post page
│   └── ...
├── scripts/
│   └── animations.ts  GSAP runtime (entrance, scroll reveal, marquee, magnets, tilts)
└── styles/
    ├── colors_and_type.css   Design tokens (colors, type, spacing, motion)
    └── styles.css            Project-specific helpers + global animation classes
public/
├── assets/            SVG icons, photos
└── fonts/             Argesta (display) + Safiro (UI) .woff2 files
```

## Develop

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # static build → dist/
npm run preview  # serve the built site
```

## Design principles

- **Argesta serif for headings only.** Body copy is always Safiro.
- **Grey cards stack visually as one continuous card.** Dark page background = the space between groups of cards, never a card itself.
- **Single chromatic accent** (`--ctf-blue` = `#0000FF`). Everything else is neutral.
- **Bold typographic hierarchy over decoration.** The blue mark, flow lines, and cursor pills are the only decorative motifs.
