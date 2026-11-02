# Site source

The website is generated. Edit the sources here, then rebuild:

```bash
pip install markdown
python3 src/build.py
```

- `content/insights/en/*.md` and `content/insights/nl/*.md`: Insights posts (same filename = same post in both languages).
- `data/founders.json`: founders and their projects. Remove `"example": true` for real profiles.
- `data/library.json`: findings and podcasts on the Library page.
- `build.py`: page templates, homepage copy (EN and NL) and SEO markup.
- `../assets/css/site.css` and `../assets/js/snake.js`: design system and the snake game.

Commit the generated HTML together with the source changes.
